from typing import Dict, List, Optional
import os
import json
from datetime import datetime, time
import PyPDF2
from pathlib import Path

class PDFProcessor:
    def __init__(self, pdf_dir: str = "data/pdfs"):
        self.pdf_dir = pdf_dir
        self.menu_dir = os.path.join(pdf_dir, "menu")
        self.faq_dir = os.path.join(pdf_dir, "faqs")
        self.timeslots_dir = os.path.join(pdf_dir, "timeslots")
        self.processed_dir = "data/processed"
        
        # Create directories if they don't exist
        os.makedirs(self.menu_dir, exist_ok=True)
        os.makedirs(self.faq_dir, exist_ok=True)
        os.makedirs(self.timeslots_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
    def process_menu_pdfs(self) -> Dict:
        """Process menu PDFs and extract structured data"""
        menu_data = {
            "categories": [],
            "items": [],
            "last_updated": datetime.now().isoformat()
        }
        
        for pdf_file in os.listdir(self.menu_dir):
            if not pdf_file.endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(self.menu_dir, pdf_file)
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                for page in reader.pages:
                    text = page.extract_text()
                    
                    # Process menu categories and items
                    # This is a basic implementation - customize based on your PDF structure
                    lines = text.split('\n')
                    current_category = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Assume categories are in ALL CAPS
                        if line.isupper():
                            current_category = {
                                "name": line,
                                "items": []
                            }
                            menu_data["categories"].append(current_category)
                        elif current_category and ':' in line:
                            # Assume items have name: description format
                            name, description = line.split(':', 1)
                            item = {
                                "name": name.strip(),
                                "description": description.strip(),
                                "category": current_category["name"]
                            }
                            menu_data["items"].append(item)
                            current_category["items"].append(item)
        
        # Save processed data
        output_path = os.path.join(self.processed_dir, "menu.json")
        with open(output_path, 'w') as f:
            json.dump(menu_data, f, indent=2)
            
        return menu_data
        
    def process_faq_pdfs(self) -> Dict:
        """Process FAQ PDFs and extract structured data"""
        faq_data = {
            "faqs": [],
            "categories": set(),
            "last_updated": datetime.now().isoformat()
        }
        
        for pdf_file in os.listdir(self.faq_dir):
            if not pdf_file.endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(self.faq_dir, pdf_file)
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                for page in reader.pages:
                    text = page.extract_text()
                    
                    # Process FAQs
                    # This is a basic implementation - customize based on your PDF structure
                    lines = text.split('\n')
                    current_question = None
                    current_answer = []
                    current_category = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Assume categories are in [Square Brackets]
                        if line.startswith('[') and line.endswith(']'):
                            current_category = line[1:-1]
                            faq_data["categories"].add(current_category)
                            continue
                            
                        # Assume questions end with ?
                        if line.endswith('?'):
                            # Save previous QA pair if exists
                            if current_question and current_answer:
                                faq_data["faqs"].append({
                                    "question": current_question,
                                    "answer": ' '.join(current_answer),
                                    "category": current_category
                                })
                            
                            current_question = line
                            current_answer = []
                        elif current_question:
                            current_answer.append(line)
                    
                    # Save last QA pair
                    if current_question and current_answer:
                        faq_data["faqs"].append({
                            "question": current_question,
                            "answer": ' '.join(current_answer),
                            "category": current_category
                        })
        
        # Convert categories set to list for JSON serialization
        faq_data["categories"] = list(faq_data["categories"])
        
        # Save processed data
        output_path = os.path.join(self.processed_dir, "faqs.json")
        with open(output_path, 'w') as f:
            json.dump(faq_data, f, indent=2)
            
        return faq_data
        
    def process_timeslot_pdfs(self) -> Dict:
        """Process time slot PDFs for different locations"""
        timeslot_data = {
            "locations": {},
            "last_updated": datetime.now().isoformat()
        }
        
        for pdf_file in os.listdir(self.timeslots_dir):
            if not pdf_file.endswith('.pdf'):
                continue
            
            # Extract location from filename (e.g., "bangalore_indiranagar.pdf")
            location_name = pdf_file[:-4].replace('_', ' ').title()
            city = location_name.split()[0]
            
            pdf_path = os.path.join(self.timeslots_dir, pdf_file)
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                location_slots = {
                    "weekday": {
                        "lunch": [],
                        "dinner": []
                    },
                    "weekend": {
                        "lunch": [],
                        "dinner": []
                    },
                    "special_days": {}
                }
                
                # Extract text from each page
                for page in reader.pages:
                    text = page.extract_text()
                    lines = text.split('\n')
                    current_section = None
                    current_meal = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Check for section headers
                        lower_line = line.lower()
                        if "weekday" in lower_line:
                            current_section = "weekday"
                            continue
                        elif "weekend" in lower_line:
                            current_section = "weekend"
                            continue
                        elif "special days" in lower_line:
                            current_section = "special_days"
                            continue
                        
                        # Check for meal type
                        if "lunch" in lower_line:
                            current_meal = "lunch"
                            continue
                        elif "dinner" in lower_line:
                            current_meal = "dinner"
                            continue
                        
                        # Process time slots
                        if current_section and current_meal and ":" in line:
                            try:
                                # Parse time in format "HH:MM" or "HH:MM AM/PM"
                                time_str = line.strip()
                                if "special_days" == current_section:
                                    # Format: "Holiday Name: HH:MM - HH:MM"
                                    day_name, time_range = time_str.split(':', 1)
                                    start_time, end_time = time_range.split('-')
                                    location_slots["special_days"][day_name.strip()] = {
                                        "start": start_time.strip(),
                                        "end": end_time.strip()
                                    }
                                else:
                                    location_slots[current_section][current_meal].append(time_str)
                            except Exception as e:
                                print(f"Error parsing time slot '{line}': {str(e)}")
                
                # Add location data
                if city not in timeslot_data["locations"]:
                    timeslot_data["locations"][city] = {}
                timeslot_data["locations"][city][location_name] = location_slots
        
        # Save processed data
        output_path = os.path.join(self.processed_dir, "timeslots.json")
        with open(output_path, 'w') as f:
            json.dump(timeslot_data, f, indent=2)
            
        return timeslot_data
        
    def process_all(self) -> Dict:
        """Process all PDFs in the knowledge base"""
        return {
            "menu": self.process_menu_pdfs(),
            "faqs": self.process_faq_pdfs(),
            "timeslots": self.process_timeslot_pdfs()
        } 