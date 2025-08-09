# Model Connector Setup

A flexible Python framework for connecting to various ML models and APIs.

## 🚀 Features

- **Universal Connector**: Works with OpenAI, Anthropic, HuggingFace, and custom APIs
- **Configuration Management**: Environment-based configuration with validation
- **Error Handling**: Robust error handling and logging
- **Multiple Endpoints**: Support for text generation, chat completion, and model management
- **Provider Templates**: Pre-configured settings for popular providers

## 📦 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your API credentials:
   ```env
   MODEL_API_KEY=your_api_key_here
   MODEL_API_URL=https://api.example.com/v1
   MODEL_NAME=your_model_name
   ```

## 🔧 Quick Start

### Basic Usage

```python
from model_connector import create_connector

# Create connector using environment variables
connector = create_connector()

# Test connection
if connector.test_connection():
    print("✅ Connected successfully!")
    
    # Generate text
    result = connector.generate_text("Hello, world!")
    print(result)
```

### Chat Completion

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"}
]

result = connector.chat_completion(messages=messages)
print(result)
```

### Custom Configuration

```python
from model_connector import ModelConnector

connector = ModelConnector(
    api_key="your-api-key",
    api_url="https://your-endpoint.com/v1",
    model_name="your-model",
    timeout=60
)
```

## 📂 File Structure

```
├── model_connector.py    # Main connector class
├── config.py            # Configuration management
├── example_usage.py     # Usage examples
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## 🧪 Running Examples

```bash
python example_usage.py
```

This will run various examples showing different features and use cases.

## 🔌 Supported Providers

### OpenAI
```python
from config import providers

openai_config = providers.get_provider_config('openai')
connector = ModelConnector(
    api_url=openai_config['api_url'],
    api_key="your-openai-key",
    model_name="gpt-3.5-turbo"
)
```

### Anthropic
```python
anthropic_config = providers.get_provider_config('anthropic')
connector = ModelConnector(
    api_url=anthropic_config['api_url'],
    api_key="your-anthropic-key",
    model_name="claude-3-sonnet"
)
```

### HuggingFace
```python
hf_config = providers.get_provider_config('huggingface')
connector = ModelConnector(
    api_url=f"{hf_config['api_url']}/your-model-name",
    api_key="your-hf-token"
)
```

## ⚙️ Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_API_KEY` | API key for authentication | Required |
| `MODEL_API_URL` | Base URL for the API | Required |
| `MODEL_NAME` | Model name/ID to use | `default_model` |
| `MAX_TOKENS` | Maximum tokens to generate | `1000` |
| `TEMPERATURE` | Sampling temperature | `0.7` |
| `TIMEOUT` | Request timeout in seconds | `30` |

## 🚨 Error Handling

The connector includes comprehensive error handling:

```python
try:
    result = connector.generate_text("Your prompt")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🧩 Extending the Connector

To add custom functionality:

```python
class CustomModelConnector(ModelConnector):
    def custom_method(self, data):
        # Your custom implementation
        pass
```

## 📝 License

This project is open source. Feel free to modify and use as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request