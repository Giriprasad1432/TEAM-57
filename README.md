# 🎯 AI Career Guidance System - Dynamic Questionnaire

## Overview
A personalized AI-powered career guidance system that adapts questions based on user responses. The system provides tailored career analysis, skill recommendations, certifications, project ideas, and a 6-month roadmap based on each user's unique educational background and interests.

## 🌟 Key Features

### 1. **Dynamic Question Flow**
- Questions adapt intelligently based on previous answers
- **Example**: If a 10th standard student selects "Medical Interest", they get NEET preparation questions. If they select "Engineering", they get engineering-specific questions
- No irrelevant questions - each user gets a personalized path
- **40+ conditional questions** covering all education levels and career paths

### 2. **Smart Branching Logic
The system creates unique paths for:
- **10th Standard Students** → Career exploration (Medical, Engineering, Commerce, Arts, Creative, Sports, Vocational)
- **12th Standard Students** → Stream-specific guidance (PCM, PCB, Commerce, Arts)
- **Undergraduates** → Field-specific career planning
- **Graduates** → Job search, higher studies, or career change
- **Working Professionals** → Career advancement and skill upgradation

### 3. **AI-Powered Career Coach**
- Real-time chat with AI career advisor
- Context-aware responses based on user profile
- Short, actionable advice (2-3 sentences)
- Available during questionnaire and analysis

### 4. **Comprehensive Analysis**
Each user receives:
- ✅ **Top 3 Career Matches** with percentage match
- ✅ **Missing Skills** (priority ordered)
- ✅ **Required Certifications** with platform and cost
- ✅ **Portfolio Projects** tailored to their field
- ✅ **6-Month Roadmap** with monthly action items
- ✅ **Job Search Strategy** / Action Plan
- ✅ **Personalized Advice**

### 5. **Interactive Features**
- Back button to revise previous answers
- Progress tracking
- Custom "Other" option with text input
- Multiple selection with limits
- Regenerate analysis after new chat insights
- Side-by-side chat during analysis review

## 📋 Prerequisites

### Backend Requirements
- Python 3.8+
- FastAPI
- Groq API (for LLaMA 3.3 70B)
- Required packages:
  ```
  fastapi
  uvicorn
  pydantic
  groq
  python-dotenv
  ```

### Frontend Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies (vanilla HTML/CSS/JavaScript)

## 🚀 Installation & Setup

### Step 1: Clone or Download Files
```bash
# Create project directory
mkdir career-guidance-system
cd career-guidance-system
```

### Step 2: Install Python Dependencies
```bash
pip install fastapi uvicorn pydantic groq python-dotenv
```

### Step 3: Setup Environment Variables
Create a `.env` file in the project root:
```env
API_KEY=your_groq_api_key_here
```

**Get Groq API Key:**
1. Visit https://console.groq.com
2. Sign up for free account
3. Go to API Keys section
4. Generate new API key
5. Copy and paste into `.env` file

### Step 4: Project Structure
```
career-guidance-system/
│
├── backend.py          # FastAPI backend (dynamic_career_backend)
├── index.html          # Frontend UI (dynamic_career_frontend)
├── .env               # Environment variables
└── README.md          # This file
```

### Step 5: Run the Application

**Start Backend:**
```bash
python backend.py
```
Backend will run on: `http://localhost:8000`

**Open Frontend:**
- Simply open `index.html` in your web browser
- Or use a local server:
```bash
python -m http.server 8080
# Then visit http://localhost:8080
```

## 🎮 How to Use

### For Students (10th/12th/UG/PG)

1. **Start Questionnaire**
   - Select your current educational level
   - Questions will adapt based on your response

2. **Answer Dynamic Questions**
   - Questions are tailored to YOUR path
   - Use back button if you want to change answers
   - Select "Other" and specify custom answers when needed

3. **Chat with Career Coach**
   - After questions, ask specific doubts
   - Get instant, focused career advice
   - Examples: "Should I learn Python or Java first?", "Best colleges for my profile?"

4. **Get Complete Analysis**
   - Click "Get Complete Analysis" button
   - AI generates personalized roadmap
   - Review all sections in detail

5. **Continue Asking Questions**
   - Use sidebar chat during analysis
   - If you ask new questions, banner appears to regenerate analysis
   - Click "Regenerate Now" for updated insights

### For Working Professionals

1. **Select Experience Level**
   - System asks about your current role and goals

2. **Define Career Goals**
   - Switch jobs, get promotion, change field, etc.

3. **Get Tailored Recommendations**
   - Skills for next level
   - Certifications employers value
   - Networking strategies

## 🔄 Dynamic Question Examples

### Example Path 1: 10th Student → Medical Interest
```
1. Educational Level → 10th Standard
2. Career Interest → Medical & Healthcare
3. Medical Specialization → MBBS, BDS, Nursing, etc.
4. NEET Preparation → Currently preparing / Planning to start
5. Study Time → 20-30 hours/week
6. Learning Style → Video tutorials + Practice
7. Budget → ₹20,000-₹50,000
8. Location → Willing to relocate
```

