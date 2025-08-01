#!/usr/bin/env python3
"""
Debug Export Data - Investigate what's actually being exported
"""

import json
import os

def debug_export_data():
    """Debug what's actually in the exported files"""
    print("=== DEBUGGING EXPORT DATA ===")
    print()
    
    # Check if files exist and their sizes
    files_to_check = ['terms.json', 'glossary.json', 'categories.json', 'quiz.json', 'api-info.json']
    
    print("📁 FILE STATUS:")
    for filename in files_to_check:
        filepath = f"../{filename}"
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            mtime = os.path.getmtime(filepath)
            print(f"   ✅ {filename}: {size:,} bytes (modified: {mtime})")
        else:
            print(f"   ❌ {filename}: Missing")
    
    # Load and analyze glossary.json
    try:
        with open('../glossary.json', 'r') as f:
            glossary_data = json.load(f)
        
        terms = glossary_data.get('terms', [])
        
        print(f"\n📊 GLOSSARY.JSON ANALYSIS:")
        print(f"   Total terms in file: {len(terms)}")
        print(f"   Metadata says: {glossary_data.get('total_terms', 'Unknown')}")
        print(f"   Last updated: {glossary_data.get('last_updated', 'Unknown')}")
        
        # Check first term structure
        if terms:
            first_term = terms[0]
            print(f"\n🔍 FIRST TERM STRUCTURE:")
            print(f"   ID: {first_term.get('id', 'Missing')}")
            print(f"   Fields: {len(first_term.keys())}")
            print(f"   All fields: {list(first_term.keys())}")
            
            # Check for the missing fields specifically
            missing_check = {
                'estimated_learning_time': first_term.get('estimated_learning_time'),
                'best_use_cases': first_term.get('best_use_cases'),
                'common_mistakes': first_term.get('common_mistakes'),
                'pro_tips': first_term.get('pro_tips'),
                'hook_sizes': first_term.get('hook_sizes'),
                'left_handed_note': first_term.get('left_handed_note')
            }
            
            print(f"\n🎯 MISSING FIELDS CHECK:")
            for field, value in missing_check.items():
                status = "✅ PRESENT" if field in first_term else "❌ MISSING"
                value_preview = str(value)[:50] if value else "EMPTY"
                print(f"   {field}: {status} = {value_preview}")
        
        # Check for terms with specific IDs
        print(f"\n🧪 SPECIFIC TERM CHECK:")
        test_ids = ['SC', 'DC', 'HDC', 'CH', 'SLST', 'SN']
        for test_id in test_ids:
            term = next((t for t in terms if t.get('id') == test_id), None)
            if term:
                fields_count = len(term.keys())
                has_missing_fields = any(field in term for field in missing_check.keys())
                print(f"   {test_id}: {fields_count} fields, missing fields present: {has_missing_fields}")
            else:
                print(f"   {test_id}: NOT FOUND")
        
        # Count empty vs filled terms
        print(f"\n📈 DATA QUALITY:")
        empty_id_count = sum(1 for term in terms if not term.get('id'))
        filled_terms = [term for term in terms if term.get('id')]
        print(f"   Terms with ID: {len(filled_terms)}")
        print(f"   Terms without ID: {empty_id_count}")
        print(f"   Total terms: {len(terms)}")
        
        # Check field coverage across all terms
        if filled_terms:
            all_fields = set()
            for term in filled_terms[:10]:  # Check first 10 terms
                all_fields.update(term.keys())
            
            print(f"\n📋 FIELD COVERAGE (first 10 terms):")
            print(f"   Unique fields found: {len(all_fields)}")
            print(f"   All fields: {sorted(all_fields)}")
        
    except Exception as e:
        print(f"❌ Error reading glossary.json: {e}")
    
    # Check terms.json for comparison
    try:
        with open('../terms.json', 'r') as f:
            terms_data = json.load(f)
        
        print(f"\n📊 TERMS.JSON COMPARISON:")
        print(f"   Terms count: {len(terms_data)}")
        
        if terms_data:
            first_simple = terms_data[0]
            print(f"   First term fields: {list(first_simple.keys())}")
            
    except Exception as e:
        print(f"❌ Error reading terms.json: {e}")

def check_export_logic():
    """Check if there's a logic issue in export"""
    print(f"\n🔧 EXPORT LOGIC CHECK:")
    print(f"   The export script logs show:")
    print(f"   - Found 300 terms in Google Sheets")
    print(f"   - Total terms exported: 300") 
    print(f"   - But test finds only 255 terms")
    print(f"   - Missing fields still not captured")
    print()
    print(f"   Possible issues:")
    print(f"   1. Export script field mapping not working")
    print(f"   2. Terms being filtered out somewhere")
    print(f"   3. Test script reading old cached data")
    print(f"   4. Export script has logical error")

def main():
    """Main debug function"""
    print("DANI's Crochet Glossary API - Export Debug")
    print("=" * 50)
    print("Investigating export discrepancies and missing fields")
    print()
    
    debug_export_data()
    check_export_logic()
    
    print(f"\n🎯 NEXT DEBUGGING STEPS:")
    print(f"   1. Check if the field mapping in export script is actually working")
    print(f"   2. Verify row filtering logic (why 300→255 terms?)")
    print(f"   3. Check if test script has cached data issues")
    print(f"   4. Manually inspect a few terms in glossary.json")
    
    print(f"\n" + "=" * 50)

if __name__ == "__main__":
    main()