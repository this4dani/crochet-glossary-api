#!/usr/bin/env python3
"""
DANI'S Glossary - Star Rating Updater for GitHub Codespaces
Simple, focused script for updating difficulty star ratings on 301+ terms
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import os

def check_for_new_terms():
    """Check if there are new terms since last analysis"""
    try:
        with open('../glossary.json', 'r') as f:
            data = json.load(f)
            current_count = len(data.get('terms', []))
        
        # Check stored count from last run
        last_count_file = 'last_term_count.txt'
        if os.path.exists(last_count_file):
            with open(last_count_file, 'r') as f:
                last_count = int(f.read().strip())
            if current_count > last_count:
                print(f"\n🆕 NEW TERMS DETECTED: {current_count} terms (was {last_count})")
                print("   Consider running analysis to check their difficulty ratings")
        
        # Update stored count
        with open(last_count_file, 'w') as f:
            f.write(str(current_count))
            
    except Exception as e:
        print(f"Could not check for new terms: {e}")

if __name__ == "__main__":
    check_for_new_terms()

# Configuration
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets connection for Codespaces"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        return None

def analyze_current_stars():
    """Quick analysis of current star ratings"""
    sheets = get_sheets_service()
    if not sheets:
        return
    
    print("🌟 ANALYZING CURRENT STAR RATINGS")
    print("=" * 40)
    
    # Get data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    if not values:
        print("❌ No data found!")
        return
    
    headers = values[0]
    data = values[1:]
    
    print(f"📊 Found {len(data)} terms")
    
    # Find difficulty column
    try:
        difficulty_col = headers.index('Difficulty')
        name_col = headers.index('Name_US')
    except ValueError:
        print("❌ Required columns not found (Difficulty, Name_US)")
        return
    
    # Count stars
    star_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    no_rating = []
    
    for i, row in enumerate(data):
        name = row[name_col] if len(row) > name_col else "Unknown"
        difficulty = row[difficulty_col] if len(row) > difficulty_col else ""
        
        try:
            stars = int(difficulty) if difficulty else 0
        except (ValueError, TypeError):
            stars = 0
        
        star_counts[stars] += 1
        
        if stars == 0:
            no_rating.append(f"Row {i+2}: {name}")
    
    # Display results
    print("\n⭐ STAR DISTRIBUTION:")
    for stars, count in star_counts.items():
        if stars == 0:
            print(f"   No Rating: {count} terms")
        else:
            star_display = "★" * stars + "☆" * (5 - stars)
            print(f"   {stars} stars {star_display}: {count} terms")
    
    if no_rating:
        print(f"\n❌ TERMS MISSING RATINGS ({len(no_rating)}):")
        for term in no_rating[:10]:  # Show first 10
            print(f"   • {term}")
        if len(no_rating) > 10:
            print(f"   ... and {len(no_rating) - 10} more")
    
    return headers, data

def update_single_star(row_number, new_stars):
    """Update a single term's star rating"""
    sheets = get_sheets_service()
    if not sheets:
        return False
    
    try:
        # Get headers to find difficulty column
        result = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!1:1'
        ).execute()
        
        headers = result.get('values', [[]])[0]
        difficulty_col = headers.index('Difficulty')
        
        # Convert column number to letter
        col_letter = chr(ord('A') + difficulty_col)
        range_name = f'Sheet1!{col_letter}{row_number}'
        
        # Update the cell
        body = {'values': [[str(new_stars)]]}
        
        result = sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Updated row {row_number} to {new_stars} stars")
        return True
        
    except Exception as e:
        print(f"❌ Error updating row {row_number}: {e}")
        return False

