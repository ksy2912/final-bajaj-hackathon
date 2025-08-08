#!/usr/bin/env python3
"""
Simple Railway Deployment Helper

This script helps you deploy your LLM Query Retrieval System to Railway.app
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git():
    """Check if git is available."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_files():
    """Check if required files exist."""
    required = ["main.py", "requirements.txt"]
    missing = [f for f in required if not Path(f).exists()]
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    return True

def init_git():
    """Initialize git if needed."""
    if Path(".git").exists():
        print("✅ Git repository exists")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def create_railway_config():
    """Create Railway configuration."""
    config = {
        "build": {
            "builder": "nixpacks"
        },
        "deploy": {
            "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
            "healthcheckPath": "/",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE"
        }
    }
    
    import json
    with open("railway.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created railway.json")

def main():
    """Main deployment helper."""
    print("🚀 Railway Deployment Helper")
    print("="*40)
    
    # Check prerequisites
    if not check_git():
        print("❌ Git not found. Please install git first.")
        return 1
    
    if not check_files():
        print("❌ Missing required files.")
        return 1
    
    # Initialize git
    if not init_git():
        return 1
    
    # Create Railway config
    create_railway_config()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Push to GitHub:")
    print("   git remote add origin <your-github-repo-url>")
    print("   git push -u origin main")
    print("\n2. Deploy to Railway:")
    print("   - Go to https://railway.app")
    print("   - Sign up with GitHub")
    print("   - Click 'New Project' → 'Deploy from GitHub repo'")
    print("   - Select your repository")
    print("   - Add environment variable: GOOGLE_API_KEY")
    print("\n3. Your API will be live at: https://your-app-name.railway.app")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
