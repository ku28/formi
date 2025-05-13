from typing import Dict, Optional, Any
from app.prompts.templates import TEMPLATES, PromptTemplate, PromptObjective
from app.services.knowledge_processor import KnowledgeProcessor
from datetime import datetime
from app.models.knowledge_base import KnowledgeBase

class PromptHandler:
    def __init__(self):
        self.templates = TEMPLATES
        self.knowledge_processor = KnowledgeProcessor()
        self.conversation_state: Dict[str, Dict] = {}
        
    def get_template(self, template_name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name"""
        return self.templates.get(template_name)
        
    def execute_template(self, template_name: str, conversation_id: str, user_input: Optional[str] = None) -> Dict[str, Any]:
        if conversation_id not in self.conversation_state:
            self.conversation_state[conversation_id] = {
                "collected_data": {},
                "current_state": "initial",
                "last_message": None
            }
            
        handler = self.templates.get(template_name)
        if not handler:
            return {
                "message": "I apologize, but I'm not sure how to handle that request.",
                "response_type": "error"
            }
            
        return handler(conversation_id, user_input)
        
    def _handle_initial_state(self, conversation_id: str, user_input: Optional[str]) -> Dict[str, Any]:
        return {
            "message": "Welcome to BBQ Nation! To better assist you, could you please let me know which city you're interested in?",
            "response_type": "transition",
            "next_state": "city_collection"
        }
        
    def _handle_city_collection(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        if not user_input:
            return {
                "message": "Please let me know which city you're interested in.",
                "response_type": "continue"
            }
            
        self.conversation_state[conversation_id]["collected_data"]["city"] = user_input
        return {
            "message": "Great! Which location in {city} would you prefer?".format(
                city=user_input
            ),
            "response_type": "transition",
            "next_state": "location_collection"
        }
        
    def _handle_location_collection(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        if not user_input:
            return {
                "message": "Please select a specific location.",
                "response_type": "continue"
            }
            
        self.conversation_state[conversation_id]["collected_data"]["location"] = user_input
        return {
            "message": "How can I help you today? Would you like to browse our menu or make a reservation?",
            "response_type": "transition",
            "next_state": "intent_identification"
        }
        
    def _handle_intent(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        if "menu" in user_input.lower():
            return {
                "message": "I'll help you explore our menu. What type of dishes are you interested in?",
                "response_type": "transition",
                "next_state": "menu_browsing"
            }
        elif "reserv" in user_input.lower() or "book" in user_input.lower():
            return {
                "message": "I'll help you make a reservation. How many people will be dining?",
                "response_type": "transition",
                "next_state": "reservation"
            }
        else:
            return {
                "message": "Could you please clarify if you'd like to browse our menu or make a reservation?",
                "response_type": "continue"
            }
            
    def _handle_menu_browsing(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        # Store menu preferences
        self.conversation_state[conversation_id]["collected_data"]["menu_preference"] = user_input
        return {
            "message": "Here are some dishes that match your preferences. Would you like to know more about any specific dish?",
            "response_type": "transition",
            "next_state": "clarification"
        }
        
    def _handle_reservation(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        try:
            party_size = int(user_input)
            self.conversation_state[conversation_id]["collected_data"]["party_size"] = party_size
            return {
                "message": "What date and time would you prefer for your reservation?",
                "response_type": "transition",
                "next_state": "time_slot_verification"
            }
        except ValueError:
            return {
                "message": "Please provide the number of people in your party.",
                "response_type": "continue"
            }
            
    def _handle_time_slot(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        # Here we would validate the time slot against available slots
        self.conversation_state[conversation_id]["collected_data"]["requested_time"] = user_input
        return {
            "message": "Let me check availability for your requested time. Would you like me to confirm this reservation?",
            "response_type": "transition",
            "next_state": "confirmation"
        }
        
    def _handle_clarification(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        return {
            "message": "I'll provide more details about that. Is there anything specific you'd like to know?",
            "response_type": "transition",
            "next_state": "modification"
        }
        
    def _handle_modification(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        return {
            "message": "I'll help you modify that. What would you like to change?",
            "response_type": "transition",
            "next_state": "confirmation"
        }
        
    def _handle_confirmation(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        if "yes" in user_input.lower() or "confirm" in user_input.lower():
            return {
                "message": "Great! Your request has been confirmed. Is there anything else I can help you with?",
                "response_type": "transition",
                "next_state": "intent_identification"
            }
        else:
            return {
                "message": "Would you like to modify your request?",
                "response_type": "transition",
                "next_state": "modification"
            }
        
    def _verify_with_tool(self, tool_name: str, value: str) -> Dict[str, Any]:
        """Verify data using the specified tool"""
        if tool_name == "get_available_cities":
            available_cities = self.knowledge_processor.get_available_cities()
            return {
                "valid": value in available_cities,
                "message": f"City {value} is {'valid' if value in available_cities else 'invalid'}"
            }
        elif tool_name == "get_locations_in_city":
            city = self.conversation_state.get("city", "")
            available_locations = self.knowledge_processor.get_locations_in_city(city)
            return {
                "valid": value in available_locations,
                "message": f"Location {value} is {'valid' if value in available_locations else 'invalid'}"
            }
        return {"valid": False, "message": f"Unknown tool: {tool_name}"}
        
    def _evaluate_condition(self, condition: str, state: Dict[str, Any]) -> bool:
        """Evaluate a transition condition"""
        # Simple condition evaluation for now
        if condition == "city_valid and city_confirmed":
            return (
                state.get("collected_data", {}).get("city") and
                state.get("confirmations", {}).get("city", False)
            )
        elif condition == "city_invalid":
            return not state.get("collected_data", {}).get("city")
        elif condition == "location_confirmed":
            return state.get("confirmations", {}).get("location", False)
        return False
        
    def _get_information(self, info_type: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Get information based on type and state"""
        if info_type == "outlet_details":
            city = state["collected_data"].get("city")
            location = state["collected_data"].get("location")
            outlet_info = self.knowledge_processor.knowledge_base.outlets.get(city, {}).get(location, {})
            return {
                "message": f"Here are the details for our {location} outlet: {outlet_info}"
            }
        return {"message": "No information available"} 