def batch_star_updates(updates):
    """Update multiple star ratings at once"""
    sheets = get_sheets_service()
    if not sheets:
        return False
    
    try:
        # Get headers
        result = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!1:1'
        ).execute()
        
        headers = result.get('values', [[]])[0]
        difficulty_col = headers.index('Difficulty')
        col_letter = chr(ord('A') + difficulty_col)
        
        # Prepare batch data
        batch_data = []
        for row_num, stars in updates:
            batch_data.append({
                'range': f'Sheet1!{col_letter}{row_num}',
                'values': [[str(stars)]]
            })
        
        # Execute batch update
        body = {
            'valueInputOption': 'RAW',
            'data': batch_data
        }
        
        result = sheets.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        
        updated_cells = result.get('totalUpdatedCells', 0)
        print(f"✅ Batch updated {updated_cells} star ratings!")
        return True
        
    except Exception as e:
        print(f"❌ Batch update failed: {e}")
        return False

def suggest_star_ratings():
    """AI suggestions for missing star ratings"""
    sheets = get_sheets_service()
    if not sheets:
        return
    
    # Get data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    difficulty_col = headers.index('Difficulty')
    name_col = headers.index('Name_US')
    
    suggestions = []
    
    # Simple AI rules for crochet difficulty
    for i, row in enumerate(data):
        row_num = i + 2
        name = row[name_col] if len(row) > name_col else ""
        current_difficulty = row[difficulty_col] if len(row) > difficulty_col else ""
        
        # Skip if already has rating
        if current_difficulty and current_difficulty != "0":
            continue
        
        name_lower = name.lower()
        suggested_stars = 3  # Default medium
        
        # Easy (1-2 stars)
        if any(word in name_lower for word in ['chain', 'slip stitch', 'single crochet', 'sc']):
            suggested_stars = 1
        elif any(word in name_lower for word in ['double crochet', 'half double', 'dc', 'hdc']):
            suggested_stars = 2
        
        # Hard (4-5 stars)
        elif any(word in name_lower for word in ['cable', 'bobble', 'popcorn', 'cluster']):
            suggested_stars = 4
        elif any(word in name_lower for word in ['tunisian', 'broomstick', 'hairpin']):
            suggested_stars = 5
        
        suggestions.append({
            'row': row_num,
            'name': name,
            'suggested': suggested_stars
        })
    
    if suggestions:
        print(f"\n🤖 AI SUGGESTIONS ({len(suggestions)} terms):")
        for sug in suggestions[:15]:  # Show first 15
            stars = "★" * sug['suggested'] + "☆" * (5 - sug['suggested'])
            print(f"   Row {sug['row']}: '{sug['name']}' → {sug['suggested']} {stars}")
        
        if len(suggestions) > 15:
            print(f"   ... and {len(suggestions) - 15} more suggestions")
    
    return suggestions

def export_for_review(filename='star_ratings_review.csv'):
    """Export all terms with current ratings for expert review"""
    sheets = get_sheets_service()
    if not sheets:
        return
    
    # Get data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    try:
        difficulty_col = headers.index('Difficulty')
        name_col = headers.index('Name_US')
        desc_col = headers.index('Description') if 'Description' in headers else None
        category_col = headers.index('Category') if 'Category' in headers else None
    except ValueError as e:
        print(f"❌ Required columns not found: {e}")
        return
    
    # Create CSV content
    csv_content = "Row,Name_US,Current_Stars,Suggested_Stars,Notes,Category,Description\n"
    
    for i, row in enumerate(data):
        row_num = i + 2
        name = row[name_col] if len(row) > name_col else ""
        current_stars = row[difficulty_col] if len(row) > difficulty_col else ""
        category = row[category_col] if category_col and len(row) > category_col else ""
        description = row[desc_col] if desc_col and len(row) > desc_col else ""
        
        # Clean up description for CSV
        description = description.replace('"', '""').replace('\n', ' ')[:100]
        
        csv_content += f'{row_num},"{name}",{current_stars},,"{category}","{description}"\n'
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(csv_content)
    
    print(f"✅ Exported {len(data)} terms to {filename}")
    print("📧 Send this file to crochet experts for review!")
    print("💡 They can edit the 'Suggested_Stars' column and add notes")

