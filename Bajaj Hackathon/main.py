"""
LLM-Powered Intelligent Query–Retrieval System

This FastAPI application implements an intelligent document processing system
that can analyze insurance policies, legal documents, HR documents, and compliance
materials using LLM-powered semantic search and retrieval.

System Architecture:
1. Input Documents - PDF Blob URL processing
2. LLM Parser - Extract structured queries  
3. Embedding Search - Google Embeddings retrieval
4. Clause Matching - Semantic similarity matching
5. Logic Evaluation - Decision processing
6. JSON Output - Structured response

Author: Hackathon Team
Version: 1.0.0
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import json
import numpy as np
import re
import requests
from io import BytesIO
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor
import time
import logging
from typing import List, Optional

# --- CONFIGURATION ---
API_TOKEN = "407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyD5PognQvrpQkOx7Q1Chb0QcCHXD1KMAAs")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# --- FASTAPI APP ---
app = FastAPI(
    title="LLM-Powered Intelligent Query–Retrieval System",
    description="""
    An intelligent document processing system that can analyze insurance policies, 
    legal documents, HR documents, and compliance materials using LLM-powered 
    semantic search and retrieval.
    
    ## Features
    * PDF document processing from URLs
    * Semantic search using Google Embeddings
    * LLM-powered question answering
    * Structured JSON responses
    * Bearer token authentication
    
    ## System Architecture
    1. **Input Documents** - PDF Blob URL processing
    2. **LLM Parser** - Extract structured queries
    3. **Embedding Search** - Google Embeddings retrieval
    4. **Clause Matching** - Semantic similarity matching
    5. **Logic Evaluation** - Decision processing
    6. **JSON Output** - Structured response
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware with more specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# --- Security Dependency ---
security = HTTPBearer()

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    """Request model for document analysis queries."""
    documents: str = Field(..., description="URL to the PDF document to analyze")
    questions: List[str] = Field(..., description="List of questions to ask about the document")

class QueryResponse(BaseModel):
    """Response model for document analysis results."""
    answers: List[str] = Field(..., description="List of answers corresponding to the questions")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    chunks_processed: Optional[int] = Field(None, description="Number of text chunks processed")

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: float = Field(..., description="Current timestamp")

# --- Utility Functions ---
def extract_text_comprehensive(url: str) -> str:
    """
    Extract comprehensive text from PDF URL.
    
    Args:
        url: URL to the PDF document
        
    Returns:
        Extracted and cleaned text from the PDF
    """
    try:
        logger.info(f"Extracting text from URL: {url}")
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            logger.error(f"Failed to download PDF: {response.status_code}")
            return ""
        
        text = extract_text(BytesIO(response.content))
        text = re.sub(r'\s+', ' ', text).strip()
        logger.info(f"Extracted {len(text)} characters of text")
        return text
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return ""

