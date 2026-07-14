# 🤖 AI Interview Assistant
# 🌐 Live Demo

🚀 Try the deployed application:

[AI Interview Assistant - Live App](https://ai-resume-interview-assistant-ds5sgazdgtebxtruug9hbi.streamlit.app/)


An AI-powered interview preparation platform that helps candidates prepare for technical and HR interviews by analyzing resumes, generating personalized interview questions, evaluating answers using Large Language Models (LLMs), and providing detailed performance reports.

The system provides a complete interview workflow from resume upload to final performance analysis with PDF report generation.

---

# 📌 Project Overview

The **AI Interview Assistant** is designed to simulate real-world interview environments using Artificial Intelligence.

Users can upload their resume, receive AI-generated interview questions based on their skills and experience, answer questions through text or voice mode, and get instant AI-based evaluation with scores, feedback, and improvement suggestions.

This project combines:

- Generative AI
- Natural Language Processing
- Resume Parsing
- Speech Processing
- Database Management
- Web Application Development

---

# 🚀 Features

## 📄 1. Resume Upload & Analysis

- Upload candidate resume in PDF format
- Extract resume content automatically
- Analyze skills, projects, education, and experience
- Generate personalized interview preparation insights

---

## 🤖 2. AI Resume Analysis

The AI engine analyzes the resume and provides:

- Candidate skill summary
- Technical strengths
- Possible interview topics
- Preparation recommendations

---

## 📝 3. Personalized Interview Question Generation

The system generates interview questions based on the uploaded resume.

Question categories include:

- Programming
- Data Structures & Algorithms
- Machine Learning
- Artificial Intelligence
- Projects
- Technical concepts
- HR questions

---

## 🎤 4. Interview Modes

### Text Interview Mode

Candidates can:

- Read AI-generated questions
- Type answers
- Receive instant evaluation


### Voice Interview Mode

Candidates can:

- Listen to questions using text-to-speech
- Answer using microphone
- Convert speech into text
- Get AI evaluation

---

## 📊 5. AI Answer Evaluation

Each answer is evaluated based on:

- Technical correctness
- Relevance
- Explanation quality
- Completeness

The system provides:

- Score
- Detailed feedback
- Improvement suggestions

---

## 📈 6. Interview Dashboard

The dashboard displays:

- Interview history
- Previous answers
- Scores
- Performance tracking

---

## 📄 7. PDF Interview Report

After completing the interview, users can generate a PDF report containing:

- Interview questions
- Candidate answers
- AI feedback
- Individual scores
- Final performance score

---

# 🏗️ System Architecture


             Resume Upload
                   |
                   ▼
          Resume Text Extraction
                   |
                   ▼
          AI Resume Analysis
                   |
                   ▼
      Personalized Question Generation
                   |
                   ▼
    Text Interview / Voice Interview
                   |
                   ▼
          AI Answer Evaluation
                   |
                   ▼
         Score & Feedback Generation
                   |
                   ▼
          Interview Dashboard
                   |
                   ▼
             PDF Report

             
---

# 🛠️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python

## Artificial Intelligence

- Groq Large Language Model
- LangChain
- Natural Language Processing

## Resume Processing

- PyMuPDF
- PDF Parsing

## Speech Processing

- Speech Recognition
- Text-to-Speech

## Database

- SQLite

## Report Generation

- ReportLab

## Deployment

- Streamlit Community Cloud

---

# 📂 Project Structure

AI_Interview_Assistant/

│
├── app.py
│
├── requirements.txt
├── packages.txt
│
├── modules/
│ │
│ ├── ai_engine.py
│ ├── auth.py
│ ├── database.py
│ ├── dashboard.py
│ ├── evaluation.py
│ ├── pdf_report.py
│ ├── resume_parser.py
│ └── voice.py
│
├── uploads/
│
└── README.md


---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/Vimalsharath/ai-resume-interview-assistant.git

## 2. Navigate to Project Directory
cd ai-resume-interview-assistant

##3. Create Virtual Environment
python -m venv venv

## Activate environment:
#Windows
venv\Scripts\activate

##4. Install Dependencies
pip install -r requirements.txt

##5. Add API Key
#Create a .env file:
GROQ_API_KEY=your_api_key_here

##6. Run Application
streamlit run app.py


🔐 Authentication
The application provides:

User login system
User-specific interview history
Secure session handling

Login
 |
 ▼
Upload Resume
 |
 ▼
AI Resume Analysis
 |
 ▼
Generate Questions
 |
 ▼
Take Interview
 |
 ▼
AI Evaluation
 |
 ▼
View Dashboard
 |
 ▼
Download Report

🎯 Use Cases
Students
Placement preparation
Mock interviews
Technical practice
Fresh Graduates
Resume-based preparation
Skill evaluation
Interview confidence improvement
Recruiters
Candidate screening
Automated evaluation
Interview assistance
🔮 Future Enhancements

Future improvements planned:

Real-time AI voice conversation
Facial expression analysis
Advanced RAG-based knowledge retrieval
Multiple interviewer personalities
Coding interview evaluation
Cloud database integration
Candidate ranking system
👨‍💻 Developer

Vimal Sharath

Computer Science Engineering Student

Skills:

Python
Artificial Intelligence
Machine Learning
Cloud Computing
Web Development
⭐ Acknowledgement

This project was developed as an AI-based placement preparation tool using modern Generative AI technologies.

📜 License

This project is created for educational and research purposes.


---

After saving:

Run:

```cmd
git add README.md
git commit -m "Add detailed project documentation"
git push

