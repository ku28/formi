import os
import sys
import argparse

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.services.pdf_processor import PDFProcessor

def main():
    parser = argparse.ArgumentParser(description='Process BBQ Nation knowledge base PDFs')
    parser.add_argument('--pdf-dir', default='data/pdfs',
                      help='Directory containing PDF files (default: data/pdfs)')
    parser.add_argument('--type', choices=['menu', 'faq', 'timeslots', 'all'],
                      default='all', help='Type of PDFs to process')
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = PDFProcessor(pdf_dir=args.pdf_dir)
    
    print(f"Processing PDFs from {args.pdf_dir}...")
    
    try:
        if args.type == 'menu':
            result = processor.process_menu_pdfs()
            print(f"Processed {len(result['items'])} menu items in {len(result['categories'])} categories")
        elif args.type == 'faq':
            result = processor.process_faq_pdfs()
            print(f"Processed {len(result['faqs'])} FAQs in {len(result['categories'])} categories")
        elif args.type == 'timeslots':
            result = processor.process_timeslot_pdfs()
            cities = result['locations'].keys()
            total_locations = sum(len(locations) for locations in result['locations'].values())
            print(f"Processed time slots for {total_locations} locations in {len(cities)} cities")
        else:
            result = processor.process_all()
            print(f"Processed:")
            print(f"- {len(result['menu']['items'])} menu items")
            print(f"- {len(result['faqs']['faqs'])} FAQs")
            cities = result['timeslots']['locations'].keys()
            total_locations = sum(len(locations) for locations in result['timeslots']['locations'].values())
            print(f"- Time slots for {total_locations} locations in {len(cities)} cities")
            
        print("\nProcessed data saved in data/processed/")
        
    except Exception as e:
        print(f"Error processing PDFs: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 