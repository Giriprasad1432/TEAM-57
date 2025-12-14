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

app = FastAPI(title="AI Career Guidance System", version="6.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionAnswer(BaseModel):
    question_id: str
    answers: List[str]
    session_id: Optional[str] = None
    custom_answer: Optional[str] = None

class ChatMessage(BaseModel):
    session_id: str
    message: str

# Dynamic Question Tree
QUESTION_TREE = {
    "start": {
        "id": "start",
        "question": "What is your current educational level?",
        "type": "single",
        "options": [
            "10th Standard (Currently Studying)",
            "10th Pass (Completed)",
            "12th Standard (Currently Studying)",
            "12th Pass (Completed)",
            "Undergraduate (Currently Studying)",
            "Undergraduate Degree Completed",
            "Postgraduate (Currently Studying)",
            "Postgraduate Degree Completed",
            "Working Professional",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "10th Standard (Currently Studying)": "career_interest_10th",
            "10th Pass (Completed)": "career_interest_10th",
            "12th Standard (Currently Studying)": "stream_12th",
            "12th Pass (Completed)": "career_interest_12th",
            "Undergraduate (Currently Studying)": "ug_field",
            "Undergraduate Degree Completed": "ug_completed_goal",
            "Postgraduate (Currently Studying)": "pg_field",
            "Postgraduate Degree Completed": "pg_completed_goal",
            "Working Professional": "work_experience",
            "Other (Specify)": "career_interest_general"
        }
    },
    
    "career_interest_10th": {
        "id": "career_interest_10th",
        "question": "Which field interests you the most for your future career?",
        "type": "single",
        "options": [
            "Science & Engineering (PCM)",
            "Medical & Healthcare (PCB)",
            "Commerce & Business (Accounting, Finance)",
            "Arts & Humanities (Literature, History, Psychology)",
            "Computer Science & Technology",
            "Creative Fields (Design, Music, Arts)",
            "Sports & Fitness",
            "Vocational/Technical Skills",
            "Not Sure Yet"
        ],
        "next_question_logic": {
            "Science & Engineering (PCM)": "engineering_interest",
            "Medical & Healthcare (PCB)": "medical_interest",
            "Commerce & Business (Accounting, Finance)": "commerce_interest",
            "Arts & Humanities (Literature, History, Psychology)": "arts_interest",
            "Computer Science & Technology": "tech_interest_school",
            "Creative Fields (Design, Music, Arts)": "creative_interest",
            "Sports & Fitness": "sports_interest",
            "Vocational/Technical Skills": "vocational_interest",
            "Not Sure Yet": "learning_style"
        }
    },
    
    "stream_12th": {
        "id": "stream_12th",
        "question": "Which stream are you studying in 12th?",
        "type": "single",
        "options": [
            "Science (PCM - Physics, Chemistry, Maths)",
            "Science (PCB - Physics, Chemistry, Biology)",
            "Science (PCMB - All subjects)",
            "Commerce",
            "Arts/Humanities",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "Science (PCM - Physics, Chemistry, Maths)": "engineering_interest",
            "Science (PCB - Physics, Chemistry, Biology)": "medical_interest",
            "Science (PCMB - All subjects)": "pcmb_preference",
            "Commerce": "commerce_interest",
            "Arts/Humanities": "arts_interest",
            "Other (Specify)": "career_interest_general"
        }
    },
    
    "pcmb_preference": {
        "id": "pcmb_preference",
        "question": "Since you have both Maths and Biology, which field interests you more?",
        "type": "single",
        "options": [
            "Engineering & Technology (Maths-focused)",
            "Medical & Healthcare (Biology-focused)",
            "Both equally - Want to explore options",
            "Neither - Considering other fields"
        ],
        "next_question_logic": {
            "Engineering & Technology (Maths-focused)": "engineering_interest",
            "Medical & Healthcare (Biology-focused)": "medical_interest",
            "Both equally - Want to explore options": "tech_or_medical_combined",
            "Neither - Considering other fields": "career_interest_general"
        }
    },
    
    "engineering_interest": {
        "id": "engineering_interest",
        "question": "Which engineering/technology field excites you? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Computer Science & Software Development",
            "Artificial Intelligence & Machine Learning",
            "Mechanical Engineering",
            "Civil Engineering & Architecture",
            "Electrical & Electronics Engineering",
            "Aerospace Engineering",
            "Chemical Engineering",
            "Biotechnology Engineering",
            "Robotics & Automation",
            "Data Science & Analytics",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "technical_skills"
        }
    },
    
    "medical_interest": {
        "id": "medical_interest",
        "question": "Which medical/healthcare field interests you most? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "MBBS (Doctor)",
            "BDS (Dentistry)",
            "BAMS (Ayurveda)",
            "BHMS (Homeopathy)",
            "B.Pharm (Pharmacy)",
            "Nursing (B.Sc Nursing)",
            "Physiotherapy (BPT)",
            "Medical Lab Technology",
            "Veterinary Science",
            "Public Health",
            "Biotechnology (Medical focus)",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "medical_preparation"
        }
    },
    
    "medical_preparation": {
        "id": "medical_preparation",
        "question": "Are you preparing for medical entrance exams?",
        "type": "single",
        "options": [
            "Yes, preparing for NEET",
            "Yes, preparing for other medical exams",
            "Planning to start preparation",
            "Not preparing - looking for alternatives",
            "Already cleared - looking for college guidance"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "commerce_interest": {
        "id": "commerce_interest",
        "question": "Which commerce career path interests you? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Chartered Accountancy (CA)",
            "Company Secretary (CS)",
            "Cost & Management Accountant (CMA)",
            "Bachelor of Commerce (B.Com)",
            "Business Administration (BBA/MBA)",
            "Banking & Finance",
            "Stock Market & Investment",
            "Economics",
            "Actuarial Science",
            "Digital Marketing & E-commerce",
            "Entrepreneurship/Startup",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "commerce_skills"
        }
    },
    
    "commerce_skills": {
        "id": "commerce_skills",
        "question": "What skills do you currently have or want to develop?",
        "type": "multiple",
        "options": [
            "Accounting & Bookkeeping",
            "Financial Analysis",
            "MS Excel & Data Analysis",
            "Taxation",
            "Business Communication",
            "Digital Marketing",
            "Stock Market Analysis",
            "Business Planning",
            "No specific skills yet"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "arts_interest": {
        "id": "arts_interest",
        "question": "Which arts/humanities field interests you? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Psychology",
            "Sociology",
            "Literature & Languages",
            "History & Archaeology",
            "Political Science & Law",
            "Journalism & Mass Communication",
            "Teaching & Education",
            "Social Work",
            "Philosophy",
            "Hotel Management & Tourism",
            "Fashion & Design",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "arts_skills"
        }
    },
    
    "arts_skills": {
        "id": "arts_skills",
        "question": "What are your strengths or skills?",
        "type": "multiple",
        "options": [
            "Writing & Communication",
            "Public Speaking",
            "Research & Analysis",
            "Creative Thinking",
            "Languages (English, Hindi, others)",
            "Teaching & Mentoring",
            "Social Media & Content Creation",
            "Art & Design",
            "No specific skills yet"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "tech_interest_school": {
        "id": "tech_interest_school",
        "question": "What specific technology areas interest you? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "App Development (Android/iOS)",
            "Game Development",
            "Website Development",
            "Coding/Programming",
            "Artificial Intelligence",
            "Cybersecurity",
            "Robotics",
            "3D Design & Animation",
            "Video Editing",
            "Graphic Design",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "technical_skills"
        }
    },
    
    "creative_interest": {
        "id": "creative_interest",
        "question": "Which creative field attracts you most? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Graphic Design",
            "UI/UX Design",
            "Fashion Design",
            "Interior Design",
            "Music Production",
            "Photography & Videography",
            "Animation & VFX",
            "Fine Arts (Painting, Sculpture)",
            "Content Creation (YouTube, Instagram)",
            "Writing (Creative, Technical)",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "creative_skills"
        }
    },
    
    "creative_skills": {
        "id": "creative_skills",
        "question": "What creative tools or skills do you know?",
        "type": "multiple",
        "options": [
            "Adobe Photoshop",
            "Adobe Illustrator",
            "Figma/Adobe XD",
            "Video Editing (Premiere, Final Cut)",
            "3D Software (Blender, Maya)",
            "Music Software (FL Studio, Ableton)",
            "Photography equipment",
            "Writing & Storytelling",
            "Social Media Management",
            "No tools yet - want to learn"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "sports_interest": {
        "id": "sports_interest",
        "question": "Which sports/fitness career interests you?",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Professional Athlete",
            "Sports Coaching",
            "Physical Education Teacher",
            "Fitness Trainer/Gym Instructor",
            "Yoga Instructor",
            "Sports Management",
            "Physiotherapy",
            "Nutritionist/Dietitian",
            "Sports Journalism",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "vocational_interest": {
        "id": "vocational_interest",
        "question": "Which vocational/technical skill interests you?",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Electrician",
            "Plumber",
            "Carpenter",
            "Mechanic (Auto/Bike)",
            "Welding",
            "Electronics Repair",
            "Computer Hardware & Networking",
            "Mobile Repair",
            "Beauty & Cosmetology",
            "Culinary Arts (Chef/Baker)",
            "Tailoring & Fashion",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "career_interest_12th": {
        "id": "career_interest_12th",
        "question": "What do you want to do after 12th?",
        "type": "single",
        "options": [
            "Engineering (B.Tech/B.E.)",
            "Medical (MBBS/BDS/etc.)",
            "Bachelor of Science (B.Sc)",
            "Bachelor of Commerce (B.Com)",
            "Bachelor of Arts (B.A.)",
            "BCA (Computer Applications)",
            "Law (LLB)",
            "Design (Fashion/Interior/Graphics)",
            "Hotel Management",
            "Get a job/Skill training",
            "Start own business",
            "Not decided yet"
        ],
        "next_question_logic": {
            "Engineering (B.Tech/B.E.)": "engineering_interest",
            "Medical (MBBS/BDS/etc.)": "medical_interest",
            "Bachelor of Science (B.Sc)": "bsc_specialization",
            "Bachelor of Commerce (B.Com)": "commerce_interest",
            "Bachelor of Arts (B.A.)": "arts_interest",
            "BCA (Computer Applications)": "tech_interest_ug",
            "Law (LLB)": "law_interest",
            "Design (Fashion/Interior/Graphics)": "creative_interest",
            "Hotel Management": "hospitality_interest",
            "Get a job/Skill training": "job_skills",
            "Start own business": "entrepreneurship_interest",
            "Not decided yet": "career_interest_general"
        }
    },
    
    "ug_field": {
        "id": "ug_field",
        "question": "What are you studying in your undergraduate degree?",
        "type": "single",
        "options": [
            "Engineering (B.Tech/B.E.)",
            "Computer Applications (BCA/B.Sc CS)",
            "Commerce (B.Com)",
            "Science (B.Sc)",
            "Arts/Humanities (B.A.)",
            "Medical/Healthcare",
            "Design/Creative field",
            "Management (BBA)",
            "Law",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "Engineering (B.Tech/B.E.)": "engineering_branch",
            "Computer Applications (BCA/B.Sc CS)": "tech_interest_ug",
            "Commerce (B.Com)": "commerce_career_ug",
            "Science (B.Sc)": "bsc_specialization",
            "Arts/Humanities (B.A.)": "arts_career_ug",
            "Medical/Healthcare": "medical_career_ug",
            "Design/Creative field": "creative_career_ug",
            "Management (BBA)": "management_interest",
            "Law": "law_career",
            "Other (Specify)": "career_goal_ug"
        }
    },
    
    "engineering_branch": {
        "id": "engineering_branch",
        "question": "Which engineering branch are you in?",
        "type": "single",
        "options": [
            "Computer Science/IT",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical/Electronics (ECE/EEE)",
            "Chemical Engineering",
            "Aerospace Engineering",
            "Biotechnology",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "default": "technical_skills"
        }
    },
    
    "tech_interest_ug": {
        "id": "tech_interest_ug",
        "question": "Which tech career path interests you? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Software Development",
            "Web Development (Frontend/Backend/Full Stack)",
            "Mobile App Development",
            "Data Science & Analytics",
            "Artificial Intelligence & ML",
            "Cloud Computing (AWS/Azure/GCP)",
            "Cybersecurity",
            "DevOps",
            "UI/UX Design",
            "Game Development",
            "Blockchain Technology",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "technical_skills"
        }
    },
    
    "technical_skills": {
        "id": "technical_skills",
        "question": "What technical skills do you currently have?",
        "type": "multiple",
        "options": [
            "Python",
            "Java",
            "C/C++",
            "JavaScript",
            "HTML/CSS",
            "SQL/Databases",
            "Git/GitHub",
            "Data Structures & Algorithms",
            "Web Frameworks (React/Node.js/Django)",
            "Mobile Development (Android/iOS)",
            "Machine Learning basics",
            "Cloud Platforms (AWS/Azure)",
            "No technical skills yet"
        ],
        "next_question_logic": {
            "default": "experience_level"
        }
    },
    
    "bsc_specialization": {
        "id": "bsc_specialization",
        "question": "What is your B.Sc specialization or interest?",
        "type": "single",
        "options": [
            "Physics",
            "Chemistry",
            "Mathematics",
            "Biology/Zoology/Botany",
            "Computer Science",
            "Data Science/Statistics",
            "Environmental Science",
            "Biotechnology",
            "Microbiology",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "Computer Science": "tech_interest_ug",
            "Data Science/Statistics": "data_science_interest",
            "default": "science_career"
        }
    },
    
    "ug_completed_goal": {
        "id": "ug_completed_goal",
        "question": "What is your main goal now after completing graduation?",
        "type": "single",
        "options": [
            "Get a job in my field",
            "Switch to a different field",
            "Pursue higher studies (Masters/MBA)",
            "Prepare for competitive exams (UPSC/Banking/SSC)",
            "Start own business/startup",
            "Learn new skills/upskill",
            "Looking for career guidance",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "Get a job in my field": "job_search_focus",
            "Switch to a different field": "career_change_interest",
            "Pursue higher studies (Masters/MBA)": "higher_studies_interest",
            "Prepare for competitive exams (UPSC/Banking/SSC)": "exam_preparation",
            "Start own business/startup": "entrepreneurship_interest",
            "Learn new skills/upskill": "upskill_interest",
            "Looking for career guidance": "career_interest_general",
            "Other (Specify)": "career_interest_general"
        }
    },
    
    "work_experience": {
        "id": "work_experience",
        "question": "How much professional experience do you have?",
        "type": "single",
        "options": [
            "Less than 1 year",
            "1-2 years",
            "2-5 years",
            "5-10 years",
            "10+ years"
        ],
        "next_question_logic": {
            "default": "career_goal_professional"
        }
    },
    
    "career_goal_professional": {
        "id": "career_goal_professional",
        "question": "What is your current career goal?",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Get promoted in current company",
            "Switch to better paying job",
            "Change career field entirely",
            "Move to managerial position",
            "Learn new technologies/skills",
            "Work internationally/relocate",
            "Start freelancing",
            "Start own business",
            "Achieve work-life balance",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "default": "current_field_professional"
        }
    },
    
    "current_field_professional": {
        "id": "current_field_professional",
        "question": "Which field/industry are you currently working in?",
        "type": "single",
        "options": [
            "Software Development/IT",
            "Data Science/Analytics",
            "Finance/Banking",
            "Marketing/Sales",
            "Healthcare",
            "Education",
            "Manufacturing",
            "E-commerce/Retail",
            "Government/Public Sector",
            "Consulting",
            "Other (Specify)"
        ],
        "next_question_logic": {
            "Software Development/IT": "tech_skills_professional",
            "Data Science/Analytics": "data_skills_professional",
            "default": "professional_skills"
        }
    },
    
    "experience_level": {
        "id": "experience_level",
        "question": "What is your experience level?",
        "type": "single",
        "options": [
            "Complete beginner (Student/Fresher)",
            "Done some projects/internships",
            "0-1 year professional experience",
            "1-3 years experience",
            "3+ years experience"
        ],
        "next_question_logic": {
            "default": "career_goals"
        }
    },
    
    "career_goals": {
        "id": "career_goals",
        "question": "What are your primary career goals? (Select all that apply)",
        "type": "multiple",
        "options": [
            "Get first job in tech/my field",
            "Switch to better paying job",
            "Learn skills for career change",
            "Get promotion in current role",
            "Build strong portfolio",
            "Start freelancing",
            "Work remotely/internationally",
            "Start own business/startup",
            "Achieve work-life balance",
            "Prepare for higher studies"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "study_time": {
        "id": "study_time",
        "question": "How much time can you dedicate to learning/preparation weekly?",
        "type": "single",
        "options": [
            "Less than 5 hours",
            "5-10 hours",
            "10-20 hours",
            "20-30 hours",
            "30+ hours (Full-time focus)",
            "Flexible - depends on schedule"
        ],
        "next_question_logic": {
            "default": "learning_style"
        }
    },
    
    "learning_style": {
        "id": "learning_style",
        "question": "What is your preferred learning style?",
        "type": "multiple",
        "options": [
            "Video tutorials (YouTube/Udemy)",
            "Online courses with certificates",
            "Books & documentation",
            "Hands-on projects & practice",
            "Bootcamps/Classroom training",
            "Mentorship/1-on-1 guidance",
            "Self-paced learning",
            "Group study/peer learning"
        ],
        "next_question_logic": {
            "default": "budget"
        }
    },
    
    "budget": {
        "id": "budget",
        "question": "What is your budget for courses/learning resources?",
        "type": "single",
        "options": [
            "Free resources only",
            "Up to ₹5,000",
            "₹5,000 - ₹20,000",
            "₹20,000 - ₹50,000",
            "₹50,000+",
            "Willing to invest for quality education"
        ],
        "next_question_logic": {
            "default": "location_preference"
        }
    },
    
    "location_preference": {
        "id": "location_preference",
        "question": "What is your location/work preference?",
        "type": "single",
        "options": [
            "Remote work only",
            "Hybrid (part office, part remote)",
            "Office-based in my city",
            "Willing to relocate anywhere in India",
            "Open to specific cities only",
            "Considering international opportunities",
            "Not applicable/Not decided yet"
        ],
        "next_question_logic": {
            "default": "end"
        }
    },
    
    # Additional specialized paths
    "career_interest_general": {
        "id": "career_interest_general",
        "question": "Which broad career area interests you most? (Select top 3)",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Technology & Software",
            "Healthcare & Medicine",
            "Business & Finance",
            "Creative & Design",
            "Education & Teaching",
            "Engineering & Manufacturing",
            "Government & Public Service",
            "Sales & Marketing",
            "Hospitality & Tourism",
            "Agriculture & Environment",
            "Sports & Fitness",
            "Not sure - need guidance"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    },
    
    "job_skills": {
        "id": "job_skills",
        "question": "What type of job skills do you want to learn?",
        "type": "multiple",
        "max_selections": 3,
        "options": [
            "Computer/IT skills",
            "Data Entry",
            "Accounting & Tally",
            "Digital Marketing",
            "Graphic Design",
            "Video Editing",
            "Language skills (English/others)",
            "Sales & Communication",
            "Customer Service",
            "Technical/Vocational skills",
            "Not sure yet"
        ],
        "next_question_logic": {
            "default": "study_time"
        }
    }
}

class CareerAgent:
    def __init__(self):
        self.name = "Career Coach Alex"
        self.chat_histories = {}
    
    def get_next_question(self, current_q_id: str, answer: List[str]) -> Optional[str]:
        """Determine next question based on current answer"""
        if current_q_id not in QUESTION_TREE:
            return None
        
        current_q = QUESTION_TREE[current_q_id]
        logic = current_q.get("next_question_logic", {})
        
        if not logic:
            return None
        
        # Check if answer matches specific logic
        for ans in answer:
            if ans in logic:
                next_q_id = logic[ans]
                return next_q_id if next_q_id != "end" else None
        
        # Use default if exists
        if "default" in logic:
            next_q_id = logic["default"]
            return next_q_id if next_q_id != "end" else None
        
        return None
    
    async def chat(self, sid: str, msg: str, profile: Dict) -> Dict:
        """Short, clear, relevant chat responses"""
        if sid not in self.chat_histories:
            self.chat_histories[sid] = []
        
        self.chat_histories[sid].append({"role": "user", "content": msg})
        
        # Build concise profile context
        profile_parts = []
        if profile.get('education'):
            profile_parts.append(f"Education: {profile['education']}")
        if profile.get('interests'):
            profile_parts.append(f"Interests: {', '.join(profile['interests'][:2])}")
        if profile.get('skills'):
            profile_parts.append(f"Skills: {', '.join(profile['skills'][:3])}")
        if profile.get('goals'):
            profile_parts.append(f"Goals: {', '.join(profile['goals'][:2])}")
        
        profile_context = '\n'.join(profile_parts) if profile_parts else "Profile being built..."
        
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
        except Exception as e:
            print(f"Chat error: {e}")
            return {"success": False, "response": "I'd suggest focusing on practical projects first. What specific area interests you most?"}
    
    async def generate_analysis(self, sid: str, profile: Dict, chat_history: List) -> Dict:
        """Generate comprehensive personalized analysis"""
        
        # Build detailed profile text
        profile_lines = []
        profile_lines.append(f"Education Level: {profile.get('education_level', 'Not specified')}")
        
        if profile.get('stream'):
            profile_lines.append(f"Academic Stream: {profile.get('stream')}")
        if profile.get('field'):
            profile_lines.append(f"Field of Study: {profile.get('field')}")
        if profile.get('interests'):
            profile_lines.append(f"Career Interests: {', '.join(profile.get('interests', []))}")
        if profile.get('skills'):
            profile_lines.append(f"Current Skills: {', '.join(profile.get('skills', []))}")
        if profile.get('experience'):
            profile_lines.append(f"Experience Level: {profile.get('experience')}")
        if profile.get('goals'):
            profile_lines.append(f"Career Goals: {', '.join(profile.get('goals', []))}")
        if profile.get('time_commitment'):
            profile_lines.append(f"Weekly Study Time: {profile.get('time_commitment')}")
        if profile.get('learning_style'):
            profile_lines.append(f"Learning Style: {', '.join(profile.get('learning_style', []))}")
        if profile.get('budget'):
            profile_lines.append(f"Budget: {profile.get('budget')}")
        if profile.get('location'):
            profile_lines.append(f"Location Preference: {profile.get('location')}")
        
        profile_text = "USER PROFILE:\n" + '\n'.join(profile_lines)
        
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
- Why it fits: [Reference their specific interests/skills/education]
- Entry Requirements: [What they need]
- Salary Range: [Realistic for their level]
- Next Steps: [Specific actions]

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
- Value: [How it helps]

🚀 PORTFOLIO PROJECTS
For each project (numbered 1-4):
- Project Name
- Technologies: [Match their field]
- Timeline: [Based on study time]
- What It Demonstrates
- Where to Showcase

🗺️ 6-MONTH ROADMAP
Month 1: [Focus area with 3 specific actions]
Month 2: [Next phase with 3 actions]
Month 3: [Skill building with 3 actions]
Month 4: [Project work with 3 actions]
Month 5: [Portfolio completion with 3 actions]
Month 6: [Goal achievement with 3 actions]

💼 ACTION PLAN
- Immediate Steps: [What to do this week]
- Resources: [Specific platforms/courses]
- Networking: [Where to connect]
- Application Strategy: [If job-seeking]

💡 PERSONALIZED ADVICE
[3-4 sentences addressing their specific situation, education level, and motivational guidance]

Make EVERYTHING specific to THIS user."""
        
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
        """Parse structured analysis - same as before"""
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
            elif "PORTFOLIO PROJECTS" in line or "PROJECTS" in line:
                current_section = "projects"
            elif "ROADMAP" in line:
                current_section = "roadmap"
            elif "ACTION PLAN" in line or "JOB SEARCH" in line:
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
                        for j in range(i+1, min(i+6, len(lines))):
                            if lines[j].strip().startswith(('-', '•', 'Why', 'Entry', 'Salary', 'Next')):
                                details.append(lines[j].strip().lstrip('-•').strip())
                        
                        result["career_matches"].append({
                            "title": title,
                            "match": match if match.isdigit() else "75",
                            "details": details[:5]
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
        return [{
            "title": "Explore Multiple Career Paths",
            "match": "80",
            "details": [
                f"Based on your {profile.get('education_level', 'current level')}",
                "Focus on building foundational skills",
                "Explore internships and projects",
                "Connect with professionals in your field"
            ]
        }]
    
    def _get_default_skills(self, profile):
        return [
            {"skill": "Communication Skills", "details": ["Essential for all careers", "Practice daily", "Join speaking clubs"]},
            {"skill": "Problem Solving", "details": ["Critical thinking", "Work on real projects", "Learn systematically"]},
            {"skill": "Digital Literacy", "details": ["Basic computer skills", "Online tools", "Essential for modern work"]}
        ]
    
    def _get_default_certs(self, profile):
        return [
            {"name": "Industry-Relevant Certification", "details": ["Research your field", "Check job requirements", "Invest in recognized certifications"]}
        ]
    
    def _get_default_projects(self, profile):
        return [
            {"name": "Portfolio Building Project", "details": ["Showcase your skills", "Document your work", "Share on LinkedIn/GitHub"]}
        ]
    
    def _get_default_roadmap(self, profile):
        return {
            "Month 1": ["Explore career options", "Learn foundational skills", "Connect with mentors"],
            "Month 2": ["Start skill development", "Work on small projects", "Build online presence"],
            "Month 3": ["Complete first major project", "Get feedback", "Refine skills"],
            "Month 4": ["Apply learning", "Network actively", "Seek opportunities"],
            "Month 5": ["Build portfolio", "Prepare applications", "Practice interviews"],
            "Month 6": ["Job search/Further study", "Follow up", "Keep learning"]
        }
    
    def _get_default_advice(self, profile):
        return f"Based on your profile, focus on consistent learning and practical application. Your journey is unique - embrace it!"
    
    def _fallback_analysis(self, profile):
        return {
            "career_matches": self._get_default_careers(profile),
            "missing_skills": self._get_default_skills(profile),
            "certifications": self._get_default_certs(profile),
            "projects": self._get_default_projects(profile),
            "roadmap": self._get_default_roadmap(profile),
            "job_search": {
                "Immediate Steps": "Research careers in your field",
                "Resources": "Use online learning platforms",
                "Networking": "Connect on LinkedIn"
            },
            "final_advice": self._get_default_advice(profile),
            "is_personalized": True
        }

agent = CareerAgent()
user_sessions = {}

@app.get("/")
async def root():
    return {"status": "active", "version": "6.0.0", "type": "dynamic"}

@app.get("/question/{question_id}")
async def get_question(question_id: str):
    """Get a specific question by ID"""
    if question_id in QUESTION_TREE:
        return {"question": QUESTION_TREE[question_id]}
    raise HTTPException(404, "Question not found")

@app.get("/start")
async def start_questionnaire():
    """Get the first question"""
    return {"question": QUESTION_TREE["start"]}

@app.post("/answer")
async def submit_answer(ans: QuestionAnswer):
    sid = ans.session_id or f"s{len(user_sessions)}_{datetime.now().strftime('%H%M%S')}"
    
    if sid not in user_sessions:
        user_sessions[sid] = {
            "answers": {},
            "created": datetime.now().isoformat(),
            "profile": {}
        }
    
    # Handle custom answer
    final_answers = []
    for answer in ans.answers:
        if answer == "Other (Specify)" and ans.custom_answer:
            final_answers.append(f"Other: {ans.custom_answer}")
        else:
            final_answers.append(answer)
    
    # Store answer
    q_data = QUESTION_TREE.get(ans.question_id, {})
    user_sessions[sid]["answers"][ans.question_id] = {
        "question": q_data.get("question", ""),
        "answers": final_answers
    }
    
    # Build profile progressively
    profile = user_sessions[sid]["profile"]
    
    if ans.question_id == "start":
        profile["education_level"] = final_answers[0]
    elif "stream" in ans.question_id or ans.question_id == "stream_12th":
        profile["stream"] = final_answers[0]
    elif "field" in ans.question_id or "branch" in ans.question_id:
        profile["field"] = final_answers[0]
    elif "interest" in ans.question_id:
        profile.setdefault("interests", []).extend(final_answers)
    elif "skill" in ans.question_id:
        profile.setdefault("skills", []).extend(final_answers)
    elif "experience" in ans.question_id:
        profile["experience"] = final_answers[0]
    elif "goal" in ans.question_id:
        profile.setdefault("goals", []).extend(final_answers)
    elif ans.question_id == "study_time":
        profile["time_commitment"] = final_answers[0]
    elif ans.question_id == "learning_style":
        profile["learning_style"] = final_answers
    elif ans.question_id == "budget":
        profile["budget"] = final_answers[0]
    elif ans.question_id == "location_preference":
        profile["location"] = final_answers[0]
    
    # Determine next question
    next_q_id = agent.get_next_question(ans.question_id, final_answers)
    
    if next_q_id and next_q_id in QUESTION_TREE:
        next_question = QUESTION_TREE[next_q_id]
        return {
            "success": True,
            "session_id": sid,
            "next_question": next_question,
            "completed": False
        }
    else:
        return {
            "success": True,
            "session_id": sid,
            "completed": True,
            "message": "Questionnaire completed! Ready for chat."
        }

@app.post("/chat")
async def chat(msg: ChatMessage):
    if msg.session_id not in user_sessions:
        raise HTTPException(404, "Complete questions first")
    
    profile = user_sessions[msg.session_id]["profile"]
    result = await agent.chat(msg.session_id, msg.message, profile)
    
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
    
    profile = user_sessions[session_id]["profile"]
    chat_history = agent.chat_histories.get(session_id, [])
    analysis = await agent.generate_analysis(session_id, profile, chat_history)
    
    user_sessions[session_id]["analysis"] = analysis
    user_sessions[session_id]["needs_regeneration"] = False
    return analysis

if __name__ == "__main__":
    print("🎯 AI Career Guidance - Dynamic Questionnaire System v6.0")
    print("📍 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)