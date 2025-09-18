# 🧠 AI Sales Analyzer

**AI-Powered Psychological Profiling for Marriage Coaching Sales**

🌐 **Live Demo:** [View Dashboard](https://your-vercel-url.vercel.app)

---

## 🎯 Quick Start

### Web Interface (No Setup Required)
1. **Visit the live demo** at your Vercel deployment URL
2. **Upload a transcript** using drag & drop
3. **Get instant AI analysis** with psychological profiling

### Local Development
```bash
# Clone repository
git clone https://github.com/ablacki/ai-sales-analyzer.git
cd ai-sales-analyzer

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your_key_here"

# Run analysis
python3 run_enhanced_analysis.py

# View dashboard
open index.html
```

---

## ✨ Features

- **🧠 Big Five Personality Analysis** - Deep psychological profiling
- **🎭 Client Archetype Classification** - 5 behavioral categories
- **📞 Sales Performance Scoring** - 7-dimension framework
- **💡 AI Coaching Recommendations** - Personalized strategies
- **🌐 Interactive Dashboard** - Real-time analysis interface
- **📊 Success Probability** - Data-driven conversion likelihood

---

## 🎭 Client Archetypes

1. **Analytical Researcher** - Data-driven, needs facts and logic
2. **Desperate Saver** - High urgency, emotional, crisis-focused
3. **Hopeful Builder** - Optimistic, growth-oriented, future-focused
4. **Skeptical Evaluator** - Cautious, needs proof and guarantees
5. **Consensus Seeker** - Collaborative, involves others in decisions

---

## 🚀 Deployment

### Vercel (Web Interface)
- **Frontend:** Static HTML/CSS/JavaScript dashboard
- **Backend:** Python serverless functions for AI analysis
- **Database:** Client-side storage with export capabilities

### Local (Full Features)
- **Complete AI Analysis Pipeline**
- **Batch Processing of Multiple Transcripts**
- **SQLite Database with Comprehensive Schema**
- **Executive Reporting and Analytics**

---

## 📊 Analysis Output

```json
{
  "archetype": "Hopeful Builder",
  "sales_score": 78,
  "success_probability": "73%",
  "big_five_personality": {
    "openness": 82,
    "conscientiousness": 76,
    "extraversion": 65,
    "agreeableness": 89,
    "neuroticism": 34
  },
  "coaching_recommendations": [
    "Focus on growth potential and future vision",
    "Use optimistic language and success stories",
    "Present solutions as building blocks"
  ]
}
```

---

## 🛠️ Tech Stack

- **AI Engine:** Anthropic Claude 3.5 Sonnet
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Backend:** Python 3.9+ with asyncio
- **Database:** SQLite (local) / Browser Storage (web)
- **Deployment:** Vercel (web) / Local Python (full)

---

## 📈 Use Cases

- **Sales Team Training** - Identify coaching priorities
- **Client Relationship Management** - Tailor communication styles
- **Conversion Optimization** - Improve closing techniques
- **Performance Analytics** - Track improvement over time

---

## 🔐 Privacy & Security

- **No Data Storage** - Transcripts processed in real-time only
- **Client-Side Analysis** - Results stored locally in browser
- **HIPAA Ready** - No external data transmission
- **Secure Processing** - Enterprise-grade AI APIs

---

**Built with ❤️ for Marriage Coaching Sales Optimization**