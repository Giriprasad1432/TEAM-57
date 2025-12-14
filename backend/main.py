from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from groq import Groq
import uvicorn
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

app = FastAPI(title="AI Career Guidance System", version="5.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionAnswer(BaseModel):
    question_id: int
    answers: List[str]
    session_id: Optional[str] = None
    custom_answer: Optional[str] = None

class ChatMessage(BaseModel):
    session_id: str
    message: str

QUESTIONS = [
    {
        "id": 1,
        "question": "What is your current educational background?",
        "type": "single",
        "options": [
            "High School/12th Pass",
            "Bachelor's Degree (B.Tech/B.E./BSc/BCA)",
            "Master's Degree (M.Tech/MBA/MSc)",
            "Doctorate (PhD)",
            "Diploma/Certification",
            "Currently Studying",
            "Other (Specify)"
        ]
    },
    {
        "id": 2,
        "question": "Which career areas interest you the most? (Select top 3)",
        "type": "multiple",
        "options": [
            "Software Development",
            "Data Science & Analytics",
            "Artificial Intelligence & ML",
            "Web Development",
            "Mobile App Development",
            "Cloud Computing",
            "Cybersecurity",
            "UI/UX Design",
            "Digital Marketing",
            "Business Analytics",
            "Finance & Banking",
            "Healthcare Technology",
            "Education Technology",
            "Entrepreneurship",
            "Research & Development",
            "Other (Specify)"
        ],
        "max_selections": 3
    },
    {
        "id": 3,
        "question": "What technical skills do you currently have?",
        "type": "multiple",
        "options": [
            "Python",
            "JavaScript",
            "Java",
            "C++/C#",
            "HTML/CSS",
            "SQL/Databases",
            "Git/GitHub",
            "Cloud Platforms (AWS/Azure/GCP)",
            "Data Analysis",
            "Machine Learning",
            "Web Frameworks (React/Node.js)",
            "Mobile Development",
            "UI/UX Tools",
            "DevOps Tools",
            "No technical skills yet",
            "Other (Specify)"
        ]
    },
    {
        "id": 4,
        "question": "How much professional experience do you have?",
        "type": "single",
        "options": [
            "No experience (Student/Fresher)",
            "0-1 years (Entry Level)",
            "1-3 years (Junior Level)",
            "3-5 years (Mid Level)",
            "5+ years (Senior Level)",
            "Career Changer from different field",
            "Other (Specify)"
        ]
    },
    {
        "id": 5,
        "question": "What are your primary career goals?",
        "type": "multiple",
        "options": [
            "Get first job in tech",
            "Switch to better paying job",
            "Learn new skills for promotion",
            "Start freelance career",
            "Build startup/own business",
            "Move to managerial role",
            "Work internationally",
            "Achieve work-life balance",
            "Other (Specify)"
        ]
    },
    {
        "id": 6,
        "question": "How much time can you dedicate to learning weekly?",
        "type": "single",
        "options": [
            "Less than 5 hours",
            "5-10 hours",
            "10-20 hours",
            "20-30 hours",
            "30+ hours (Full-time learning)",
            "Other (Specify)"
        ]
    },
    {
        "id": 7,
        "question": "What is your preferred learning style?",
        "type": "single",
        "options": [
            "Video tutorials (YouTube/Udemy)",
            "Online courses with certificates",
            "Books & documentation",
            "Hands-on projects",
            "Bootcamps/Classroom training",
            "Mentorship/1-on-1 guidance",
            "Other (Specify)"
        ]
    },
    {
        "id": 8,
        "question": "Which industries interest you?",
        "type": "multiple",
        "options": [
            "Technology/IT",
            "Finance/Banking",
            "Healthcare",
            "E-commerce/Retail",
            "Education",
            "Entertainment/Media",
            "Manufacturing",
            "Government/Public Sector",
            "Startups",
            "Consulting",
            "Other (Specify)"
        ]
    },
    {
        "id": 9,
        "question": "What are your salary expectations for first job?",
        "type": "single",
        "options": [
            "Less than ₹3 LPA",
            "₹3-6 LPA",
            "₹6-10 LPA",
            "₹10-15 LPA",
            "₹15-20 LPA",
            "₹20+ LPA",
            "Looking for experience, not salary",
            "Other (Specify)"
        ]
    },
    {
        "id": 10,
        "question": "Are you willing to relocate for opportunities?",
        "type": "single",
        "options": [
            "Yes, anywhere in India",
            "Yes, specific cities only",
            "No, remote only",
            "Open to hybrid (part office/part remote)",
            "Considering international relocation",
            "Other (Specify)"
        ]
    }
]

class CareerAgent:
    def __init__(self):
        self.name = "Career Coach Alex"
        self.chat_histories = {}
    
    async def chat(self, sid: str, msg: str, profile: Dict) -> Dict:
        """Short, clear, relevant chat responses"""
        if sid not in self.chat_histories:
            self.chat_histories[sid] = []
        
        self.chat_histories[sid].append({"role": "user", "content": msg})
        
        profile_context = f"""Education: {profile.get('education')}
Interests: {', '.join(profile.get('interests', [])[:2])}
Skills: {', '.join(profile.get('skills', [])[:3])}
Experience: {profile.get('experience')}
Goals: {', '.join(profile.get('goals', [])[:2])}"""
        
        system_prompt = f"""You are a friendly career advisor. Keep responses SHORT (2-3 sentences max).

User Profile:
{profile_context}

Rules:
- Be direct and specific to THEIR profile
- Give ONE actionable tip per response
- Stay on topic (career, skills, jobs)
- End with a brief follow-up question if relevant"""
        
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": msg}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=150
            )
            
            response = completion.choices[0].message.content.strip()
            self.chat_histories[sid].append({"role": "assistant", "content": response})
            
            return {"success": True, "response": response}
        except:
            return {"success": False, "response": "I'd suggest focusing on practical projects first. What specific area interests you most?"}
    
    async def generate_analysis(self, sid: str, profile: Dict, chat_history: List) -> Dict:
        """Generate comprehensive personalized analysis"""
        
        profile_text = f"""USER PROFILE:
Education: {profile.get('education')}
Career Interests: {', '.join(profile.get('interests', []))}
Current Skills: {', '.join(profile.get('skills', []))}
Experience: {profile.get('experience')}
Goals: {', '.join(profile.get('goals', []))}
Weekly Study Time: {profile.get('time_commitment')}
Learning Style: {profile.get('learning_style')}
Target Industries: {profile.get('preferred_industry')}
Salary Expectation: {profile.get('salary_expectation')}
Relocation: {profile.get('relocation_willingness')}"""
        
        chat_context = ""
        if chat_history:
            recent = [m['content'][:80] for m in chat_history[-4:] if m['role'] == 'user']
            if recent:
                chat_context = f"\n\nCHAT TOPICS: {'; '.join(recent)}"
        
        prompt = f"""Create a DETAILED career analysis based on this SPECIFIC user's profile.

{profile_text}{chat_context}

FORMAT EXACTLY AS:

🎯 TOP 3 CAREER MATCHES
For each career (numbered 1-3):
- Job Title | XX% match
- Why it fits: [Reference their specific interests/skills]
- Salary Range: [Realistic for their experience]
- Entry Path: [Specific first steps]

💪 MISSING SKILLS (Priority Order)
For each skill (numbered 1-5):
- Skill Name
- Why Critical: [For their target careers]
- Learning Time: [With their study hours]
- Best Resources: [2-3 specific courses/platforms]

📜 REQUIRED CERTIFICATIONS
For each cert (numbered 1-4):
- Certification Name
- Why Essential: [Career impact]
- Platform & Cost
- Duration
- Value: [How it helps job search]

🚀 PORTFOLIO PROJECTS (Career-Specific)
For each project (numbered 1-4):
- Project Name
- Technologies: [Match their skills + gap skills]
- Timeline: [Weeks based on their study time]
- What It Demonstrates
- Where to Showcase

🗺️ 6-MONTH ROADMAP
Month 1: [Focus area with 3 specific actions]
Month 2: [Next phase with 3 actions]
Month 3: [Skill building with 3 actions]
Month 4: [Project work with 3 actions]
Month 5: [Portfolio completion with 3 actions]
Month 6: [Job search with 3 actions]

💼 JOB SEARCH STRATEGY
- Target Companies: [5 companies in their industries]
- Application Tips: [Tailored to their level]
- Networking: [Specific actions]
- Interview Prep: [Focus areas]

💡 PERSONALIZED ADVICE
[3-4 sentences addressing their specific situation, concerns from chat, and motivational guidance]

Make EVERYTHING specific to THIS user - reference their actual answers."""
        
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Generate my comprehensive career analysis."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=2500
            )
            
            analysis_text = completion.choices[0].message.content
            return self._parse_analysis(analysis_text, profile)
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._fallback_analysis(profile)
    
    def _parse_analysis(self, text: str, profile: Dict) -> Dict:
        """Parse structured analysis"""
        result = {
            "career_matches": [],
            "missing_skills": [],
            "certifications": [],
            "projects": [],
            "roadmap": {},
            "job_search": {},
            "final_advice": "",
            "is_personalized": True
        }
        
        lines = text.split('\n')
        current_section = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            if "CAREER MATCHES" in line:
                current_section = "careers"
            elif "MISSING SKILLS" in line:
                current_section = "skills"
            elif "CERTIFICATIONS" in line:
                current_section = "certs"
            elif "PORTFOLIO PROJECTS" in line:
                current_section = "projects"
            elif "ROADMAP" in line:
                current_section = "roadmap"
            elif "JOB SEARCH" in line:
                current_section = "job"
            elif "PERSONALIZED ADVICE" in line:
                current_section = "advice"
                advice_lines = []
                for j in range(i+1, min(i+8, len(lines))):
                    if lines[j].strip() and not lines[j].startswith(('🎯', '💪', '📜', '🚀', '🗺️', '💼')):
                        advice_lines.append(lines[j].strip())
                result["final_advice"] = ' '.join(advice_lines)
                continue
            
            if current_section == "careers":
                if line.startswith(('-', '1.', '2.', '3.')):
                    if '|' in line and '%' in line:
                        parts = line.split('|')
                        title = parts[0].split('.', 1)[-1].strip().strip('-').strip()
                        match = parts[1].split('%')[0].strip()
                        
                        details = []
                        for j in range(i+1, min(i+5, len(lines))):
                            if lines[j].strip().startswith(('-', '•', 'Why', 'Salary', 'Entry')):
                                details.append(lines[j].strip().lstrip('-•').strip())
                        
                        result["career_matches"].append({
                            "title": title,
                            "match": match if match.isdigit() else "75",
                            "details": details[:4]
                        })
            
            elif current_section == "skills":
                if line.startswith(('-', '1.', '2.', '3.', '4.', '5.')):
                    skill_name = line.split('.', 1)[-1].strip().strip('-').strip()
                    if skill_name and len(skill_name) < 50:
                        details = []
                        for j in range(i+1, min(i+5, len(lines))):
                            if lines[j].strip().startswith(('-', '•', 'Why', 'Learning', 'Best')):
                                details.append(lines[j].strip().lstrip('-•').strip())
                        
                        result["missing_skills"].append({
                            "skill": skill_name,
                            "details": details[:4]
                        })
            
            elif current_section == "certs":
                if line.startswith(('-', '1.', '2.', '3.', '4.')):
                    cert_name = line.split('.', 1)[-1].strip().strip('-').strip()
                    if cert_name and len(cert_name) < 60:
                        details = []
                        for j in range(i+1, min(i+6, len(lines))):
                            if lines[j].strip().startswith(('-', '•', 'Why', 'Platform', 'Duration', 'Value')):
                                details.append(lines[j].strip().lstrip('-•').strip())
                        
                        result["certifications"].append({
                            "name": cert_name,
                            "details": details[:5]
                        })
            
            elif current_section == "projects":
                if line.startswith(('-', '1.', '2.', '3.', '4.')):
                    project_name = line.split('.', 1)[-1].strip().strip('-').strip()
                    if project_name and len(project_name) < 70:
                        details = []
                        for j in range(i+1, min(i+6, len(lines))):
                            if lines[j].strip().startswith(('-', '•', 'Technologies', 'Timeline', 'What', 'Where')):
                                details.append(lines[j].strip().lstrip('-•').strip())
                        
                        result["projects"].append({
                            "name": project_name,
                            "details": details[:5]
                        })
            
            elif current_section == "roadmap":
                if line.startswith('Month'):
                    month_num = line.split(':')[0].strip()
                    month_content = line.split(':', 1)[1].strip() if ':' in line else ''
                    actions = [month_content] if month_content else []
                    
                    for j in range(i+1, min(i+4, len(lines))):
                        if lines[j].strip().startswith(('-', '•', '1.', '2.', '3.')):
                            actions.append(lines[j].strip().lstrip('-•123.').strip())
                    
                    result["roadmap"][month_num] = actions[:3]
            
            elif current_section == "job":
                if ':' in line:
                    key = line.split(':')[0].strip()
                    value = line.split(':', 1)[1].strip()
                    result["job_search"][key] = value
        
        if not result["career_matches"]:
            result["career_matches"] = self._get_default_careers(profile)
        if not result["missing_skills"]:
            result["missing_skills"] = self._get_default_skills(profile)
        if not result["certifications"]:
            result["certifications"] = self._get_default_certs(profile)
        if not result["projects"]:
            result["projects"] = self._get_default_projects(profile)
        if not result["roadmap"]:
            result["roadmap"] = self._get_default_roadmap(profile)
        if not result["final_advice"]:
            result["final_advice"] = self._get_default_advice(profile)
        
        return result
    
    def _get_default_careers(self, profile):
        interests = profile.get('interests', ['Software Development'])
        exp = profile.get('experience', '')
        
        careers = []
        if 'Software Development' in interests or 'Web Development' in interests:
            careers.append({
                "title": "Full Stack Developer",
                "match": "85",
                "details": [
                    f"Matches your interest in {interests[0]}",
                    f"Salary: ₹{'6-12' if 'No experience' in exp else '10-18'} LPA",
                    "Build MERN/MEAN stack projects",
                    "Learn React, Node.js, MongoDB"
                ]
            })
        
        if 'Data Science' in str(interests) or 'Analytics' in str(interests):
            careers.append({
                "title": "Data Analyst",
                "match": "78",
                "details": [
                    "Aligns with your data interests",
                    f"Salary: ₹{'5-10' if 'No experience' in exp else '8-15'} LPA",
                    "Master SQL, Python, Excel",
                    "Create data visualization dashboards"
                ]
            })
        
        return careers[:3] if careers else [{
            "title": "Software Developer",
            "match": "80",
            "details": ["Start with programming basics", "Build portfolio projects", "Apply to entry-level roles"]
        }]
    
    def _get_default_skills(self, profile):
        return [
            {"skill": "Problem Solving & DSA", "details": ["Critical for interviews", "Practice on LeetCode/HackerRank", "2-3 months of daily practice"]},
            {"skill": "Version Control (Git)", "details": ["Essential for all developers", "Learn on GitHub", "1 week to basics"]},
            {"skill": "Full Stack Development", "details": ["High demand skill", "MERN or MEAN stack", "3-4 months to proficiency"]}
        ]
    
    def _get_default_certs(self, profile):
        return [
            {"name": "AWS Cloud Practitioner", "details": ["Industry-recognized certification", "Platform: AWS Training", "Duration: 1-2 months", "Cost: $100"]},
            {"name": "Google Data Analytics", "details": ["Beginner-friendly", "Platform: Coursera", "6 months program", "Free to audit"]}
        ]
    
    def _get_default_projects(self, profile):
        interests = profile.get('interests', ['Software'])
        return [
            {"name": f"{interests[0]} Portfolio Project", "details": ["Showcase your skills", "3-4 weeks timeline", "Deploy on GitHub Pages", "Add to resume"]},
            {"name": "Full Stack Application", "details": ["End-to-end project", "Use modern tech stack", "6-8 weeks", "Real-world problem solving"]}
        ]
    
    def _get_default_roadmap(self, profile):
        return {
            "Month 1": ["Learn core technologies", "Complete 2 mini projects", "Join tech communities"],
            "Month 2": ["Build main portfolio project", "Practice DSA daily", "Network on LinkedIn"],
            "Month 3": ["Complete certifications", "Polish resume", "Start applying to jobs"],
            "Month 4": ["Interview preparation", "Mock interviews", "Keep building projects"],
            "Month 5": ["Active job search", "Follow up applications", "Expand network"],
            "Month 6": ["Negotiate offers", "Prepare for onboarding", "Keep learning"]
        }
    
    def _get_default_advice(self, profile):
        return f"Based on your {profile.get('education')} background and interest in {', '.join(profile.get('interests', ['technology'])[:2])}, focus on building practical projects that solve real problems. Don't wait for perfection - start applying and learning simultaneously."
    
    def _fallback_analysis(self, profile):
        return {
            "career_matches": self._get_default_careers(profile),
            "missing_skills": self._get_default_skills(profile),
            "certifications": self._get_default_certs(profile),
            "projects": self._get_default_projects(profile),
            "roadmap": self._get_default_roadmap(profile),
            "job_search": {
                "Target Companies": "Research companies in your target industry",
                "Application Tips": "Tailor resume for each application",
                "Networking": "Connect with professionals on LinkedIn"
            },
            "final_advice": self._get_default_advice(profile),
            "is_personalized": True
        }

