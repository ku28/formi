from typing import List, Dict, Optional
from app.models.faq import FAQ, FAQCategory

class FAQProcessor:
    def __init__(self):
        self.raw_faqs = {
            "Menu & Drinks": [
                {
                    "id": "Q1",
                    "question": "Is Jain food available in BBQ nation?",
                    "answer": "Yes, we have Jain food available but variety will be limited. Please inform the outlet team about Jain food requirements when you arrive.",
                    "tags": ["jain", "food", "dietary", "restrictions"]
                },
                {
                    "id": "Q2",
                    "question": "Does Barbeque Nation serve Halal food?",
                    "answer": "Yes, we serve Halal food (Meat) in all the barbeque nation outlets.",
                    "tags": ["halal", "meat", "food", "dietary"]
                },
                {
                    "id": "Q3",
                    "question": "Do you have any proof / Certificate for Halal?",
                    "answer": "Yes, we do have Halal certificates in all the barbeque nation outlets.",
                    "tags": ["halal", "certificate", "proof"]
                },
                {
                    "id": "Q4",
                    "question": "What is the menu for today?",
                    "answer": "Our menu includes a wide variety of veg and non-veg options. Would you like to know about specific items or categories?",
                    "tags": ["menu", "today", "food"]
                }
            ]
        }

    def process_raw_faqs(self) -> List[FAQCategory]:
        categories: List[FAQCategory] = []
        
        for category_name, faqs_data in self.raw_faqs.items():
            faq_list = [
                FAQ(
                    question_id=faq["id"],
                    question=faq["question"],
                    answer=faq["answer"],
                    category=category_name,
                    tags=faq["tags"]
                )
                for faq in faqs_data
            ]
            
            categories.append(
                FAQCategory(
                    name=category_name,
                    faqs=faq_list
                )
            )
        
        return categories

    def search_faqs(self, query: str) -> List[FAQ]:
        """Search FAQs based on query matching against questions, answers, and tags."""
        query = query.lower()
        results: List[FAQ] = []
        
        for category in self.process_raw_faqs():
            for faq in category.faqs:
                # Check if query matches question, answer, or tags
                if (query in faq.question.lower() or
                    query in faq.answer.lower() or
                    any(query in tag.lower() for tag in faq.tags)):
                    results.append(faq)
        
        return results

    def get_faq_by_id(self, faq_id: str) -> Optional[FAQ]:
        """Get a specific FAQ by its ID."""
        for category in self.process_raw_faqs():
            for faq in category.faqs:
                if faq.question_id.lower() == faq_id.lower():
                    return faq
        return None

    def get_faqs_by_category(self, category: str) -> List[FAQ]:
        """Get all FAQs in a specific category."""
        for cat in self.process_raw_faqs():
            if cat.name.lower() == category.lower():
                return cat.faqs
        return [] 