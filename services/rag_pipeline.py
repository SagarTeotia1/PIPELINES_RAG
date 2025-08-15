import logging
from typing import List, Dict, Any
from database.chroma_client import ChromaDBClient
from services.gemini_client import GeminiClient
from config import Config

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.chroma_client = ChromaDBClient()
        self.gemini_client = GeminiClient()
    
    def process_query(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Process a user query through the RAG pipeline"""
        try:
            # Validate query
            if not query or len(query.strip()) < 3:
                return {
                    'success': False,
                    'error': 'Query must be at least 3 characters long'
                }
            
            # Search for relevant document chunks
            logger.info(f"Searching for relevant chunks for query: {query}")
            relevant_chunks = self.chroma_client.search_similar(query, n_results)
            
            if not relevant_chunks:
                return {
                    'success': False,
                    'error': 'No relevant documents found for your query'
                }
            
            # Extract text from chunks
            context_texts = [chunk['text'] for chunk in relevant_chunks]
            
            # Generate response using Gemini
            logger.info("Generating response using Gemini LLM")
            response = self.gemini_client.generate_response(query, context_texts)
            
            # Prepare result
            result = {
                'success': True,
                'query': query,
                'response': response,
                'sources': [
                    {
                        'filename': chunk['metadata']['filename'],
                        'chunk_index': chunk['metadata']['chunk_index'],
                        'relevance_score': 1.0 - (chunk.get('distance', 0) if chunk.get('distance') else 0),
                        'text_preview': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text']
                    }
                    for chunk in relevant_chunks
                ],
                'total_sources': len(relevant_chunks)
            }
            
            logger.info(f"Successfully processed query. Found {len(relevant_chunks)} relevant sources.")
            return result
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {
                'success': False,
                'error': f'An error occurred while processing your query: {str(e)}'
            }
    
    def process_query_async(self, query: str, n_results: int = 5):
        """Async version of process_query"""
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, self.process_query, query, n_results)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            chroma_info = self.chroma_client.get_collection_info()
            
            return {
                'success': True,
                'chroma_db': chroma_info,
                'max_documents': Config.MAX_DOCUMENTS,
                'max_pages_per_document': Config.MAX_PAGES_PER_DOCUMENT,
                'chunk_size': Config.CHUNK_SIZE,
                'chunk_overlap': Config.CHUNK_OVERLAP
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {
                'success': False,
                'error': f'Error retrieving system statistics: {str(e)}'
            }
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate a user query"""
        try:
            if not query or not query.strip():
                return {
                    'valid': False,
                    'error': 'Query cannot be empty'
                }
            
            if len(query.strip()) < 3:
                return {
                    'valid': False,
                    'error': 'Query must be at least 3 characters long'
                }
            
            if len(query.strip()) > 1000:
                return {
                    'valid': False,
                    'error': 'Query is too long (maximum 1000 characters)'
                }
            
            # Check for inappropriate content
            if not self.gemini_client.validate_text(query):
                return {
                    'valid': False,
                    'error': 'Query contains inappropriate content'
                }
            
            return {
                'valid': True,
                'query_length': len(query.strip())
            }
            
        except Exception as e:
            logger.error(f"Error validating query: {e}")
            return {
                'valid': False,
                'error': f'Error validating query: {str(e)}'
            }
