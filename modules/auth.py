import streamlit as st

from modules.database import (
    create_user,
    verify_user
)



def login_page():

    st.title("🔐 AI Interview Assistant Login")


    option = st.selectbox(
        "Select Option",
        [
            "Login",
            "Register"
        ]
    )


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if option=="Register":


        if st.button("Create Account"):

            result = create_user(
                username,
                password
            )


            if result:

                st.success(
                    "Account created successfully"
                )

            else:

                st.error(
                    "Username already exists"
                )



    else:


        if st.button("Login"):


            result = verify_user(
                username,
                password
            )


            if result:

                st.session_state.logged_in=True
                st.session_state.username=username

                st.success(
                    "Login successful"
                )

                st.rerun()


            else:

                st.error(
                    "Invalid username or password"
                )