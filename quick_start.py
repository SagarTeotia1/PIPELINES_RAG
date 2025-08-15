#!/usr/bin/env python3
"""
Quick Start Script for RAG Pipeline
One-command setup and start
"""

import subprocess
import sys
import os
import getpass

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected!")
    return True

def install_dependencies():
    """Install dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                  capture_output=True)
    
    # Install numpy first
    if not run_command(f"{sys.executable} -m pip install numpy>=1.26.0 --only-binary=all", "Installing numpy"):
        return False
    
    # Install other dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'logs', 'static', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    print("✅ Directories created!")
    return True

def create_env_file():
    """Create .env file with credentials"""
    print("🔧 Setting up environment...")
    
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
    
    # Get MongoDB password
    mongodb_password = getpass.getpass("Enter your MongoDB Atlas password: ").strip()
    if not mongodb_password:
        print("❌ MongoDB password is required!")
        return False
    
    MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{mongodb_password}@{MONGODB_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Create .env content
    env_content = f"""# RAG Pipeline Environment Configuration
MONGODB_URI={MONGODB_URI}
MONGODB_DATABASE=rag_pipeline
MONGODB_COLLECTION=documents
GEMINI_API_KEY={GEMINI_API_KEY}
CHROMA_API_KEY={CHROMA_API_KEY}
CHROMA_TENANT={CHROMA_TENANT}
CHROMA_DATABASE={CHROMA_DATABASE}
MAX_DOCUMENTS=20
MAX_PAGES_PER_DOCUMENT=1000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_setup():
    """Test the setup"""
    print("🧪 Testing setup...")
    try:
        from config import Config
        print("✅ Configuration loaded!")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def start_application():
    """Start the application"""
    print("🚀 Starting RAG Pipeline...")
    print("🌐 Access at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "start.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

def main():
    """Main quick start function"""
    print("🚀 RAG Pipeline Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed!")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories!")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file!")
        sys.exit(1)
    
    # Test setup
    if not test_setup():
        print("❌ Setup test failed!")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    
    # Ask if user wants to start the application
    start_now = input("\n🚀 Start the application now? (y/N): ").strip().lower()
    if start_now == 'y':
        start_application()
    else:
        print("\n📋 To start later, run: python start.py")

if __name__ == "__main__":
    main()
