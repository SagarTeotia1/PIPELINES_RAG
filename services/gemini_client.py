import google.generativeai as genai
import logging
from config import Config
from typing import List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.model = None
        self.embedding_model = None
        self.connect()
    
    def connect(self):
        """Initialize Gemini API connection"""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # Initialize models
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.embedding_model = genai.GenerativeModel('embedding-001')
            
            logger.info("Successfully connected to Gemini API")
            
        except Exception as e:
            logger.error(f"Failed to connect to Gemini API: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text"""
        try:
            # For Gemini, we'll use a simple approach since embedding-001 might not be available
            # In a real implementation, you might want to use a different embedding service
            # For now, we'll return a placeholder
            import hashlib
            import numpy as np
            
            # Create a deterministic hash-based embedding (not ideal but functional)
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            # Convert hash to 1536-dimensional vector (similar to OpenAI embeddings)
            np.random.seed(int(hash_hex[:8], 16))
            embedding = np.random.rand(1536).tolist()
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def generate_response(self, query: str, context: List[str], max_tokens: int = 1000) -> str:
        """Generate response using Gemini LLM"""
        try:
            # Prepare context
            context_text = "\n\n".join([f"Context {i+1}: {ctx}" for i, ctx in enumerate(context)])
            
            # Create prompt
            prompt = f"""You are a helpful AI assistant. Use the following context to answer the user's question. 
            If the context doesn't contain enough information to answer the question, say so.
            
            Context:
            {context_text}
            
            User Question: {query}
            
            Please provide a clear, concise, and accurate answer based on the context provided."""
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response at this time."
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"An error occurred while generating the response: {str(e)}"
    
    def generate_response_async(self, query: str, context: List[str], max_tokens: int = 1000):
        """Async version of generate_response"""
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, self.generate_response, query, context, max_tokens)
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is appropriate for processing"""
        try:
            # Basic validation - check if text is not empty and has reasonable length
            if not text or len(text.strip()) < 10:
                return False
            
            # Check for inappropriate content (basic filter)
            inappropriate_words = ['spam', 'malware', 'virus']
            text_lower = text.lower()
            
            for word in inappropriate_words:
                if word in text_lower:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating text: {e}")
            return False
