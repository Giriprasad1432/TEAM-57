# -------------------------------
# AI Career Guidance System - GROQ (FIXED VERSION)
# Properly formatted output with spacing fixes
# -------------------------------

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
import json
import uvicorn
import re
import os 
from dotenv import load_dotenv

# -------------------------------
# Configure Groq API (FREE TIER)
# Get your FREE key from: https://console.groq.com/keys
# -------------------------------
load_dotenv()
client = Groq(
    api_key=os.getenv("API_KEY")  # ← Replace with your FREE Groq key
)

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(
    title="AI Career Guidance System",
    description="Powered by Groq - Lightning Fast & Free - FIXED VERSION",
    version="2.1.0"
)

# -------------------------------
# CORS Configuration
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Input Schemas
# -------------------------------
class QuestionnaireInput(BaseModel):
    """16-question career assessment input"""
    areas_of_interest: Optional[List[str]] = None
    preferred_activities: Optional[List[str]] = None
    technical_skills: Optional[List[str]] = None
    education_level: Optional[str] = None
    work_style: Optional[List[str]] = None
    interest_in_data: Optional[str] = None
    interest_in_coding: Optional[str] = None
    preferred_industry: Optional[List[str]] = None
    career_priorities: Optional[List[str]] = None
    project_experience: Optional[List[str]] = None
    core_strengths: Optional[List[str]] = None
    learning_style: Optional[str] = None
    interview_confidence: Optional[str] = None
    career_vision: Optional[str] = None
    willingness_to_upskill: Optional[str] = None
    preferred_role_type: Optional[List[str]] = None

# -------------------------------
# Default Sample Data
# -------------------------------
DEFAULT_PROFILE = {
    "areas_of_interest": ["Data Analytics", "Machine Learning", "Problem Solving"],
    "preferred_activities": ["Analysis", "Research", "Building Solutions"],
    "technical_skills": ["Python", "SQL", "Excel"],
    "education_level": "Final Year B.Tech Student",
    "work_style": ["Independent", "Team Collaboration"],
    "interest_in_data": "High",
    "interest_in_coding": "High",
    "preferred_industry": ["Technology", "Finance", "E-commerce"],
    "career_priorities": ["Learning & Growth", "High Salary", "Job Security"],
    "project_experience": ["Data Analysis Dashboard", "Python Automation"],
    "core_strengths": ["Analytical Thinking", "Problem Solving", "Quick Learner"],
    "learning_style": "Hands-on with Projects",
    "interview_confidence": "Medium",
    "career_vision": "Want to become a Data Scientist or ML Engineer in next 3-5 years",
    "willingness_to_upskill": "Very High",
    "preferred_role_type": ["Technical", "Hybrid"]
}

