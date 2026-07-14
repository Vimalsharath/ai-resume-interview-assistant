import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pypdf import PdfReader


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=api_key
)


def extract_resume(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text



resume_text = extract_resume("resumes/resume.pdf")


prompt = f"""
You are an AI Interview Assistant.

Analyze this resume:

{resume_text}


Generate:

1. Candidate skills
2. Possible interview questions
3. Technical questions
4. HR questions
5. Areas to improve
"""


response = llm.invoke(prompt)


print(response.content)