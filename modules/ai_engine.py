import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


api_key = os.getenv(
    "GROQ_API_KEY"
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=api_key
)



def analyze_resume(resume_text):


    prompt = f"""

You are an expert technical interviewer.

Analyze this candidate resume:

----------------------
{resume_text}
----------------------


Generate a detailed interview preparation report.


Include:


1. Candidate Profile Summary


2. Technical Skills Identified


3. Technical Interview Questions

Generate 10 questions based on:
- Projects
- Programming skills
- AI/ML knowledge


4. HR Interview Questions

Generate 5 questions.


5. Important Topics To Prepare


6. Resume Improvement Suggestions


7. Expected Interview Difficulty Level


"""


    response = llm.invoke(
        prompt
    )


    return response.content