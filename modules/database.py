import sqlite3
import os
os.makedirs("data", exist_ok=True)


DATABASE = "interview.db"



def get_connection():

    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    return conn



def create_tables():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        question TEXT,
        answer TEXT,
        feedback TEXT,
        score INTEGER
    )
    """)


    conn.commit()

    conn.close()



def save_interview(
    username,
    question,
    answer,
    feedback,
    score
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO interviews
        (
            username,
            question,
            answer,
            feedback,
            score
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            username,
            question,
            answer,
            feedback,
            score
        )

    )


    conn.commit()

    conn.close()



def get_history(username):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT question, answer, feedback, score
        FROM interviews
        WHERE username=?
        """,

        (username,)

    )


    data = cursor.fetchall()


    conn.close()


    return data