from typing import Optional
from pydantic import BaseModel

class FAQ(BaseModel):
    question_id: str
    question: str
    answer: str
    category: str
    tags: list[str]
    response_template: Optional[str] = None

class FAQCategory(BaseModel):
    name: str
    description: Optional[str] = None
    faqs: list[FAQ] 