from typing import Dict, Optional, Any
from app.prompts.templates import TEMPLATES, PromptTemplate, PromptObjective
from app.services.knowledge_processor import KnowledgeProcessor

class PromptHandler:
    def __init__(self):
        self.templates = TEMPLATES
        self.knowledge_processor = KnowledgeProcessor()
        self.conversation_state: Dict[str, Dict[str, Any]] = {}
        
    def get_template(self, template_name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name"""
        return self.templates.get(template_name)
        
    def execute_template(self, template_name: str, conversation_id: str, user_input: Optional[str] = None) -> Dict[str, Any]:
        """Execute a prompt template for a given conversation"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")
            
        # Initialize conversation state if needed
        if conversation_id not in self.conversation_state:
            self.conversation_state[conversation_id] = {
                "current_template": template_name,
                "collected_data": {},
                "confirmations": {},
                "informed_data": {}
            }
            
        state = self.conversation_state[conversation_id]
        
        # Handle template based on objective
        if template.objective == PromptObjective.COLLECT_CONFIRM:
            return self._handle_collect_confirm(template, state, user_input)
        elif template.objective == PromptObjective.COLLECT_CONFIRM_INFORM:
            return self._handle_collect_confirm_inform(template, state, user_input)
        # Add more objective handlers as needed
        
        raise ValueError(f"Unsupported template objective: {template.objective}")
        
    def _handle_collect_confirm(self, template: PromptTemplate, state: Dict[str, Any], user_input: Optional[str]) -> Dict[str, Any]:
        """Handle collection and confirmation of data"""
        entity = template.entities[0]  # Assume single entity for now
        
        # If no user input, start collection
        if not user_input:
            return {
                "response_type": "collect",
                "message": template.examples[0]["response"],
                "requires_input": True
            }
            
        # Verify collected data
        if entity.verification_method == "tool":
            tool_result = self._verify_with_tool(entity.tool_name, user_input)
            if not tool_result["valid"]:
                return {
                    "response_type": "error",
                    "message": tool_result["message"],
                    "requires_input": True
                }
                
        # Store collected data
        state["collected_data"][entity.name] = user_input
        
        # If confirmation required
        if template.confirmation_required and entity.name not in state["confirmations"]:
            confirmation_msg = f"Just to confirm, you selected {user_input}. Is this correct?"
            return {
                "response_type": "confirm",
                "message": confirmation_msg,
                "requires_input": True
            }
            
        # Handle transition
        for rule in template.transition_rules:
            if self._evaluate_condition(rule.condition, state):
                return {
                    "response_type": "transition",
                    "next_state": rule.next_state,
                    "message": "Great! Let's proceed.",
                    "requires_input": False
                }
                
        return {
            "response_type": "error",
            "message": "Unable to determine next step",
            "requires_input": False
        }
        
    def _handle_collect_confirm_inform(self, template: PromptTemplate, state: Dict[str, Any], user_input: Optional[str]) -> Dict[str, Any]:
        """Handle collection, confirmation and information delivery"""
        # First handle collection and confirmation
        collect_confirm_result = self._handle_collect_confirm(template, state, user_input)
        if collect_confirm_result["response_type"] != "transition":
            return collect_confirm_result
            
        # If we have conditions for informing
        if template.inform_conditions:
            for condition in template.inform_conditions:
                if self._evaluate_condition(condition["condition"], state):
                    info = self._get_information(condition["information"], state)
                    return {
                        "response_type": "inform",
                        "message": info["message"],
                        "next_state": collect_confirm_result["next_state"],
                        "requires_input": False
                    }
                    
        return collect_confirm_result
        
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