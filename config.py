"""
Configuration module for Model Connector
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for model connector settings"""
    
    # API Configuration
    API_KEY = os.getenv('MODEL_API_KEY')
    API_URL = os.getenv('MODEL_API_URL', 'https://api.example.com/v1')
    MODEL_NAME = os.getenv('MODEL_NAME', 'default_model')
    
    # Request Configuration
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database Configuration (if needed)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    @classmethod
    def get_model_params(cls) -> Dict[str, Any]:
        """Get default model parameters"""
        return {
            'max_tokens': cls.MAX_TOKENS,
            'temperature': cls.TEMPERATURE,
        }
    
    @classmethod
    def get_request_headers(cls) -> Dict[str, str]:
        """Get default request headers"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        if cls.API_KEY:
            headers['Authorization'] = f'Bearer {cls.API_KEY}'
        
        return headers
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        required_vars = ['API_KEY', 'API_URL']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required configuration: {', '.join(missing_vars)}")
            print("Please set these environment variables in your .env file")
            return False
        
        return True


# Pre-configured settings for different model providers
class ModelProviders:
    """Pre-configured settings for popular model providers"""
    
    OPENAI = {
        'api_url': 'https://api.openai.com/v1',
        'endpoints': {
            'chat': '/chat/completions',
            'completions': '/completions',
            'models': '/models'
        }
    }
    
    ANTHROPIC = {
        'api_url': 'https://api.anthropic.com/v1',
        'endpoints': {
            'messages': '/messages',
            'models': '/models'
        }
    }
    
    HUGGINGFACE = {
        'api_url': 'https://api-inference.huggingface.co/models',
        'endpoints': {
            'inference': ''
        }
    }
    
    @classmethod
    def get_provider_config(cls, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider"""
        return getattr(cls, provider.upper(), {})


# Export commonly used configurations
config = Config()
providers = ModelProviders()