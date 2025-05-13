from fastapi import FastAPI, HTTPException, Query
from app.services.menu_processor import MenuProcessor
from app.services.faq_processor import FAQProcessor
from app.services.chat_handler import ChatHandler, UserMessage, ChatResponse
from app.models.menu import MenuItem, SpiceLevel, Menu
from app.models.faq import FAQ
from typing import List, Optional
from datetime import datetime, time

app = FastAPI(
    title="BBQ Nation Interactive Menu API",
    description="Advanced API for BBQ Nation's intelligent menu system",
    version="2.0.0"
)

menu_processor = MenuProcessor()
faq_processor = FAQProcessor()
chat_handler = ChatHandler()

@app.get("/")
async def root():
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
            "Interactive Chat Support"
        ]
    }

@app.get("/menu", response_model=Menu)
async def get_full_menu(
    time_of_day: Optional[str] = Query(None, description="Filter by time of day (lunch/dinner)")
):
    menu = menu_processor.process_raw_menu()
    if time_of_day:
        # Filter categories by available times
        menu.categories = [
            cat for cat in menu.categories 
            if time_of_day.lower() in [t.lower() for t in cat.available_times]
        ]
    return menu

@app.get("/menu/dietary", response_model=List[MenuItem])
async def get_menu_by_dietary_preferences(
    is_veg: Optional[bool] = None,
    is_jain: Optional[bool] = None,
    is_halal: Optional[bool] = None,
    gluten_free: Optional[bool] = None
):
    items = menu_processor.get_menu_by_dietary_preference(
        is_veg=is_veg,
        is_jain=is_jain,
        is_halal=is_halal,
        gluten_free=gluten_free
    )
    if not items:
        raise HTTPException(
            status_code=404,
            detail="No items found matching the dietary preferences"
        )
    return items

@app.get("/menu/spice-level/{level}", response_model=List[MenuItem])
async def get_menu_by_spice_level(level: SpiceLevel):
    items = menu_processor.get_items_by_spice_level(level)
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No items found with spice level '{level}'"
        )
    return items

@app.get("/menu/chef-specials", response_model=List[MenuItem])
async def get_chef_specials():
    items = menu_processor.get_chef_specials()
    if not items:
        raise HTTPException(
            status_code=404,
            detail="No chef's specials available at the moment"
        )
    return items

@app.get("/menu/category/{category}", response_model=List[MenuItem])
async def get_menu_by_category(
    category: str,
    spice_level: Optional[SpiceLevel] = None
):
    items = menu_processor.get_menu_by_category(category)
    if spice_level:
        items = [item for item in items if item.spice_level == spice_level]
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No items found in category '{category}'"
        )
    return items

@app.get("/faq/search", response_model=List[FAQ])
async def search_faqs(
    query: str,
    category: Optional[str] = None
):
    results = faq_processor.search_faqs(query)
    if category:
        results = [faq for faq in results if faq.category.lower() == category.lower()]
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No FAQs found matching '{query}'"
        )
    return results

@app.get("/faq/{faq_id}", response_model=FAQ)
async def get_faq(faq_id: str):
    faq = faq_processor.get_faq_by_id(faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail=f"FAQ with ID '{faq_id}' not found")
    return faq

@app.post("/chat", response_model=ChatResponse)
async def chat(message: UserMessage):
    """
    Chat endpoint that handles user messages and returns appropriate responses
    
    The chat system will:
    1. Collect city information if not provided
    2. Collect specific location if multiple outlets exist in the city
    3. Process the actual user query once location is confirmed
    """
    try:
        return chat_handler.handle_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 