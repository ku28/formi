from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class PhoneContact(BaseModel):
    outlet_name: str
    city: str
    primary_number: str
    secondary_number: Optional[str]
    booking_number: Optional[str]
    support_number: Optional[str]

class Conversation(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()

class KnowledgeEntry(BaseModel):
    query: str
    expected_answer: str
    source: str
    conversation_history: List[Conversation] = []

class OutletInfo(BaseModel):
    name: str
    city: str
    address: Optional[str] = None
    facilities: Dict[str, bool] = {
        "bar": False,
        "baby_chairs": False,
        "lift": False,
        "valet_parking": False,
        "wheelchair_access": False
    }
    timings: Dict[str, Dict[str, str]] = {
        "lunch": {"open": "", "last_entry": "", "close": ""},
        "dinner": {"open": "", "last_entry": "", "close": ""}
    }
    complimentary_drinks: bool = False
    private_dining: bool = False
    phone_contact: Optional[PhoneContact] = None

class KnowledgeBase(BaseModel):
    menu_items: Dict[str, List[str]] = {
        "veg_starters": [],
        "non_veg_starters": [],
        "veg_main_course": [],
        "non_veg_main_course": [],
        "desserts": [],
        "drinks": []
    }
    outlets: Dict[str, Dict[str, OutletInfo]] = {}
    phone_contacts: Dict[str, Dict[str, PhoneContact]] = {} 