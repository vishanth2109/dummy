# ---------- IMPORTS ----------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
import os
from dotenv import load_dotenv
import ast

# ---------- LOAD ENV ----------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# ============================================================
# 1️⃣ ATS SIMILARITY SCORE (TF-IDF)
# ============================================================

def calculate_similarity(resume_text, job_desc):
    """
    Calculate ATS similarity score between resume and job description.
    Returns score in percentage (0-100).
    """
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return round(similarity[0][0] * 100, 2)
    except Exception:
        return 0.0


# ============================================================
# 2️⃣ GEMINI AI RESUME ANALYSIS
# ============================================================

def analyze_resume(resume_text, job_desc):
    """
    Uses Gemini 2.5 Flash to analyze resume against job description.
    """

    prompt = f"""
You are an expert ATS Resume Analyzer.

Compare this Resume and Job Description carefully.

Resume:
{resume_text}

Job Description:
{job_desc}

Provide a structured response with:

1. ATS Score (0-100)
2. Missing Skills
3. Strengths
4. Improvement Suggestions
5. Keywords to Add
6. Final Recommendation (Hire / Improve / Not Suitable)

Be clear and professional.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"


# ============================================================
# 3️⃣ 🔥 AI-BASED SKILL EXTRACTION
# ============================================================

def extract_skills_with_ai(text):
    """
    Uses Gemini to extract important technical and soft skills from text.
    Returns a Python list of skills.
    """

    prompt = f"""
Extract only the important technical and soft skills from the following text.

Return ONLY a valid Python list.
Example:
["Python", "SQL", "AWS", "Communication"]

Text:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        skills_text = response.text.strip()

        # Convert string list to actual Python list
        skills_list = ast.literal_eval(skills_text)

        # Normalize to lowercase
        return [skill.lower() for skill in skills_list]

    except Exception:
        return []


# ============================================================
# 4️⃣ SKILL GAP DETECTION (AI-POWERED)
# ============================================================

def get_skill_gap(resume_text, job_desc):
    """
    Compare resume skills vs job description skills using AI extraction.
    Returns:
        job_skills
        resume_skills
        missing_skills
    """

    resume_skills = extract_skills_with_ai(resume_text)
    job_skills = extract_skills_with_ai(job_desc)

    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    return job_skills, resume_skills, missing_skills