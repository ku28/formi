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
git clone https://github.com/ku28/Formi.git
cd formi
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
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
- Collects city and location information if not provided
- Processes queries once location is confirmed
- Provides intelligent responses for bookings and inquiries

### Menu Endpoints

#### GET /menu/categories 
Get all available menu categories.

#### GET /menu/items/{category}
Get menu items for a specific category.
- Optional dietary preference filter
- Optional spice level filter

### Location Endpoints

#### GET /cities
Get list of all available cities.

#### GET /locations/{city}
Get all locations for a specific city.

#### GET /outlet/{city}/{location}
Get detailed information about a specific outlet.

### Time Slot Endpoints

#### GET /time-slots/{city}/{location}
Get available booking time slots.
- Optional date parameter
- Returns list of available slots

### Contact Endpoints

#### GET /contact/{city}/{location}
Get contact information for a specific outlet.
- Phone numbers
- Location details

## Knowledge Base

The system uses a structured knowledge base containing:
- Menu items and categories
- Outlet information by city and location
- Available time slots
- Contact information