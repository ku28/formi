from typing import Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel

class PromptObjective(str, Enum):
    COLLECT = "collect"
    CONFIRM = "confirm"
    INFORM = "inform"
    COLLECT_CONFIRM = "collect_confirm"
    COLLECT_INFORM = "collect_inform"
    CONFIRM_INFORM = "confirm_inform"
    COLLECT_CONFIRM_INFORM = "collect_confirm_inform"

class EntityType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    OPTION = "option"
    DATE = "date"
    TIME = "time"

class VerificationMethod(str, Enum):
    TOOL = "tool"
    IN_CONTEXT = "in_context"
    BOTH = "both"

class TransitionRule(BaseModel):
    condition: str
    next_state: str
    reason: str

class EntityDefinition(BaseModel):
    name: str
    type: EntityType
    collection_method: str
    verification_method: VerificationMethod
    tool_name: Optional[str] = None
    options: Optional[List[str]] = None
    validation_rules: Optional[Dict[str, str]] = None

class PromptTemplate(BaseModel):
    name: str
    objective: PromptObjective
    description: str
    instructions: List[str]
    entities: List[EntityDefinition]
    confirmation_required: bool = False
    confirmation_method: Optional[str] = None
    inform_conditions: Optional[List[Dict[str, str]]] = None
    negative_consequences: List[str]
    transition_rules: List[TransitionRule]
    examples: List[Dict[str, str]]

# City Collection Template
CITY_COLLECTION_TEMPLATE = PromptTemplate(
    name="city_collection",
    objective=PromptObjective.COLLECT_CONFIRM,
    description="Collect and confirm the city where the user wants to dine",
    instructions=[
        "1. Ask the user which city they would like to dine in",
        "2. Verify if the city has BBQ Nation outlets",
        "3. If valid, confirm the city with the user",
        "4. If invalid, inform about available cities"
    ],
    entities=[
        EntityDefinition(
            name="city",
            type=EntityType.STRING,
            collection_method="direct_input",
            verification_method=VerificationMethod.TOOL,
            tool_name="get_available_cities",
            validation_rules={
                "must_exist": "City must be in available_cities list"
            }
        )
    ],
    confirmation_required=True,
    confirmation_method="explicit_confirmation",
    negative_consequences=[
        "If city is invalid, user cannot proceed with booking",
        "If city is not confirmed, location selection cannot begin"
    ],
    transition_rules=[
        TransitionRule(
            condition="city_valid and city_confirmed",
            next_state="location_collection",
            reason="City is valid and confirmed, proceed to collect specific location"
        ),
        TransitionRule(
            condition="city_invalid",
            next_state="city_collection",
            reason="City is invalid, ask for a valid city"
        )
    ],
    examples=[
        {
            "user_input": "Mumbai",
            "response": "I apologize, but we currently don't have outlets in Mumbai. We are present in Bangalore and New Delhi. Which of these cities would you like to dine in?",
            "explanation": "Example of handling invalid city"
        },
        {
            "user_input": "Bangalore",
            "response": "Great! Just to confirm, you'd like to dine at BBQ Nation in Bangalore?",
            "explanation": "Example of confirming valid city"
        }
    ]
)

# Location Collection Template
LOCATION_COLLECTION_TEMPLATE = PromptTemplate(
    name="location_collection",
    objective=PromptObjective.COLLECT_CONFIRM_INFORM,
    description="Collect and confirm specific outlet location in the selected city",
    instructions=[
        "1. Get available locations in the selected city",
        "2. Present location options to user",
        "3. Collect user's preferred location",
        "4. Verify if location exists",
        "5. Confirm location with user",
        "6. Inform about location-specific details"
    ],
    entities=[
        EntityDefinition(
            name="location",
            type=EntityType.OPTION,
            collection_method="selection_from_list",
            verification_method=VerificationMethod.TOOL,
            tool_name="get_locations_in_city",
            validation_rules={
                "must_exist": "Location must be in available_locations list for the city"
            }
        )
    ],
    confirmation_required=True,
    confirmation_method="explicit_confirmation",
    inform_conditions=[
        {
            "condition": "location_confirmed",
            "information": "outlet_details"
        }
    ],
    negative_consequences=[
        "If location is invalid, user cannot proceed with menu or booking",
        "If location is not confirmed, dining preferences cannot be collected"
    ],
    transition_rules=[
        TransitionRule(
            condition="location_valid and location_confirmed",
            next_state="menu_exploration",
            reason="Location is valid and confirmed, proceed to menu options"
        ),
        TransitionRule(
            condition="location_invalid",
            next_state="location_collection",
            reason="Location is invalid, ask for a valid location"
        )
    ],
    examples=[
        {
            "user_input": "Indiranagar",
            "response": "Perfect! Just to confirm, you'd like to dine at our Indiranagar outlet? It's located at No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038.",
            "explanation": "Example of confirming location and providing address"
        }
    ]
)

# Add more templates for menu selection, booking, etc.

TEMPLATES = {
    "city_collection": CITY_COLLECTION_TEMPLATE,
    "location_collection": LOCATION_COLLECTION_TEMPLATE
} 