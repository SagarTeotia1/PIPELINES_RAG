import os
import logging
import tempfile
import shutil
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn

from database.mongodb_client import MongoDBClient
from database.chroma_client import ChromaDBClient
from services.document_processor import DocumentProcessor
from services.rag_pipeline import RAGPipeline
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Pipeline API",
    description="Retrieval-Augmented Generation pipeline for document processing and querying",
    version="1.0.0"
)

# Initialize services
mongodb_client = MongoDBClient()
chroma_client = ChromaDBClient()
document_processor = DocumentProcessor()
rag_pipeline = RAGPipeline()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    file_size: int
    file_extension: str
    total_characters: int
    total_pages: int
    chunks_count: int
    processing_status: str

class QueryResponse(BaseModel):
    success: bool
    query: str
    response: str
    sources: List[dict]
    total_sources: int

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with document upload and query interface"""
    try:
        # Get system stats
        stats = rag_pipeline.get_system_stats()
        
        # Get all documents
        documents = mongodb_client.get_all_documents()
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "stats": stats,
                "documents": documents,
                "max_documents": Config.MAX_DOCUMENTS
            }
        )
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size
        file_size = 0
        temp_file_path = None
        
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file_path = temp_file.name
            
            # Write uploaded file to temp file
            shutil.copyfileobj(file.file, temp_file)
            temp_file.close()
            
            # Get file size
            file_size = os.path.getsize(temp_file_path)
            
        except Exception as e:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
        
        # Validate file
        if not document_processor.validate_file(file.filename, file_size):
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=400, detail="Invalid file type or size")
        
        # Check document limit
        existing_docs = mongodb_client.get_all_documents()
        if len(existing_docs) >= Config.MAX_DOCUMENTS:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=400, detail=f"Maximum number of documents ({Config.MAX_DOCUMENTS}) reached")
        
        try:
            # Process document
            result = document_processor.process_document(temp_file_path, file.filename)
            
            # Store metadata in MongoDB
            document_id = mongodb_client.insert_document(result['metadata'])
            
            # Store chunks in ChromaDB
            chroma_client.add_documents(result['chunks'])
            
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            return {
                "success": True,
                "message": "Document uploaded and processed successfully",
                "document_id": document_id,
                "filename": file.filename,
                "chunks_count": result['metadata']['chunks_count']
            }
            
        except Exception as e:
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/query")
async def query_documents(query_request: QueryRequest):
    """Query documents using RAG pipeline"""
    try:
        # Validate query
        validation = rag_pipeline.validate_query(query_request.query)
        if not validation['valid']:
            raise HTTPException(status_code=400, detail=validation['error'])
        
        # Process query
        result = rag_pipeline.process_query(query_request.query, query_request.n_results)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/documents")
async def get_documents():
    """Get all processed documents"""
    try:
        documents = mongodb_client.get_all_documents()
        return {
            "success": True,
            "documents": documents,
            "total_count": len(documents)
        }
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Get a specific document by ID"""
    try:
        document = mongodb_client.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "success": True,
            "document": document
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its chunks"""
    try:
        # Delete from MongoDB
        success = mongodb_client.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete chunks from ChromaDB
        chroma_client.delete_document_chunks(document_id)
        
        return {
            "success": True,
            "message": "Document deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        stats = rag_pipeline.get_system_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        mongodb_client.client.admin.command('ping')
        
        # Test ChromaDB connection
        chroma_client.get_collection_info()
        
        return {
            "status": "healthy",
            "mongodb": "connected",
            "chromadb": "connected",
            "gemini": "configured"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # Changed to localhost for security
        port=8000,
        reload=True,
        log_level="info"
    )