agent = CareerAgent()
user_sessions = {}

@app.get("/")
async def root():
    return {"status": "active", "version": "5.1.0"}

@app.get("/questions")
async def get_questions():
    return {"total": len(QUESTIONS), "questions": QUESTIONS}

@app.post("/answer")
async def submit_answer(ans: QuestionAnswer):
    sid = ans.session_id or f"s{len(user_sessions)}_{datetime.now().strftime('%H%M%S')}"
    
    if sid not in user_sessions:
        user_sessions[sid] = {"answers": {}, "created": datetime.now().isoformat()}
    
    # Handle custom answer for "Other" option
    final_answers = []
    for answer in ans.answers:
        if answer == "Other (Specify)" and ans.custom_answer:
            final_answers.append(f"Other: {ans.custom_answer}")
        else:
            final_answers.append(answer)
    
    user_sessions[sid]["answers"][f"q{ans.question_id}"] = {
        "question": QUESTIONS[ans.question_id-1]["question"],
        "answers": final_answers
    }
    
    return {"success": True, "session_id": sid, "progress": f"{len(user_sessions[sid]['answers'])}/{len(QUESTIONS)}"}

@app.post("/chat")
async def chat(msg: ChatMessage):
    if msg.session_id not in user_sessions:
        raise HTTPException(404, "Complete questions first")
    
    answers = user_sessions[msg.session_id]["answers"]
    
    profile = {
        "education": answers.get("q1", {}).get("answers", ["Not specified"])[0],
        "interests": answers.get("q2", {}).get("answers", []),
        "skills": answers.get("q3", {}).get("answers", []),
        "experience": answers.get("q4", {}).get("answers", ["No experience"])[0],
        "goals": answers.get("q5", {}).get("answers", []),
        "time_commitment": answers.get("q6", {}).get("answers", ["5-10 hours"])[0],
        "learning_style": answers.get("q7", {}).get("answers", ["Video tutorials"])[0],
        "preferred_industry": ", ".join(answers.get("q8", {}).get("answers", ["Technology"])),
        "salary_expectation": answers.get("q9", {}).get("answers", ["₹3-6 LPA"])[0],
        "relocation_willingness": answers.get("q10", {}).get("answers", ["Open"])[0]
    }
    
    result = await agent.chat(msg.session_id, msg.message, profile)
    
    # Mark that analysis needs regeneration if it exists
    needs_regen = False
    if "analysis" in user_sessions[msg.session_id]:
        user_sessions[msg.session_id]["needs_regeneration"] = True
        needs_regen = True
    
    return {
        "success": result["success"], 
        "response": result["response"],
        "needs_regeneration": needs_regen
    }

