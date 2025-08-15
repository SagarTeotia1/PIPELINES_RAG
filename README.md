# RAG Pipeline - Retrieval-Augmented Generation System

A complete Retrieval-Augmented Generation (RAG) pipeline that allows users to upload documents and ask questions based on their content. The system leverages vector databases for efficient retrieval and Gemini API for generating intelligent responses.

## 🚀 Features

- **Document Processing**: Support for PDF, DOCX, and TXT files
- **Smart Chunking**: Intelligent text chunking with configurable overlap
- **Vector Storage**: ChromaDB Cloud for efficient similarity search
- **LLM Integration**: Gemini API for context-aware response generation
- **Metadata Management**: MongoDB for document metadata storage
- **Modern Web UI**: Responsive Bootstrap-based interface with drag & drop
- **Containerized**: Docker support for easy deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   FastAPI App   │    │   RAG Pipeline  │
│   (HTML/JS)    │◄──►│   (main.py)     │◄──►│   (Services)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   ChromaDB      │
                       │   (Metadata)    │    │   (Vectors)     │
                       └─────────────────┘    └─────────────────┘
```

## 📋 Requirements

- Python 3.11+
- MongoDB 6.0+
- ChromaDB Cloud account
- Gemini API key
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Prerequisites

1. **MongoDB Atlas Setup**
   - Create a MongoDB Atlas account at https://www.mongodb.com/atlas
   - Create a new cluster
   - Create a database user
   - Add your IP address to the IP Access List

2. **API Keys Setup**
   - Get your Gemini API key from https://ai.google.dev/
   - Get your ChromaDB Cloud credentials from https://www.trychroma.com/

### Quick Start (Recommended)

**One-command setup:**
```bash
python quick_start.py
```

This will:
- ✅ Install all dependencies automatically
- ✅ Create the `.env` file with your credentials
- ✅ Only ask for your MongoDB password
- ✅ Test all connections
- ✅ Optionally start the application

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create credentials file**
   ```bash
   # Edit credentials.py with your API keys
   ```

3. **Setup environment**
   ```bash
   python auto_setup.py
   ```

4. **Start application**
   ```bash
   python start.py
   ```

### Access the Application
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Gemini API key for LLM and embeddings | Required |
| `CHROMA_API_KEY` | ChromaDB Cloud API key | Required |
| `CHROMA_TENANT` | ChromaDB Cloud tenant ID | Required |
| `CHROMA_DATABASE` | ChromaDB Cloud database name | Required |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/` |
| `MONGODB_DATABASE` | MongoDB database name | `rag_pipeline` |
| `MONGODB_COLLECTION` | MongoDB collection name | `documents` |

### Application Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_DOCUMENTS` | Maximum number of documents | 20 |
| `MAX_PAGES_PER_DOCUMENT` | Maximum pages per document | 1000 |
| `CHUNK_SIZE` | Text chunk size in words | 1000 |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 |

## 📚 Usage

### 1. Upload Documents

- **Supported Formats**: PDF, DOCX, TXT
- **File Size Limit**: 50MB per file
- **Document Limit**: Up to 20 documents
- **Page Limit**: Up to 1000 pages per document

### 2. Ask Questions

- Use natural language to query your documents
- The system will:
  1. Search for relevant document chunks
  2. Retrieve the most similar content
  3. Generate contextual responses using Gemini
  4. Provide source references

### 3. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/upload` | POST | Upload documents |
| `/query` | POST | Query documents |
| `/documents` | GET | List all documents |
| `/documents/{id}` | GET | Get specific document |
| `/documents/{id}` | DELETE | Delete document |
| `/stats` | GET | System statistics |
| `/health` | GET | Health check |

## 🔧 API Examples

### Upload Document
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Query Documents
```bash
curl -X POST "http://localhost:8000/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic of the document?", "n_results": 5}'
```

### Get Documents
```bash
curl -X GET "http://localhost:8000/documents" \
  -H "accept: application/json"
```

## 🔒 Security

### Credentials Management
- API keys are stored in `credentials.py` (not tracked by git)
- Environment variables are stored in `.env` (not tracked by git)
- Only MongoDB password is prompted during setup
- All sensitive files are in `.gitignore`

### File Security
- `credentials.py` - Contains API keys (excluded from git)
- `.env` - Contains environment variables (excluded from git)
- `uploads/` - Contains uploaded documents (excluded from git)
- `logs/` - Contains application logs (excluded from git)

## 📁 Project Structure

```
rag-pipeline/
├── database/                 # Database clients
│   ├── __init__.py
│   ├── mongodb_client.py    # MongoDB operations
│   └── chroma_client.py     # ChromaDB operations
├── services/                 # Core services
│   ├── __init__.py
│   ├── document_processor.py # Document processing
│   ├── gemini_client.py     # Gemini API client
│   └── rag_pipeline.py      # RAG orchestration
├── templates/                # HTML templates
│   └── index.html           # Main web interface
├── static/                   # Static assets
├── main.py                  # FastAPI application
├── config.py                # Configuration
├── requirements.txt          # Python dependencies
├── credentials.py           # API keys (not tracked by git)
├── quick_start.py           # One-command setup
├── auto_setup.py            # Environment setup
├── start.py                 # Application startup
├── test_setup.py            # Setup testing
└── README.md                # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check if MongoDB is running
   - Verify connection string and credentials
   - Ensure network connectivity

2. **ChromaDB Connection Failed**
   - Verify API key and tenant ID
   - Check ChromaDB Cloud status
   - Ensure proper database permissions

3. **Gemini API Errors**
   - Verify API key is valid
   - Check API quota and limits
   - Ensure proper API configuration

4. **Document Processing Errors**
   - Check file format support
   - Verify file size limits
   - Ensure file is not corrupted

### Logs and Debugging

```bash
# View application logs
docker-compose logs rag_app

# View MongoDB logs
docker-compose logs mongodb

# Access MongoDB shell
docker exec -it rag_mongodb mongosh -u admin -p password123

# Check application health
curl http://localhost:8000/health
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **Database Security**: Enable authentication and encryption
3. **Network Security**: Use reverse proxy and SSL termination
4. **Monitoring**: Implement logging and metrics
5. **Backup**: Regular database backups
6. **Scaling**: Consider horizontal scaling for high load

### Cloud Deployment

- **AWS**: Use ECS/EKS with RDS and ElastiCache
- **Azure**: Use AKS with Azure Database
- **GCP**: Use GKE with Cloud SQL
- **Kubernetes**: Use provided manifests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Gemini](https://ai.google.dev/) - AI model API
- [MongoDB](https://www.mongodb.com/) - Document database
- [Bootstrap](https://getbootstrap.com/) - CSS framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Happy Document Processing! 🚀**