### Example Path 2: 12th Science (PCM) → Engineering
```
1. Educational Level → 12th Standard (Currently Studying)
2. Stream → Science (PCM)
3. Engineering Interest → Computer Science, AI/ML, Data Science
4. Technical Skills → Python, HTML/CSS, No experience yet
5. Experience → Complete beginner
6. Career Goals → Get first tech job, Build portfolio
7. Study Time → 10-20 hours/week
8. Learning Style → Hands-on projects, Online courses
```

### Example Path 3: Working Professional → Career Change
```
1. Educational Level → Working Professional
2. Experience → 2-5 years
3. Career Goal → Change career field entirely
4. Current Field → Marketing/Sales
5. Target Field → Software Development/IT
6. Technical Skills → No technical skills yet
7. Study Time → 10-20 hours/week
8. Budget → ₹50,000+
```

## 🎯 Question Categories

The system includes questions about:
- **Educational Background** (10th, 12th, UG, PG, Professional)
- **Academic Streams** (Science PCM/PCB, Commerce, Arts)
- **Career Interests** (40+ career fields)
- **Technical Skills** (Programming, Design, Business, etc.)
- **Experience Level** (Fresher to 10+ years)
- **Career Goals** (First job, Switch, Promotion, Business)
- **Learning Preferences** (Videos, Books, Projects, Bootcamps)
- **Budget** (Free to ₹50,000+)
- **Location** (Remote, Office, Relocate, International)
- **Field-Specific** (Engineering branches, Medical specializations, Commerce paths, etc.)

## 🛠️ Technical Architecture

### Backend (FastAPI)
- **Framework**: FastAPI (modern, async Python web framework)
- **AI Model**: Groq LLaMA 3.3 70B Versatile
- **Question Engine**: Tree-based conditional logic
- **Session Management**: In-memory storage with session IDs
- **API Endpoints**:
  - `GET /` - Health check
  - `GET /start` - Get first question
  - `GET /question/{id}` - Get specific question
  - `POST /answer` - Submit answer & get next question
  - `POST /chat` - Chat with AI coach
  - `POST /analyze` - Generate comprehensive analysis

### Frontend (HTML/CSS/JavaScript)
- **Vanilla JavaScript** (no framework dependencies)
- **Responsive Design** (mobile, tablet, desktop)
- **Dynamic UI Updates** (smooth animations)
- **Real-time Chat** (WebSocket-style experience)
- **Split-Screen Layout** (chat + analysis)

### Data Flow
```
User Answer → Backend → Question Logic → Next Question
                     ↓
                Profile Building
                     ↓
            Stored in Session
                     ↓
        Used for Chat Context & Analysis
```

## 🧠 How Dynamic Logic Works

### Question Tree Structure
Each question has:
```python
{
    "id": "unique_id",
    "question": "Question text",
    "type": "single" or "multiple",
    "options": [...],
    "next_question_logic": {
        "Option 1": "next_question_id_1",
        "Option 2": "next_question_id_2",
        "default": "fallback_question_id"
    }
}
```

### Example Logic
```python
"next_question_logic": {
    "Science (PCM)": "engineering_interest",      # Goes to engineering path
    "Science (PCB)": "medical_interest",          # Goes to medical path
    "Commerce": "commerce_interest",              # Goes to commerce path
    "Arts/Humanities": "arts_interest",           # Goes to arts path
    "default": "career_interest_general"          # Fallback
}
```

## 📊 Analysis Generation

### AI Prompt Engineering
The system builds a detailed prompt with:
- User's educational level
- Stream/field of study
- All selected interests
- Current skills
- Career goals
- Time commitment
- Learning preferences
- Budget and location
- Recent chat conversation context

### Output Format
The AI generates structured analysis with sections:
1. **Career Matches** (with % match based on profile fit)
2. **Skills Gap** (priority ordered for target careers)
3. **Certifications** (with platform, cost, duration)
4. **Projects** (technologies matching their level)
5. **6-Month Roadmap** (month-by-month action plan)
6. **Job Search Strategy** (tailored to their situation)
7. **Personalized Advice** (motivational guidance)

## 🎨 Customization

### Add New Questions
1. Open `backend.py`
2. Find `QUESTION_TREE` dictionary
3. Add new question entry:
```python
"your_question_id": {
    "id": "your_question_id",
    "question": "Your question text?",
    "type": "single",  # or "multiple"
    "options": ["Option 1", "Option 2", "..."],
    "next_question_logic": {
        "Option 1": "next_q_id",
        "default": "fallback_q_id"
    }
}
```
4. Link from previous question's `next_question_logic`

