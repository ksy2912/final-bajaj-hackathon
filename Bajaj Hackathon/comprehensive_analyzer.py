# 📦 Install required packages
# !pip install -q google-generativeai PyPDF2 pandas numpy scikit-learn pdfminer.six

# 📚 Imports
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
import ast

# 🔐 Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyD5PognQvrpQkOx7Q1Chb0QcCHXD1KMAAs"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 📄 Comprehensive Text Extraction
def extract_text_comprehensive(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return ""
        text = extract_text(BytesIO(response.content))
        text = re.sub(r'\s+', ' ', text).strip()
        return text  # No limit - get full text
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

# ✂ Make 50 chunks with overlap
def chunk_text_fixed_overlap(text, num_chunks=50, overlap_ratio=0.4):
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
    return chunks

# 🤖 Fast embedding with timeout
def get_embedding_fast(text):
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text[:1000],  # Limit text length
            task_type="semantic_similarity"
        )
        return np.array(response["embedding"])
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return np.zeros(768)

# 🔎 Retrieve top 5 chunks for each question
def get_top_chunks_comprehensive(query_embedding, embeddings, texts, k=5):
    try:
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = similarities.argsort()[-k:][::-1]
        return [texts[i] for i in top_indices]
    except:
        return texts[:k] if len(texts) >= k else texts

# 🧾 Comprehensive LLM call
def ask_llm_comprehensive(contexts, question):
    # Combine multiple contexts
    context_str = "\n\n".join(contexts)
    
    prompt = f"""You are an insurance policy expert. Answer the question based on the provided policy context.

Context: {context_str[:2000]}

Question: {question}

Return ONLY a JSON object with this format:
{{
  "answer": "Detailed answer based on the policy information"
}}

If the information is not found in the context, say "Information not found in the provided policy document."
"""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        output = response.text.strip()
        
        # Extract JSON
        start = output.find('{')
        end = output.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(output[start:end])
        else:
            return {"answer": "Unable to process the request"}
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return {"answer": "Service error occurred"}

# 🚀 COMPREHENSIVE TEST RUNNER
def comprehensive_run():
    start_time = time.time()
    
    # 📥 Prompt user for input JSON
    raw_input = input("Paste your input JSON (with 'documents' and 'questions'):\n")
    input_data = ast.literal_eval(raw_input)
    
    pdf_url = input_data["documents"]
    questions = input_data["questions"]
    
    print("🚀 Starting Comprehensive Insurance Policy Analyzer...")
    print(f"📄 PDF URL: {pdf_url}")
    print(f"❓ Questions: {len(questions)}")
    
    # 🔍 Extract & chunk
    print("\n📖 Extracting text from PDF...")
    text = extract_text_comprehensive(pdf_url)
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    print(f"📄 Extracted {len(text)} characters of text")
    
    # ✂ Chunk
    chunks = chunk_text_fixed_overlap(text, num_chunks=50)
    print(f"✂ Chunked into {len(chunks)} parts.")
    
    # 🧠 Embed chunks (parallel)
    print("🔗 Generating embeddings for chunks...")
    
    def embed_chunk(chunk):
        return get_embedding_fast(chunk)
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # More workers
        embeddings = list(executor.map(embed_chunk, chunks))
    
    embeddings = np.array(embeddings)
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # 📊 Process questions
    all_answers = []
    for idx, question in enumerate(questions):
        print(f"\n❓ Processing question {idx+1}/{len(questions)}: {question[:50]}...")
        
        query_embedding = get_embedding_fast(question).reshape(1, -1)
        top_chunks = get_top_chunks_comprehensive(query_embedding, embeddings, chunks, k=5)  # Get top 5 chunks
        answer = ask_llm_comprehensive(top_chunks, question)
        
        all_answers.append(answer["answer"])
    
    elapsed = time.time() - start_time
    print(f"\n⏱ Total processing time: {elapsed:.2f} seconds")
    print("\n✅ Final Results:")
    final_output = {"answers": all_answers}
    print(json.dumps(final_output, indent=2))

if __name__ == "__main__":
    comprehensive_run()