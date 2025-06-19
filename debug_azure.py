# debug_azure.py - Detailed Azure OpenAI debugging
import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def debug_azure_connection():
    """Debug Azure OpenAI connection step by step"""
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
    deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-4.1')
    
    print("🔍 Debugging Azure OpenAI connection...")
    print(f"Endpoint: {endpoint}")
    print(f"API Version: {api_version}")
    print(f"Deployment: {deployment_name}")
    print(f"API Key: {api_key[:20]}..." if api_key else "❌ No API Key")
    print()
    
    # Test 1: Basic endpoint connectivity
    print("📡 Test 1: Basic endpoint connectivity...")
    try:
        # Remove trailing slash and test basic connection
        base_url = endpoint.rstrip('/')
        test_url = f"{base_url}/openai/deployments?api-version={api_version}"
        
        response = requests.get(
            test_url,
            headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint is reachable")
            deployments = response.json()
            print(f"Available deployments: {[d.get('id', 'unknown') for d in deployments.get('data', [])]}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("💡 Check if endpoint URL is correct")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print()
    
    # Test 2: Check deployment existence
    print("🎯 Test 2: Check deployment existence...")
    try:
        base_url = endpoint.rstrip('/')
        deployment_url = f"{base_url}/openai/deployments/{deployment_name}?api-version={api_version}"
        
        response = requests.get(
            deployment_url,
            headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Deployment exists")
            deployment_info = response.json()
            print(f"Model: {deployment_info.get('model', 'unknown')}")
            print(f"Status: {deployment_info.get('status', 'unknown')}")
        else:
            print(f"❌ Deployment not found: {response.status_code}")
            print("💡 Check deployment name in Azure portal")
            
    except Exception as e:
        print(f"❌ Error checking deployment: {e}")
    
    print()
    
    # Test 3: Try different API versions
    print("🔄 Test 3: Try different API versions...")
    api_versions_to_try = [
        "2024-12-01-preview",
        "2024-10-21",
        "2024-08-01-preview", 
        "2024-06-01",
        "2024-02-01"
    ]
    
    for version in api_versions_to_try:
        try:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=version,
                azure_endpoint=endpoint
            )
            
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            print(f"✅ API Version {version} works!")
            print(f"Response: {response.choices[0].message.content}")
            return version
            
        except Exception as e:
            print(f"❌ API Version {version} failed: {str(e)[:100]}...")
    
    print()
    
    # Test 4: Try simple HTTP request to chat endpoint
    print("💬 Test 4: Direct HTTP request to chat endpoint...")
    try:
        base_url = endpoint.rstrip('/')
        chat_url = f"{base_url}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
        
        payload = {
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            chat_url,
            headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Direct HTTP request successful!")
            result = response.json()
            print(f"Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ HTTP request failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Direct HTTP request failed: {e}")
    
    return None

def suggest_fixes():
    """Suggest common fixes"""
    print("\n🔧 Common fixes to try:")
    print("1. Check endpoint URL format: https://your-resource.openai.azure.com/")
    print("2. Verify API key from Azure portal")
    print("3. Ensure deployment is deployed and running")
    print("4. Try different API version")
    print("5. Check Azure resource region and access permissions")
    print("6. Test from Azure portal playground first")

if __name__ == "__main__":
    working_version = debug_azure_connection()
    suggest_fixes()
    
    if working_version:
        print(f"\n🎉 Use API version: {working_version}")
        print("Update your .env file accordingly")