@app.post("/analyze")
async def analyze(data: dict):
    session_id = data.get("session_id")
    if session_id not in user_sessions:
        raise HTTPException(404, "Session not found")
    
    answers = user_sessions[session_id]["answers"]
    
    profile = {
        "education": answers.get("q1", {}).get("answers", ["Not specified"])[0],
        "interests": answers.get("q2", {}).get("answers", []),
        "skills": answers.get("q3", {}).get("answers", []),
        "experience": answers.get("q4", {}).get("answers", ["No experience"])[0],
        "goals": answers.get("q5", {}).get("answers", []),
        "time_commitment": answers.get("q6", {}).get("answers", ["5-10 hours"])[0],
        "learning_style": answers.get("q7", {}).get("answers", ["Video tutorials"])[0],
        "preferred_industry": ", ".join(answers.get("q8", {}).get("answers", ["Technology"])),
        "salary_expectation": answers.get("q9", {}).get("answers", ["₹3-6 LPA"])[0],
        "relocation_willingness": answers.get("q10", {}).get("answers", ["Open"])[0]
    }
    
    chat_history = agent.chat_histories.get(session_id, [])
    analysis = await agent.generate_analysis(session_id, profile, chat_history)
    
    user_sessions[session_id]["analysis"] = analysis
    user_sessions[session_id]["needs_regeneration"] = False
    return analysis

if __name__ == "__main__":
    print("🎯 AI Career Guidance - Personalized Analysis System v5.1")
    print("📍 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)