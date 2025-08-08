
LLM-Powered Intelligent Query–Retrieval System
🚀 Overview
This is an LLM-powered intelligent query–retrieval system designed for processing large documents and making contextual decisions in insurance, legal, HR, and compliance domains.

🏗️ System Architecture
The system follows a 6-component architecture:

Input Documents - PDF Blob URL processing
LLM Parser - Extract structured queries
Embedding Search - FAISS/Pinecone retrieval (using Google Embeddings)
Clause Matching - Semantic similarity matching
Logic Evaluation - Decision processing
JSON Output - Structured response
🛠️ Tech Stack
Backend: FastAPI
Vector DB: Google Embeddings (with cosine similarity)
LLM: Google Gemini 1.5 Flash
Document Processing: PDFMiner, PyPDF2
ML: scikit-learn, numpy, pandas
📦 Installation
Clone the repository
Install dependencies:
pip install -r requirements.txt
Set up environment variables:
export GOOGLE_API_KEY="your_google_api_key"
🚀 Running the Application
Development Server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Production Server
uvicorn main:app --host 0.0.0.0 --port 8000
📚 API Documentation
Base URL
Local Development: http://localhost:8000
API Docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Authentication
All endpoints require Bearer token authentication:

Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9
Endpoints
POST /hackrx/run
Run submissions for document analysis and question answering.

Request Body:

{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
}
Response:

{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered."
    ]
}
GET /
Health check endpoint.

🔧 Key Features
1. Document Processing
PDF Support: Full text extraction from PDF URLs
Text Chunking: Intelligent chunking with 40% overlap
Error Handling: Robust error handling for network issues
2. Semantic Search
Embeddings: Google Embeddings for semantic similarity
Chunking Strategy: 50 chunks with overlap for optimal coverage
Top-K Retrieval: Retrieves top 5 most relevant chunks
3. LLM Integration
Model: Google Gemini 1.5 Flash
Context-Aware: Uses retrieved chunks as context
Structured Output: Returns JSON-formatted answers
4. Performance Optimization
Parallel Processing: ThreadPoolExecutor for embeddings
Token Efficiency: Optimized chunk sizes and context limits
Latency: Target response time under 30 seconds
📊 Evaluation Parameters
The system is designed to meet the following evaluation criteria:

Accuracy: Precision of query understanding and clause matching
Token Efficiency: Optimized LLM token usage and cost-effectiveness
Latency: Response speed and real-time performance
Reusability: Code modularity and extensibility
Explainability: Clear decision reasoning and clause traceability
🧪 Testing
Manual Testing
Start the server: uvicorn main:app --reload
Open Swagger UI: http://localhost:8000/docs
Click "Authorize" and enter the Bearer token
Test the /hackrx/run endpoint with sample data
Sample Test Data
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
🔍 System Components
1. Text Extraction (extract_text_comprehensive)
Downloads PDF from URL
Extracts full text using PDFMiner
Cleans and normalizes text
2. Text Chunking (chunk_text_fixed_overlap)
Creates 50 chunks with 40% overlap
Ensures comprehensive coverage
Optimized for semantic search
3. Embedding Generation (get_embedding_safe)
Uses Google Embeddings API
Implements retry logic
Handles API rate limits
4. Semantic Search (get_top_chunks)
Cosine similarity calculation
Top-K retrieval (k=5)
Fallback handling
5. LLM Processing (ask_llm)
Context-aware prompting
Structured JSON output
Error handling
🚀 Performance Metrics
Response Time: < 30 seconds
Chunk Count: 50 chunks per document
Top-K Retrieval: 5 most relevant chunks
Parallel Processing: 5 workers for embeddings
📝 Code Structure
├── main.py                 # FastAPI application
├── comprehensive_analyzer.py  # ML pipeline functions
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
🔐 Security
Bearer token authentication
Input validation using Pydantic
Error handling for unauthorized access
Secure API key management
🎯 Future Enhancements
Vector Database: Integration with Pinecone or FAISS
Document Types: Support for DOCX and email documents
Caching: Redis integration for performance
Monitoring: Logging and metrics
Scalability: Horizontal scaling support
📄 License
This project is developed for hackathon purposes.
