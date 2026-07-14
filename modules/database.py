import sqlite3
import hashlib


DATABASE = "database/users.db"



def create_tables():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews(

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




def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()




def create_user(username,password):

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    try:

        cursor.execute(
        """
        INSERT INTO users(username,password)
        VALUES(?,?)
        """,
        (
            username,
            hash_password(password)
        ))


        conn.commit()

        return True


    except:

        return False


    finally:

        conn.close()




def verify_user(username,password):

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    cursor.execute(
    """
    SELECT *
    FROM users
    WHERE username=? AND password=?
    """,
    (
        username,
        hash_password(password)
    ))


    result=cursor.fetchone()


    conn.close()


    return result is not None





def save_interview(
        username,
        question,
        answer,
        feedback,
        score
):


    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    cursor.execute(
    """
    INSERT INTO interviews
    VALUES(NULL,?,?,?,?,?)
    """,
    (
        username,
        question,
        answer,
        feedback,
        score
    ))


    conn.commit()

    conn.close()





def get_history(username):


    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    cursor.execute(
    """
    SELECT question,answer,feedback,score
    FROM interviews
    WHERE username=?
    """,
    (username,)
    )


    data=cursor.fetchall()


    conn.close()


    return data