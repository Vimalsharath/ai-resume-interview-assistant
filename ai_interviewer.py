import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from ocr_reader import extract_text_from_pdf


# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# Connect Groq model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=api_key
)


# Extract resume text
resume_text = extract_text_from_pdf(
    "resumes/resume.pdf"
)


prompt = f"""
You are an expert technical interviewer.

Analyze this resume:

-----------------
{resume_text}
-----------------


Generate:

1. Candidate skill summary

2. 10 technical interview questions
   based on the candidate projects and skills

3. 5 HR interview questions

4. Suggested answers for important questions

5. Areas where the candidate should improve
"""


response = llm.invoke(prompt)


print("==============================")
print("AI INTERVIEW ANALYSIS")
print("==============================")

print(response.content)