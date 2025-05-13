from typing import List, Optional, Dict
from pydantic import BaseModel

class Conversation(BaseModel):
    role: str
    content: str

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

class KnowledgeBase(BaseModel):
    menu_items: Dict[str, List[str]] = {
        "veg_starters": [],
        "non_veg_starters": [],
        "veg_main_course": [],
        "non_veg_main_course": [],
        "desserts": [],
        "drinks": []
    }
    outlets: Dict[str, Dict[str, OutletInfo]] = {}  # city -> {outlet_name -> info}
    faqs: List[KnowledgeEntry] = []
    evaluations: List[KnowledgeEntry] = [] 