def import_expert_reviews(filename='star_ratings_review.csv'):
    """Import expert-reviewed star ratings from CSV"""
    try:
        import csv
        updates = []
        
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Suggested_Stars'] and row['Suggested_Stars'].strip():
                    try:
                        new_stars = int(row['Suggested_Stars'].strip())
                        if 1 <= new_stars <= 5:
                            updates.append((int(row['Row']), new_stars))
                            print(f"✅ Will update '{row['Name_US']}' to {new_stars} stars")
                        else:
                            print(f"❌ Invalid stars for '{row['Name_US']}': {row['Suggested_Stars']}")
                    except ValueError:
                        print(f"❌ Invalid format for '{row['Name_US']}': {row['Suggested_Stars']}")
        
        if updates:
            print(f"\n📊 Found {len(updates)} expert-reviewed changes")
            confirm = input("Apply all expert changes? (y/n): ")
            if confirm.lower() == 'y':
                return batch_star_updates(updates)
        else:
            print("❌ No valid updates found in the file")
            
    except FileNotFoundError:
        print(f"❌ File {filename} not found")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def enhanced_ai_suggestions():
    """Enhanced AI that can suggest upgrades to existing ratings"""
    sheets = get_sheets_service()
    if not sheets:
        return
    
    # Get data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    difficulty_col = headers.index('Difficulty')
    name_col = headers.index('Name_US')
    
    suggestions = []
    
    # Enhanced AI rules for crochet difficulty
    expert_techniques = ['tunisian', 'broomstick', 'hairpin', 'bavarian', 'entrelac', 'intarsia', 'tapestry', 'irish crochet', 'filet']
    advanced_techniques = ['cable', 'bobble', 'popcorn', 'cluster', 'shell', 'fan', 'puff']
    intermediate_techniques = ['increase', 'decrease', 'join', 'round', 'magic ring', 'color change', 'front post', 'back post']
    basic_techniques = ['chain', 'slip stitch', 'single crochet', 'sc', 'ch', 'sl st']
    
    for i, row in enumerate(data):
        row_num = i + 2
        name = row[name_col] if len(row) > name_col else ""
        current_difficulty = row[difficulty_col] if len(row) > difficulty_col else ""
        
        try:
            current_stars = int(current_difficulty) if current_difficulty else 0
        except (ValueError, TypeError):
            current_stars = 0
        
        name_lower = name.lower()
        suggested_stars = current_stars  # Start with current
        reason = ""
        
        # Check for expert techniques (should be 5 stars)
        if any(expert in name_lower for expert in expert_techniques):
            if current_stars < 5:
                suggested_stars = 5
                reason = f"Expert technique (currently {current_stars}★)"
        
        # Check for advanced techniques (should be 4 stars)
        elif any(adv in name_lower for adv in advanced_techniques):
            if current_stars < 4:
                suggested_stars = 4
                reason = f"Advanced technique (currently {current_stars}★)"
        
        # Check for basic techniques (should be 1-2 stars)
        elif any(basic in name_lower for basic in basic_techniques):
            if current_stars > 2:
                suggested_stars = 1 if 'chain' in name_lower or 'slip stitch' in name_lower else 2
                reason = f"Basic technique (currently {current_stars}★)"
        
        # Add to suggestions if different from current
        if suggested_stars != current_stars and reason:
            suggestions.append({
                'row': row_num,
                'name': name,
                'current': current_stars,
                'suggested': suggested_stars,
                'reason': reason
            })
    
    if suggestions:
        print(f"\n🤖 ENHANCED AI SUGGESTIONS ({len(suggestions)} changes):")
        for sug in suggestions:
            current_display = "★" * sug['current'] + "☆" * (5 - sug['current'])
            suggested_display = "★" * sug['suggested'] + "☆" * (5 - sug['suggested'])
            print(f"   Row {sug['row']}: '{sug['name']}': {sug['current']} {current_display} → {sug['suggested']} {suggested_display} ({sug['reason']})")
    else:
        print("✅ No rating changes suggested - your ratings look accurate!")
    
    return suggestions