# -------------------------------
# Helper Functions
# -------------------------------
def fix_text_spacing(text: str) -> str:
    """Fix common spacing issues in AI-generated text"""
    if not isinstance(text, str):
        return text
    
    # Add space after punctuation if missing
    text = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', text)
    
    # Add space between lowercase and uppercase (camelCase splits)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Fix common concatenations
    text = re.sub(r'(\w)(and|but|or|the|with|from|have|has)([A-Z])', r'\1 \2 \3', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_json_response(data: dict) -> dict:
    """Clean all text fields in JSON response"""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned[key] = fix_text_spacing(value)
            elif isinstance(value, list):
                cleaned[key] = [clean_json_response(item) if isinstance(item, (dict, list)) else fix_text_spacing(item) if isinstance(item, str) else item for item in value]
            elif isinstance(value, dict):
                cleaned[key] = clean_json_response(value)
            else:
                cleaned[key] = value
        return cleaned
    elif isinstance(data, list):
        return [clean_json_response(item) if isinstance(item, (dict, list)) else fix_text_spacing(item) if isinstance(item, str) else item for item in data]
    return data

def extract_json_from_text(text: str) -> dict:
    """Extract JSON from text that might contain markdown or extra text"""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Find JSON object
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass
    
    return json.loads(text.strip())

def call_groq(prompt: str) -> dict:
    """Call Groq API and parse JSON response with proper formatting"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert AI Career Counselor. 

CRITICAL FORMATTING RULES:
1. Always respond with valid JSON only
2. Use proper spacing between ALL words in every text field
3. Write naturally with complete, well-spaced sentences
4. No markdown, no code blocks, no extra formatting
5. Add proper punctuation and spacing after periods, commas
6. Make text readable and professional

Your JSON must be perfectly formatted and all text must have proper spacing."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,  # Lower temperature for more consistent output
            max_tokens=4000,
            top_p=0.9
        )
        
        text = chat_completion.choices[0].message.content.strip()
        
        # Parse JSON
        result = extract_json_from_text(text)
        
        # CRITICAL: Clean all text spacing issues
        result = clean_json_response(result)
        
        print("✅ Response cleaned and formatted successfully")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Raw response (first 500 chars): {text[:500] if 'text' in locals() else 'No response'}")
        raise HTTPException(status_code=500, detail="AI returned invalid JSON format")
    except Exception as e:
        print(f"❌ Groq API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

def format_questionnaire_data(data: dict) -> str:
    """Convert questionnaire responses into structured text for AI"""
    return f"""
📋 STUDENT CAREER ASSESSMENT PROFILE

1️⃣ Areas of Interest: {', '.join(data.get('areas_of_interest', ['Not specified']))}
2️⃣ Preferred Activities: {', '.join(data.get('preferred_activities', ['Not specified']))}
3️⃣ Technical Skills: {', '.join(data.get('technical_skills', ['None'])) if data.get('technical_skills') else 'Beginner level'}
4️⃣ Education Level: {data.get('education_level', 'Not specified')}
5️⃣ Work Style Preference: {', '.join(data.get('work_style', ['Not specified']))}
6️⃣ Interest in Data & Analytics: {data.get('interest_in_data', 'Medium')}
7️⃣ Interest in Coding/Programming: {data.get('interest_in_coding', 'Medium')}
8️⃣ Preferred Industry: {', '.join(data.get('preferred_industry', ['Open to all']))}
9️⃣ Career Priorities: {', '.join(data.get('career_priorities', ['Career growth']))}
🔟 Project Experience: {', '.join(data.get('project_experience', ['None yet'])) if data.get('project_experience') else 'No projects yet'}
1️⃣1️⃣ Core Strengths: {', '.join(data.get('core_strengths', ['Learning ability']))}
1️⃣2️⃣ Learning Style: {data.get('learning_style', 'Mixed approach')}
1️⃣3️⃣ Interview Confidence Level: {data.get('interview_confidence', 'Medium')}
1️⃣4️⃣ Career Vision (5 years): {data.get('career_vision', 'Exploring options')}
1️⃣5️⃣ Willingness to Upskill: {data.get('willingness_to_upskill', 'High')}
1️⃣6️⃣ Preferred Role Type: {', '.join(data.get('preferred_role_type', ['Technical']))}
"""

def merge_with_defaults(user_data: QuestionnaireInput) -> dict:
    """Merge user input with default values"""
    result = DEFAULT_PROFILE.copy()
    
    if user_data:
        user_dict = user_data.dict(exclude_none=True)
        result.update(user_dict)
    
    return result

# -------------------------------
# MAIN ENDPOINT: Comprehensive Career Analysis
# -------------------------------
@app.post("/comprehensive-career-analysis")
async def comprehensive_career_analysis(data: Optional[QuestionnaireInput] = None):
    """
    Main endpoint: Analyzes career assessment and provides complete guidance
    If no data provided, uses DEFAULT_PROFILE for demo
    """
    
    if data is None:
        profile_data = DEFAULT_PROFILE
        print("📝 Using default demo profile...")
    else:
        profile_data = merge_with_defaults(data)
        print("📝 Using user-provided profile...")
    
    user_profile = format_questionnaire_data(profile_data)
    
    prompt = f"""
You are an expert AI Career Counselor with deep knowledge of industry trends, job markets, and student career development.

**IMPORTANT FORMATTING**: 
- Use proper spacing between ALL words
- Write naturally with complete sentences
- Add proper punctuation
- Make text easy to read

**IMPORTANT CONTENT**: 
- Be encouraging and personalized
- Provide actionable advice
- Avoid repetitive corporate phrases
- Vary your language

Analyze this student's career profile thoroughly:

{user_profile}

Provide comprehensive career guidance with these sections:

**Return ONLY valid JSON (no markdown, no extra text):**

{{
  "recommended_careers": [
    {{
      "career_name": "Specific job title",
      "match_percentage": 85,
      "reason_for_match": "Detailed explanation why this fits their profile (2-3 well-spaced sentences)",
      "typical_salary_range": "INR range for India or USD for global",
      "job_outlook": "Growth prospects in next 3-5 years",
      "day_to_day_work": "What they'll actually do daily"
    }}
  ],
  "skill_analysis": {{
    "existing_strengths": ["Skills they already have that are valuable"],
    "critical_gaps": [
      {{
        "skill": "Specific skill name",
        "why_important": "Real-world reason this matters",
        "how_to_learn": "Specific actionable way to learn this",
        "time_to_learn": "Realistic timeframe"
      }}
    ]
  }},
  "recommended_certifications": [
    {{
      "cert_name": "Full certification name",
      "provider": "Organization offering it",
      "why_valuable": "Career benefit explained clearly",
      "estimated_duration": "Time needed",
      "difficulty_level": "Beginner/Intermediate/Advanced",
      "cost_range": "Approximate cost or 'Free'"
    }}
  ],
  "portfolio_projects": [
    {{
      "project_name": "Catchy project title",
      "what_to_build": "Clear description of the project",
      "skills_demonstrated": ["List of skills this project proves"],
      "technologies": ["Tech stack to use"],
      "complexity": "Beginner/Intermediate/Advanced",
      "time_estimate": "How long it takes",
      "wow_factor": "Why this impresses recruiters"
    }}
  ],
  "interview_preparation": {{
    "technical_questions": [
      {{
        "question": "Actual interview question",
        "topic_area": "What concept this tests",
        "difficulty": "Easy/Medium/Hard"
      }}
    ],
    "behavioral_questions": ["Real behavioral questions they'll face"],
    "coding_challenges": ["Types of coding problems to practice"],
    "how_to_prepare": ["Step by step preparation advice"]
  }},
  "learning_roadmap": {{
    "month_1": {{
      "focus": "Main theme for this month",
      "goals": ["Specific achievable goals"],
      "resources": ["Where to learn"],
      "success_metric": "How to know you succeeded"
    }},
    "month_2": {{
      "focus": "Main theme",
      "goals": ["Specific goals"],
      "resources": ["Resources"],
      "success_metric": "Success criteria"
    }},
    "month_3": {{
      "focus": "Main theme",
      "goals": ["Specific goals"],
      "resources": ["Resources"],
      "success_metric": "Success criteria"
    }}
  }},
  "personalized_message": "Write 3-4 encouraging sentences addressing their specific situation. Use proper spacing. Be genuine and motivating. Mention something specific from their profile.",
  "red_flags_to_avoid": ["Common mistakes beginners make in this career path"],
  "networking_tips": ["Specific ways to connect with professionals in these fields"],
  "salary_negotiation_prep": ["Tips for discussing compensation when they get offers"]
}}

CRITICAL: Ensure ALL text fields have proper spacing between words. Write naturally and professionally.
"""
    
    result = call_groq(prompt)
    
    print("✅ Career analysis generated successfully!")
    return result

# -------------------------------
# ENDPOINT 2: Quick Career Match
# -------------------------------
@app.post("/quick-career-match")
async def quick_career_match(data: Optional[QuestionnaireInput] = None):
    """Fast career matching - top 5 careers only"""
    
    if data is None:
        profile_data = DEFAULT_PROFILE
    else:
        profile_data = merge_with_defaults(data)
    
    user_profile = format_questionnaire_data(profile_data)
    
    prompt = f"""
Based on this student profile:

{user_profile}

Provide the top 5 career matches. Be specific and honest about fit. USE PROPER SPACING.

Return ONLY valid JSON:
{{
  "top_careers": [
    {{
      "career_name": "Specific job title",
      "match_score": 88,
      "one_line_reason": "Why this is a great fit",
      "entry_difficulty": "Easy/Moderate/Challenging",
      "first_step": "Immediate action they should take"
    }}
  ],
  "quick_advice": "2-3 sentence summary with proper spacing of what they should focus on now"
}}
"""
    
    result = call_groq(prompt)
    return result

# -------------------------------
# ENDPOINT 3: Project Ideas Generator
# -------------------------------
@app.post("/project-ideas")
async def project_ideas(data: Optional[QuestionnaireInput] = None):
    """Generate portfolio project ideas"""
    
    if data is None:
        profile_data = DEFAULT_PROFILE
    else:
        profile_data = merge_with_defaults(data)
    
    user_profile = format_questionnaire_data(profile_data)
    
    prompt = f"""
Generate 5 impressive portfolio projects for this student:

{user_profile}

Focus on projects that:
- Match their current skill level but stretch them slightly
- Demonstrate real-world problem solving
- Impress recruiters and hiring managers
- Can be completed in 2-4 weeks

USE PROPER SPACING IN ALL TEXT.

Return ONLY valid JSON:
{{
  "projects": [
    {{
      "title": "Catchy project name",
      "description": "What it does and why it matters",
      "target_audience": "Who would use this",
      "key_features": ["Main features to build"],
      "tech_stack": ["Technologies to use"],
      "learning_outcomes": ["What skills you'll gain"],
      "difficulty": "Beginner/Intermediate/Advanced",
      "estimated_time": "Time to complete",
      "github_tips": "How to present this on GitHub",
      "resume_impact": "Why this impresses employers"
    }}
  ]
}}
"""
    
    result = call_groq(prompt)
    return result

# -------------------------------
# ENDPOINT 4: Interview Mastery
# -------------------------------
@app.post("/interview-mastery")
async def interview_mastery(data: Optional[QuestionnaireInput] = None):
    """Complete interview preparation package"""
    
    if data is None:
        profile_data = DEFAULT_PROFILE
    else:
        profile_data = merge_with_defaults(data)
    
    user_profile = format_questionnaire_data(profile_data)
    
    prompt = f"""
Create a comprehensive interview prep guide for this student:

{user_profile}

Cover technical, behavioral, and practical aspects. USE PROPER SPACING.

Return ONLY valid JSON:
{{
  "technical_prep": {{
    "must_know_concepts": ["Core concepts they must master"],
    "practice_questions": [
      {{
        "question": "Actual interview question",
        "difficulty": "Easy/Medium/Hard",
        "key_points": ["What answer should cover"]
      }}
    ],
    "coding_practice": ["Where and what to practice"]
  }},
  "behavioral_prep": {{
    "common_questions": ["Behavioral questions they'll face"],
    "star_examples": ["Situations they should prepare stories for"],
    "red_flag_answers": ["What NOT to say"]
  }},
  "company_research": {{
    "what_to_research": ["Key things to know about target companies"],
    "questions_to_ask": ["Smart questions to ask interviewers"]
  }},
  "day_before_checklist": ["Last day preparation items"],
  "during_interview_tips": ["In-the-moment advice"],
  "follow_up": ["Post-interview actions"],
  "confidence_boosters": ["Mental preparation techniques"]
}}
"""
    
    result = call_groq(prompt)
    return result

# -------------------------------
# TEST ENDPOINT: Get Demo with Default Data
# -------------------------------
@app.get("/demo-analysis")
async def demo_analysis():
    """
    GET endpoint to see demo analysis with default profile
    Perfect for testing without sending POST data
    """
    print("🎯 Generating demo career analysis with Groq...")
    
    result = await comprehensive_career_analysis(None)
    
    return {
        "note": "This is a DEMO analysis using default profile",
        "default_profile_used": DEFAULT_PROFILE,
        "career_analysis": result
    }

# -------------------------------
# Health Check
# -------------------------------
@app.get("/")
async def root():
    return {
        "message": "🎓 AI Career Guidance System - Powered by Groq! ⚡ (FIXED VERSION)",
        "version": "2.1.0",
        "status": "active",
        "ai_model": "llama-3.3-70b-versatile (Groq)",
        "improvements": "Fixed text spacing issues in all responses",
        "quick_test": "Visit /demo-analysis to see instant results!",
        "endpoints": {
            "demo": "/demo-analysis (GET - no data needed!)",
            "main": "/comprehensive-career-analysis (POST)",
            "quick": "/quick-career-match (POST)",
            "projects": "/project-ideas (POST)",
            "interview": "/interview-mastery (POST)"
        },
        "tip": "All POST endpoints work with default data if you send empty body: {}"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "ai_model": "llama-3.3-70b-versatile",
        "provider": "Groq (FREE & FAST)",
        "version": "2.1.0 - Fixed spacing issues",
        "default_profile_loaded": bool(DEFAULT_PROFILE)
    }

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 AI CAREER GUIDANCE SYSTEM - FIXED VERSION")
    print("=" * 70)
    print("📍 Main URL: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 Quick Demo: http://localhost:8000/demo-analysis")
    print("=" * 70)
    print("✅ IMPROVEMENTS:")
    print("   - Fixed text spacing issues")
    print("   - Better formatting in all responses")
    print("   - Lower temperature for consistency")
    print("   - Automatic text cleaning")
    print("=" * 70)
    print("💡 Get FREE Groq API key: https://console.groq.com/keys")
    print("⚡ Lightning fast inference - No rate limit issues!")
    print("=" * 70)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )