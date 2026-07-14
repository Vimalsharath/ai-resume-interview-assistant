import streamlit as st
import os

# ==========================================
# DATABASE
# ==========================================

from modules.database import (
    create_tables,
    save_interview,
    get_history
)

# ==========================================
# AUTH
# ==========================================

from modules.auth import (
    login_page
)

# ==========================================
# RESUME PARSER
# ==========================================

from modules.resume_parser import (
    extract_resume_text
)

# ==========================================
# AI ENGINE
# ==========================================

from modules.ai_engine import (
    analyze_resume
)

# ==========================================
# INTERVIEW
# ==========================================

from modules.evaluation import (
    generate_questions,
    evaluate_answer,
    extract_score
)

# ==========================================
# VOICE
# ==========================================

from modules.voice import (
    speak,
    listen
)

# ==========================================
# DASHBOARD
# ==========================================

from modules.dashboard import (
    show_dashboard
)

# ==========================================
# PDF REPORT
# ==========================================

from modules.pdf_report import (
    create_pdf_report
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="AI Interview Assistant",

    page_icon="🤖",

    layout="wide"

)

# ==========================================
# DATABASE INITIALIZATION
# ==========================================

create_tables()

# ==========================================
# SESSION STATE
# ==========================================

default_states = {

    "logged_in": False,

    "username": "",

    "resume_text": "",

    "report": "",

    "questions": [],

    "current_question": 0,

    "answers": [],

    "feedbacks": [],

    "scores": [],

    "voice_answer": "",

    "mode": "Text Interview 📝",

    "pdf_file": "",

    "resume_uploaded": False

}

for key, value in default_states.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================
# LOGIN
# ==========================================

if not st.session_state.logged_in:

    login_page()

    st.stop()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 AI Interview Assistant")

    st.success(

        f"Welcome\n\n{st.session_state.username}"

    )

    st.divider()

    page = st.radio(

        "Navigation",

        [

            "🏠 Home",

            "📄 Resume",

            "🤖 AI Analysis",

            "🎤 Interview",

            "📊 Dashboard",

            "📄 PDF Report"

        ]

    )

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.clear()

        st.rerun()

        # ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.title("🤖 AI Interview Assistant")

    st.caption(
        "AI Powered Resume Analyzer & Interview Preparation System"
    )

    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.session_state.resume_uploaded:

            status = "Uploaded ✅"

        else:

            status = "Not Uploaded ❌"

        st.metric(

            "Resume",

            status

        )

    with col2:

        st.metric(

            "Questions",

            len(st.session_state.questions)

        )

    with col3:

        if len(st.session_state.scores) > 0:

            average = sum(

                st.session_state.scores

            ) / len(

                st.session_state.scores

            )

        else:

            average = 0

        st.metric(

            "Average Score",

            round(average, 2)

        )

    st.write("---")

    left, right = st.columns(2)

    with left:

        st.subheader("🚀 Features")

        st.markdown("""

- 📄 Resume Upload
- 🔍 OCR Resume Reader
- 🤖 AI Resume Analysis
- 🎤 AI Mock Interview
- 🎧 Voice Interview
- 📊 AI Answer Evaluation
- 📈 Interview Dashboard
- 📄 PDF Interview Report

""")

    with right:

        st.subheader("📋 Workflow")

        st.markdown("""

1. Upload Resume

2. Generate AI Resume Analysis

3. Start AI Interview

4. Answer Questions

5. Receive AI Feedback

6. Download PDF Report

7. View Dashboard

""")

    st.write("---")

    st.info(
        "Use the left sidebar to navigate through each module."
    )

    st.subheader("📌 Interview Process")

    st.progress(0)

    st.markdown("""
### Interview Workflow

Upload Resume

⬇

AI Resume Analysis

⬇

Generate Interview Questions

⬇

Text / Voice Interview

⬇

AI Evaluation

⬇

Interview Dashboard

⬇

PDF Report
""")
    
    # ==========================================
# RESUME PAGE
# ==========================================

