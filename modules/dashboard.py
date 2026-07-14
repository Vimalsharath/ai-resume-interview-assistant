import streamlit as st
import pandas as pd


def show_dashboard(history):


    if len(history) == 0:

        st.info(
            "No interview records found"
        )

        return



    df = pd.DataFrame(

        history,

        columns=[
            "Question",
            "Answer",
            "Feedback",
            "Score"
        ]

    )


    st.dataframe(
        df,
        use_container_width=True
    )


    average = df["Score"].mean()


    st.metric(
        "Average Score",
        round(average, 2)
    )