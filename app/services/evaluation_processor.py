from typing import List, Dict, Optional
from datetime import datetime
from app.models.evaluation import (
    ConversationEvaluation, EvaluationResult, ConversationMetrics,
    CategoryType, EvaluationCriteria
)

class EvaluationProcessor:
    def __init__(self):
        self.evaluation_criteria = ConversationEvaluation()
        self.results: List[EvaluationResult] = []
        
    def evaluate_conversation(
        self,
        conversation_id: str,
        evaluation_data: Dict[str, Dict[int, bool]]
    ) -> List[EvaluationResult]:
        """
        Evaluate a conversation against the criteria
        
        Args:
            conversation_id: Unique identifier for the conversation
            evaluation_data: Dict mapping criteria_id to Dict of check_id -> bool results
        """
        results = []
        timestamp = datetime.now().isoformat()
        
        for criteria_id, checks in evaluation_data.items():
            for check_id, result in checks.items():
                evaluation_result = EvaluationResult(
                    conversation_id=conversation_id,
                    timestamp=timestamp,
                    criteria_id=criteria_id,
                    check_id=check_id,
                    result=result
                )
                results.append(evaluation_result)
                self.results.append(evaluation_result)
        
        return results

    def get_conversation_metrics(
        self,
        conversation_id: Optional[str] = None
    ) -> ConversationMetrics:
        """Calculate metrics for a specific conversation or all conversations"""
        if conversation_id:
            relevant_results = [r for r in self.results if r.conversation_id == conversation_id]
        else:
            relevant_results = self.results
        
        total_checks = len(relevant_results)
        successful_checks = len([r for r in relevant_results if r.result])
        
        return ConversationMetrics(
            total_conversations=len(set(r.conversation_id for r in relevant_results)),
            successful_intents=successful_checks,
            failed_intents=total_checks - successful_checks,
            avg_conversation_duration=0.0,  # This would need actual conversation duration data
            accuracy_score=successful_checks / total_checks if total_checks > 0 else 0.0,
            completion_rate=1.0,  # This would need actual completion data
            customer_satisfaction=None  # This would need actual CSAT data
        )

    def get_criteria_performance(
        self,
        category_type: Optional[CategoryType] = None
    ) -> Dict[str, float]:
        """Calculate performance metrics for each criteria"""
        criteria_results: Dict[str, Dict[str, int]] = {}
        
        for result in self.results:
            if result.criteria_id not in criteria_results:
                criteria_results[result.criteria_id] = {
                    "total": 0,
                    "successful": 0
                }
            
            criteria_results[result.criteria_id]["total"] += 1
            if result.result:
                criteria_results[result.criteria_id]["successful"] += 1
        
        return {
            criteria_id: stats["successful"] / stats["total"]
            for criteria_id, stats in criteria_results.items()
        }

    def generate_evaluation_report(
        self,
        conversation_id: Optional[str] = None
    ) -> Dict[str, any]:
        """Generate a comprehensive evaluation report"""
        metrics = self.get_conversation_metrics(conversation_id)
        criteria_performance = self.get_criteria_performance()
        
        return {
            "metrics": metrics.dict(),
            "criteria_performance": criteria_performance,
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id
        }

    def get_improvement_suggestions(
        self,
        conversation_id: str
    ) -> List[str]:
        """Generate improvement suggestions based on evaluation results"""
        conversation_results = [
            r for r in self.results if r.conversation_id == conversation_id
        ]
        
        suggestions = []
        for result in conversation_results:
            if not result.result:
                # Find the corresponding criteria and check
                for criteria_list in [
                    self.evaluation_criteria.positive_neutral_criteria,
                    self.evaluation_criteria.negative_criteria,
                    self.evaluation_criteria.ambiguous_complex_criteria
                ]:
                    for criteria in criteria_list:
                        if criteria.ctq == result.criteria_id:
                            for check in criteria.qa_checks:
                                if check.check_id == result.check_id:
                                    suggestions.append(
                                        f"Improve: {criteria.ctq} - {check.description}"
                                    )
        
        return suggestions 