elif page == "📄 Resume":

    st.title("📄 Resume Upload")

    st.write(
        "Upload your resume in PDF format. The AI will extract the text and use it for resume analysis and interview question generation."
    )

    st.write("---")

    uploaded_file = st.file_uploader(

        "Choose Resume PDF",

        type=["pdf"]

    )

    if uploaded_file is not None:

        os.makedirs(

            "uploads",

            exist_ok=True

        )

        file_path = os.path.join(

            "uploads",

            f"{st.session_state.username}_resume.pdf"

        )

        with open(file_path, "wb") as file:

            file.write(

                uploaded_file.getbuffer()

            )

        st.session_state.resume_uploaded = True

        st.success(

            "Resume uploaded successfully."

        )

        with st.spinner(

            "Extracting resume text..."

        ):

            resume_text = extract_resume_text(

                file_path

            )

        st.session_state.resume_text = resume_text

        st.write("---")

        st.subheader(

            "📃 Extracted Resume Content"

        )

        st.text_area(

            "Resume Text",

            value=resume_text,

            height=350

        )

        word_count = len(

            resume_text.split()

        )

        char_count = len(

            resume_text

        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Words",

                word_count

            )

        with col2:

            st.metric(

                "Characters",

                char_count

            )

    else:

        if st.session_state.resume_uploaded:

            st.success(

                "Resume already uploaded."

            )

            st.text_area(

                "Resume Text",

                value=st.session_state.resume_text,

                height=350

            )

        else:

            st.warning(

                "Please upload your resume to continue."

            )

    st.write("---")

    st.info(

        "Next Step → Open 🤖 AI Analysis to generate your interview preparation report."

    )

    # ==========================================
# AI RESUME ANALYSIS PAGE
# ==========================================

elif page == "🤖 AI Analysis":

    st.title("🤖 AI Resume Analysis")

    if not st.session_state.resume_uploaded:

        st.warning(
            "Please upload your resume first."
        )

    else:

        st.write(
            "Click the button below to generate a complete AI analysis of your resume."
        )

        st.write("---")

        if st.button(
            "🚀 Generate AI Report"
        ):

            with st.spinner(
                "AI is analyzing your resume..."
            ):

                report = analyze_resume(
                    st.session_state.resume_text
                )

            st.session_state.report = report

            st.success(
                "AI Report Generated Successfully!"
            )

        if st.session_state.report != "":

            st.write("---")

            st.subheader(
                "📋 Interview Preparation Report"
            )

            st.text_area(
                "AI Report",
                value=st.session_state.report,
                height=500
            )

            st.write("---")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Resume",
                    "Analyzed ✅"
                )

            with col2:

                st.metric(
                    "Questions Ready",
                    "15"
                )

            with col3:

                st.metric(
                    "Interview",
                    "Ready"
                )

            st.info(
                "Your resume has been analyzed successfully. You can now start the AI Interview."
            )

        else:

            st.info(
                "Click 'Generate AI Report' to begin resume analysis."
            )

            # ==========================================
# AI INTERVIEW PAGE
# ==========================================

