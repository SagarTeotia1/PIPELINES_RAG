import chromadb
import logging
from config import Config
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ChromaDBClient:
    def __init__(self):
        self.client = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to ChromaDB Cloud"""
        try:
            self.client = chromadb.CloudClient(
                api_key=Config.CHROMA_API_KEY,
                tenant=Config.CHROMA_TENANT,
                database=Config.CHROMA_DATABASE
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection("document_chunks")
                logger.info("Connected to existing ChromaDB collection")
            except:
                self.collection = self.client.create_collection(
                    name="document_chunks",
                    metadata={"description": "Document chunks for RAG pipeline"}
                )
                logger.info("Created new ChromaDB collection")
                
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add document chunks to ChromaDB"""
        try:
            if not documents:
                return
            
            # Prepare data for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for doc in documents:
                ids.append(doc['chunk_id'])
                texts.append(doc['text'])
                metadatas.append({
                    'document_id': doc['document_id'],
                    'chunk_index': doc['chunk_index'],
                    'filename': doc['filename'],
                    'page_number': doc.get('page_number', 0)
                })
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(documents)} chunks to ChromaDB")
            
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            raise
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar document chunks"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []
    
    def delete_document_chunks(self, document_id: str):
        """Delete all chunks for a specific document"""
        try:
            # Get all chunks for the document
            results = self.collection.query(
                query_texts=[""],
                n_results=1000,
                where={"document_id": document_id}
            )
            
            if results['ids']:
                # Delete chunks
                self.collection.delete(ids=results['ids'][0])
                logger.info(f"Deleted {len(results['ids'][0])} chunks for document {document_id}")
            
        except Exception as e:
            logger.error(f"Error deleting document chunks: {e}")
    
    def get_collection_info(self):
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
