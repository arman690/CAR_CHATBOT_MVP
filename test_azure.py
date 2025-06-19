# test_azure.py - Test Azure OpenAI connection
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def test_azure_openai():
    """Test Azure OpenAI connection"""
    
    # Get credentials from environment
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
    deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-4.1')
    
    print("🔧 Testing Azure OpenAI configuration...")
    print(f"Endpoint: {endpoint}")
    print(f"API Version: {api_version}")
    print(f"Deployment: {deployment_name}")
    print(f"API Key: {api_key[:10]}..." if api_key else "❌ No API Key")
    
    if not api_key or not endpoint:
        print("❌ Missing Azure OpenAI credentials!")
        return False
    
    try:
        # Initialize client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        print("✅ Azure OpenAI client created")
        
        # Test simple call
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "سلام! تست کردن Azure OpenAI"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        print("✅ Azure OpenAI response received!")
        print(f"Response: {ai_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_azure_openai()
    if success:
        print("\n🎉 Azure OpenAI is working! You can now run the main app.")
    else:
        print("\n💀 Fix Azure OpenAI configuration before running main app.")