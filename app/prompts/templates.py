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

# Booking Collection Template
BOOKING_TEMPLATE = PromptTemplate(
    name="booking_collection",
    objective=PromptObjective.COLLECT_CONFIRM_INFORM,
    description="Collect and confirm booking details",
    instructions=[
        "1. Collect date and time for booking",
        "2. Collect number of guests",
        "3. Verify availability",
        "4. Collect customer name and contact",
        "5. Confirm all booking details",
        "6. Inform about booking confirmation"
    ],
    entities=[
        EntityDefinition(
            name="date",
            type=EntityType.DATE,
            collection_method="direct_input",
            verification_method=VerificationMethod.TOOL,
            tool_name="verify_date",
            validation_rules={
                "not_past": "Date cannot be in the past",
                "within_range": "Date must be within next 30 days"
            }
        ),
        EntityDefinition(
            name="time",
            type=EntityType.TIME,
            collection_method="option_selection",
            verification_method=VerificationMethod.TOOL,
            tool_name="verify_time_slot",
            options=["12:00 PM", "1:00 PM", "2:00 PM", "7:00 PM", "8:00 PM", "9:00 PM"],
            validation_rules={
                "valid_slot": "Time must be an available slot"
            }
        ),
        EntityDefinition(
            name="guests",
            type=EntityType.NUMBER,
            collection_method="direct_input",
            verification_method=VerificationMethod.IN_CONTEXT,
            validation_rules={
                "min_guests": "Minimum 2 guests required",
                "max_guests": "Maximum 20 guests allowed per booking"
            }
        ),
        EntityDefinition(
            name="customer_name",
            type=EntityType.STRING,
            collection_method="direct_input",
            verification_method=VerificationMethod.IN_CONTEXT,
            validation_rules={
                "required": "Name is required"
            }
        ),
        EntityDefinition(
            name="contact_number",
            type=EntityType.STRING,
            collection_method="direct_input",
            verification_method=VerificationMethod.TOOL,
            tool_name="verify_phone",
            validation_rules={
                "valid_phone": "Must be a valid 10-digit phone number"
            }
        )
    ],
    confirmation_required=True,
    confirmation_method="explicit_confirmation",
    inform_conditions=[
        {
            "condition": "booking_confirmed",
            "information": "booking_details"
        }
    ],
    negative_consequences=[
        "If date is invalid, booking cannot proceed",
        "If time slot is unavailable, alternate slots must be suggested",
        "If guest count exceeds limit, booking cannot proceed",
        "If contact details are invalid, booking confirmation cannot be sent"
    ],
    transition_rules=[
        TransitionRule(
            condition="all_details_valid and booking_confirmed",
            next_state="booking_confirmation",
            reason="All booking details are valid and confirmed"
        ),
        TransitionRule(
            condition="date_invalid or time_invalid",
            next_state="booking_collection",
            reason="Date or time is invalid, need to recollect"
        ),
        TransitionRule(
            condition="guests_invalid",
            next_state="booking_collection",
            reason="Guest count is invalid, need to recollect"
        )
    ],
    examples=[
        {
            "user_input": "I want to book for tomorrow",
            "response": "Sure! What time would you prefer? We have slots available at 12:00 PM, 1:00 PM, 2:00 PM, 7:00 PM, 8:00 PM, and 9:00 PM.",
            "explanation": "Example of collecting booking time after date"
        },
        {
            "user_input": "8 PM for 4 people",
            "response": "Great! Could you please provide your name for the booking?",
            "explanation": "Example of collecting customer details"
        }
    ]
)

# FAQ Handling Template
FAQ_TEMPLATE = PromptTemplate(
    name="faq_handling",
    objective=PromptObjective.COLLECT_INFORM,
    description="Handle FAQ queries and provide relevant information",
    instructions=[
        "1. Identify FAQ category from user query",
        "2. Search knowledge base for relevant answer",
        "3. Provide answer with any related information",
        "4. Ask if the answer was helpful"
    ],
    entities=[
        EntityDefinition(
            name="query",
            type=EntityType.STRING,
            collection_method="direct_input",
            verification_method=VerificationMethod.TOOL,
            tool_name="search_faqs",
            validation_rules={
                "min_length": "Query must not be empty"
            }
        )
    ],
    confirmation_required=False,
    inform_conditions=[
        {
            "condition": "faq_found",
            "information": "faq_answer"
        },
        {
            "condition": "no_faq_found",
            "information": "alternative_help"
        }
    ],
    negative_consequences=[
        "If FAQ not found, user may need to be redirected to support",
        "If answer is incomplete, user satisfaction may be affected"
    ],
    transition_rules=[
        TransitionRule(
            condition="answer_provided and user_satisfied",
            next_state="end_conversation",
            reason="User's query has been answered satisfactorily"
        ),
        TransitionRule(
            condition="answer_provided and not user_satisfied",
            next_state="support_redirect",
            reason="User needs additional support"
        ),
        TransitionRule(
            condition="no_answer_found",
            next_state="support_redirect",
            reason="No relevant FAQ found, redirecting to support"
        )
    ],
    examples=[
        {
            "user_input": "What's your cancellation policy?",
            "response": "Our cancellation policy allows free cancellation up to 4 hours before your booking time. After that, a cancellation fee may apply. Would you like more details about specific scenarios?",
            "explanation": "Example of providing FAQ answer with follow-up option"
        },
        {
            "user_input": "Do you have valet parking?",
            "response": "Yes, we offer complimentary valet parking at most of our outlets. However, this may vary by location. Since you're interested in our {location} outlet, I can confirm that they do offer valet parking service.",
            "explanation": "Example of location-specific FAQ answer"
        }
    ]
)

# Add more templates for menu selection, booking, etc.

TEMPLATES = {
    "city_collection": CITY_COLLECTION_TEMPLATE,
    "location_collection": LOCATION_COLLECTION_TEMPLATE,
    "booking_collection": BOOKING_TEMPLATE,
    "faq_handling": FAQ_TEMPLATE
} 