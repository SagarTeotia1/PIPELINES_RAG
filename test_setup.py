#!/usr/bin/env python3
"""
RAG Pipeline Setup Test Script
Tests all components to ensure they're working correctly
"""

import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports() -> Dict[str, bool]:
    """Test if all required modules can be imported"""
    results = {}
    
    try:
        import fastapi
        results['fastapi'] = True
        logger.info(f"✓ FastAPI imported successfully (version: {fastapi.__version__})")
    except ImportError as e:
        results['fastapi'] = False
        logger.error(f"✗ FastAPI import failed: {e}")
    
    try:
        import chromadb
        results['chromadb'] = True
        logger.info("✓ ChromaDB imported successfully")
    except ImportError as e:
        results['chromadb'] = False
        logger.error(f"✗ ChromaDB import failed: {e}")
    
    try:
        import google.generativeai
        results['google_generativeai'] = True
        logger.info("✓ Google Generative AI imported successfully")
    except ImportError as e:
        results['google_generativeai'] = False
        logger.error(f"✗ Google Generative AI import failed: {e}")
    
    try:
        import pymongo
        results['pymongo'] = True
        logger.info("✓ PyMongo imported successfully")
    except ImportError as e:
        results['pymongo'] = False
        logger.error(f"✗ PyMongo import failed: {e}")
    
    try:
        import PyPDF2
        results['PyPDF2'] = True
        logger.info("✓ PyPDF2 imported successfully")
    except ImportError as e:
        results['PyPDF2'] = False
        logger.error(f"✗ PyPDF2 import failed: {e}")
    
    try:
        import docx
        results['python_docx'] = True
        logger.info("✓ Python-docx imported successfully")
    except ImportError as e:
        results['python_docx'] = False
        logger.error(f"✗ Python-docx import failed: {e}")
    
    return results

def test_config() -> Dict[str, bool]:
    """Test configuration loading"""
    results = {}
    
    try:
        from config import Config
        results['config_loading'] = True
        logger.info("✓ Configuration loaded successfully")
        logger.info(f"  - Max Documents: {Config.MAX_DOCUMENTS}")
        logger.info(f"  - Max Pages: {Config.MAX_PAGES_PER_DOCUMENT}")
        logger.info(f"  - Chunk Size: {Config.CHUNK_SIZE}")
        logger.info(f"  - Chunk Overlap: {Config.CHUNK_OVERLAP}")
    except Exception as e:
        results['config_loading'] = False
        logger.error(f"✗ Configuration loading failed: {e}")
    
    return results

def test_database_clients() -> Dict[str, bool]:
    """Test database client initialization"""
    results = {}
    
    # Test MongoDB client
    try:
        from database.mongodb_client import MongoDBClient
        results['mongodb_client'] = True
        logger.info("✓ MongoDB client imported successfully")
    except Exception as e:
        results['mongodb_client'] = False
        logger.error(f"✗ MongoDB client import failed: {e}")
    
    # Test ChromaDB client
    try:
        from database.chroma_client import ChromaDBClient
        results['chromadb_client'] = True
        logger.info("✓ ChromaDB client imported successfully")
    except Exception as e:
        results['chromadb_client'] = False
        logger.error(f"✗ ChromaDB client import failed: {e}")
    
    return results

def test_services() -> Dict[str, bool]:
    """Test service modules"""
    results = {}
    
    # Test document processor
    try:
        from services.document_processor import DocumentProcessor
        results['document_processor'] = True
        logger.info("✓ Document processor imported successfully")
    except Exception as e:
        results['document_processor'] = False
        logger.error(f"✗ Document processor import failed: {e}")
    
    # Test Gemini client
    try:
        from services.gemini_client import GeminiClient
        results['gemini_client'] = True
        logger.info("✓ Gemini client imported successfully")
    except Exception as e:
        results['gemini_client'] = False
        logger.error(f"✗ Gemini client import failed: {e}")
    
    # Test RAG pipeline
    try:
        from services.rag_pipeline import RAGPipeline
        results['rag_pipeline'] = True
        logger.info("✓ RAG pipeline imported successfully")
    except Exception as e:
        results['rag_pipeline'] = False
        logger.error(f"✗ RAG pipeline import failed: {e}")
    
    return results

def test_fastapi_app() -> Dict[str, bool]:
    """Test FastAPI application"""
    results = {}
    
    try:
        from main import app
        results['fastapi_app'] = True
        logger.info("✓ FastAPI application imported successfully")
        
        # Check if app has required attributes
        if hasattr(app, 'routes'):
            results['app_routes'] = True
            logger.info(f"  - App has {len(app.routes)} routes")
        else:
            results['app_routes'] = False
            logger.error("✗ App missing routes attribute")
            
    except Exception as e:
        results['fastapi_app'] = False
        logger.error(f"✗ FastAPI application import failed: {e}")
    
    return results

def run_all_tests() -> Dict[str, Dict[str, bool]]:
    """Run all tests and return results"""
    logger.info("🧪 Starting RAG Pipeline Setup Tests...")
    logger.info("=" * 50)
    
    all_results = {}
    
    # Test imports
    logger.info("\n📦 Testing Module Imports...")
    all_results['imports'] = test_imports()
    
    # Test configuration
    logger.info("\n⚙️  Testing Configuration...")
    all_results['config'] = test_config()
    
    # Test database clients
    logger.info("\n🗄️  Testing Database Clients...")
    all_results['database'] = test_database_clients()
    
    # Test services
    logger.info("\n🔧 Testing Services...")
    all_results['services'] = test_services()
    
    # Test FastAPI app
    logger.info("\n🌐 Testing FastAPI Application...")
    all_results['fastapi'] = test_fastapi_app()
    
    return all_results

def print_summary(results: Dict[str, Dict[str, bool]]):
    """Print test results summary"""
    logger.info("\n" + "=" * 50)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 50)
    
    total_tests = 0
    passed_tests = 0
    
    for category, category_results in results.items():
        logger.info(f"\n{category.upper()}:")
        for test_name, test_result in category_results.items():
            total_tests += 1
            if test_result:
                passed_tests += 1
                logger.info(f"  ✓ {test_name}")
            else:
                logger.info(f"  ✗ {test_name}")
    
    logger.info(f"\n🎯 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        logger.info("🎉 All tests passed! Your RAG Pipeline is ready to use.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return False

def main():
    """Main test function"""
    try:
        # Run all tests
        results = run_all_tests()
        
        # Print summary
        success = print_summary(results)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"💥 Test execution failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
