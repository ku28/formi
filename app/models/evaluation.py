from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class CategoryType(str, Enum):
    POSITIVE_NEUTRAL = "Positive / Neutral"
    NEGATIVE = "Negative"
    AMBIGUOUS_COMPLEX = "Ambiguous / Complex"

class QACheck(BaseModel):
    check_id: int
    description: str
    is_mandatory: bool = True

class EvaluationCriteria(BaseModel):
    category: CategoryType
    ctq: str  # Critical to Quality
    qa_checks: List[QACheck]

class ConversationEvaluation(BaseModel):
    positive_neutral_criteria: List[EvaluationCriteria] = [
        EvaluationCriteria(
            category=CategoryType.POSITIVE_NEUTRAL,
            ctq="Accurate Initial Information Collection",
            qa_checks=[
                QACheck(check_id=1, description="Was the correct City collected from the user at the start of the interaction?"),
                QACheck(check_id=2, description="If applicable, was the specific Location within the City collected accurately?"),
                QACheck(check_id=3, description="Did the agent confirm the collected City/Location before proceeding?")
            ]
        ),
        EvaluationCriteria(
            category=CategoryType.POSITIVE_NEUTRAL,
            ctq="Correct Intent Identification and Flow Navigation",
            qa_checks=[
                QACheck(check_id=1, description="Did the agent correctly identify the user's primary intent (Inquiry, New Booking, Cancellation, Modification)?"),
                QACheck(check_id=2, description="Did the agent guide the conversation down the appropriate path in the flow based on the identified intent?"),
                QACheck(check_id=3, description="Did the agent avoid unnecessary steps or loops in the conversation flow based on user intent?")
            ]
        ),
        # Add other positive/neutral criteria here
    ]

    negative_criteria: List[EvaluationCriteria] = [
        EvaluationCriteria(
            category=CategoryType.NEGATIVE,
            ctq="Accuracy (in understanding issue)",
            qa_checks=[
                QACheck(check_id=1, description="Did the agent accurately identify the core issue or reason for the customer's feedback/complaint?"),
                QACheck(check_id=2, description="Were the specific details provided by the customer about the issue correctly understood and noted?"),
                QACheck(check_id=3, description="Did the agent confirm their understanding of the complaint back to the customer to ensure alignment?")
            ]
        ),
        # Add other negative criteria here
    ]

    ambiguous_complex_criteria: List[EvaluationCriteria] = [
        EvaluationCriteria(
            category=CategoryType.AMBIGUOUS_COMPLEX,
            ctq="Accurate Identification of Existing Booking Details",
            qa_checks=[
                QACheck(check_id=1, description="Was the customer's Name provided for an existing booking accurately used to search for the reservation?"),
                QACheck(check_id=2, description="Was the Time provided for the existing booking accurately used to search for the reservation?"),
                QACheck(check_id=3, description="If multiple bookings matched, did the agent accurately confirm the correct one with the customer?")
            ]
        ),
        # Add other ambiguous/complex criteria here
    ]

class EvaluationResult(BaseModel):
    conversation_id: str
    timestamp: str
    criteria_id: str
    check_id: int
    result: bool
    notes: Optional[str] = None

class ConversationMetrics(BaseModel):
    total_conversations: int
    successful_intents: int
    failed_intents: int
    avg_conversation_duration: float
    accuracy_score: float
    completion_rate: float
    customer_satisfaction: Optional[float] = None 