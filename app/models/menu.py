from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import Enum

class SpiceLevel(str, Enum):
    MILD = "mild"
    MEDIUM = "medium"
    SPICY = "spicy"
    EXTRA_SPICY = "extra_spicy"

class CookingMethod(str, Enum):
    GRILLED = "grilled"
    TANDOOR = "tandoor"
    TAWA = "tawa"
    CURRY = "curry"
    STEAMED = "steamed"
    BAKED = "baked"

class DietaryInfo(BaseModel):
    is_veg: bool
    is_jain: bool = False
    is_halal: bool = True
    contains_egg: bool = False
    contains_dairy: bool = False
    contains_nuts: bool = False
    gluten_free: bool = False

class MenuItem(BaseModel):
    name: str
    category: str
    sub_category: str
    description: Optional[str] = None
    price: float
    spice_level: SpiceLevel
    cooking_method: CookingMethod
    dietary_info: DietaryInfo
    preparation_time: int  # in minutes
    chef_special: bool = False
    ingredients: List[str]
    accompaniments: List[str] = []
    customization_options: Dict[str, List[str]] = {}

class MenuCategory(BaseModel):
    name: str
    description: str
    items: List[MenuItem]
    available_times: List[str]  # e.g., ["lunch", "dinner"]
    image_url: Optional[str] = None

class Menu(BaseModel):
    categories: List[MenuCategory]
    last_updated: str
    special_offers: List[str] = []
    seasonal_items: List[str] = []
    festival_specials: Dict[str, List[str]] = {} 