elif page == "🎤 Interview":

    st.title("🎤 AI Interview")

    if not st.session_state.resume_uploaded:

        st.warning(
            "Please upload your resume first."
        )

    elif st.session_state.report == "":

        st.warning(
            "Please generate the AI Resume Analysis before starting the interview."
        )

    else:

        st.write(
            "The AI interviewer will generate personalized interview questions based on your resume."
        )

        st.write("---")

        mode = st.radio(

            "Select Interview Mode",

            [

                "Text Interview 📝",

                "Voice Interview 🎤"

            ],

            horizontal=True

        )

        st.session_state.mode = mode

        st.write("---")

        # ==========================
        # START INTERVIEW
        # ==========================

        if len(st.session_state.questions) == 0:

            if st.button(
                "🚀 Start AI Interview"
            ):

                with st.spinner(
                    "Generating Interview Questions..."
                ):

                    questions = generate_questions(
                        st.session_state.resume_text
                    )

                st.session_state.questions = questions

                st.session_state.current_question = 0

                st.session_state.answers = []

                st.session_state.feedbacks = []

                st.session_state.scores = []

                st.success(
                    "Interview Questions Generated Successfully!"
                )

                st.rerun()

        # ==========================
        # INTERVIEW STARTED
        # ==========================

        if len(st.session_state.questions) > 0:

            total_questions = len(
                st.session_state.questions
            )

            current = st.session_state.current_question

            progress = current / total_questions

            st.progress(progress)

            st.caption(
                f"Question {current+1} of {total_questions}"
            )

            st.write("---")

                        # ==========================================
            # CURRENT QUESTION
            # ==========================================

            if current < total_questions:

                question = st.session_state.questions[current]

                st.subheader(
                    f"Question {current + 1}"
                )

                st.info(question)

                # ==========================================
                # VOICE MODE
                # ==========================================

                if st.session_state.mode == "Voice Interview 🎤":

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "🔊 Speak Question"
                        ):

                            speak(question)

                    with col2:

                        if st.button(
                            "🎙 Record Voice Answer"
                        ):

                            with st.spinner(
                                "Listening..."
                            ):

                                answer = listen()

                            st.session_state.voice_answer = answer

                    answer = st.session_state.get(
                        "voice_answer",
                        ""
                    )

                    if answer != "":

                        st.success(
                            "Voice Recorded Successfully"
                        )

                        st.text_area(
                            "Recorded Answer",
                            answer,
                            height=150
                        )

                # ==========================================
                # TEXT MODE
                # ==========================================

                else:

                    answer = st.text_area(

                        "Type Your Answer",

                        height=200

                    )

                st.write("---")

                # ==========================================
                # SUBMIT ANSWER
                # ==========================================

                if st.button(
                    "✅ Submit Answer"
                ):

                    if answer.strip() == "":

                        st.warning(
                            "Please answer the question before continuing."
                        )

                    else:

                        with st.spinner(
                            "AI is evaluating your answer..."
                        ):

                            feedback = evaluate_answer(

                                question,

                                answer,

                                st.session_state.resume_text

                            )

                        score = extract_score(
                            feedback
                        )

                        st.session_state.answers.append(
                            answer
                        )

                        st.session_state.feedbacks.append(
                            feedback
                        )

                        st.session_state.scores.append(
                            score
                        )

                        save_interview(

                            st.session_state.username,

                            question,

                            answer,

                            feedback,

                            score

                        )

                        st.success(
                            "Answer Submitted Successfully!"
                        )

                        st.subheader(
                            "📊 AI Evaluation"
                        )

                        st.write(feedback)

                        if "voice_answer" in st.session_state:

                            st.session_state.voice_answer = ""

                        st.session_state.current_question += 1

                        st.rerun()

                                    # ==========================================
            # INTERVIEW COMPLETED
            # ==========================================

            else:

                st.balloons()

                st.success(
                    "🎉 Congratulations! You have completed the AI Interview."
                )

                st.write("---")

                total_score = sum(
                    st.session_state.scores
                )

                average_score = round(

                    total_score / len(st.session_state.scores),

                    2

                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Questions Answered",
                        len(st.session_state.answers)
                    )

                with col2:

                    st.metric(
                        "Average Score",
                        average_score
                    )

                with col3:

                    percentage = round(
                        (average_score / 10) * 100,
                        2
                    )

                    st.metric(
                        "Performance",
                        f"{percentage}%"
                    )

                st.write("---")

                # ==========================================
                # PERFORMANCE LEVEL
                # ==========================================

                if average_score >= 9:

                    st.success(
                        "🌟 Excellent Performance"
                    )

                elif average_score >= 8:

                    st.success(
                        "👏 Very Good Performance"
                    )

                elif average_score >= 7:

                    st.info(
                        "👍 Good Performance"
                    )

                elif average_score >= 6:

                    st.warning(
                        "🙂 Average Performance"
                    )

                else:

                    st.error(
                        "📚 Needs More Practice"
                    )

                st.write("---")

                st.subheader(
                    "📄 Interview Report"
                )

                if st.button(
                    "Generate PDF Report"
                ):

                    with st.spinner(
                        "Generating PDF Report..."
                    ):

                        pdf_file = create_pdf_report(

                            st.session_state.username,

                            st.session_state.questions,

                            st.session_state.answers,

                            st.session_state.feedbacks,

                            st.session_state.scores

                        )

                    st.session_state.pdf_file = pdf_file

                    st.success(
                        "PDF Report Generated Successfully!"
                    )

                if st.session_state.pdf_file != "":

                    with open(

                        st.session_state.pdf_file,

                        "rb"

                    ) as pdf:

                        st.download_button(

                            label="⬇ Download PDF Report",

                            data=pdf,

                            file_name=os.path.basename(
                                st.session_state.pdf_file
                            ),

                            mime="application/pdf"

                        )

                st.write("---")

                if st.button(
                    "🔄 Start New Interview"
                ):

                    st.session_state.questions = []

                    st.session_state.answers = []

                    st.session_state.feedbacks = []

                    st.session_state.scores = []

                    st.session_state.current_question = 0

                    st.session_state.voice_answer = ""

                    st.session_state.pdf_file = ""

                    st.rerun()

                    # ==========================================
# DASHBOARD PAGE
# ==========================================

elif page == "📊 Dashboard":

    st.title("📊 Interview Dashboard")

    history = get_history(
        st.session_state.username
    )

    if len(history) == 0:

        st.warning(
            "No interview records found."
        )

    else:

        st.success(
            f"{len(history)} Interview Records Found"
        )

        st.write("---")

        # ==========================
        # SHOW DASHBOARD
        # ==========================

        show_dashboard(
            history
        )

        st.write("---")

        # ==========================
        # SUMMARY
        # ==========================

        total_interviews = len(history)

        total_score = 0

        highest_score = 0

        lowest_score = 10

        for record in history:

            score = record[3]

            total_score += score

            if score > highest_score:

                highest_score = score

            if score < lowest_score:

                lowest_score = score

        average_score = round(

            total_score / total_interviews,

            2

        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Total Interviews",

                total_interviews

            )

        with col2:

            st.metric(

                "Highest Score",

                highest_score

            )

        with col3:

            st.metric(

                "Average Score",

                average_score

            )

        st.write("---")

        st.subheader(
            "📋 Previous Interview Records"
        )

        for index, row in enumerate(history, start=1):

            with st.expander(

                f"Interview {index}"

            ):

                st.markdown(
                    f"### Question\n{row[0]}"
                )

                st.markdown(
                    f"### Answer\n{row[1]}"
                )

                st.markdown(
                    f"### Feedback\n{row[2]}"
                )

                st.metric(
                    "Score",
                    row[3]
                )

        st.write("---")

        st.success(
            "Dashboard Loaded Successfully."
        )

        # ==========================================