def debug_term_search():
    """Debug function to see what terms we actually have"""
    sheets = get_sheets_service()
    if not sheets:
        return
    
    # Get data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    name_col = headers.index('Name_US')
    difficulty_col = headers.index('Difficulty')
    
    print("\n🔍 SEARCHING FOR EXPERT TECHNIQUES:")
    
    # Look for potential expert techniques
    expert_keywords = ['tunisian', 'broomstick', 'hairpin', 'bavarian', 'entrelac', 'intarsia', 'tapestry', 'irish', 'filet']
    
    found_terms = []
    for i, row in enumerate(data):
        name = row[name_col] if len(row) > name_col else ""
        difficulty = row[difficulty_col] if len(row) > difficulty_col else ""
        
        name_lower = name.lower()
        
        for keyword in expert_keywords:
            if keyword in name_lower:
                found_terms.append({
                    'row': i + 2,
                    'name': name,
                    'stars': difficulty,
                    'keyword': keyword
                })
    
    if found_terms:
        print("Found potential expert techniques:")
        for term in found_terms:
            print(f"   Row {term['row']}: '{term['name']}' = {term['stars']} stars (contains '{term['keyword']}')")
    else:
        print("❌ No expert technique keywords found!")
        print("\n🔍 Let's see some random terms to understand your naming:")
        for i in range(min(10, len(data))):
            name = data[i][name_col] if len(data[i]) > name_col else ""
            difficulty = data[i][difficulty_col] if len(data[i]) > difficulty_col else ""
            print(f"   Row {i+2}: '{name}' = {difficulty} stars")

def interactive_menu():
    """Enhanced menu for collaborative star rating management"""
    while True:
        print("\n🌟 COLLABORATIVE STAR RATING UPDATER")
        print("=" * 40)
        print("1. Analyze current ratings")
        print("2. Export for expert review (CSV)")
        print("3. Import expert reviews (CSV)")
        print("4. Enhanced AI suggestions")
        print("5. Apply AI suggestions")
        print("6. Manual single update")
        print("7. Manual batch update")
        print("8. Exit")
        print("9. Debug term search")
        
        choice = input("\nChoice (1-9): ").strip()
        
        if choice == '1':
            analyze_current_stars()
        
        elif choice == '2':
            filename = input("Export filename (default: star_ratings_review.csv): ").strip()
            if not filename:
                filename = 'star_ratings_review.csv'
            export_for_review(filename)
        
        elif choice == '3':
            filename = input("Import filename (default: star_ratings_review.csv): ").strip()
            if not filename:
                filename = 'star_ratings_review.csv'
            import_expert_reviews(filename)
        
        elif choice == '4':
            enhanced_ai_suggestions()
        
        elif choice == '5':
            suggestions = enhanced_ai_suggestions()
            if suggestions:
                confirm = input(f"\nApply {len(suggestions)} AI suggestions? (y/n): ")
                if confirm.lower() == 'y':
                    updates = [(s['row'], s['suggested']) for s in suggestions]
                    batch_star_updates(updates)
        
        elif choice == '6':
            try:
                row = int(input("Row number: "))
                stars = int(input("Star rating (1-5): "))
                if 1 <= stars <= 5:
                    update_single_star(row, stars)
                else:
                    print("❌ Stars must be 1-5")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '7':
            print("Enter updates as 'row,stars' (one per line, empty line to finish):")
            updates = []
            while True:
                line = input().strip()
                if not line:
                    break
                try:
                    row, stars = map(int, line.split(','))
                    if 1 <= stars <= 5:
                        updates.append((row, stars))
                    else:
                        print(f"❌ Invalid stars for row {row}")
                except ValueError:
                    print(f"❌ Invalid format: {line}")
            
            if updates:
                batch_star_updates(updates)
        
        elif choice == '8':
            print("👋 Done! Your star ratings look great!")
            break
        
        elif choice == '9':
            debug_term_search()
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    print("🌟 DANI'S CROCHET GLOSSARY - STAR UPDATER")
    print("Optimized for GitHub Codespaces")
    print("=" * 50)
    
    # Quick connection test
    if get_sheets_service():
        print("✅ Google Sheets connection successful!")
        interactive_menu()
    else:
        print("❌ Could not connect to Google Sheets")
        print("Make sure credentials.json is in the same folder")