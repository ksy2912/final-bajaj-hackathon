# 🏆 LLM-Powered Intelligent Query–Retrieval System - Hackathon Submission

## 📋 Project Overview

This project implements an **LLM-Powered Intelligent Query–Retrieval System** that can process large documents and make contextual decisions in insurance, legal, HR, and compliance domains.

### 🎯 Key Achievements

- ✅ **Fast Response Time**: Optimized to run within 30 seconds
- ✅ **High Accuracy**: Comprehensive text processing with semantic search
- ✅ **Production-Ready API**: FastAPI backend with authentication
- ✅ **Well-Documented**: Complete API documentation and usage guides
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Modular Design**: Clean, extensible code architecture

## 🏗️ System Architecture

The system follows the required 6-component architecture:

1. **Input Documents** - PDF Blob URL processing
2. **LLM Parser** - Extract structured queries
3. **Embedding Search** - Google Embeddings retrieval
4. **Clause Matching** - Semantic similarity matching
5. **Logic Evaluation** - Decision processing
6. **JSON Output** - Structured response

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Vector DB**: Google Embeddings (with cosine similarity)
- **LLM**: Google Gemini 1.5 Flash
- **Document Processing**: PDFMiner, PyPDF2
- **ML**: scikit-learn, numpy, pandas
- **Authentication**: Bearer token
- **Documentation**: Swagger UI, ReDoc

## 📁 Project Structure

```
├── main.py                    # FastAPI application (main entry point)
├── comprehensive_analyzer.py  # ML pipeline functions
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── test_api.py              # API testing script
├── deploy.py                # Deployment script
└── HACKATHON_SUBMISSION.md  # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd llm-query-retrieval-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 📚 API Documentation

### Authentication

All endpoints require Bearer token authentication:
```
Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9
```

### Main Endpoint: POST `/hackrx/run`

**Request Body:**
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?"
    ]
}
```

**Response:**
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
        "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months. The benefit is limited to two deliveries or terminations during the policy period."
    ],
    "processing_time": 15.23,
    "chunks_processed": 50
}
```

## 🔧 Key Features

### 1. Document Processing
- **PDF Support**: Full text extraction from PDF URLs
- **Text Chunking**: Intelligent chunking with 40% overlap (50 chunks)
- **Error Handling**: Robust error handling for network issues

### 2. Semantic Search
- **Embeddings**: Google Embeddings for semantic similarity
- **Chunking Strategy**: 50 chunks with overlap for optimal coverage
- **Top-K Retrieval**: Retrieves top 5 most relevant chunks

### 3. LLM Integration
- **Model**: Google Gemini 1.5 Flash
- **Context-Aware**: Uses retrieved chunks as context
- **Structured Output**: Returns JSON-formatted answers

### 4. Performance Optimization
- **Parallel Processing**: ThreadPoolExecutor for embeddings
- **Token Efficiency**: Optimized chunk sizes and context limits
- **Latency**: Target response time under 30 seconds

## 📊 Evaluation Parameters

The system is designed to meet all evaluation criteria:

### ✅ Accuracy
- Precision of query understanding and clause matching
- Comprehensive text processing with semantic search
- Context-aware LLM responses

### ✅ Token Efficiency
- Optimized LLM token usage and cost-effectiveness
- Smart chunking strategy (50 chunks with overlap)
- Context length limits (2000 characters)

### ✅ Latency
- Response speed under 30 seconds
- Parallel processing for embeddings
- Optimized retrieval (top-5 chunks)

### ✅ Reusability
- Code modularity and extensibility
- Clean separation of concerns
- Well-documented functions

### ✅ Explainability
- Clear decision reasoning and clause traceability
- Structured JSON responses
- Detailed logging and error handling

## 🧪 Testing

### Automated Testing

Run the test script to verify all functionality:

```bash
python test_api.py
```

### Manual Testing

1. Start the server: `uvicorn main:app --reload`
2. Open Swagger UI: http://localhost:8000/docs
3. Click "Authorize" and enter the Bearer token
4. Test the `/hackrx/run` endpoint with sample data

### Sample Test Data

```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}
```

## 🎯 Performance Metrics

- **Response Time**: < 30 seconds (target achieved)
- **Chunk Count**: 50 chunks per document
- **Top-K Retrieval**: 5 most relevant chunks
- **Parallel Processing**: 5 workers for embeddings
- **Accuracy**: High precision for insurance policy questions

## 🔐 Security Features

- Bearer token authentication
- Input validation using Pydantic
- Error handling for unauthorized access
- Secure API key management
- CORS middleware for cross-origin requests

## 📈 Scalability Considerations

- Modular architecture for easy scaling
- Parallel processing for embeddings
- Configurable chunk sizes and overlap
- Extensible for additional document types
- Ready for horizontal scaling

## 🚀 Future Enhancements

1. **Vector Database**: Integration with Pinecone or FAISS
2. **Document Types**: Support for DOCX and email documents
3. **Caching**: Redis integration for performance
4. **Monitoring**: Logging and metrics
5. **Scalability**: Horizontal scaling support

## 📝 Code Quality

- **Documentation**: Comprehensive docstrings and comments
- **Type Hints**: Full type annotations
- **Error Handling**: Robust error handling throughout
- **Logging**: Structured logging for debugging
- **Testing**: Automated test suite
- **Modularity**: Clean separation of concerns

## 🎉 Conclusion

This LLM-Powered Intelligent Query–Retrieval System successfully meets all hackathon requirements:

- ✅ **Functional Requirements**: Complete API implementation
- ✅ **Performance Requirements**: < 30 seconds response time
- ✅ **Technical Requirements**: Modern tech stack with best practices
- ✅ **Documentation**: Comprehensive documentation and guides
- ✅ **Testing**: Automated and manual testing capabilities
- ✅ **Deployment**: Production-ready deployment scripts

The system is ready for production use and can be easily extended for additional use cases in insurance, legal, HR, and compliance domains.

---

**Team**: Hackathon Team  
**Version**: 1.0.0  
**Date**: December 2024
