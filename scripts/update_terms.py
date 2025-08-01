#!/usr/bin/env python3
"""
Generic Glossary Updater - Reusable script for adding terms
Copy/paste new term data as needed
"""

import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
RANGE_NAME = 'Sheet1!A:Q'
CREDENTIALS_FILE = 'credentials.json'

# Set up credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def update_glossary_terms():
    """Add new terms to the crochet glossary - UPDATE THE new_terms LIST BELOW"""
    
    # Load credentials
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # ========================================
    # COPY/PASTE NEW TERMS HERE:
    # ========================================
    new_terms = [
    ['CHUNKYHANDLE', 'New', 'Chunky Hook Handle', 'Chunky Hook Handle', '🤏', 'Tools', 
     'tools, comfort, ergonomic, handles, grip', '',
     'Thick, comfortable hook handles that reduce hand strain. Popular brands include Chunky Boy, Clover Amour, and others.',
     'High', '1', '1 minute',
     'Wrong size for your hand; Not trying different shapes',
     'Test different thicknesses; Consider hand size; Look for non-slip surfaces',
     'Long crochet sessions, arthritis, comfort improvement', '', ''],
     
    ['YARNBOWL', 'New', 'Yarn Bowl', 'Yarn Bowl', '🍲', 'Tools',
     'tools, organization, yarn-management, helpful', '',
     'Ceramic or wooden bowl with slot to keep yarn from rolling away while crocheting.',
     'High', '1', '1 minute',
     'Bowl too small; Sharp edges that catch yarn',
     'Choose size for your yarn; Look for smooth slots; Consider weight',
     'Organized workspace, preventing yarn tangles', '', ''],
     
    ['PROJECTBAG', 'New', 'Project Bag', 'Project Bag', '👜', 'Tools',
     'tools, organization, portable, storage', '',
     'Specialized bag for keeping crochet project and supplies organized.',
     'High', '1', '1 minute',
     'Bag too small; No compartments for tools',
     'Consider project size; Look for multiple pockets; Choose good zippers',
     'Travel crochet, keeping projects organized', '', ''],
     
    ['COLORWAY', 'New', 'Colorway', 'Colorway', '🎨', 'Yarn',
     'yarn, color, design, selection', '',
     'Specific combination of colors in variegated or multi-colored yarn.',
     'High', '2', '5 minutes',
     'Not considering how colors pool; Mismatched dye lots',
     'Buy enough from same dye lot; Consider color dominance',
     'Yarn selection, color planning, matching projects', '', ''],
     
    ['GAUGESWATCH', 'New', 'Gauge Swatch', 'Tension Square', '⏹️', 'Technique',
     'technique, gauge, measurement, essential', '',
     'Small test piece to check gauge and practice stitches before starting project.',
     'High', '2', '10 minutes',
     'Making swatch too small; Not blocking swatch',
     'Make 6+ inches square; Block like finished project; Measure carefully',
     'Proper sizing, avoiding project disasters', '', '']
]

    # ========================================
    # END TERMS - UPDATE ABOVE AS NEEDED
    # ========================================
    
    try:
        # Get current data to find next row
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        current_data = result.get('values', [])
        next_row = len(current_data) + 1
        
        print(f"Current sheet has {len(current_data)} rows")
        print(f"Adding {len(new_terms)} new terms starting at row {next_row}")
        
        # Append new terms
        range_to_update = f'Sheet1!A{next_row}:Q{next_row + len(new_terms) - 1}'
        
        body = {
            'values': new_terms
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_to_update,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Successfully added {len(new_terms)} terms!")
        print(f"Updated range: {range_to_update}")
        print(f"Rows added: {result.get('updatedRows', 0)}")
        
        # Print summary
        print("\n📋 Added terms:")
        for i, term in enumerate(new_terms, 1):
            symbol = f" ({term[4]})" if term[4] else ""
            category = term[5]
            print(f"  {i}. {term[0]}: {term[2]}{symbol} [{category}]")
            
        print(f"\n🎯 New total: ~{len(current_data) + len(new_terms)} terms")
            
    except FileNotFoundError:
        print("❌ Error: credentials.json not found")
        print("Make sure your credentials.json file is in the same folder as this script")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧶 DANI'S Glossary Updater")
    print("=" * 30)
    update_glossary_terms()