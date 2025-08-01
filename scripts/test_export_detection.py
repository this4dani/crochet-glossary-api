#!/usr/bin/env python3
"""
Test Export Detection Script
Tests the auto-detection export and shows what fields are captured vs missing

Run this AFTER running your modified export_from_sheets.py
"""

import json
import os
from datetime import datetime

def test_auto_detection():
    """Test the auto-detection export results"""
    print("=== TESTING AUTO-DETECTION EXPORT ===")
    print()
    
    # Fields that README promises (what developers expect)
    readme_promised_fields = [
        'id', 'name_us', 'name_uk', 'description', 
        'difficulty', 'tags', 'category', 'instruction',
        'estimated_learning_time', 'best_use_cases',
        'common_mistakes', 'pro_tips', 'hook_sizes', 
        'left_handed_note'
    ]
    
    # Check if export ran successfully
    if not os.path.exists('../glossary.json'):
        print("❌ No glossary.json found!")
        print("   Please run: cd scripts && python export_from_sheets.py")
        return False
    
    # Load the exported data
    try:
        with open('../glossary.json', 'r') as f:
            api_data = json.load(f)
        
        terms = api_data.get('terms', [])
        if not terms:
            print("❌ No terms found in exported data")
            return False
            
        print(f"✅ Export successful - found {len(terms)} terms")
        
    except Exception as e:
        print(f"❌ Error reading exported data: {e}")
        return False
    
    # Analyze what fields were captured
    sample_term = terms[0]
    captured_fields = list(sample_term.keys())
    
    print(f"\n📊 FIELD ANALYSIS:")
    print(f"   Google Sheets Columns Detected: {len(captured_fields)}")
    print(f"   README Promised Fields: {len(readme_promised_fields)}")
    
    print(f"\n✅ FIELDS SUCCESSFULLY CAPTURED:")
    captured_promised = []
    for field in readme_promised_fields:
        if field in captured_fields:
            captured_promised.append(field)
            value = sample_term.get(field, '')
            value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"   ✅ {field}: {value_preview}")
    
    print(f"\n❌ FIELDS MISSING FROM EXPORT:")
    missing_from_export = []
    for field in readme_promised_fields:
        if field not in captured_fields:
            missing_from_export.append(field)
            print(f"   ❌ {field}")
    
    print(f"\n🔍 EXTRA FIELDS CAPTURED (not in README):")
    extra_fields = []
    for field in captured_fields:
        if field not in readme_promised_fields:
            extra_fields.append(field)
            value = sample_term.get(field, '')
            value_preview = str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
            print(f"   🆕 {field}: {value_preview}")
    
    # Check data quality
    print(f"\n📋 DATA QUALITY CHECK:")
    empty_fields = []
    for field in captured_fields:
        empty_count = sum(1 for term in terms if not term.get(field))
        if empty_count == len(terms):
            empty_fields.append(field)
            print(f"   🔴 {field}: ALL EMPTY ({empty_count}/{len(terms)})")
        elif empty_count > len(terms) * 0.8:  # More than 80% empty
            print(f"   🟡 {field}: MOSTLY EMPTY ({empty_count}/{len(terms)})")
        else:
            print(f"   🟢 {field}: HAS DATA ({len(terms) - empty_count}/{len(terms)} filled)")
    
    # Summary and next steps
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Captured: {len(captured_promised)}/{len(readme_promised_fields)} promised fields")
    print(f"   ❌ Missing: {len(missing_from_export)} promised fields")
    print(f"   🆕 Extra: {len(extra_fields)} bonus fields")
    print(f"   🔴 Empty: {len(empty_fields)} completely empty fields")
    
    success_rate = (len(captured_promised) / len(readme_promised_fields)) * 100
    print(f"   📈 Success Rate: {success_rate:.1f}%")
    
    # Determine next steps
    print(f"\n🎯 NEXT STEPS:")
    
    if len(missing_from_export) == 0:
        print(f"   🎉 PERFECT! All README fields captured")
        print(f"   ✅ Auto-detection working perfectly")
        print(f"   🚀 Ready for Phase 2: Quiz classification fixes")
        
    elif len(missing_from_export) <= 3:
        print(f"   🔧 ALMOST THERE! Just {len(missing_from_export)} missing fields:")
        for field in missing_from_export:
            # Suggest Google Sheets column names
            suggested_column = field.replace("_", "_").title().replace("_", "_")
            print(f"      - Add '{suggested_column}' column to Google Sheets")
        print(f"   📝 Then re-run export to capture them")
        
    else:
        print(f"   📋 NEEDS WORK: {len(missing_from_export)} fields missing")
        print(f"   💡 Check Google Sheets column names:")
        print(f"      Current columns detected: {len(captured_fields)}")
        print(f"      Expected: {readme_promised_fields}")
    
    return success_rate >= 80

def show_google_sheets_mapping():
    """Show the mapping between expected API fields and Google Sheets columns"""
    print(f"\n📋 GOOGLE SHEETS COLUMN MAPPING:")
    print(f"   README Field → Expected Google Sheets Column")
    print(f"   " + "="*50)
    
    field_mapping = {
        'estimated_learning_time': 'Time_To_Learn',
        'best_use_cases': 'Best_For',
        'common_mistakes': 'Common_Mistakes', 
        'pro_tips': 'Pro_Tips',
        'hook_sizes': 'Hook_Sizes',
        'left_handed_note': 'Left_Handed_Note',
        'difficulty': 'Difficulty',
        'description': 'Description',
        'category': 'Category',
        'tags': 'Tags',
        'instruction': 'Instruction'
    }
    
    for api_field, sheets_column in field_mapping.items():
        print(f"   {api_field} → {sheets_column}")

def check_beginner_stitches():
    """Check if basic stitches are properly exported for quiz testing"""
    print(f"\n🎯 BEGINNER STITCH CHECK:")
    
    try:
        with open('../glossary.json', 'r') as f:
            api_data = json.load(f)
        terms = api_data.get('terms', [])
        
        # Check for essential beginner stitches
        beginner_stitches = ['SC', 'DC', 'HDC', 'CH', 'SLST', 'SN']
        
        for stitch_id in beginner_stitches:
            term = next((t for t in terms if t.get('id') == stitch_id), None)
            if term:
                difficulty = term.get('difficulty', 'Unknown')
                tags = term.get('tags', [])
                has_instruction = bool(term.get('instruction'))
                print(f"   ✅ {stitch_id}: difficulty={difficulty}, tags={tags}, instruction={has_instruction}")
            else:
                print(f"   ❌ {stitch_id}: Not found in export")
                
    except Exception as e:
        print(f"   ❌ Error checking stitches: {e}")

def main():
    """Main test function"""
    print("DANI's Crochet Glossary API - Auto-Detection Test")
    print("=" * 55)
    print("Testing the modified export script with auto-field detection")
    print()
    
    success = test_auto_detection()
    show_google_sheets_mapping()
    check_beginner_stitches()
    
    print(f"\n📝 READY FOR PHASE 2?")
    if success:
        print(f"   ✅ Data export looks good!")
        print(f"   🎯 Next: Fix quiz classification logic")
        print(f"   📋 Focus: Get beginner quiz working with basic stitches")
    else:
        print(f"   🔧 Data export needs work first")
        print(f"   📝 Add missing columns to Google Sheets")
        print(f"   🔄 Then re-run export and test again")
    
    print(f"\n" + "=" * 55)

if __name__ == "__main__":
    main()