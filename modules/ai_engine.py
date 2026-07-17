import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=api_key,
)


def analyze_resume(resume_text):
    if not resume_text or not str(resume_text).strip():
        return "Resume text is empty. Please upload a valid resume first."

    prompt = f"""
You are an expert technical interviewer and hiring coach.
Analyze this resume and produce a concise but actionable interview preparation report.

Resume:
{resume_text}

Return a report with these sections:
1. Candidate Profile Summary
2. Key Skills Identified
3. Suggested Interview Topics
4. Technical Questions to Practice
5. HR and Behavioral Questions to Practice
6. Resume Improvement Suggestions
7. Expected Interview Difficulty
"""

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as exc:
        return f"AI analysis could not be completed: {exc}"