### Modify UI Colors/Styling
Edit the `<style>` section in `index.html`:
```css
/* Change primary color from purple to blue */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change to: */
background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%);
```

### Change AI Model
In `backend.py`, modify:
```python
model="llama-3.3-70b-versatile"
# Change to other Groq models:
# "llama-3.1-70b-versatile"
# "mixtral-8x7b-32768"
# "gemma-7b-it"
```

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Install missing packages
pip install -r requirements.txt

# Verify .env file exists with API_KEY
cat .env
```

### CORS Errors
If frontend can't connect to backend:
1. Ensure backend is running on `localhost:8000`
2. Check browser console for errors
3. Verify `API_URL` in `index.html` matches backend address

### API Key Invalid
```bash
# Verify Groq API key in .env
echo $API_KEY  # On Mac/Linux
echo %API_KEY%  # On Windows

# Get new key from https://console.groq.com
```

### Questions Not Loading
1. Check browser console (F12)
2. Verify backend `/start` endpoint works: `http://localhost:8000/start`
3. Check backend logs for errors

### Analysis Generation Fails
- **Groq API Quota**: Free tier has limits (check console.groq.com)
- **Network Issues**: Check internet connection
- **Timeout**: Analysis takes 10-15 seconds, wait patiently

## 🔒 Security Notes

### For Production Deployment
1. **Never expose API keys in frontend code**
2. **Use environment variables** for sensitive data
3. **Add authentication** for multi-user systems
4. **Implement rate limiting** to prevent abuse
5. **Use HTTPS** for secure communication
6. **Validate all user inputs** on backend
7. **Add CORS restrictions** to allowed domains

### Current Security (Development)
- ⚠️ No authentication (single-user local use)
- ⚠️ In-memory session storage (resets on restart)
- ⚠️ CORS open to all origins (development only)

## 📈 Future Enhancements

### Planned Features
- [ ] User accounts & persistent storage (database)
- [ ] Resume/CV builder integration
- [ ] Job board integration (real job listings)
- [ ] College/university recommendations
- [ ] Scholarship finder
- [ ] Mock interview practice
- [ ] Peer comparison (anonymous)
- [ ] Progress tracking over time
- [ ] Email reports (PDF download)
- [ ] Multi-language support

### Advanced Features
- [ ] Voice input/output
- [ ] Video analysis (explain career paths)
- [ ] Mentorship matching
- [ ] Success stories from similar profiles
- [ ] Integration with LinkedIn
- [ ] Industry expert Q&A
- [ ] Live webinar scheduling

## 🤝 Contributing

Want to improve the system? Here's how:

1. **Add More Questions**: Expand the question tree
2. **Improve Analysis**: Enhance AI prompt engineering
3. **Better UI/UX**: Improve design and animations
4. **Bug Fixes**: Report and fix issues
5. **Documentation**: Improve this README

## 📝 License

This project is provided as-is for educational and personal use.

## 🆘 Support

### Common Questions

**Q: How many questions will I get?**
A: Depends on your path! Usually 6-10 questions, all relevant to your situation.

**Q: Can I change my answers?**
A: Yes! Use the "Previous" button to go back.

**Q: Is my data saved?**
A: Currently stored in memory only (resets when you close). For permanent storage, we'd need a database.

**Q: Can I use this offline?**
A: Backend needs internet for AI API. Frontend works offline if you've loaded it once.

**Q: Is it free?**
A: Yes! Groq offers free tier API access. Paid tiers available for heavy usage.

**Q: How accurate is the analysis?**
A: AI provides guidance based on current trends and your profile. Always consult professionals for major decisions.

### Contact & Support

- **Issues**: Check browser console and backend logs
- **Questions**: Review this README thoroughly
- **API Issues**: Visit https://console.groq.com/docs

## 🎓 Educational Value

### For Students Learning:
- **Python & FastAPI** - Modern web development
- **AI Integration** - Using LLMs via API
- **Frontend Development** - Vanilla JavaScript
- **Dynamic UIs** - Conditional rendering
- **API Design** - RESTful endpoints
- **Session Management** - User state handling

### Use Cases:
- School/college career counseling
- Ed-tech platforms
- Job portals
- Skill assessment tools
- Learning management systems
- HR recruitment tools

## 🎉 Credits

- **AI Model**: Groq (LLaMA 3.3 70B Versatile)
- **Framework**: FastAPI
- **Icons**: Unicode Emoji
- **Design**: Custom CSS3

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install dependencies
pip install fastapi uvicorn pydantic groq python-dotenv

# 2. Create .env file
echo "API_KEY=your_groq_api_key" > .env

# 3. Run backend
python backend.py

# 4. Open index.html in browser

# 5. Start your career journey! 🎯
```

---

**Version**: 6.0.0  
**Last Updated**: December 2024  
**Status**: Production Ready ✅

**Enjoy your personalized career guidance journey! 🎯🚀**