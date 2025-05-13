# BBQ Nation Chatbot

An intelligent chatbot for Barbeque Nation restaurant chain that handles reservations, menu inquiries, and FAQs.

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
RETELL_API_KEY=your_api_key
REDIS_URL=your_redis_url
```

## Project Structure

```
bbq-nation-chatbot/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── data/              # Knowledge base data
├── tests/             # Test files
├── .env              # Environment variables
└── requirements.txt   # Project dependencies
```

## Features

- Menu information retrieval
- Location-based services
- Reservation management
- FAQ handling
- Post-call analysis
- Custom web interface

## API Documentation

The API documentation is available at `/docs` when running the server.

## Testing

Run tests using:
```bash
pytest
``` 