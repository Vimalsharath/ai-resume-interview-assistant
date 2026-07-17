import pandas as pd
import streamlit as st


def show_dashboard(history):
    if len(history) == 0:
        st.info("No interview records found yet. Complete your first mock interview to populate this dashboard.")
        return

    records = []
    for item in history:
        records.append({
            "Question": item[0] if len(item) > 0 else "",
            "Answer": item[1] if len(item) > 1 else "",
            "Feedback": item[2] if len(item) > 2 else "",
            "Score": item[3] if len(item) > 3 else 0,
        })

    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True, hide_index=True)

    average = round(float(df["Score"].mean()), 2)
    st.metric("Average Score", average)

    if average >= 8:
        st.success("Excellent progress. Your interview performance is trending strongly.")
    elif average >= 6:
        st.info("Solid performance. Keep refining your answers and communication style.")
    else:
        st.warning("You are still building momentum. Keep practicing and reviewing your feedback.")