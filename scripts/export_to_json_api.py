#!/usr/bin/env python3
"""
Export crochet glossary from Google Sheets to JSON API format
Modified from export_to_glossarydata.py for API use
"""

import sys
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets API service"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        sys.exit(1)

def read_sheet_data(sheets):
    """Read all data from the Google Sheet"""
    try:
        result = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:Z'
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("No data found in spreadsheet!")
            return []
        
        headers = values[0]
        terms = []
        
        for row_idx, row in enumerate(values[1:], start=2):
            if not row:  # Skip empty rows
                continue
                
            term = {}
            for col_idx, header in enumerate(headers):
                if col_idx < len(row) and row[col_idx].strip():
                    term[header] = row[col_idx].strip()
            
            # Only include if has ID
            if term.get('ID'):
                terms.append(term)
        
        print(f"✅ Read {len(terms)} terms from Google Sheets")
        return terms
        
    except Exception as e:
        print(f"Error reading sheet data: {e}")
        return []

def clean_and_validate_terms(terms):
    """Clean and validate term data"""
    cleaned_terms = []
    seen_ids = set()
    
    for term in terms:
        # Skip duplicates
        term_id = term.get('ID', '').upper()
        if term_id in seen_ids:
            print(f"⚠️  Skipping duplicate: {term_id}")
            continue
        seen_ids.add(term_id)
        
        # Clean the term data
        cleaned_term = {
            'id': term_id,
            'name_us': term.get('Name_US', ''),
            'name_uk': term.get('Name_UK', ''),
            'category': term.get('Category', 'Other'),
            'difficulty': term.get('Difficulty', '1'),
            'description': term.get('Description_Brief', term.get('Description', '')),
            'symbol': term.get('Symbol', ''),
            'tags': term.get('Tags', '').split(',') if term.get('Tags') else [],
            'time_to_learn': term.get('Time_To_Learn', ''),
            'best_for': term.get('Best_For', ''),
            'updated': datetime.now().isoformat()
        }
        
        # Clean tags
        cleaned_term['tags'] = [tag.strip() for tag in cleaned_term['tags'] if tag.strip()]
        
        # Validate required fields
        if cleaned_term['name_us'] and cleaned_term['name_uk']:
            cleaned_terms.append(cleaned_term)
        else:
            print(f"⚠️  Skipping incomplete term: {term_id}")
    
    print(f"✅ Cleaned and validated {len(cleaned_terms)} terms")
    return cleaned_terms

