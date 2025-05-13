from typing import List, Dict, Optional
from app.models.knowledge_base import KnowledgeBase, KnowledgeEntry, OutletInfo, Conversation
import json
import os
from datetime import datetime, time

class KnowledgeProcessor:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.processed_data_path = "data/processed"
        self.cities = {
            "Bangalore": ["Indiranagar", "JP Nagar"],
            "New Delhi": ["Connaught Place", "Vasant Kunj"]
        }
        self.menu_categories = {
            "starters": ["veg", "non-veg"],
            "main_course": ["indian", "chinese", "continental"],
            "desserts": ["indian", "international"]
        }

    def save_processed_data(self) -> None:
        """Save processed data to JSON files"""
        if not os.path.exists(self.processed_data_path):
            os.makedirs(self.processed_data_path)

        # Save menu items
        with open(f"{self.processed_data_path}/menu_items.json", "w") as f:
            json.dump(self.knowledge_base.menu_items, f, indent=2)

        # Save outlet information
        with open(f"{self.processed_data_path}/outlets.json", "w") as f:
            json.dump(self.knowledge_base.outlets, f, indent=2, default=lambda x: x.dict())

    def load_processed_data(self) -> None:
        """Load processed data from JSON files"""
        try:
            # Load menu items
            with open(f"{self.processed_data_path}/menu_items.json", "r") as f:
                self.knowledge_base.menu_items = json.load(f)

            # Load outlet information
            with open(f"{self.processed_data_path}/outlets.json", "r") as f:
                outlets_data = json.load(f)
                for city, outlets in outlets_data.items():
                    self.knowledge_base.outlets[city] = {
                        name: OutletInfo(**info) for name, info in outlets.items()
                    }

        except FileNotFoundError:
            print("Processed data files not found. Please run processing first.")
        
    def get_available_cities(self) -> List[str]:
        """Get list of available cities"""
        return list(self.cities.keys())
        
    def get_locations_in_city(self, city: str) -> List[str]:
        """Get available locations for a given city"""
        return self.cities.get(city, [])
        
    def get_menu_items(self, preference: str) -> List[Dict]:
        """Get menu items based on preference"""
        # Implementation would filter based on preference
        return []
        
    def get_available_time_slots(self, location: str) -> List[str]:
        """Get available time slots for a location"""
        # This would normally check a database or reservation system
        # For now, return sample slots
        return [
            "11:30 AM", "12:00 PM", "12:30 PM",
            "1:00 PM", "1:30 PM", "2:00 PM",
            "7:00 PM", "7:30 PM", "8:00 PM",
            "8:30 PM", "9:00 PM", "9:30 PM"
        ]
        
    def verify_time_slot(self, location: str, requested_time: str) -> bool:
        """Verify if a time slot is available"""
        available_slots = self.get_available_time_slots(location)
        return requested_time in available_slots
        
    def get_menu_recommendations(self, preferences: Dict[str, str]) -> List[Dict]:
        """Get menu recommendations based on preferences"""
        # Implementation would use preferences to filter and rank items
        return []
        
    def get_dietary_options(self) -> Dict[str, List[str]]:
        """Get available dietary options"""
        return {
            "vegetarian": ["Pure Veg", "Jain"],
            "non_vegetarian": ["Chicken", "Mutton", "Seafood"],
            "special": ["Gluten Free", "Low Calorie"]
        }
        
    def get_spice_levels(self) -> List[str]:
        """Get available spice levels"""
        return ["Mild", "Medium", "Spicy", "Extra Spicy"]
        
    def search_menu_items(self, query: str) -> List[Dict]:
        """Search menu items by query"""
        # Implementation would search through menu items
        return []
        
    def get_popular_dishes(self) -> List[Dict]:
        """Get list of popular dishes"""
        # Implementation would return popular dishes
        return []
        
    def get_special_offers(self) -> List[Dict]:
        """Get current special offers"""
        # Implementation would return current offers
        return [] 