"""
Example usage of the Model Connector

This script demonstrates various ways to use the ModelConnector class
for connecting to different types of ML models and APIs.
"""

import asyncio
from model_connector import ModelConnector, create_connector
from config import config, providers


def basic_example():
    """Basic example of using the model connector"""
    print("🚀 Basic Model Connector Example")
    print("=" * 50)
    
    # Create a connector using environment variables
    connector = create_connector()
    
    # Test the connection
    print("Testing connection...")
    if connector.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed. Please check your configuration.")
        return
    
    # Example text generation
    try:
        print("\n📝 Generating text...")
        result = connector.generate_text(
            prompt="Write a short poem about programming:",
            max_tokens=100,
            temperature=0.8
        )
        print("Generated text:", result)
    except Exception as e:
        print(f"❌ Text generation failed: {e}")


def chat_example():
    """Example of using chat completion"""
    print("\n💬 Chat Completion Example")
    print("=" * 50)
    
    connector = create_connector()
    
    # Example conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ]
    
    try:
        print("Sending chat completion request...")
        result = connector.chat_completion(messages=messages)
        print("Chat response:", result)
    except Exception as e:
        print(f"❌ Chat completion failed: {e}")


def custom_config_example():
    """Example with custom configuration"""
    print("\n⚙️  Custom Configuration Example")
    print("=" * 50)
    
    # Create connector with custom settings
    connector = ModelConnector(
        api_key="your-custom-api-key",
        api_url="https://your-custom-endpoint.com/v1",
        model_name="custom-model",
        timeout=60
    )
    
    print(f"Connector configured with:")
    print(f"  Model: {connector.model_name}")
    print(f"  API URL: {connector.api_url}")
    print(f"  Timeout: {connector.timeout}s")


def provider_specific_examples():
    """Examples for specific model providers"""
    print("\n🏢 Provider-Specific Examples")
    print("=" * 50)
    
    # OpenAI example
    print("\n🤖 OpenAI Configuration:")
    openai_config = providers.get_provider_config('openai')
    print(f"  API URL: {openai_config['api_url']}")
    print(f"  Endpoints: {openai_config['endpoints']}")
    
    # Anthropic example
    print("\n🧠 Anthropic Configuration:")
    anthropic_config = providers.get_provider_config('anthropic')
    print(f"  API URL: {anthropic_config['api_url']}")
    print(f"  Endpoints: {anthropic_config['endpoints']}")
    
    # Example of creating connector for specific provider
    # Uncomment and modify based on your needs:
    """
    openai_connector = ModelConnector(
        api_key="your-openai-api-key",
        api_url=openai_config['api_url'],
        model_name="gpt-3.5-turbo"
    )
    """


def error_handling_example():
    """Example of proper error handling"""
    print("\n🚨 Error Handling Example")
    print("=" * 50)
    
    # Example with invalid configuration
    connector = ModelConnector(
        api_key="invalid-key",
        api_url="https://invalid-url.com",
        model_name="non-existent-model"
    )
    
    try:
        connector.test_connection()
    except Exception as e:
        print(f"Expected error caught: {e}")
    
    try:
        connector.generate_text("Test prompt")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Request error: {e}")


def batch_processing_example():
    """Example of processing multiple requests"""
    print("\n📊 Batch Processing Example")
    print("=" * 50)
    
    connector = create_connector()
    
    # Multiple prompts to process
    prompts = [
        "Explain artificial intelligence in one sentence.",
        "What is the difference between ML and AI?",
        "Name three applications of machine learning."
    ]
    
    results = []
    for i, prompt in enumerate(prompts, 1):
        try:
            print(f"Processing prompt {i}/{len(prompts)}...")
            result = connector.generate_text(prompt, max_tokens=50)
            results.append(result)
        except Exception as e:
            print(f"Error processing prompt {i}: {e}")
            results.append(None)
    
    print(f"✅ Processed {len([r for r in results if r])} out of {len(prompts)} prompts successfully")


def model_management_example():
    """Example of model management features"""
    print("\n🔧 Model Management Example")
    print("=" * 50)
    
    connector = create_connector()
    
    try:
        # Get available models
        print("Fetching available models...")
        models = connector.get_models()
        print(f"Available models: {len(models)}")
        
        # Switch model if multiple are available
        if models:
            first_model = models[0].get('id', 'default')
            print(f"Switching to model: {first_model}")
            connector.set_model(first_model)
            
    except Exception as e:
        print(f"Model management error: {e}")


def main():
    """Run all examples"""
    print("🧪 Model Connector Examples")
    print("=" * 70)
    
    # Check configuration first
    if not config.validate_config():
        print("\n📋 To run these examples:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your API key and URL in the .env file")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Run this script again")
        return
    
    # Run examples
    basic_example()
    chat_example()
    custom_config_example()
    provider_specific_examples()
    error_handling_example()
    batch_processing_example()
    model_management_example()
    
    print("\n🎉 All examples completed!")
    print("\nNext steps:")
    print("- Modify the examples to fit your specific use case")
    print("- Add your own custom methods to the ModelConnector class")
    print("- Implement additional error handling as needed")


if __name__ == "__main__":
    main()