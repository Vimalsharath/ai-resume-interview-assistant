import streamlit as st

from modules.database import (
    create_user,
    verify_user,
)


def login_page():
    st.title("🔐 Welcome to AI Interview Assistant")
    st.caption("Secure access to your interview workspace")

    st.markdown(
        """
        <div style='padding: 0.8rem 0 1.2rem 0; color: #cbd5e1;'>
        Register a new profile or sign in to continue preparing for your next interview.
        </div>
        """,
        unsafe_allow_html=True,
    )

    option = st.selectbox("Select Option", ["Login", "Register"], key="auth_option")

    if option == "Register":
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")

        if st.button("Create Account", use_container_width=True):
            if not username or not email or not password:
                st.error("Please fill in username, email, and password.")
            else:
                result = create_user(username, email, password)
                if result["success"]:
                    st.success(result["message"])
                    st.info("You can now switch to Login and continue to your workspace.")
                else:
                    st.error(result["message"])

    else:
        identifier = st.text_input("Email or Username", key="login_identifier")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            result = verify_user(identifier, password)
            if result["success"]:
                st.session_state.logged_in = True
                st.session_state.username = result["user"]["username"]
                st.session_state.resume_uploaded = False
                st.session_state.report = ""
                st.session_state.questions = []
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.feedbacks = []
                st.session_state.scores = []
                st.session_state.voice_answer = ""
                st.session_state.pdf_file = ""
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])
