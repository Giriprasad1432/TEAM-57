from fastapi import FastAPI

app = FastAPI(title="Personalized Career Guidance Using GenAI")

# -------------------------------
# Health check API
# -------------------------------
@app.get("/")
def home():
    return {"status": "Backend is running successfully"}

# -------------------------------
# Career Analysis API
# -------------------------------
@app.post("/analyze")
def analyze(resume: str, interest: str):
    resume = resume.lower()
    interest = interest.lower()

    # Data Analyst path
    if "python" in resume and "data" in interest:
        return {
            "career": "Data Analyst",
            "missing_skills": ["Statistics", "Power BI"],
            "recommended_certifications": ["Google Data Analytics", "IBM Data Analyst"],
            "recommended_project": "Sales Data Dashboard"
        }

    # AI / ML path
    if "python" in resume and "machine learning" in resume:
        return {
            "career": "AI Engineer",
            "missing_skills": ["Deep Learning", "MLOps"],
            "recommended_certifications": ["Deep Learning Specialization"],
            "recommended_project": "AI Chatbot"
        }

    # Default Software Developer path
    return {
        "career": "Software Developer",
        "missing_skills": ["DSA", "System Design"],
        "recommended_certifications": ["Java/Python Full Stack"],
        "recommended_project": "Task Management Application"
    }