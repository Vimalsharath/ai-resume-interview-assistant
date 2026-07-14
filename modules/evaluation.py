from modules.ai_engine import llm
import re



# =====================================
# GENERATE INTERVIEW QUESTIONS
# =====================================

def generate_questions(resume_text):


    prompt = f"""

You are an expert technical interviewer.


Analyze this candidate resume:


{resume_text}



Generate exactly 15 interview questions.


Format:


Technical Questions:

1. Question
2. Question
3. Question
4. Question
5. Question


Project Questions:

6. Question
7. Question
8. Question
9. Question
10. Question


HR Questions:

11. Question
12. Question
13. Question
14. Question
15. Question



Return only questions.


"""


    response = llm.invoke(
        prompt
    )


    text = response.content


    questions = []



    for line in text.split("\n"):


        line = line.strip()



        if line:


            if line[0].isdigit():


                parts = line.split(
                    ".",
                    1
                )


                if len(parts) > 1:


                    questions.append(

                        parts[1].strip()

                    )



    return questions





# =====================================
# EVALUATE ANSWER
# =====================================


def evaluate_answer(
        question,
        answer,
        resume_text
):


    prompt = f"""

You are an expert technical interviewer.



Candidate Resume:

{resume_text}



Interview Question:

{question}



Candidate Answer:

{answer}




Evaluate the candidate answer.



Give response exactly in this format:


Score: X/10


Strengths:
- Mention good points


Weakness:
- Mention missing points


Suggestions:
- How to improve answer



"""


    response = llm.invoke(
        prompt
    )


    feedback = response.content


    return feedback





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