from typing import List, Dict, Optional
from app.models.knowledge_base import KnowledgeBase, KnowledgeEntry, OutletInfo, Conversation
from app.models.evaluation import ConversationEvaluation, EvaluationCriteria, QACheck, CategoryType
import json
import os

class KnowledgeProcessor:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.processed_data_path = "data/processed"
        self.conversation_evaluation = ConversationEvaluation()

    def process_evaluation_data(self, evaluations: List[Dict]) -> None:
        """Process the evaluation data into structured format"""
        for eval_data in evaluations:
            entry = KnowledgeEntry(
                query=eval_data["query"],
                expected_answer=eval_data["expected_answer"],
                source=eval_data["source"],
                conversation_history=[
                    Conversation(**conv) for conv in eval_data.get("conversation_history", [])
                ]
            )
            self.knowledge_base.evaluations.append(entry)

    def process_evaluation_criteria(self, criteria_data: List[Dict]) -> None:
        """Process the evaluation criteria data"""
        for criteria in criteria_data:
            category_type = CategoryType(criteria["Customer Action Category"])
            ctq = criteria["CTQ"]
            qa_checks = [
                QACheck(check_id=i+1, description=check)
                for i, check in enumerate([
                    criteria["QA Check 1"],
                    criteria["QA Check 2"],
                    criteria["QA Check 3"]
                ])
            ]
            
            evaluation_criteria = EvaluationCriteria(
                category=category_type,
                ctq=ctq,
                qa_checks=qa_checks
            )
            
            if category_type == CategoryType.POSITIVE_NEUTRAL:
                self.conversation_evaluation.positive_neutral_criteria.append(evaluation_criteria)
            elif category_type == CategoryType.NEGATIVE:
                self.conversation_evaluation.negative_criteria.append(evaluation_criteria)
            else:
                self.conversation_evaluation.ambiguous_complex_criteria.append(evaluation_criteria)

    def extract_menu_items(self) -> None:
        """Extract menu items from evaluation data"""
        menu_items = {
            "veg_starters": ["Grill Veg", "Mushroom", "Paneer", "Veg Kebab", "Cajun Spice Potato", "Pineapple"],
            "non_veg_starters": ["Chicken Tangdi", "Chicken Skewer", "Mutton", "Fish", "Prawns"],
            "veg_main_course": ["Noodles", "Oriental Veg", "Paneer", "Aloo", "Veg Kofta", "Dal Tadka", 
                              "Dal Makhani", "Veg Biryani", "Rice"],
            "non_veg_main_course": ["Non Veg Biryani", "Mutton Curry", "Chicken Curry", "Fish Gravy"],
            "desserts": ["Angori Gulab Jamun", "Phirnee", "Ice Cream", "Pie/tart", "Fruits", 
                        "Pastry", "Brownie", "Pudding/soufflé"],
            "drinks": ["Soft drinks", "Mocktails"]
        }
        self.knowledge_base.menu_items.update(menu_items)

    def extract_outlet_info(self) -> None:
        """Extract outlet information from evaluation data"""
        bangalore_outlets = {
            "Indiranagar": OutletInfo(
                name="Indiranagar",
                city="Bangalore",
                address="No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038",
                facilities={
                    "bar": True,
                    "baby_chairs": True,
                    "lift": True,
                    "valet_parking": True,
                    "wheelchair_access": True
                },
                complimentary_drinks=True
            ),
            "JP Nagar": OutletInfo(
                name="JP Nagar",
                city="Bangalore",
                address="67, 3rd Floor, 6th B Main, Phase III, J P Nagar, Bengaluru, Karnataka 560078",
                facilities={
                    "bar": True,
                    "baby_chairs": True,
                    "lift": True,
                    "wheelchair_access": True
                }
            )
        }

        delhi_outlets = {
            "Connaught Place": OutletInfo(
                name="Connaught Place",
                city="New Delhi",
                facilities={
                    "bar": True,
                    "baby_chairs": True,
                    "lift": True,
                    "valet_parking": True
                }
            ),
            "Vasant Kunj": OutletInfo(
                name="Sector C, Vasant Kunj",
                city="New Delhi",
                facilities={
                    "bar": True,
                    "lift": True,
                    "valet_parking": True
                }
            )
        }

        self.knowledge_base.outlets = {
            "Bangalore": bangalore_outlets,
            "New Delhi": delhi_outlets
        }

    def save_processed_data(self) -> None:
        """Save processed data to JSON files"""
        if not os.path.exists(self.processed_data_path):
            os.makedirs(self.processed_data_path)

        # Save menu items
        with open(f"{self.processed_data_path}/menu_items.json", "w") as f:
            json.dump(self.knowledge_base.menu_items, f, indent=2)

        # Save outlet information
        with open(f"{self.processed_data_path}/outlets.json", "w") as f:
            json.dump(self.knowledge_base.outlets, f, indent=2, default=lambda x: x.dict())

        # Save evaluations
        with open(f"{self.processed_data_path}/evaluations.json", "w") as f:
            json.dump([eval.dict() for eval in self.knowledge_base.evaluations], f, indent=2)

        # Save evaluation criteria
        with open(f"{self.processed_data_path}/evaluation_criteria.json", "w") as f:
            json.dump(self.conversation_evaluation.dict(), f, indent=2)

    def load_processed_data(self) -> None:
        """Load processed data from JSON files"""
        try:
            # Load menu items
            with open(f"{self.processed_data_path}/menu_items.json", "r") as f:
                self.knowledge_base.menu_items = json.load(f)

            # Load outlet information
            with open(f"{self.processed_data_path}/outlets.json", "r") as f:
                outlets_data = json.load(f)
                for city, outlets in outlets_data.items():
                    self.knowledge_base.outlets[city] = {
                        name: OutletInfo(**info) for name, info in outlets.items()
                    }

            # Load evaluations
            with open(f"{self.processed_data_path}/evaluations.json", "r") as f:
                evaluations = json.load(f)
                self.knowledge_base.evaluations = [KnowledgeEntry(**eval) for eval in evaluations]

            # Load evaluation criteria
            with open(f"{self.processed_data_path}/evaluation_criteria.json", "r") as f:
                criteria_data = json.load(f)
                self.conversation_evaluation = ConversationEvaluation(**criteria_data)

        except FileNotFoundError:
            print("Processed data files not found. Please run processing first.") 