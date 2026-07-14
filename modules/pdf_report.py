from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet



def create_pdf_report(
        username,
        questions,
        answers,
        feedbacks,
        scores
):


    filename = f"{username}_AI_Interview_Report.pdf"


    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()


    content = []



    content.append(

        Paragraph(
            "AI Interview Assistant Report",
            styles["Title"]
        )

    )


    content.append(
        Spacer(1,20)
    )



    content.append(

        Paragraph(
            f"Candidate Name: {username}",
            styles["Normal"]
        )

    )


    content.append(
        Spacer(1,20)
    )



    total_questions = len(questions)



    for i in range(total_questions):


        question = questions[i]


        if i < len(answers):

            answer = answers[i]

        else:

            answer = "Not Answered"



        if i < len(feedbacks):

            feedback = feedbacks[i]

        else:

            feedback = "No Feedback"



        if i < len(scores):

            score = scores[i]

        else:

            score = 0




        content.append(

            Paragraph(

                f"Question {i+1}: {question}",

                styles["Heading3"]

            )

        )


        content.append(

            Paragraph(

                f"Answer: {answer}",

                styles["Normal"]

            )

        )


        content.append(

            Paragraph(

                f"Feedback: {feedback}",

                styles["Normal"]

            )

        )


        content.append(

            Paragraph(

                f"Score: {score}/10",

                styles["Normal"]

            )

        )


        content.append(
            Spacer(1,20)
        )





    if len(scores) > 0:


        average = sum(scores) / len(scores)


        content.append(

            Paragraph(

                f"Final Average Score: {round(average,2)}/10",

                styles["Title"]

            )

        )



    doc.build(
        content
    )


    return filename