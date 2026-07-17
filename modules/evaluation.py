import re

from modules.ai_engine import llm
from modules.rag import retrieve_resume


def generate_questions(resume_text):
    context = retrieve_resume("skills projects education experience certifications")

    if not context.strip():
        return [
            "Tell me about yourself and your background.",
            "Describe a project you are most proud of.",
            "How do you approach problem-solving in a new technical challenge?"
        ]

    prompt = f"""
You are an expert technical interviewer.
Candidate Resume:
{context}

Generate exactly 12 interview questions tailored to the resume. Make sure the questions cover:
- Technical depth
- Projects and experience
- Behavioral and HR areas
- Scenario-based discussion

Return only questions, one per line.
"""

    try:
        response = llm.invoke(prompt)
        text = response.content
    except Exception:
        text = ""

    questions = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            parts = line.split(".", 1)
            if len(parts) > 1:
                questions.append(parts[1].strip())
        elif line.startswith("-"):
            questions.append(line[1:].strip())
        elif line not in questions:
            questions.append(line)

    return questions[:12]


# =====================================
# EVALUATE ANSWER
# =====================================

def evaluate_answer(question, answer, resume_text):
    context = retrieve_resume(question)

    prompt = f"""
You are an expert technical interviewer.
Candidate Resume:
{context}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate answer. Keep it practical and concise.
Return exactly in this format:
Score: X/10
Strengths:
- ...
Weakness:
- ...
Suggestions:
- ...
"""

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as exc:
        return f"Score: 0/10\nStrengths:\n- None\nWeakness:\n- Evaluation unavailable\nSuggestions:\n- {exc}"

# =====================================
# EXTRACT SCORE FROM AI FEEDBACK
# =====================================

def extract_score(feedback):

    match = re.search(
        r"Score:\s*(\d+)/10",
        feedback
    )

    if match:

        return int(
            match.group(1)
        )

    return 0