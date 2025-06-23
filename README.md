# 🚗 Car Dealership AI Chatbot MVP

> An intelligent car dealership chatbot powered by Azure OpenAI, built with FastAPI and modern web technologies.

## 🎯 Features

- **AI-Powered Conversations**: Natural language processing with Azure OpenAI GPT-4
- **Smart Car Search**: Intent recognition and entity extraction for precise car matching
- **Multi-language Support**: English and Persian language support
- **Real-time Chat Interface**: Modern, responsive web interface
- **Car Database**: SQLite database with 20+ sample cars
- **Price Calculations**: Australian on-road cost calculations
- **RESTful API**: Clean API endpoints for car data and chat interactions

## 🏗️ Architecture

```
├── main.py                 # FastAPI application entry point
├── database/
│   ├── models.py          # SQLite database models
│   └── sample_data.py     # Sample car data population
├── repositories/
│   └── car_repository.py  # Data access layer
├── services/
│   ├── ai_service.py      # Azure OpenAI integration
│   └── car_service.py     # Business logic for cars
├── static/
│   └── index.html         # Frontend web interface
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure OpenAI resource with GPT-4 deployment
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd car_chatbot_mvp
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Azure OpenAI**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_DEPLOYMENT_NAME=gpt-4
```

5. **Test Azure OpenAI connection**
```bash
python test_azure.py
```

6. **Run the application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

7. **Access the application**
```
http://localhost:8000
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Required |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Required |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-12-01-preview` |
| `AZURE_DEPLOYMENT_NAME` | GPT model deployment name | `gpt-4` |

### Azure OpenAI Setup

1. Create Azure OpenAI resource in Azure Portal
2. Deploy a GPT-4 model
3. Get API key and endpoint from Azure Portal
4. Update `.env` file with credentials

## 📊 API Endpoints

### Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "message": "I want a BMW under $50,000"
}
```

Response:
```json
{
  "response": "I found 2 BMW cars under $50,000...",
  "cars": [
    {
      "id": 1,
      "make": "BMW",
      "model": "3 Series",
      "year": 2024,
      "price": 45000,
      "body_type": "Sedan"
    }
  ]
}
```

### Other Endpoints
- `GET /` - Serve web interface
- `GET /cars` - Get all cars
- `GET /cars/{id}` - Get specific car details
- `GET /health` - Health check

## 🎨 Frontend Features

- **Modern UI**: Clean, responsive design
- **Real-time Chat**: Instant messaging with typing indicators
- **Car Cards**: Visual car listings with details
- **Quick Actions**: Pre-defined question buttons
- **Mobile Friendly**: Responsive design for all devices

## 🧪 Testing

```bash
# Test Azure OpenAI connection
python test_azure.py

# Test specific functions
python -c "from services.ai_service import AIService; print('AI Service OK')"

# Debug Azure issues
python debug_azure.py
```

## 🌐 Deployment

### Azure App Service

1. **Create Azure App Service**
```bash
az webapp create --resource-group myResourceGroup --plan myPlan --name car-chatbot-app
```

2. **Configure environment variables**
```bash
az webapp config appsettings set --resource-group myResourceGroup --name car-chatbot-app --settings AZURE_OPENAI_API_KEY="your_key"
```

3. **Deploy code**
```bash
az webapp deployment source config --resource-group myResourceGroup --name car-chatbot-app --repo-url https://github.com/your-repo --branch main
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku Deployment

```bash
# Install Heroku CLI and login
heroku create car-chatbot-mvp

# Set environment variables
heroku config:set AZURE_OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

## 💡 Usage Examples

### Sample Conversations

**User**: "I need a family SUV under $45,000"
**Bot**: "I found 3 family SUVs under $45,000. Here are the best options: Toyota RAV4 2023 ($42,000), Honda CR-V 2023 ($43,000)..."

**User**: "What's the price of BMW X3?"
**Bot**: "The BMW X3 2023 is priced at $65,000. This luxury SUV comes with advanced technology..."

**User**: "Show me economical cars"
**Bot**: "Here are the most economical options: Toyota Corolla 2024 ($32,000), Hyundai Elantra 2024 ($30,000)..."

## 🔍 How It Works

1. **User Input**: User types a question about cars
2. **Intent Analysis**: Azure OpenAI analyzes the message to extract intent and entities
3. **Car Search**: System searches database based on extracted criteria
4. **Response Generation**: AI generates a natural response with relevant car suggestions
5. **Display Results**: Frontend shows the response and car cards

## 🛠️ Development

### Adding New Car Brands

Edit `database/sample_data.py` to add more car data:

```python
sample_cars = [
    ("Tesla", "Model 3", 2024, 55000, "Sedan", "Electric", "Automatic", 0, "Electric luxury sedan"),
    # Add more cars...
]
```

### Extending AI Capabilities

Modify `services/ai_service.py` to add new intents:

```python
if any(word in message_lower for word in ["financing", "loan", "payment"]):
    intent = "financing_inquiry"
```

### Customizing Frontend

Edit `static/index.html` to modify the web interface design and functionality.

## 📈 Performance Considerations

- **Database**: SQLite for development, consider PostgreSQL for production
- **Caching**: Implement Redis for AI response caching
- **Rate Limiting**: Add API rate limiting for production
- **Monitoring**: Use Azure Application Insights for monitoring

## 🔐 Security

- **Environment Variables**: Never commit API keys to version control
- **Input Validation**: All user inputs are validated and sanitized
- **CORS**: Configure CORS for production domains
- **HTTPS**: Always use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request



## 🔮 Roadmap

- [ ] Add image recognition for car photos
- [ ] Implement user authentication
- [ ] Add booking/appointment system
- [ ] Integrate with real car inventory APIs
- [ ] Add voice chat capabilities
- [ ] Multi-language expansion

---

**Built with ❤️ using Azure OpenAI, FastAPI, and modern web technologies.**
