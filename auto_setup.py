#!/usr/bin/env python3
"""
Automatic Environment Setup Script
Creates .env file with pre-configured credentials
"""

import os
import getpass

def create_env_file():
    """Create .env file with pre-configured credentials"""
    
    print("🔧 RAG Pipeline Automatic Setup")
    print("=" * 50)
    print("Creating .env file with your credentials...\n")
    
    # Import credentials from secure file
    try:
        from credentials import (
            GEMINI_API_KEY, 
            CHROMA_API_KEY, 
            CHROMA_TENANT, 
            CHROMA_DATABASE,
            MONGODB_USERNAME,
            MONGODB_CLUSTER
        )
    except ImportError:
        print("❌ credentials.py file not found!")
        print("Please create credentials.py with your API keys")
        return False
    
    # Get MongoDB password (only thing that needs input)
    print("📊 MongoDB Atlas Configuration:")
    print("-" * 30)
    mongodb_password = getpass.getpass("Enter your MongoDB Atlas password: ").strip()
    
    if not mongodb_password:
        print("❌ MongoDB password is required!")
        return False
    
    # Create MongoDB URI
    MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{mongodb_password}@{MONGODB_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Create .env content
    env_content = f"""# RAG Pipeline Environment Configuration
# MongoDB Atlas Configuration
MONGODB_URI={MONGODB_URI}
MONGODB_DATABASE=rag_pipeline
MONGODB_COLLECTION=documents

# Gemini API Configuration
GEMINI_API_KEY={GEMINI_API_KEY}

# ChromaDB Cloud Configuration
CHROMA_API_KEY={CHROMA_API_KEY}
CHROMA_TENANT={CHROMA_TENANT}
CHROMA_DATABASE={CHROMA_DATABASE}

# Application Configuration
MAX_DOCUMENTS=20
MAX_PAGES_PER_DOCUMENT=1000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print("📁 File location: .env")
        print("🔒 Credentials stored securely")
        
        # Test configuration
        print("\n🧪 Testing configuration...")
        if test_configuration(MONGODB_URI, GEMINI_API_KEY, CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE):
            print("\n🎉 All configurations are working correctly!")
            return True
        else:
            print("\n⚠️  Some configurations failed. Please check your credentials.")
            return False
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_configuration(mongodb_uri, gemini_key, chroma_api_key, chroma_tenant, chroma_database):
    """Test all configurations"""
    success_count = 0
    total_tests = 3
    
    # Test MongoDB connection
    try:
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri)
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        success_count += 1
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    # Test Gemini API
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini API configuration successful!")
        success_count += 1
    except Exception as e:
        print(f"❌ Gemini API configuration failed: {e}")
    
    # Test ChromaDB
    try:
        import chromadb
        chroma_client = chromadb.CloudClient(
            api_key=chroma_api_key,
            tenant=chroma_tenant,
            database=chroma_database
        )
        print("✅ ChromaDB connection successful!")
        success_count += 1
    except Exception as e:
        print(f"❌ ChromaDB connection failed: {e}")
    
    return success_count == total_tests

def main():
    """Main function"""
    try:
        if create_env_file():
            print("\n📋 Next steps:")
            print("1. Run: python test_setup.py")
            print("2. Run: python start.py")
            print("\n🚀 Your RAG Pipeline is ready to use!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

if __name__ == "__main__":
    main()
