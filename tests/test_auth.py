import importlib
import os
import shutil
import sqlite3
import tempfile
import unittest


class AuthFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="ai_assistant_", dir=os.getcwd())
        self.original_cwd = os.getcwd()
        self.db_path = os.path.join(self.temp_dir, "data", "interview_new.db")
        self.legacy_db_path = os.path.join(self.temp_dir, "data", "interview.db")
        os.environ["AI_INTERVIEW_DB_PATH"] = self.db_path
        os.environ["AI_INTERVIEW_LEGACY_DB_PATH"] = self.legacy_db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.chdir(self.temp_dir)
        import modules.database as database
        importlib.reload(database)
        database.create_tables()
        self.database = database

    def tearDown(self):
        os.chdir(self.original_cwd)
        os.environ.pop("AI_INTERVIEW_DB_PATH", None)
        os.environ.pop("AI_INTERVIEW_LEGACY_DB_PATH", None)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_registration_and_login_flow(self):
        result = self.database.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!"
        )
        self.assertTrue(result["success"], result.get("message"))

        duplicate = self.database.create_user(
            username="alice",
            email="another@example.com",
            password="OtherPass" 
        )
        self.assertFalse(duplicate["success"])

        invalid_email = self.database.create_user(
            username="bob",
            email="invalid-email",
            password="Pass123!"
        )
        self.assertFalse(invalid_email["success"])

        verified = self.database.verify_user("alice", "StrongPass123!")
        self.assertTrue(verified["success"], verified.get("message"))

        wrong_password = self.database.verify_user("alice", "wrong")
        self.assertFalse(wrong_password["success"])

    def test_legacy_plaintext_password_is_upgraded(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            ("legacy", "legacy@example.com", "legacy-pass")
        )
        conn.commit()
        conn.close()

        result = self.database.verify_user("legacy", "legacy-pass")
        self.assertTrue(result["success"], result.get("message"))

    def test_migrate_legacy_database_users(self):
        legacy_conn = sqlite3.connect(self.legacy_db_path)
        legacy_cursor = legacy_conn.cursor()
        legacy_cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
        )
        legacy_cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("olduser", "OldPass123!")
        )
        legacy_conn.commit()
        legacy_conn.close()

        self.database.create_tables()
        result = self.database.verify_user("olduser", "OldPass123!")
        self.assertTrue(result["success"], result.get("message"))


if __name__ == "__main__":
    unittest.main()
