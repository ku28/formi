from fastapi import FastAPI, HTTPException, Query, Path
from app.services.menu_processor import MenuProcessor
from app.services.faq_processor import FAQProcessor
from app.services.chat_handler import ChatHandler, UserMessage, ChatResponse
from app.models.menu import MenuItem, SpiceLevel, Menu
from app.models.faq import FAQ
from app.models.knowledge_base import PhoneContact, OutletInfo
from typing import List, Optional, Dict
from datetime import datetime, time

app = FastAPI(
    title="BBQ Nation Interactive Menu API",
    description="""
    Advanced API for BBQ Nation's intelligent menu and booking system.
    
    Features:
    - Interactive chat support for bookings and inquiries
    - Dynamic menu recommendations
    - FAQ handling
    - Phone contact information
    
    Available Cities:
    - Bangalore (Indiranagar, JP Nagar)
    - New Delhi (Connaught Place, Vasant Kunj)
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize services
menu_processor = MenuProcessor()
faq_processor = FAQProcessor()
chat_handler = ChatHandler()

@app.get("/")
async def root():
    """Get API status and available features"""
    return {
        "message": "Welcome to BBQ Nation Interactive Menu API",
        "version": "2.0.0",
        "last_updated": datetime.now().isoformat(),
        "features": [
            "Dynamic menu recommendations",
            "Dietary preference filtering",
            "Chef's specials",
            "Festival menu items",
            "Intelligent FAQ system",
            "Interactive Chat Support",
            "Phone Contact Information"
        ]
    }

@app.get("/knowledge-base/cities")
async def get_cities() -> List[str]:
    """Get list of available cities"""
    return chat_handler.knowledge_processor.get_available_cities()

@app.get("/knowledge-base/locations/{city}")
async def get_locations(city: str) -> List[str]:
    """Get locations for a specific city"""
    locations = chat_handler.knowledge_processor.get_locations_in_city(city)
    if not locations:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    return locations

@app.get("/knowledge-base/outlet/{city}/{location}")
async def get_outlet_info(city: str, location: str) -> OutletInfo:
    """Get detailed information about a specific outlet"""
    outlet = chat_handler.knowledge_processor.knowledge_base.outlets.get(city, {}).get(location)
    if not outlet:
        raise HTTPException(
            status_code=404,
            detail=f"Outlet not found in {location}, {city}"
        )
    return outlet

@app.get("/knowledge-base/menu/categories")
async def get_menu_categories() -> Dict[str, List[str]]:
    """Get all menu categories"""
    return chat_handler.knowledge_processor.menu_categories

@app.get("/knowledge-base/menu/items/{category}")
async def get_menu_items(
    category: str,
    dietary: Optional[str] = None,
    spice_level: Optional[str] = None
) -> List[Dict]:
    """Get menu items with optional filters"""
    items = chat_handler.knowledge_processor.knowledge_base.menu_items.get(category, [])
    if not items:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    return items

@app.get("/knowledge-base/contact/{city}/{location}")
async def get_contact_info(city: str, location: str) -> PhoneContact:
    """Get contact information for a specific outlet"""
    contact = chat_handler.knowledge_processor.knowledge_base.phone_contacts.get(city, {}).get(location)
    if not contact:
        raise HTTPException(
            status_code=404,
            detail=f"Contact information not found for {location}, {city}"
        )
    return contact

@app.get("/knowledge-base/time-slots/{city}/{location}")
async def get_available_slots(
    city: str,
    location: str,
    date: Optional[str] = None
) -> List[str]:
    """Get available time slots for a specific outlet"""
    slots = chat_handler.knowledge_processor.get_available_time_slots(location)
    if not slots:
        raise HTTPException(
            status_code=404,
            detail=f"No time slots available for {location}, {city}"
        )
    return slots

@app.post("/chat")
async def chat(message: UserMessage) -> ChatResponse:
    """
    Chat endpoint that handles user messages and returns appropriate responses
    
    The chat system will:
    1. Collect city information if not provided
    2. Collect specific location if multiple outlets exist in the city
    3. Process the actual query once location is confirmed
    
    Available cities:
    - Bangalore (Indiranagar, JP Nagar)
    - New Delhi (Connaught Place, Vasant Kunj)
    """
    try:
        return chat_handler.handle_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 