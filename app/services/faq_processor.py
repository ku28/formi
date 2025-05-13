from typing import List, Dict, Optional
from app.models.faq import FAQ, FAQCategory, FAQResponse

class FAQProcessor:
    def __init__(self):
        self.faqs: List[FAQ] = [
            # Menu & Food Related FAQs
            FAQ(
                id="menu-1",
                question="Is Jain food available in BBQ nation?",
                answer="Yes, we have Jain food available but variety will be limited. Please inform the outlet team about Jain food requirements when you arrive.",
                category=FAQCategory.MENU,
                keywords=["jain", "food", "dietary", "restrictions"],
                related_questions=["What vegetarian options do you have?", "Do you have special dietary menus?"]
            ),
            FAQ(
                id="menu-2",
                question="Does Barbeque Nation serve Halal food?",
                answer="Yes, we serve Halal food (Meat) in all the barbeque nation outlets.",
                category=FAQCategory.MENU,
                keywords=["halal", "meat", "food", "dietary"],
                related_questions=["Do you have Halal certification?", "What meat options are available?"]
            ),
            FAQ(
                id="menu-3",
                question="Do you have any proof / Certificate for Halal?",
                answer="Yes, we do have Halal certificates in all the barbeque nation outlets.",
                category=FAQCategory.MENU,
                keywords=["halal", "certificate", "proof", "documentation"],
                related_questions=["Is your meat Halal certified?", "Can I see the Halal certificate?"]
            ),
            FAQ(
                id="menu-4",
                question="What is included in the menu?",
                answer="Our menu includes a variety of starters (veg and non-veg), main course dishes (Indian, Chinese, and Continental), live grill options, and an extensive dessert selection. The exact menu may vary by location and season.",
                category=FAQCategory.MENU,
                keywords=["menu", "items", "food", "dishes", "options"],
                related_questions=["What are your signature dishes?", "Do you have seasonal specials?"]
            ),
            
            # Booking Related FAQs
            FAQ(
                id="booking-1",
                question="How do I make a reservation?",
                answer="You can make a reservation through our website, mobile app, or by calling the restaurant directly. We also accept walk-ins subject to availability.",
                category=FAQCategory.BOOKING,
                keywords=["reservation", "booking", "table"],
                related_questions=["What's the cancellation policy?", "Do you accept walk-ins?"]
            ),
            FAQ(
                id="booking-2",
                question="What is the seating capacity?",
                answer="Seating capacity varies by location. Our outlets typically accommodate between 100-150 guests. For large group bookings, please contact the specific outlet in advance.",
                category=FAQCategory.BOOKING,
                keywords=["capacity", "seating", "group", "booking"],
                related_questions=["Can you accommodate large groups?", "Do you have private dining areas?"]
            ),
            
            # Timing Related FAQs
            FAQ(
                id="timing-1",
                question="What are your operating hours?",
                answer="We are open for both lunch (12:00 PM - 3:30 PM) and dinner (7:00 PM - 11:00 PM). Last orders are taken 30 minutes before closing time.",
                category=FAQCategory.TIMING,
                keywords=["timing", "hours", "open", "close"],
                related_questions=["When is the last order taken?", "Are you open on holidays?"]
            ),
            
            # Payment Related FAQs
            FAQ(
                id="payment-1",
                question="What payment methods do you accept?",
                answer="We accept all major credit/debit cards, UPI payments, digital wallets, and cash. Corporate cards are also accepted.",
                category=FAQCategory.PAYMENT,
                keywords=["payment", "cards", "UPI", "cash"],
                related_questions=["Do you accept corporate cards?", "Is advance payment required for booking?"]
            ),
            
            # Facilities Related FAQs
            FAQ(
                id="facilities-1",
                question="Do you have parking facilities?",
                answer="Yes, we provide valet parking services at most of our outlets. Some locations also have dedicated parking areas.",
                category=FAQCategory.FACILITIES,
                keywords=["parking", "valet", "facility"],
                related_questions=["Is wheelchair access available?", "Do you have private dining rooms?"]
            ),
            FAQ(
                id="facilities-2",
                question="Do you have wheelchair accessibility?",
                answer="Yes, most of our outlets are wheelchair accessible with ramps and elevators. Please check with specific outlets for detailed accessibility information.",
                category=FAQCategory.FACILITIES,
                keywords=["wheelchair", "accessibility", "disabled", "access"],
                related_questions=["Do you have disabled parking?", "Is there elevator access?"]
            )
        ]
        
    def get_faq_by_id(self, faq_id: str) -> Optional[FAQ]:
        """Get FAQ by ID"""
        for faq in self.faqs:
            if faq.id == faq_id:
                return faq
        return None
        
    def search_faqs(self, query: str, category: Optional[FAQCategory] = None) -> List[FAQResponse]:
        """Search FAQs by query and optional category"""
        results = []
        query = query.lower()
        
        for faq in self.faqs:
            # Skip if category doesn't match
            if category and faq.category != category:
                continue
                
            # Check if query matches keywords or question
            if (query in faq.question.lower() or
                query in faq.answer.lower() or
                any(query in keyword.lower() for keyword in faq.keywords)):
                
                results.append(FAQResponse(
                    question=faq.question,
                    answer=faq.answer,
                    category=faq.category,
                    related_questions=faq.related_questions
                ))
                
        return results
        
    def get_faqs_by_category(self, category: FAQCategory) -> List[FAQResponse]:
        """Get all FAQs in a category"""
        return [
            FAQResponse(
                question=faq.question,
                answer=faq.answer,
                category=faq.category,
                related_questions=faq.related_questions
            )
            for faq in self.faqs
            if faq.category == category
        ]
        
    def add_faq(self, faq: FAQ) -> None:
        """Add a new FAQ"""
        self.faqs.append(faq)
        
    def update_faq(self, faq_id: str, updated_faq: FAQ) -> bool:
        """Update an existing FAQ"""
        for i, faq in enumerate(self.faqs):
            if faq.id == faq_id:
                self.faqs[i] = updated_faq
                return True
        return False
        
    def delete_faq(self, faq_id: str) -> bool:
        """Delete an FAQ"""
        for i, faq in enumerate(self.faqs):
            if faq.id == faq_id:
                self.faqs.pop(i)
                return True
        return False 