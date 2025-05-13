from typing import List, Dict
from app.models.menu import (
    Menu, MenuCategory, MenuItem, SpiceLevel,
    CookingMethod, DietaryInfo
)

class MenuProcessor:
    def __init__(self):
        self.menu_categories = {
            "BBQ Starters": {
                "description": "Signature live grill specialties served at your table",
                "available_times": ["lunch", "dinner"],
                "items": [
                    {
                        "name": "Bharwan Mushroom",
                        "sub_category": "Vegetarian Grill",
                        "price": 299.0,
                        "spice_level": SpiceLevel.MEDIUM,
                        "cooking_method": CookingMethod.GRILLED,
                        "dietary_info": DietaryInfo(is_veg=True),
                        "preparation_time": 15,
                        "ingredients": ["mushroom", "cheese", "spices", "herbs"],
                        "accompaniments": ["mint chutney", "onion rings"]
                    },
                    {
                        "name": "Tandoori Chicken Wings",
                        "sub_category": "Non-Vegetarian Grill",
                        "price": 349.0,
                        "spice_level": SpiceLevel.SPICY,
                        "cooking_method": CookingMethod.TANDOOR,
                        "dietary_info": DietaryInfo(is_veg=False),
                        "preparation_time": 20,
                        "ingredients": ["chicken wings", "yogurt", "tandoori masala"],
                        "chef_special": True
                    }
                ]
            },
            "Coastal Delights": {
                "description": "Fresh seafood specialties from coastal regions",
                "available_times": ["dinner"],
                "items": [
                    {
                        "name": "Konkan Fish Curry",
                        "sub_category": "Seafood",
                        "price": 449.0,
                        "spice_level": SpiceLevel.SPICY,
                        "cooking_method": CookingMethod.CURRY,
                        "dietary_info": DietaryInfo(is_veg=False),
                        "preparation_time": 25,
                        "ingredients": ["fish", "coconut", "kokum", "spices"],
                        "customization_options": {
                            "spice_level": ["mild", "medium", "spicy"]
                        }
                    }
                ]
            }
        }

    def process_raw_menu(self) -> Menu:
        categories: List[MenuCategory] = []
        
        for cat_name, cat_data in self.menu_categories.items():
            menu_items: List[MenuItem] = []
            
            for item_data in cat_data["items"]:
                menu_items.append(
                    MenuItem(
                        name=item_data["name"],
                        category=cat_name,
                        sub_category=item_data["sub_category"],
                        price=item_data["price"],
                        spice_level=item_data["spice_level"],
                        cooking_method=item_data["cooking_method"],
                        dietary_info=item_data["dietary_info"],
                        preparation_time=item_data["preparation_time"],
                        ingredients=item_data["ingredients"],
                        chef_special=item_data.get("chef_special", False),
                        accompaniments=item_data.get("accompaniments", []),
                        customization_options=item_data.get("customization_options", {})
                    )
                )
            
            categories.append(
                MenuCategory(
                    name=cat_name,
                    description=cat_data["description"],
                    items=menu_items,
                    available_times=cat_data["available_times"]
                )
            )
        
        return Menu(
            categories=categories,
            last_updated="2024-05-12",
            special_offers=[
                "20% off on weekday lunches",
                "Complimentary dessert on birthdays"
            ],
            seasonal_items=[
                "Mango Dessert Festival",
                "Summer Coolers Special"
            ],
            festival_specials={
                "Diwali": ["Special Thali", "Festival Sweets"],
                "Christmas": ["Plum Cake", "Mulled Wine"]
            }
        )

    def get_menu_by_category(self, category: str) -> List[MenuItem]:
        menu = self.process_raw_menu()
        for cat in menu.categories:
            if cat.name.lower() == category.lower():
                return cat.items
        return []

    def get_menu_by_dietary_preference(self, 
                                     is_veg: bool = None,
                                     is_jain: bool = None,
                                     is_halal: bool = None,
                                     gluten_free: bool = None) -> List[MenuItem]:
        menu = self.process_raw_menu()
        filtered_items = []
        
        for category in menu.categories:
            for item in category.items:
                if (is_veg is None or item.dietary_info.is_veg == is_veg) and \
                   (is_jain is None or item.dietary_info.is_jain == is_jain) and \
                   (is_halal is None or item.dietary_info.is_halal == is_halal) and \
                   (gluten_free is None or item.dietary_info.gluten_free == gluten_free):
                    filtered_items.append(item)
        
        return filtered_items

    def get_chef_specials(self) -> List[MenuItem]:
        menu = self.process_raw_menu()
        return [item for cat in menu.categories 
                for item in cat.items if item.chef_special]

    def get_items_by_spice_level(self, spice_level: SpiceLevel) -> List[MenuItem]:
        menu = self.process_raw_menu()
        return [item for cat in menu.categories 
                for item in cat.items if item.spice_level == spice_level] 