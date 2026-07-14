import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from ocr_reader import extract_text_from_pdf


# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# Initialize Groq model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=api_key
)


# Read resume
resume_text = extract_text_from_pdf(
    "resumes/resume.pdf"
)


print("==============================")
print("AI INTERVIEW ASSISTANT")
print("==============================")

print("\nResume analyzed successfully!")


# Generate first question

question_prompt = f"""

You are a technical interviewer.

Based on this resume:

{resume_text}


Ask one important technical interview question.

Only output the question.
"""


question = llm.invoke(question_prompt)


print("\nInterviewer:")
print(question.content)


# User answer

answer = input("\nYour Answer: ")


# Evaluate answer

evaluation_prompt = f"""

You are an expert interviewer.

Resume:
{resume_text}


Interview Question:
{question.content}


Candidate Answer:
{answer}


Evaluate the answer.

Give:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Better answer suggestion

"""


feedback = llm.invoke(evaluation_prompt)


print("\n==============================")
print("AI FEEDBACK")
print("==============================")

print(feedback.content)