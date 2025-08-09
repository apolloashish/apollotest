"""
Model Connector - A flexible class for connecting to various ML models and APIs
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelConnector:
    """
    A flexible connector for various ML models and APIs
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 api_url: Optional[str] = None,
                 model_name: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize the model connector
        
        Args:
            api_key: API key for authentication
            api_url: Base URL for the API
            model_name: Name/ID of the model to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv('MODEL_API_KEY')
        self.api_url = api_url or os.getenv('MODEL_API_URL')
        self.model_name = model_name or os.getenv('MODEL_NAME', 'default_model')
        self.timeout = timeout
        
        # Default headers
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        }
        
        logger.info(f"ModelConnector initialized with model: {self.model_name}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to the model API
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            if not self.api_url:
                logger.warning("No API URL configured")
                return False
                
            # Try a simple health check or list models endpoint
            response = requests.get(
                f"{self.api_url}/health",
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info("Connection test successful")
                return True
            else:
                logger.warning(f"Connection test failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def generate_text(self, 
                     prompt: str, 
                     max_tokens: Optional[int] = None,
                     temperature: Optional[float] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Generate text using the connected model
        
        Args:
            prompt: Input prompt for text generation
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional model parameters
            
        Returns:
            Dict containing the response from the model
        """
        if not self.api_url or not self.api_key:
            raise ValueError("API URL and API key must be configured")
        
        # Default parameters
        max_tokens = max_tokens or int(os.getenv('MAX_TOKENS', 1000))
        temperature = temperature or float(os.getenv('TEMPERATURE', 0.7))
        
        # Prepare request payload
        payload = {
            'model': self.model_name,
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            **kwargs
        }
        
        try:
            logger.info(f"Sending request to {self.api_url}/generate")
            response = requests.post(
                f"{self.api_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info("Text generation successful")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Text generation failed: {e}")
            raise
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       **kwargs) -> Dict[str, Any]:
        """
        Generate chat completion using the connected model
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional model parameters
            
        Returns:
            Dict containing the chat completion response
        """
        if not self.api_url or not self.api_key:
            raise ValueError("API URL and API key must be configured")
        
        # Prepare request payload
        payload = {
            'model': self.model_name,
            'messages': messages,
            **kwargs
        }
        
        try:
            logger.info(f"Sending chat completion request to {self.api_url}/chat/completions")
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info("Chat completion successful")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Chat completion failed: {e}")
            raise
    
    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models
        
        Returns:
            List of available models
        """
        if not self.api_url or not self.api_key:
            raise ValueError("API URL and API key must be configured")
        
        try:
            response = requests.get(
                f"{self.api_url}/models",
                headers=self.headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Retrieved {len(result.get('data', []))} models")
            return result.get('data', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get models: {e}")
            raise
    
    def set_model(self, model_name: str):
        """
        Set the model to use for requests
        
        Args:
            model_name: Name/ID of the model to use
        """
        self.model_name = model_name
        logger.info(f"Model set to: {model_name}")


# Convenience function for quick setup
def create_connector(**kwargs) -> ModelConnector:
    """
    Create a ModelConnector instance with configuration from environment variables
    
    Args:
        **kwargs: Override any default configuration
        
    Returns:
        ModelConnector instance
    """
    return ModelConnector(**kwargs)


if __name__ == "__main__":
    # Example usage
    connector = create_connector()
    
    # Test connection
    if connector.test_connection():
        print("✅ Connection successful!")
        
        # Example text generation
        try:
            result = connector.generate_text("Hello, how are you?")
            print("Generated text:", result)
        except Exception as e:
            print(f"❌ Text generation failed: {e}")
    else:
        print("❌ Connection failed. Please check your configuration.")