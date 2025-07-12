#!/usr/bin/env python3
"""
Export crochet glossary data from Google Sheets to JSON API files
Includes Column H (Instruction) data
"""

import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
RANGE_NAME = 'Sheet1!A:Z'
CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheets_data():
    """Get data from Google Sheets"""
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found in spreadsheet')
        return []
    
    headers = values[0]
    data_rows = values[1:]
    
    print(f"Found {len(data_rows)} terms in Google Sheets")
    print(f"Columns: {headers}")
    
    return headers, data_rows

def create_api_files(headers, data_rows):
    """Create all API JSON files"""
    
    # Find column positions
    col_indices = {header: i for i, header in enumerate(headers)}
    
    terms_data = []
    categories = {}
    quiz_questions = []
    
    for row in data_rows:
        if len(row) < 2:  # Skip empty rows
            continue
            
        # Get values safely
        def get_cell(col_name, default=""):
            idx = col_indices.get(col_name, -1)
            return row[idx] if idx >= 0 and idx < len(row) else default
        
        # Create term object
        term = {
            "id": get_cell("ID"),
            "name_us": get_cell("Name_US"),
            "name_uk": get_cell("Name_UK", get_cell("Name_US")),
            "abbreviation_us": get_cell("Abbrev_US"),
            "abbreviation_uk": get_cell("Abbrev_UK"),
            "symbol": get_cell("Symbol"),
            "category": get_cell("Category", "Basic"),
            "description": get_cell("Description"),
            "instruction": get_cell("Instruction"),  # Column H
            "tags": get_cell("Tags", "").split(",") if get_cell("Tags") else [],
            "difficulty": get_cell("Difficulty", "Beginner"),
            "status": get_cell("Status", "Active")
        }
        
        # Clean up tags
        term["tags"] = [tag.strip() for tag in term["tags"] if tag.strip()]
        
        if term["id"]:  # Only include if has ID
            terms_data.append(term)
            
            # Group by category
            cat = term["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(term)
            
            # Create quiz question if has instruction
            if term["instruction"]:
                quiz_questions.append({
                    "id": f"q_{term['id']}",
                    "question": f"How do you make a {term['name_us']}?",
                    "answer": term["instruction"],
                    "term_id": term["id"],
                    "category": term["category"],
                    "difficulty": term["difficulty"]
                })
    
    # Create terms.json (lightweight)
    terms_simple = [
        {
            "id": term["id"],
            "name_us": term["name_us"],
            "name_uk": term["name_uk"],
            "category": term["category"]
        }
        for term in terms_data
    ]
    
    # Create glossary.json (complete)
    glossary_complete = {
        "version": "1.0",
        "last_updated": "2025-07-12",
        "total_terms": len(terms_data),
        "terms": terms_data,
        "search_index": list(set([
            term["name_us"].lower() for term in terms_data
        ] + [
            term["name_uk"].lower() for term in terms_data if term["name_uk"]
        ]))
    }
    
    # Create categories.json
    categories_output = {
        "categories": {cat: len(terms) for cat, terms in categories.items()},
        "terms_by_category": categories
    }
    
    # Create quiz.json
    quiz_output = {
        "total_questions": len(quiz_questions),
        "categories": list(set([q["category"] for q in quiz_questions])),
        "questions": quiz_questions
    }
    
    # Create api-info.json
    api_info = {
        "name": "DANI's Crochet Glossary API",
        "version": "1.0",
        "description": "Comprehensive crochet terminology API with instructions",
        "endpoints": {
            "terms.json": "Lightweight list of all terms",
            "glossary.json": "Complete glossary with full data",
            "categories.json": "Terms organized by category",
            "quiz.json": "Quiz questions and answers",
            "api-info.json": "This documentation"
        },
        "base_url": "https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/",
        "example_usage": {
            "get_all_terms": "curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json",
            "get_complete_data": "curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json"
        },
        "total_terms": len(terms_data),
        "terms_with_instructions": len([t for t in terms_data if t["instruction"]])
    }
    
    # Write all files
    files_to_write = {
        'terms.json': terms_simple,
        'glossary.json': glossary_complete,
        'categories.json': categories_output,
        'quiz.json': quiz_output,
        'api-info.json': api_info
    }
    
    for filename, data in files_to_write.items():
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Created {filename} ({len(json.dumps(data))} bytes)")
    
    return len(terms_data)

def main():
    """Main export process"""
    print("Exporting DANI's Crochet Glossary from Google Sheets...")
    
    # Get data from sheets
    headers, data_rows = get_sheets_data()
    
    if not data_rows:
        print("❌ No data found")
        return
    
    # Create API files
    total_terms = create_api_files(headers, data_rows)
    
    print(f"\nExport complete!")
    print(f"📊 Total terms exported: {total_terms}")
    print(f"📄 Files created: terms.json, glossary.json, categories.json, quiz.json, api-info.json")
    print(f"\n📋 Next steps:")
    print(f"   git add *.json")
    print(f"   git commit -m 'Update from Google Sheets with instructions'")
    print(f"   git push")

if __name__ == "__main__":
    main()