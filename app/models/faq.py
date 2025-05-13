from typing import Optional, List, Dict
from pydantic import BaseModel
from enum import Enum

class FAQCategory(str, Enum):
    BOOKING = "booking"
    MENU = "menu"
    PAYMENT = "payment"
    FACILITIES = "facilities"
    TIMING = "timing"
    GENERAL = "general"

class FAQ(BaseModel):
    id: str
    question: str
    answer: str
    category: FAQCategory
    keywords: List[str]
    related_questions: List[str] = []
    metadata: Dict[str, str] = {}

class FAQResponse(BaseModel):
    question: str
    answer: str
    category: FAQCategory
    related_questions: List[str] = [] 