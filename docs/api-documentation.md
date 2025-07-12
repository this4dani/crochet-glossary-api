# DANI's Crochet Glossary API Documentation

## Overview

The DANI's Crochet Glossary API provides comprehensive access to crochet terminology, including stitch names, abbreviations, symbols, and **step-by-step instructions**. All data is sourced from curated Google Sheets and updated regularly.

## Base URL
```
https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/
```

## API Endpoints

### 1. `terms.json` - Quick Reference
**Purpose:** Lightweight list of all terms  
**Use Case:** Fast loading, basic term lookups  
**Size:** ~50KB

```bash
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json
```

**Response Format:**
```json
[
  {
    "id": "SC",
    "name_us": "Single Crochet",
    "name_uk": "Double Crochet", 
    "category": "Basic"
  }
]
```

### 2. `glossary.json` - Complete Data
**Purpose:** Full glossary with all details including instructions  
**Use Case:** Applications needing complete information  
**Size:** ~200KB

```bash
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json
```

**Response Format:**
```json
{
  "version": "1.0",
  "last_updated": "2025-07-12",
  "total_terms": 265,
  "terms": [
    {
      "id": "SC",
      "name_us": "Single Crochet",
      "name_uk": "Double Crochet",
      "abbreviation_us": "sc",
      "abbreviation_uk": "dc",
      "symbol": "×",
      "category": "Basic",
      "description": "The most basic crochet stitch",
      "instruction": "Insert hook, yarn over, pull through (2 loops on hook), yarn over, pull through both loops",
      "tags": ["basic", "foundation", "common"],
      "difficulty": "Beginner",
      "status": "Active"
    }
  ],
  "search_index": ["single crochet", "double crochet", ...]
}
```

### 3. `categories.json` - Organized by Category
**Purpose:** Terms grouped by category (Basic, Advanced, Tools, etc.)  
**Use Case:** Building category-based navigation  

```bash
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/categories.json
```

**Response Format:**
```json
{
  "categories": {
    "Basic": 45,
    "Advanced": 32,
    "Tools": 18
  },
  "terms_by_category": {
    "Basic": [
      { "id": "SC", "name_us": "Single Crochet", ... }
    ]
  }
}
```

### 4. `quiz.json` - Interactive Quizzes
**Purpose:** Quiz questions generated from glossary data  
**Use Case:** Educational apps, skill testing  

```bash
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/quiz.json
```

**Response Format:**
```json
{
  "total_packages": 4,
  "packages": {
    "beginner_pack": {
      "name": "Beginner Crochet Quiz",
      "total_questions": 20,
      "questions": [
        {
          "id": "inst_SC",
          "type": "instruction",
          "question": "How do you make a Single Crochet?",
          "answer": "Insert hook, yarn over, pull through...",
          "points": 10
        }
      ]
    }
  }
}
```

### 5. `api-info.json` - API Metadata
**Purpose:** API information and usage statistics  
**Use Case:** Discovering available endpoints and data  

## Data Structure

### Term Object
Every term contains these fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | "SC" |
| `name_us` | string | US terminology | "Single Crochet" |
| `name_uk` | string | UK terminology | "Double Crochet" |
| `abbreviation_us` | string | US abbreviation | "sc" |
| `abbreviation_uk` | string | UK abbreviation | "dc" |
| `symbol` | string | Crochet chart symbol | "×" |
| `category` | string | Term category | "Basic" |
| `description` | string | Brief description | "Most basic stitch" |
| `instruction` | string | **Step-by-step how-to** | "Insert hook, yarn over..." |
| `tags` | array | Searchable tags | ["basic", "common"] |
| `difficulty` | string | Skill level | "Beginner" |
| `status` | string | Active/Deprecated | "Active" |

## Categories

### Available Categories:
- **Basic** - Fundamental stitches (SC, DC, HDC)
- **Advanced** - Complex techniques (cables, bobbles)
- **Tools** - Equipment and materials
- **Techniques** - Methods and processes
- **US_vs_UK** - Terminology differences
- **Symbols** - Chart reading

## Usage Examples

### JavaScript Fetch
```javascript
async function getCrochetTerms() {
  const response = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json');
  const data = await response.json();
  return data.terms;
}
```

### Python Requests
```python
import requests

url = "https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json"
response = requests.get(url)
terms = response.json()
```

### cURL with jq
```bash
# Get all single crochet variations
curl -s https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json | \
  jq '.terms[] | select(.name_us | contains("Single"))'
```

## Features

### ✅ What's Included:
- **265+ verified terms** from expert curation
- **Step-by-step instructions** for major stitches
- **US and UK terminology** differences
- **Crochet symbols** for chart reading
- **Difficulty ratings** for learning progression
- **Searchable tags** for easy filtering
- **Quiz system** with multiple difficulty levels

### 🔄 Regular Updates:
- Data sourced from Google Sheets
- Updated as new terms are added
- Version tracking for API changes

## Integration Ideas

### For Websites:
- **Tooltip definitions** on hover over crochet terms
- **Interactive glossaries** with search and filter
- **Educational content** with embedded definitions

### For Apps:
- **Offline crochet dictionary** with full data
- **Learning modules** with quiz integration
- **Pattern readers** with automatic term lookup

### For Developers:
- **Browser extensions** for automatic term detection
- **Plugin development** for blog platforms
- **API mashups** with pattern databases

## Rate Limits & Usage

### No Authentication Required
This is a **public, free API** hosted on GitHub.

### Rate Limits:
- GitHub raw file serving limits apply
- Recommended: Cache responses for production use
- Consider downloading JSON files for heavy usage

### Best Practices:
- **Cache responses** - Files don't change frequently
- **Use appropriate endpoint** - Don't load full glossary for simple lookups
- **Handle errors gracefully** - Network issues can occur

## Support & Updates

### Data Issues:
- Report via GitHub Issues on the repository
- Email: this4dani@users.noreply.github.com

### API Changes:
- Breaking changes will increment version number
- Monitor repository for updates
- Version field in JSON responses indicates data version

## License

This API and data are provided under **MIT License** for educational and commercial use.

### Attribution:
When using this API, please credit:
- **Data Source:** DANI's Crochet Glossary
- **Repository:** https://github.com/this4dani/crochet-glossary-api

---

## Quick Start

```bash
# Test the API right now:
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/api-info.json

# Get your first crochet term:
curl https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json | head -20
```

**Happy Crocheting!**