from typing import Dict, Optional, List
from pydantic import BaseModel
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
    available_cities: List[str] = []
    available_locations: Dict[str, List[str]] = {}

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
                "current_template": "city_collection",
                "history": []
            }
        else:
            conversation_id = user_message.conversation_id
            
        conversation = self.conversations[conversation_id]
        current_template = conversation["current_template"]
        
        # Execute current template
        result = self.prompt_handler.execute_template(
            current_template,
            conversation_id,
            user_message.message if user_message.conversation_id else None
        )
        
        # Update conversation state based on template result
        if result["response_type"] == "transition":
            conversation["current_template"] = result["next_state"]
            
        # Store message in conversation history
        conversation["history"].append(
            Conversation(role="user", content=user_message.message)
        )
        
        # Build response
        response = ChatResponse(
            response=result["message"],
            conversation_id=conversation_id
        )
        
        # Add city/location requirements if needed
        if current_template == "city_collection":
            response.requires_city = True
            response.available_cities = self.knowledge_processor.get_available_cities()
        elif current_template == "location_collection":
            response.requires_location = True
            city = self.prompt_handler.conversation_state[conversation_id]["collected_data"].get("city")
            if city:
                response.available_locations = {
                    city: self.knowledge_processor.get_locations_in_city(city)
                }
                
        return response 