def create_api_structure(terms):
    """Create the complete API structure"""
    
    # Group terms by category
    categories = {}
    for term in terms:
        cat = term['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(term)
    
    # Create basic stats
    stats = {
        'total_terms': len(terms),
        'categories': list(categories.keys()),
        'last_updated': datetime.now().isoformat(),
        'version': '1.0.0'
    }
    
    # Create the main API response
    api_data = {
        'meta': stats,
        'data': {
            'terms': terms,
            'categories': categories,
            'search_index': create_search_index(terms)
        }
    }
    
    return api_data

def create_search_index(terms):
    """Create a search index for faster lookups"""
    index = {
        'by_id': {},
        'by_name_us': {},
        'by_name_uk': {},
        'by_category': {},
        'all_tags': set()
    }
    
    for term in terms:
        term_id = term['id']
        
        # Index by ID
        index['by_id'][term_id] = term
        
        # Index by names (lowercased for case-insensitive search)
        index['by_name_us'][term['name_us'].lower()] = term
        index['by_name_uk'][term['name_uk'].lower()] = term
        
        # Index by category
        category = term['category']
        if category not in index['by_category']:
            index['by_category'][category] = []
        index['by_category'][category].append(term_id)
        
        # Collect all tags
        index['all_tags'].update(term['tags'])
    
    # Convert set to sorted list
    index['all_tags'] = sorted(list(index['all_tags']))
    
    return index

def create_quiz_data(terms):
    """Generate quiz questions from glossary terms"""
    
    # Basic question types
    quiz_questions = []
    
    # Type 1: "What does X stand for?" questions
    for term in terms:
        if len(term['id']) <= 5 and term['description']:  # Good for abbreviations
            question = {
                'id': len(quiz_questions) + 1,
                'type': 'multiple_choice',
                'difficulty': term['difficulty'],
                'category': term['category'],
                'question': f"What does '{term['id']}' stand for?",
                'options': [
                    term['name_us'],
                    # We'd need to generate wrong answers here
                ],
                'correct_answer': term['name_us'],
                'explanation': term['description'],
                'term_id': term['id']
            }
            quiz_questions.append(question)
    
    # Type 2: US vs UK terminology
    for term in terms:
        if term['name_us'] != term['name_uk'] and term['name_uk']:
            question = {
                'id': len(quiz_questions) + 1,
                'type': 'multiple_choice',
                'difficulty': term['difficulty'],
                'category': 'terminology',
                'question': f"What is the UK term for '{term['name_us']}'?",
                'options': [
                    term['name_uk'],
                    # We'd need to generate wrong answers here
                ],
                'correct_answer': term['name_uk'],
                'explanation': f"In the UK, '{term['name_us']}' is called '{term['name_uk']}'",
                'term_id': term['id']
            }
            quiz_questions.append(question)
    
    return quiz_questions[:50]  # Limit for now

def save_json_files(api_data, quiz_data):
    """Save all JSON files"""
    
    # Main glossary API
    with open('glossary.json', 'w', encoding='utf-8') as f:
        json.dump(api_data, f, indent=2, ensure_ascii=False)
    print("✅ Created glossary.json")
    
    # Terms only (lighter version)
    terms_only = {
        'meta': api_data['meta'],
        'data': api_data['data']['terms']
    }
    with open('terms.json', 'w', encoding='utf-8') as f:
        json.dump(terms_only, f, indent=2, ensure_ascii=False)
    print("✅ Created terms.json")
    
    # Categories
    categories_data = {
        'meta': api_data['meta'],
        'data': api_data['data']['categories']
    }
    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, indent=2, ensure_ascii=False)
    print("✅ Created categories.json")
    
    # Quiz data
    quiz_structure = {
        'meta': {
            'total_questions': len(quiz_data),
            'question_types': ['multiple_choice'],
            'last_updated': datetime.now().isoformat(),
            'version': '1.0.0'
        },
        'data': quiz_data
    }
    with open('quiz.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_structure, f, indent=2, ensure_ascii=False)
    print("✅ Created quiz.json")
    
    # API info/documentation
    api_info = {
        'name': 'Crochet Glossary API',
        'description': 'Comprehensive crochet terminology and quiz data',
        'version': '1.0.0',
        'endpoints': {
            'glossary.json': 'Complete glossary with search index',
            'terms.json': 'Terms only (lighter)',
            'categories.json': 'Terms grouped by category',
            'quiz.json': 'Quiz questions and answers'
        },
        'usage': {
            'base_url': 'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/',
            'example': 'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json'
        },
        'last_updated': datetime.now().isoformat()
    }
    with open('api-info.json', 'w', encoding='utf-8') as f:
        json.dump(api_info, f, indent=2, ensure_ascii=False)
    print("✅ Created api-info.json")

def main():
    """Main export function"""
    print("🧶 DANI'S Crochet Glossary → JSON API Export")
    print("=" * 50)
    
    # Connect to Google Sheets
    sheets = get_sheets_service()
    
    # Read data
    raw_terms = read_sheet_data(sheets)
    if not raw_terms:
        print("❌ No data to export!")
        return
    
    # Clean and validate
    terms = clean_and_validate_terms(raw_terms)
    
    # Create API structure
    api_data = create_api_structure(terms)
    
    # Generate quiz data
    quiz_data = create_quiz_data(terms)
    
    # Save all files
    save_json_files(api_data, quiz_data)
    
    print("\n🎉 Export Complete!")
    print(f"📊 {len(terms)} terms exported")
    print(f"🧠 {len(quiz_data)} quiz questions generated")
    print(f"📁 5 JSON files created")
    
    print("\n📋 Next Steps:")
    print("1. Create new repository: crochet-glossary-api")
    print("2. Copy these JSON files to the repo")
    print("3. Push to GitHub")
    print("4. Access via: https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json")

if __name__ == "__main__":
    main()