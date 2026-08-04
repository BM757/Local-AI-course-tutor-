import sqlite3
import time

def init_monitor_db():
    conn = sqlite3.connect("monitoring.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            retrieval_latency_ms REAL,
            generation_latency_ms REAL,
            prompt_length INT,
            response_length INT,
            user_feedback INT DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def log_telemetry(ret_time, gen_time, p_len, r_len):
    conn = sqlite3.connect("monitoring.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO telemetry 
        (retrieval_latency_ms, generation_latency_ms, prompt_length, response_length)
        VALUES (?, ?, ?, ?)
    ''', (ret_time, gen_time, p_len, r_len))
    log_id = c.lastrowid
    conn.commit()
    conn.close()
    return log_id

def log_feedback(log_id, feedback_value):
    conn = sqlite3.connect("monitoring.db")
    c = conn.cursor()
    c.execute('UPDATE telemetry SET user_feedback = ? WHERE id = ?', (feedback_value, log_id))
    conn.commit()
    conn.close()