from typing import Dict, Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.knowledge_base import Conversation, KnowledgeBase
from app.services.knowledge_processor import KnowledgeProcessor
from app.services.prompt_handler import PromptHandler

class UserMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    requires_city: bool = False
    requires_location: bool = False
    requires_time_slot: bool = False
    requires_confirmation: bool = False
    available_cities: List[str] = []
    available_locations: Dict[str, List[str]] = {}
    available_time_slots: List[str] = []
    menu_items: List[Dict] = []

class ChatHandler:
    def __init__(self):
        self.knowledge_processor = KnowledgeProcessor()
        self.knowledge_processor.load_processed_data()
        self.prompt_handler = PromptHandler()
        self.conversations: Dict[str, Dict] = {}
        
    def handle_message(self, user_message: UserMessage) -> ChatResponse:
        """Handle incoming user message and generate appropriate response"""
        
        # Initialize conversation if new
        if not user_message.conversation_id:
            conversation_id = f"conv_{len(self.conversations) + 1}"
            self.conversations[conversation_id] = {
                "current_template": "initial",
                "history": [],
                "state": {}
            }
        else:
            conversation_id = user_message.conversation_id
            
        conversation = self.conversations[conversation_id]
        current_template = conversation["current_template"]
        
        # Execute current template
        result = self.prompt_handler.execute_template(
            current_template,
            conversation_id,
            user_message.message
        )
        
        # Update conversation state based on template result
        if result["response_type"] == "transition":
            conversation["current_template"] = result["next_state"]
            
        # Store message in conversation history
        conversation["history"].append(
            Conversation(
                role="user",
                content=user_message.message,
                timestamp=datetime.now()
            )
        )
        
        # Build response
        response = ChatResponse(
            response=result["message"],
            conversation_id=conversation_id
        )
        
        # Add state-specific requirements and data
        self._add_state_requirements(response, current_template, conversation_id)
        
        return response
        
    def _add_state_requirements(self, response: ChatResponse, current_template: str, conversation_id: str):
        """Add state-specific requirements and data to the response"""
        
        if current_template == "initial":
            response.requires_city = True
            response.available_cities = self.knowledge_processor.get_available_cities()
            
        elif current_template == "city_collection":
            response.requires_location = True
            city = self.prompt_handler.conversation_state[conversation_id]["collected_data"].get("city")
            if city:
                response.available_locations = {
                    city: self.knowledge_processor.get_locations_in_city(city)
                }
                
        elif current_template == "menu_browsing":
            menu_preference = self.prompt_handler.conversation_state[conversation_id]["collected_data"].get("menu_preference")
            if menu_preference:
                response.menu_items = self.knowledge_processor.get_menu_items(menu_preference)
                
        elif current_template == "time_slot_verification":
            response.requires_time_slot = True
            location = self.prompt_handler.conversation_state[conversation_id]["collected_data"].get("location")
            if location:
                response.available_time_slots = self.knowledge_processor.get_available_time_slots(location)
                
        elif current_template == "confirmation":
            response.requires_confirmation = True 