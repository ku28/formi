from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
import pandas as pd
import json

class ConversationMetrics(BaseModel):
    conversation_id: str
    start_time: datetime
    end_time: datetime
    duration: float  # in seconds
    total_turns: int
    user_messages: int
    bot_messages: int
    intent_success_rate: float
    task_completion: bool
    user_satisfaction: Optional[float]
    error_count: int
    state_transitions: List[Dict[str, str]]

class AnalysisHandler:
    def __init__(self):
        self.metrics: Dict[str, ConversationMetrics] = {}
        
    def analyze_conversation(self, conversation_id: str, conversation_data: Dict) -> ConversationMetrics:
        """Analyze a completed conversation and generate metrics"""
        
        # Calculate basic metrics
        start_time = datetime.fromisoformat(conversation_data["start_time"])
        end_time = datetime.fromisoformat(conversation_data["end_time"])
        duration = (end_time - start_time).total_seconds()
        
        # Count messages
        messages = conversation_data["history"]
        user_messages = len([m for m in messages if m["role"] == "user"])
        bot_messages = len([m for m in messages if m["role"] == "assistant"])
        
        # Analyze intent success
        state_transitions = conversation_data["state_transitions"]
        successful_transitions = len([t for t in state_transitions if t["success"]])
        intent_success_rate = successful_transitions / len(state_transitions) if state_transitions else 0
        
        # Check task completion
        task_completion = conversation_data.get("task_completed", False)
        
        # Count errors
        error_count = len([m for m in messages if m.get("error", False)])
        
        # Create metrics object
        metrics = ConversationMetrics(
            conversation_id=conversation_id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            total_turns=len(messages),
            user_messages=user_messages,
            bot_messages=bot_messages,
            intent_success_rate=intent_success_rate,
            task_completion=task_completion,
            user_satisfaction=conversation_data.get("user_satisfaction"),
            error_count=error_count,
            state_transitions=state_transitions
        )
        
        self.metrics[conversation_id] = metrics
        return metrics
        
    def generate_analysis_report(self, time_period: Optional[str] = None) -> Dict:
        """Generate analysis report for all conversations or specific time period"""
        
        metrics_list = list(self.metrics.values())
        
        if time_period:
            # Filter metrics by time period
            end_time = datetime.now()
            if time_period == "day":
                start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)
            elif time_period == "week":
                start_time = end_time - timedelta(days=7)
            elif time_period == "month":
                start_time = end_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            metrics_list = [
                m for m in metrics_list 
                if start_time <= m.end_time <= end_time
            ]
        
        # Calculate aggregate metrics
        total_conversations = len(metrics_list)
        avg_duration = sum(m.duration for m in metrics_list) / total_conversations if total_conversations > 0 else 0
        avg_turns = sum(m.total_turns for m in metrics_list) / total_conversations if total_conversations > 0 else 0
        overall_success_rate = sum(m.intent_success_rate for m in metrics_list) / total_conversations if total_conversations > 0 else 0
        completion_rate = len([m for m in metrics_list if m.task_completion]) / total_conversations if total_conversations > 0 else 0
        
        return {
            "period": time_period or "all",
            "total_conversations": total_conversations,
            "average_duration": avg_duration,
            "average_turns": avg_turns,
            "intent_success_rate": overall_success_rate,
            "task_completion_rate": completion_rate,
            "error_rate": sum(m.error_count for m in metrics_list) / total_conversations if total_conversations > 0 else 0,
            "user_satisfaction": sum(m.user_satisfaction or 0 for m in metrics_list) / total_conversations if total_conversations > 0 else None
        }
        
    def export_to_excel(self, filepath: str):
        """Export conversation metrics to Excel"""
        
        # Convert metrics to DataFrame
        data = []
        for metrics in self.metrics.values():
            data.append({
                "Conversation ID": metrics.conversation_id,
                "Start Time": metrics.start_time,
                "End Time": metrics.end_time,
                "Duration (sec)": metrics.duration,
                "Total Turns": metrics.total_turns,
                "User Messages": metrics.user_messages,
                "Bot Messages": metrics.bot_messages,
                "Intent Success Rate": metrics.intent_success_rate,
                "Task Completed": metrics.task_completion,
                "User Satisfaction": metrics.user_satisfaction,
                "Error Count": metrics.error_count
            })
            
        df = pd.DataFrame(data)
        
        # Add summary sheet
        with pd.ExcelWriter(filepath) as writer:
            df.to_excel(writer, sheet_name="Conversation Details", index=False)
            
            # Create summary sheet
            summary = pd.DataFrame([self.generate_analysis_report()])
            summary.to_excel(writer, sheet_name="Summary", index=False)
            
    def save_metrics(self, filepath: str):
        """Save metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(
                {k: v.dict() for k, v in self.metrics.items()},
                f,
                indent=2,
                default=str
            )
            
    def load_metrics(self, filepath: str):
        """Load metrics from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.metrics = {
                k: ConversationMetrics(**v) for k, v in data.items()
            } 