def chunk_text_fixed_overlap(text: str, num_chunks: int = 50, overlap_ratio: float = 0.4) -> List[str]:
    """
    Create text chunks with fixed overlap for optimal semantic search.
    
    Args:
        text: Input text to chunk
        num_chunks: Number of chunks to create
        overlap_ratio: Overlap ratio between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) < 2000:
        return [text]
    
    chunk_size = len(text) // num_chunks
    overlap = int(chunk_size * overlap_ratio)
    chunks = []
    i = 0
    
    while i < len(text):
        chunk = text[i:i+chunk_size]
        if chunk.strip():
            chunks.append(chunk)
        if len(chunks) >= num_chunks:
            break
        i += chunk_size - overlap
    
    logger.info(f"Created {len(chunks)} chunks with {overlap_ratio*100}% overlap")
    return chunks

def get_embedding_safe(text: str) -> np.ndarray:
    """
    Generate embeddings with retry logic and error handling.
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector
    """
    for attempt in range(3):
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text[:1000],  # Limit text length for efficiency
                task_type="semantic_similarity"
            )
            return np.array(response["embedding"])
        except Exception as e:
            logger.warning(f"Embedding error (attempt {attempt+1}): {e}")
            if attempt < 2:
                time.sleep(1)
    
    logger.error("Failed to generate embedding after 3 attempts")
    return np.zeros(768)

def get_top_chunks(query_embedding: np.ndarray, embeddings: np.ndarray, texts: List[str], k: int = 5) -> List[str]:
    """
    Retrieve top-k most relevant chunks using cosine similarity.
    
    Args:
        query_embedding: Query embedding vector
        embeddings: All chunk embeddings
        texts: All chunk texts
        k: Number of top chunks to retrieve
        
    Returns:
        List of top-k most relevant chunks
    """
    try:
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = similarities.argsort()[-k:][::-1]
        return [texts[i] for i in top_indices]
    except Exception as e:
        logger.error(f"Error in similarity calculation: {e}")
        return texts[:k] if len(texts) >= k else texts

def ask_llm(contexts: List[str], question: str) -> dict:
    """
    Ask LLM for answer based on retrieved contexts.
    
    Args:
        contexts: Retrieved relevant text chunks
        question: Question to answer
        
    Returns:
        Dictionary with answer
    """
    context_str = "\n\n".join(contexts)
    prompt = f"""You are an insurance policy expert. Answer the question based on the provided policy context.

Context: {context_str[:2000]}

Question: {question}

Return ONLY a JSON object with this format:
{{
  "answer": "Detailed answer based on the policy information"
}}

If the information is not found in the context, say:
{{
  "answer": "Information not found in the provided policy document."
}}
"""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        output = response.text.strip()
        
        # Extract JSON from response
        start = output.find('{')
        end = output.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(output[start:end])
        else:
            logger.warning("Failed to extract JSON from LLM response")
            return {"answer": "Unable to extract answer"}
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return {"answer": "Error during LLM response"}

# --- API Endpoints ---
@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Run the LLM-powered query–retrieval pipeline on the provided document and questions.
    
    This endpoint processes a PDF document and answers a list of questions based on its content.
    The system uses semantic search to find relevant information and LLM processing to generate
    accurate, contextual answers.
    
    Args:
        request: QueryRequest containing document URL and questions
        credentials: Bearer token for authentication
        
    Returns:
        QueryResponse containing answers and processing metadata
        
    Raises:
        HTTPException: If authentication fails or document processing fails
    """
    start_time = time.time()
    
    # Authentication check
    if credentials.credentials != API_TOKEN:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    logger.info(f"Processing request with {len(request.questions)} questions")
    
    try:
        # 1. Extract text from PDF
        text = extract_text_comprehensive(request.documents)
        if not text:
            raise HTTPException(status_code=400, detail="Failed to extract text from document.")
        
        # 2. Create text chunks
        chunks = chunk_text_fixed_overlap(text, num_chunks=50)
        
        # 3. Generate embeddings (parallel processing)
        logger.info("Generating embeddings for chunks...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            embeddings = list(executor.map(get_embedding_safe, chunks))
        embeddings = np.array(embeddings)
        
        # 4. Process questions and generate answers
        answers = []
        for i, question in enumerate(request.questions):
            logger.info(f"Processing question {i+1}/{len(request.questions)}: {question[:50]}...")
            
            # Generate query embedding
            query_embedding = get_embedding_safe(question).reshape(1, -1)
            
            # Retrieve relevant chunks
            top_chunks = get_top_chunks(query_embedding, embeddings, chunks, k=5)
            
            # Generate answer using LLM
            answer = ask_llm(top_chunks, question)
            answers.append(answer["answer"])
            
            # Add small delay to avoid rate limits
            time.sleep(0.1)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"Request completed in {processing_time:.2f} seconds")
        
        return QueryResponse(
            answers=answers,
            processing_time=processing_time,
            chunks_processed=len(chunks)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/", response_model=HealthResponse)
async def root():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with service status and metadata
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint (alternative).
    
    Returns:
        HealthResponse with service status and metadata
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )

# --- Error Handlers ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with structured error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with structured error responses."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
