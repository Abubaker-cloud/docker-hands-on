import os
import time
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "appdb")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
        autocommit=True
    )

def initialize_database():
    for attempt in range(30):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visits (
                        id INT PRIMARY KEY,
                        count INT NOT NULL
                    )
                """)
                cursor.execute("""
                    INSERT IGNORE INTO visits (id, count)
                    VALUES (1, 0)
                """)
            connection.close()
            print("Database initialized successfully")
            return
        except pymysql.MySQLError as error:
            print(f"Database not ready: {error}")
            time.sleep(2)

    raise RuntimeError("Could not connect to MySQL")

@app.route("/")
def home():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE visits SET count = count + 1 WHERE id = 1"
            )
            cursor.execute("SELECT count FROM visits WHERE id = 1")
            count = cursor.fetchone()[0]

        return jsonify(
            message="Docker project is running!",
            visits=count
        )
    finally:
        connection.close()

@app.route("/health")
def health():
    return jsonify(status="ok")

initialize_database()