# PDF REPORT PAGE
# ==========================================

elif page == "📄 PDF Report":

    st.title("📄 AI Interview PDF Report")

    if len(st.session_state.answers) == 0:

        st.warning(
            "Complete an interview before generating the PDF report."
        )

    else:

        st.subheader(
            "Interview Summary"
        )

        total_questions = len(
            st.session_state.answers
        )

        average_score = round(

            sum(st.session_state.scores) /

            len(st.session_state.scores),

            2

        )

        highest_score = max(
            st.session_state.scores
        )

        lowest_score = min(
            st.session_state.scores
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Candidate",
                st.session_state.username
            )

            st.metric(
                "Questions Answered",
                total_questions
            )

        with col2:

            st.metric(
                "Average Score",
                average_score
            )

            st.metric(
                "Highest Score",
                highest_score
            )

        st.write("---")

        st.subheader(
            "Performance"
        )

        if average_score >= 9:

            st.success(
                "🌟 Excellent Interview Performance"
            )

        elif average_score >= 8:

            st.success(
                "👏 Very Good Performance"
            )

        elif average_score >= 7:

            st.info(
                "👍 Good Performance"
            )

        elif average_score >= 6:

            st.warning(
                "🙂 Average Performance"
            )

        else:

            st.error(
                "📚 Needs Improvement"
            )

        st.write("---")

        if st.button(
            "📄 Generate PDF Report"
        ):

            with st.spinner(
                "Generating PDF..."
            ):

                pdf_file = create_pdf_report(

                    st.session_state.username,

                    st.session_state.questions,

                    st.session_state.answers,

                    st.session_state.feedbacks,

                    st.session_state.scores

                )

            st.session_state.pdf_file = pdf_file

            st.success(
                "PDF Report Generated Successfully!"
            )

        if st.session_state.pdf_file != "":

            with open(

                st.session_state.pdf_file,

                "rb"

            ) as pdf:

                st.download_button(

                    label="⬇ Download Interview Report",

                    data=pdf,

                    file_name=os.path.basename(
                        st.session_state.pdf_file
                    ),

                    mime="application/pdf"

                )

        st.write("---")

        st.subheader(
            "Report Includes"
        )

        st.markdown("""

- Candidate Name

- Interview Questions

- Candidate Answers

- AI Feedback

- Individual Scores

- Overall Average Score

- Interview Performance

- AI Suggestions

""")
        # ==========================================
# FOOTER
# ==========================================

st.write("---")

footer_col1, footer_col2 = st.columns(2)

with footer_col1:

    st.caption(
        "🤖 AI Interview Assistant"
    )

    st.caption(
        "AI Powered Resume Analyzer & Interview Preparation System"
    )

with footer_col2:

    st.caption(
        "Developed by"
    )

    st.caption(
        "R. V. Vimal"
    )

st.write("---")

# ==========================================
# ABOUT APPLICATION
# ==========================================

with st.expander(
    "ℹ About This Application"
):

    st.markdown("""

### AI Interview Assistant

This application helps candidates prepare for technical and HR interviews using Artificial Intelligence.

### Features

- Resume Upload
- Resume OCR
- AI Resume Analysis
- AI Interview Questions
- Text Interview
- Voice Interview
- AI Answer Evaluation
- Interview Dashboard
- PDF Report Generation

### Technologies Used

- Python
- Streamlit
- SQLite
- LangChain
- Groq LLM
- PyMuPDF
- SpeechRecognition
- pyttsx3
- ReportLab

""")

# ==========================================
# RESET INTERVIEW
# ==========================================

st.write("---")

if st.button(
    "🔄 Reset Interview Session"
):

    st.session_state.questions = []

    st.session_state.answers = []

    st.session_state.feedbacks = []

    st.session_state.scores = []

    st.session_state.current_question = 0

    st.session_state.voice_answer = ""

    st.session_state.pdf_file = ""

    st.success(
        "Interview session has been reset."
    )

# ==========================================
# LOGOUT
# ==========================================

st.write("---")

logout_col1, logout_col2, logout_col3 = st.columns([1, 2, 1])

with logout_col2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        username = st.session_state.username

        st.session_state.clear()

        st.session_state.logged_in = False

        st.session_state.username = username

        st.success(
            "Logged out successfully."
        )

        st.rerun()

# ==========================================
# END OF APPLICATION
# ==========================================