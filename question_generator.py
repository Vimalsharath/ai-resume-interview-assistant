QUESTION_BANK = {
    "Python": [
        "Explain the difference between List and Tuple.",
        "What is a Dictionary in Python?",
        "What are decorators in Python?"
    ],

    "Java": [
        "Explain OOP concepts.",
        "What is inheritance?",
        "Difference between Interface and Abstract class?"
    ],

    "TensorFlow": [
        "What is TensorFlow?",
        "Why do we use Keras?",
        "What is an Epoch?"
    ],

    "OpenCV": [
        "What is OpenCV?",
        "Why do we resize images?",
        "Difference between OpenCV and TensorFlow?"
    ],

    "Git": [
        "What is Git?",
        "Difference between Git and GitHub?",
        "What is a Git commit?"
    ]
}


def generate_questions(skills):

    questions = []

    for skill in skills:

        if skill in QUESTION_BANK:

            questions.extend(QUESTION_BANK[skill])

    return questions