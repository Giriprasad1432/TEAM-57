🎓 Personalized Career Guidance Using GenAI

📌 Problem Statement

Many students are confused about choosing the right career path due to lack of awareness about industry roles, required skills, and personal strengths. Existing guidance systems are generic and do not adapt to individual profiles.


---

💡 Proposed Solution

This project uses Generative AI (Google Gemini) to provide personalized career guidance through a structured 16-question checkbox-based questionnaire.

Based on the user’s selections, the system intelligently:

Understands interests and strengths

Maps suitable career paths

Identifies missing skills

Suggests certifications and projects

Generates interview questions



---

🧠 System Flow

1. User answers 16 multiple-choice (checkbox) questions


2. Selected options are converted into structured input


3. Gemini AI analyzes the responses


4. Personalized career recommendations are generated




---

📝 User Questionnaire (16 Questions)

Users can select one or more options for each question.

1. Areas of interest (Programming, Data, Business, Design, etc.)


2. Preferred activities (Problem-solving, Analysis, Creativity)


3. Known technical skills


4. Current education level


5. Preferred work style


6. Interest in data & numbers


7. Interest in coding


8. Preferred industry


9. Career priorities


10. Project experience


11. Core strengths


12. Learning style


13. Interview confidence


14. Long-term career vision


15. Willingness to upskill


16. Preferred role type




---

📥 Sample Input (Processed from User Answers)

{
  "interests": "Data Analytics, Problem Solving",
  "skills": "Python, SQL",
  "education": "Final Year Student",
  "preferences": "Data-oriented roles"
}


---

📤 Sample Output (AI-Generated)

{
  "Recommended Careers": [
    "Data Analyst",
    "Business Intelligence Analyst"
  ],
  "Missing Skills": [
    "Statistics",
    "Power BI",
    "Advanced SQL"
  ],
  "Recommended Certifications": [
    "Google Data Analytics",
    "IBM Data Analyst"
  ],
  "Suggested Projects": [
    "Sales Dashboard using Power BI",
    "Customer Churn Analysis"
  ],
  "Interview Questions": [
    "What is normalization in SQL?",
    "Explain supervised vs unsupervised learning",
    "How do you handle missing data?"
  ]
}


---

🚀 Key Features

16-question structured decision framework

Checkbox-based user interaction

AI-driven personalized analysis

Career mapping + skill gap detection

Interview preparation support



---

🛠 Technology Stack

Backend: Python, FastAPI

GenAI: Google Gemini 1.5

API Testing: Swagger UI

Version Control: Git & GitHub



---

📊 Innovation

Converts subjective career choices into AI-analyzed insights

Combines career guidance, learning roadmap, and interview prep

POC-level MVP designed for scalability



---

🌍 Impact

Helps students make informed career decisions

Reduces confusion and trial-and-error learning

Improves employability and confidence



---

📽 Demo

A 10-minute demo includes:

Problem explanation

Questionnaire flow

Backend working

AI-generated recommendations

Innovation & impact



---

👥 Team

Group-based hackathon project
All contributions tracked via GitHub commits.


---

📜 License

Developed for academic and hackathon purposes only.


---