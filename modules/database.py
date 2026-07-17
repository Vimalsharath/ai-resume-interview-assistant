import hashlib
import os
import re
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE = os.environ.get(
    "AI_INTERVIEW_DB_PATH",
    str(DATA_DIR / "interview_new.db")
)
LEGACY_DATABASE = os.environ.get(
    "AI_INTERVIEW_LEGACY_DB_PATH",
    str(Path(DATABASE).parent / "interview.db")
)


os.makedirs(DATA_DIR, exist_ok=True)


SALT = b"ai_interview_assistant"


def get_connection():

    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    return sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )


def _hash_password(password):

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        SALT,
        100000
    ).hex()


def _is_hashed_password(value):

    return bool(re.fullmatch(r"[0-9a-f]{64}", value or ""))


def _ensure_user_columns(conn):

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in cursor.fetchall()}

    if "email" not in columns:

        cursor.execute(
            "ALTER TABLE users ADD COLUMN email TEXT"
        )

        cursor.execute(
            "UPDATE users SET email = username WHERE email IS NULL OR email = ''"
        )

    conn.commit()


def _migrate_legacy_users():

    if not os.path.exists(LEGACY_DATABASE):

        return

    if os.path.abspath(LEGACY_DATABASE) == os.path.abspath(DATABASE):

        return

    legacy_conn = sqlite3.connect(LEGACY_DATABASE, check_same_thread=False)
    legacy_cursor = legacy_conn.cursor()
    legacy_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")

    if not legacy_cursor.fetchone():

        legacy_conn.close()
        return

    legacy_cursor.execute("PRAGMA table_info(users)")
    columns = {row[1] for row in legacy_cursor.fetchall()}

    if "email" in columns:

        legacy_cursor.execute("SELECT username, email, password FROM users")
        rows = legacy_cursor.fetchall()

    else:

        legacy_cursor.execute("SELECT username, password FROM users")
        rows = [
            (username, f"{username}@legacy.local", password)
            for username, password in legacy_cursor.fetchall()
        ]

    legacy_conn.close()

    if not rows:

        return

    conn = get_connection()
    cursor = conn.cursor()

    for username, email, password in rows:

        cursor.execute(
            "SELECT id FROM users WHERE username=? COLLATE NOCASE OR email=? COLLATE NOCASE",
            (username, email)
        )

        if cursor.fetchone():

            continue

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email, password)
        )

    conn.commit()
    conn.close()


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
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


    _ensure_user_columns(conn)

    conn.commit()
    conn.close()

    _migrate_legacy_users()


# =========================
# AUTH FUNCTIONS
# =========================


def create_user(username, email, password):

    username = (username or "").strip()
    email = (email or "").strip().lower()
    password = password or ""

    if not username:

        return {
            "success": False,
            "message": "Username is required."
        }

    if len(username) < 3:

        return {
            "success": False,
            "message": "Username must be at least 3 characters long."
        }

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):

        return {
            "success": False,
            "message": "Please enter a valid email address."
        }

    if len(password) < 8:

        return {
            "success": False,
            "message": "Password must be at least 8 characters long."
        }

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username=? COLLATE NOCASE",
            (username,)
        )

        if cursor.fetchone():

            conn.close()

            return {
                "success": False,
                "message": "Username already exists."
            }

        cursor.execute(
            "SELECT id FROM users WHERE email=? COLLATE NOCASE",
            (email,)
        )

        if cursor.fetchone():

            conn.close()

            return {
                "success": False,
                "message": "Email already registered."
            }

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password
            )
            VALUES (?,?,?)
            """,
            (
                username,
                email,
                _hash_password(password)
            )
        )

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": "Account created successfully."
        }

    except sqlite3.IntegrityError:

        return {
            "success": False,
            "message": "Unable to create account. Please try again."
        }


def verify_user(identifier, password):

    identifier = (identifier or "").strip()
    password = password or ""

    if not identifier:

        return {
            "success": False,
            "message": "Please enter your email or username."
        }

    if not password:

        return {
            "success": False,
            "message": "Please enter your password."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, email, password
        FROM users
        WHERE username=? COLLATE NOCASE
        OR email=? COLLATE NOCASE
        """,
        (
            identifier,
            identifier.lower()
        )
    )

    user = cursor.fetchone()
    conn.close()

    if not user:

        return {
            "success": False,
            "message": "User not found."
        }

    stored_hash = user[2]

    if _is_hashed_password(stored_hash):

        password_matches = _hash_password(password) == stored_hash

    else:

        password_matches = password == stored_hash

    if not password_matches:

        return {
            "success": False,
            "message": "Invalid username/email or password."
        }

    if not _is_hashed_password(stored_hash):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password=? WHERE username=? COLLATE NOCASE OR email=? COLLATE NOCASE",
            (_hash_password(password), identifier, identifier.lower())
        )
        conn.commit()
        conn.close()

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "username": user[0],
            "email": user[1]
        }
    }


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