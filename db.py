import mysql.connector
import streamlit as st
from mysql.connector import Error
import hashlib

DB_NAME = "railway"

def get_db_connection(create_db=False):
    import mysql.connector

    if create_db:
        # Connect without database first
        conn = mysql.connector.connect(
            host="tramway.proxy.rlwy.net",
            port=13359,
            user="root",
            password="uIFvZQyimbghigbQOZOQZkGFampbOehe"
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()

    # Connect to the actual database
    return mysql.connector.connect(
        host="tramway.proxy.rlwy.net",
        port=13359,
        user="root",
        password="uIFvZQyimbghigbQOZOQZkGFampbOehe",
        database=DB_NAME
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrkey (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            filename VARCHAR(255) NOT NULL,
            secrkey VARCHAR(255) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

def check_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT id FROM users WHERE username=%s AND password_hash=%s",
        (username, password_hash)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:  # result is a tuple like (1,)
        return result[0]  # return the int, not the tuple
    return None

def store_key(user_id, filename, key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secrkey (user_id, filename, secrkey) VALUES (%s, %s, %s)", (user_id, filename, key.decode()))
    conn.commit()
    cursor.close()
    conn.close()

def get_key(user_id, filename):
    """
    Return the stored secrkey (string) for a given user and filename,
    or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT secrkey FROM secrkey WHERE user_id=%s AND filename=%s",
        (user_id, filename)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_user_files(user_id):
    """
    Return a list of filenames (without .enc) uploaded by this user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename FROM secrkey WHERE user_id = %s",
        (user_id,)
    )
    files = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return files
