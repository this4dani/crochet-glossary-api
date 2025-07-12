# 🧶 Crochet Glossary API

> A comprehensive, free API for crochet terminology, techniques, and quiz systems. Perfect for websites, mobile apps, and educational platforms.

![API Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Terms](https://img.shields.io/badge/terms-265+-purple)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

## 🚀 Quick Start

```javascript
// Fetch all crochet terms
const response = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json');
const data = await response.json();
console.log(`Loaded ${data.meta.total_terms} crochet terms!`);
```

## 📡 API Endpoints

| Endpoint | Description | Size | Use Case |
|----------|-------------|------|----------|
| [`terms.json`](https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json) | All terms (lightweight) | ~50KB | General lookups, apps |
| [`glossary.json`](https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json) | Complete API with search index | ~80KB | Advanced features |
| [`categories.json`](https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/categories.json) | Terms grouped by category | ~60KB | Filtering, menus |
| [`quiz.json`](https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/quiz.json) | Quiz questions & answers | ~30KB | Educational apps |
| [`api-info.json`](https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/api-info.json) | API metadata | ~2KB | Version info |

### Base URL
```
https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/
```

## 🎯 What's Included

### ✅ **265+ Crochet Terms**
- **Basic Stitches**: SC, DC, HDC, TR, etc.
- **Advanced Techniques**: Cables, colorwork, construction methods
- **US & UK Terminology**: Complete translation pairs
- **Community Slang**: WIP, CAL, frogging, yarn chicken
- **Modern Methods**: C2C, graphgans, planned pooling

### ✅ **Rich Data Structure**
```json
{
  "id": "SC",
  "name_us": "Single Crochet",
  "name_uk": "Double Crochet",
  "category": "Basic Stitches",
  "difficulty": "1",
  "description": "The most basic crochet stitch...",
  "tags": ["basic", "fundamental", "beginner"],
  "time_to_learn": "5 minutes",
  "best_for": "Tight fabric, amigurumi"
}
```

### ✅ **Quiz System Ready**
- 50+ auto-generated questions
- Multiple choice format
- Difficulty levels
- US vs UK terminology challenges

## 💡 Use Cases

### **Crochet Websites**
```javascript
// Add term tooltips to your patterns
function addGlossaryTooltips() {
  const terms = await fetchTerms();
  document.querySelectorAll('.stitch-abbr').forEach(el => {
    const term = terms.find(t => t.id === el.textContent);
    if (term) el.title = term.name_us;
  });
}
```

### **Mobile Apps**
```javascript
// Offline-capable glossary
async function cacheGlossary() {
  const terms = await fetch(API_URL + 'terms.json');
  localStorage.setItem('crochet-terms', JSON.stringify(terms));
}
```

### **Educational Platforms**
```javascript
// Random quiz question
async function getRandomQuiz() {
  const quiz = await fetch(API_URL + 'quiz.json');
  const questions = quiz.data;
  return questions[Math.floor(Math.random() * questions.length)];
}
```

### **WordPress Plugins**
```php
// Shortcode for term definitions
function crochet_term_shortcode($atts) {
    $term_id = $atts['id'];
    $api_data = wp_remote_get('https://raw.githubusercontent.com/...');
    // Display term definition
}
```

## 🎮 Quiz & Badge System

Perfect foundation for educational features:

### **Quiz Categories**
- 🧶 **Stitch Master**: Basic stitches (SC, DC, HDC)
- 🌍 **Global Crocheter**: US vs UK terminology  
- 🎨 **Technique Expert**: Advanced methods
- 💬 **Community Pro**: Crochet slang and culture

### **Badge Ideas**
- Complete accuracy on basic stitches
- Master US/UK terminology differences
- Advanced technique knowledge
- Community terminology expert

## 🔄 Data Updates

The API is automatically updated from our master Google Sheets database:

- ✅ **Always Current**: Latest terminology and techniques
- ✅ **Community Driven**: Crowdsourced definitions
- ✅ **Quality Controlled**: Expert review process
- ✅ **Version Tracked**: Each update is timestamped

## 📚 Examples

### Simple Term Lookup
```javascript
const terms = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json')
  .then(r => r.json());

const singleCrochet = terms.data.find(term => term.id === 'SC');
console.log(singleCrochet.name_us); // "Single Crochet"
console.log(singleCrochet.name_uk); // "Double Crochet"
```

### Category Filtering
```javascript
const categories = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/categories.json')
  .then(r => r.json());

const basicStitches = categories.data['Basic Stitches'];
// Array of all basic stitch terms
```

### Search Implementation
```javascript
function searchTerms(query, terms) {
  return terms.filter(term => 
    term.name_us.toLowerCase().includes(query.toLowerCase()) ||
    term.name_uk.toLowerCase().includes(query.toLowerCase()) ||
    term.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
  );
}
```

## 🤝 Contributing

We welcome contributions to improve the glossary!

### **Data Improvements**
- Submit corrections via [Issues](../../issues)
- Suggest new terms
- Report US/UK terminology differences

### **Technical Contributions**
- Improve quiz generation
- Add new data formats
- Enhance API documentation

## 📈 API Stats

- **🎯 265+ Terms**: Most comprehensive free crochet API
- **🌍 Global Coverage**: US, UK, and international terminology
- **📱 Mobile Ready**: Lightweight JSON, CORS enabled
- **⚡ Fast**: Served via GitHub CDN
- **🔒 Reliable**: 99.9% uptime via GitHub infrastructure

## 🎉 Who's Using This API

- **Pattern Websites**: Adding glossary tooltips
- **Mobile Apps**: Offline crochet companions  
- **Educational Platforms**: Interactive learning tools
- **Browser Extensions**: Instant term lookups
- **WordPress Sites**: Automated glossary features

*[Add your project here by submitting a PR!]*

## 📄 License

MIT License - feel free to use in any project, commercial or personal. Just include attribution.

## 💬 Support & Community

- 🐛 **Bug Reports**: [Open an Issue](../../issues)
- 💡 **Feature Requests**: [Start a Discussion](../../discussions)
- 📧 **Direct Contact**: via GitHub
- 🌟 **Show Support**: Star this repository!

## 🔗 Related Projects

- **[DANI'S Website](https://this4dani.com)**: The original crochet glossary
- **[Pattern Library](#)**: Coming soon
- **[Mobile App](#)**: In development

---

**Made with ❤️ for the crochet community by [DANI](https://github.com/this4dani)**

*Helping crocheters understand patterns, one stitch at a time* 🧶