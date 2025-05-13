# BBQ Nation Chatbot

An intelligent chatbot system for BBQ Nation restaurant chain, handling bookings, inquiries, and FAQs.

## Features

- Interactive chat support for bookings and inquiries
- Dynamic menu recommendations
- Dietary preference filtering
- FAQ handling system
- Post-conversation analysis
- Comprehensive API documentation

## Available Cities

- Bangalore
  - Indiranagar
  - JP Nagar
- New Delhi
  - Connaught Place
  - Vasant Kunj

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bbq-nation-chatbot.git
cd bbq-nation-chatbot
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python run.py
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Documentation

### Chat Endpoints

#### POST /chat
Handle user messages and manage conversation flow.
- Collects city and location information
- Handles bookings and inquiries
- Provides relevant information

### Menu Endpoints

#### GET /menu
Get the full menu with optional time-based filtering.
- Filter by time of day (lunch/dinner)
- View all categories and items

#### GET /menu/dietary
Get menu items filtered by dietary preferences.
- Vegetarian options
- Jain food
- Halal certified
- Gluten-free options

### FAQ Endpoints

#### GET /faq/search
Search through frequently asked questions.
- Search by query
- Filter by category
- Get relevant answers

### Analysis Endpoints

#### GET /analysis/metrics
Get conversation analysis metrics.
- Filter by time period (day/week/month)
- View success rates and metrics

#### POST /analysis/export
Export conversation analysis data.
- Excel format with detailed metrics
- JSON format for raw data

## Project Structure

```
bbq-nation-chatbot/
├── app/
│   ├── services/
│   │   ├── chat_handler.py      # Chat management
│   │   ├── prompt_handler.py    # Prompt templates
│   │   ├── analysis_handler.py  # Conversation analysis
│   │   └── knowledge_processor.py # Data processing
│   ├── models/
│   │   └── knowledge_base.py    # Data models
│   ├── prompts/
│   │   └── templates.py         # Prompt templates
│   └── main.py                  # FastAPI application
├── data/
│   └── processed/              # Processed data files
├── scripts/
│   └── process_knowledge_base.py # Data processing scripts
├── requirements.txt            # Dependencies
└── run.py                     # Server startup script
```

## Knowledge Base

The system uses a structured knowledge base containing:
- Menu items and categories
- Outlet information
- FAQs and responses
- Booking policies

## Post-Call Analysis

The system generates comprehensive analysis including:
- Conversation metrics
- Success rates
- User satisfaction
- Error analysis

Analysis data can be exported in Excel or JSON format.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 