#!/usr/bin/env python3
"""
Deployment script for the LLM-Powered Intelligent Query–Retrieval System.

This script helps deploy and run the FastAPI application for the hackathon.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "google-generativeai",
        "pdfminer.six",
        "requests",
        "numpy",
        "scikit-learn",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_environment():
    """Check environment variables and configuration."""
    print("\n🔍 Checking environment...")
    
    # Check Google API key
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        print("⚠️ GOOGLE_API_KEY not set in environment variables")
        print("The application will use the default key from the code")
    else:
        print("✅ GOOGLE_API_KEY found in environment")
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("❌ main.py not found in current directory")
        return False
    
    print("✅ Environment check passed!")
    return True

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI server."""
    print(f"\n🚀 Starting FastAPI server on {host}:{port}...")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", host,
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        print(f"Command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def test_server(host="localhost", port=8000, timeout=30):
    """Test if the server is running correctly."""
    print(f"\n🔍 Testing server at http://{host}:{port}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://{host}:{port}/", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and responding!")
                print(f"📊 Health check response: {response.json()}")
                return True
        except requests.exceptions.RequestException:
            print("⏳ Waiting for server to start...")
            time.sleep(2)
    
    print("❌ Server failed to start within timeout")
    return False

def show_usage_info():
    """Show usage information."""
    print("\n" + "="*60)
    print("🎯 LLM-Powered Intelligent Query–Retrieval System")
    print("="*60)
    print("\n📚 Available endpoints:")
    print("  • GET  /              - Health check")
    print("  • GET  /health        - Health check (alternative)")
    print("  • POST /hackrx/run    - Main endpoint for document analysis")
    print("  • GET  /docs          - Swagger UI documentation")
    print("  • GET  /redoc         - ReDoc documentation")
    
    print("\n🔐 Authentication:")
    print("  Bearer token: 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9")
    
    print("\n📝 Sample request:")
    print("""
curl -X POST "http://localhost:8000/hackrx/run" \\
  -H "Authorization: Bearer 407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9" \\
  -H "Content-Type: application/json" \\
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
      "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
  }'
    """)
    
    print("\n🌐 Access URLs:")
    print(f"  • API Documentation: http://localhost:8000/docs")
    print(f"  • ReDoc Documentation: http://localhost:8000/redoc")
    print(f"  • Health Check: http://localhost:8000/")

def main():
    """Main deployment function."""
    print("🚀 LLM-Powered Intelligent Query–Retrieval System Deployment")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        return 1
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed.")
        return 1
    
    # Show usage info
    show_usage_info()
    
    # Ask user if they want to start the server
    print("\n" + "="*60)
    response = input("Do you want to start the server now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting server...")
        print("Press Ctrl+C to stop the server")
        
        # Start server
        if start_server():
            print("\n✅ Server started successfully!")
        else:
            print("\n❌ Failed to start server")
            return 1
    else:
        print("\n📝 To start the server manually, run:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
