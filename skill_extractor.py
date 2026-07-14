def extract_skills(text):

    skills_database = [
        "Python",
        "Java",
        "C",
        "C++",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "OpenCV",
        "Scikit-learn",
        "NumPy",
        "Pandas",
        "SQL",
        "MySQL",
        "MongoDB",
        "Git",
        "GitHub",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "FastAPI",
        "Flask",
        "Django"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_database:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills