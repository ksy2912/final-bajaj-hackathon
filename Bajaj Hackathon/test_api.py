#!/usr/bin/env python3
"""
Test script for the LLM-Powered Intelligent Query–Retrieval System API.

This script tests the main API endpoints to ensure they're working correctly.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_TOKEN = "407ec480fc8736fa886a97555ef36f9aaf987fdddbcccb94ce9c908530f6fbc9"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_hackrx_run():
    """Test the main /hackrx/run endpoint."""
    print("\n🔍 Testing /hackrx/run endpoint...")
    
    # Test data
    test_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=test_data
        )
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /hackrx/run test passed!")
            print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
            print(f"📊 Processing time: {data.get('processing_time', 'N/A')} seconds")
            print(f"🔢 Chunks processed: {data.get('chunks_processed', 'N/A')}")
            print(f"❓ Questions processed: {len(data.get('answers', []))}")
            print("\n📝 Sample answers:")
            for i, answer in enumerate(data.get('answers', [])[:2], 1):
                print(f"  {i}. {answer[:100]}...")
            return True
        else:
            print(f"❌ /hackrx/run test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ /hackrx/run test error: {e}")
        return False

def test_unauthorized_access():
    """Test unauthorized access."""
    print("\n🔍 Testing unauthorized access...")
    
    test_data = {
        "documents": "https://example.com/test.pdf",
        "questions": ["Test question"]
    }
    
    try:
        # Test without authorization header
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            json=test_data
        )
        
        if response.status_code == 401:
            print("✅ Unauthorized access correctly blocked")
            return True
        else:
            print(f"❌ Unauthorized access not blocked: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Unauthorized access test error: {e}")
        return False

def test_invalid_input():
    """Test invalid input handling."""
    print("\n🔍 Testing invalid input handling...")
    
    # Test with invalid URL
    test_data = {
        "documents": "https://invalid-url-that-does-not-exist.com/test.pdf",
        "questions": ["Test question"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=test_data
        )
        
        if response.status_code == 400:
            print("✅ Invalid input correctly handled")
            return True
        else:
            print(f"❌ Invalid input not handled correctly: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid input test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting API tests...\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Main Endpoint", test_hackrx_run),
        ("Unauthorized Access", test_unauthorized_access),
        ("Invalid Input", test_invalid_input)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
