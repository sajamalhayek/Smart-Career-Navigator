import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جدول المرشحين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            resume_text TEXT,
            skills_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول تحليل الفجوات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gap_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            target_job TEXT,
            match_percentage INTEGER,
            missing_skills_json TEXT,
            roadmap_json TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')
    
    conn.commit()
    conn.close()