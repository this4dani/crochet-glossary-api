#!/usr/bin/env python3
"""
Generate quiz questions from crochet glossary data
Creates multiple quiz formats for different skill levels
"""

import json
import random
from typing import List, Dict

def check_if_update_needed():
    """Check if quiz files need updating based on glossary.json timestamp"""
    try:
        import os
        glossary_time = os.path.getmtime('../glossary.json')
        quiz_file = '../data/quizzes/intermediate_pack.json'
        
        if os.path.exists(quiz_file):
            quiz_time = os.path.getmtime(quiz_file)
            if quiz_time >= glossary_time:
                print("📋 Quiz files are up-to-date, skipping generation")
                return False
        
        print("🔄 Glossary data is newer, regenerating quizzes...")
        return True
        
    except Exception as e:
        print(f"Timestamp check failed: {e}")
        return True

if __name__ == "__main__":
    if not check_if_update_needed():
        exit(0)

def load_glossary_data():
    """Load the complete glossary data"""
    try:
        with open('glossary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('terms', [])
    except FileNotFoundError:
        print("❌ glossary.json not found. Run export_from_sheets.py first.")
        return []

def create_instruction_quizzes(terms: List[Dict]) -> List[Dict]:
    """Create quizzes based on instructions"""
    quizzes = []
    
    # Only terms with instructions
    terms_with_instructions = [t for t in terms if t.get('instruction')]
    
    for term in terms_with_instructions:
        # Basic instruction quiz
        quizzes.append({
            "id": f"inst_{term['id']}",
            "type": "instruction",
            "category": term.get('category', 'Basic'),
            "difficulty": term.get('difficulty', 'Beginner'),
            "question": f"How do you make a {term['name_us']}?",
            "answer": term['instruction'],
            "term_id": term['id'],
            "points": 10
        })
        
        # Multiple choice if we have enough similar terms
        similar_terms = [t for t in terms_with_instructions 
                        if t.get('category') == term.get('category') and t['id'] != term['id']]
        
        if len(similar_terms) >= 3:
            wrong_answers = random.sample([t['instruction'] for t in similar_terms[:3]], 3)
            choices = [term['instruction']] + wrong_answers
            random.shuffle(choices)
            
            quizzes.append({
                "id": f"mc_{term['id']}",
                "type": "multiple_choice",
                "category": term.get('category', 'Basic'),
                "difficulty": term.get('difficulty', 'Beginner'),
                "question": f"What is the correct instruction for {term['name_us']}?",
                "choices": choices,
                "correct_answer": term['instruction'],
                "term_id": term['id'],
                "points": 15
            })
    
    return quizzes

def create_terminology_quizzes(terms: List[Dict]) -> List[Dict]:
    """Create quizzes about terminology (US vs UK, abbreviations)"""
    quizzes = []
    
    for term in terms:
        if not term.get('id'):
            continue
            
        # US vs UK terminology
        if term.get('name_uk') and term['name_uk'] != term['name_us']:
            quizzes.append({
                "id": f"uk_{term['id']}",
                "type": "terminology",
                "category": "US_vs_UK",
                "difficulty": "Intermediate",
                "question": f"What is the UK term for '{term['name_us']}'?",
                "answer": term['name_uk'],
                "term_id": term['id'],
                "points": 5
            })
        
        # Abbreviation quiz
        if term.get('abbreviation_us'):
            quizzes.append({
                "id": f"abbrev_{term['id']}",
                "type": "abbreviation",
                "category": term.get('category', 'Basic'),
                "difficulty": "Beginner",
                "question": f"What does '{term['abbreviation_us']}' stand for?",
                "answer": term['name_us'],
                "term_id": term['id'],
                "points": 5
            })
    
    return quizzes

def create_symbol_quizzes(terms: List[Dict]) -> List[Dict]:
    """Create quizzes about crochet symbols"""
    quizzes = []
    
    terms_with_symbols = [t for t in terms if t.get('symbol')]
    
    for term in terms_with_symbols:
        quizzes.append({
            "id": f"symbol_{term['id']}",
            "type": "symbol",
            "category": "Symbols",
            "difficulty": "Advanced",
            "question": f"What stitch does this symbol represent: {term['symbol']}?",
            "answer": term['name_us'],
            "term_id": term['id'],
            "points": 10
        })
    
    return quizzes

def create_mixed_quizzes(terms: List[Dict]) -> List[Dict]:
    """Create mixed-difficulty comprehensive quizzes"""
    quizzes = []
    
    # Definition matching
    for term in terms:
        if term.get('description'):
            quizzes.append({
                "id": f"def_{term['id']}",
                "type": "definition",
                "category": term.get('category', 'Basic'),
                "difficulty": term.get('difficulty', 'Beginner'),
                "question": f"Which stitch matches this description: {term['description']}?",
                "answer": term['name_us'],
                "term_id": term['id'],
                "points": 8
            })
    
    return quizzes

def organize_by_difficulty():
    """Create quiz sets organized by difficulty level"""
    terms = load_glossary_data()
    if not terms:
        return
    
    all_quizzes = []
    all_quizzes.extend(create_instruction_quizzes(terms))
    all_quizzes.extend(create_terminology_quizzes(terms))
    all_quizzes.extend(create_symbol_quizzes(terms))
    all_quizzes.extend(create_mixed_quizzes(terms))
    
    # Organize by difficulty
    difficulty_sets = {
        "Beginner": [],
        "Intermediate": [],
        "Advanced": []
    }
    
    for quiz in all_quizzes:
        diff = quiz.get('difficulty', 'Beginner')
        if diff in difficulty_sets:
            difficulty_sets[diff].append(quiz)
    
    # Create quiz packages
    quiz_packages = {
        "beginner_pack": {
            "name": "Beginner Crochet Quiz",
            "description": "Basic stitches and abbreviations",
            "total_questions": len(difficulty_sets["Beginner"]),
            "total_points": sum(q.get('points', 0) for q in difficulty_sets["Beginner"]),
            "questions": difficulty_sets["Beginner"][:20]  # Limit to 20 questions
        },
        "intermediate_pack": {
            "name": "Intermediate Crochet Quiz", 
            "description": "US vs UK terms and complex stitches",
            "total_questions": len(difficulty_sets["Intermediate"]),
            "total_points": sum(q.get('points', 0) for q in difficulty_sets["Intermediate"]),
            "questions": difficulty_sets["Intermediate"][:25]
        },
        "advanced_pack": {
            "name": "Advanced Crochet Quiz",
            "description": "Symbols, complex techniques, and expert knowledge",
            "total_questions": len(difficulty_sets["Advanced"]),
            "total_points": sum(q.get('points', 0) for q in difficulty_sets["Advanced"]),
            "questions": difficulty_sets["Advanced"][:30]
        },
        "master_challenge": {
            "name": "Crochet Master Challenge",
            "description": "Mixed questions from all skill levels",
            "total_questions": 50,
            "total_points": 500,
            "questions": random.sample(all_quizzes, min(50, len(all_quizzes)))
        }
    }
    
    return quiz_packages

def create_quiz_files():
    """Create all quiz-related files"""
    print("Generating quiz files from glossary data...")
    
    terms = load_glossary_data()
    if not terms:
        return
    
    # Create comprehensive quiz data
    quiz_packages = organize_by_difficulty()
    
    # Main quiz file (updated)
    quiz_data = {
        "version": "1.0",
        "generated": "2025-07-12",
        "total_packages": len(quiz_packages),
        "packages": quiz_packages,
        "api_info": {
            "description": "Crochet quiz system with multiple difficulty levels",
            "usage": "Select a package and present questions to users"
        }
    }
    
    # Write quiz.json
    with open('quiz.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    # Create individual quiz files
    os.makedirs('quizzes', exist_ok=True)
    
    for package_name, package_data in quiz_packages.items():
        filename = f'quizzes/{package_name}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Created {filename}")
    
    # Create quiz statistics
    stats = {
        "total_quizzes": sum(len(pkg['questions']) for pkg in quiz_packages.values()),
        "terms_with_instructions": len([t for t in terms if t.get('instruction')]),
        "terms_with_symbols": len([t for t in terms if t.get('symbol')]),
        "categories": list(set(t.get('category', 'Basic') for t in terms)),
        "difficulty_breakdown": {
            diff: len(pkg['questions']) 
            for diff, pkg in zip(['Beginner', 'Intermediate', 'Advanced'], 
                                [quiz_packages['beginner_pack'], 
                                 quiz_packages['intermediate_pack'], 
                                 quiz_packages['advanced_pack']])
        }
    }
    
    with open('quizzes/quiz_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\nQuiz generation complete!")
    print(f"📊 Total quiz questions: {stats['total_quizzes']}")
    print(f"📚 Quiz packages: {len(quiz_packages)}")
    print(f"📝 Terms with instructions: {stats['terms_with_instructions']}")

def main():
    create_quiz_files()

if __name__ == "__main__":
    import os
    main()