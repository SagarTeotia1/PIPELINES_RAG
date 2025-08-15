#!/usr/bin/env python3
"""
RAG Pipeline Startup Script
Simple script to start the application locally
"""

import uvicorn
import logging
import os
import sys

def check_environment():
    """Check if environment is properly configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run 'python setup_env.py' first to configure your environment.")
        return False
    
    try:
        from config import Config
        print("✅ Environment configuration loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and run 'python setup_env.py' to fix it.")
        return False

def main():
    """Main startup function"""
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    print("🚀 RAG Pipeline Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        from config import Config
        
        print(f"📊 Max Documents: {Config.MAX_DOCUMENTS}")
        print(f"📄 Max Pages per Document: {Config.MAX_PAGES_PER_DOCUMENT}")
        print(f"✂️  Chunk Size: {Config.CHUNK_SIZE}")
        print(f"🔄 Chunk Overlap: {Config.CHUNK_OVERLAP}")
        print("\n🌐 Access the application at: http://localhost:8000")
        print("📚 API documentation at: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the server")
        
        # Start the server
        uvicorn.run(
            "main:app",
            host="127.0.0.1",  # Changed to localhost for security
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down RAG Pipeline...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
