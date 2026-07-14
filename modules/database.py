import sqlite3
import os


os.makedirs(
    "data",
    exist_ok=True
)


DATABASE = "data/interview_new.db"



def get_connection():

    return sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )



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



# =========================
# AUTH FUNCTIONS
# =========================


def create_user(username, password):

    try:

        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password
            )
            VALUES (?,?)
            """,
            (
                username,
                password
            )
        )


        conn.commit()
        conn.close()


        return True


    except sqlite3.IntegrityError:

        return False
    

def verify_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password
        )
    )


    user = cursor.fetchone()


    conn.close()


    return user    


# =========================
# INTERVIEW FUNCTIONS
# =========================


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

        VALUES(?,?,?,?,?)
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
        SELECT question,answer,feedback,score
        FROM interviews
        WHERE username=?
        """,
        (username,)
    )


    result = cursor.fetchall()


    conn.close()


    return result