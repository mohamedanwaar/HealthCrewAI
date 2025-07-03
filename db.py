#!/usr/bin/env python3
"""
Database module for simplified medical assistant system
Contains only patients and medical_history tables
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "medical_assistant.db"

def init_database():
    """Initialize SQLite database with existing data preservation."""
    # Only create new database if it doesn't exist
    if not os.path.exists(DB_PATH):
        # Create new database with correct schema
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Patients table with national_id as primary key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                national_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Medical history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                national_id TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (national_id) REFERENCES patients (national_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ New database initialized successfully")
    else:
        # Database exists - check if it has the correct schema
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            # Check if patients table has national_id column
            cursor.execute("PRAGMA table_info(patients)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'national_id' not in columns:
                print("⚠️ Database schema needs migration - please backup and recreate database")
            else:
                print("✅ Existing database schema is correct")
                
        except Exception as e:
            print(f"⚠️ Database check error: {e}")
        finally:
            conn.close()

def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def check_patient_by_national_id(national_id):
    """Check if patient exists by national ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT national_id, name, age, gender FROM patients WHERE national_id = ?",
        (str(national_id),)  # Convert to string to handle number input
    )
    patient = cursor.fetchone()
    conn.close()
    return patient  # Returns None if not found

def check_patient(name, age, gender):
    """Check if patient exists by name, age, and gender (legacy function)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT national_id FROM patients WHERE name = ? AND age = ? AND gender = ?",
        (name, age, gender)
    )
    patient = cursor.fetchone()
    conn.close()
    return patient  # Returns None if not found

def create_patient(name, national_id, age, gender):
    """Create a new patient with national ID as primary key."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (national_id, name, age, gender) VALUES (?, ?, ?, ?)",
            (str(national_id), name, age, gender)  # Convert to string to handle number input
        )
        conn.commit()
        conn.close()
        return str(national_id)  # Return national_id as the identifier
    except sqlite3.IntegrityError:
        conn.close()
        return None  # National ID already exists

def add_medical_history(national_id, description):
    """Add medical history entry for a patient using national_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medical_history (national_id, description) VALUES (?, ?)",
        (str(national_id), description)  # Convert to string to handle number input
    )
    history_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return history_id

def get_patient_medical_history(national_id):
    """Get all medical history entries for a patient using national_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT description, timestamp FROM medical_history WHERE national_id = ? ORDER BY timestamp DESC",
        (str(national_id),)  # Convert to string to handle number input
    )
    history = cursor.fetchall()
    conn.close()
    return history

def get_patient_by_national_id(national_id):
    """Get patient information by national_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT national_id, name, age, gender FROM patients WHERE national_id = ?",
        (str(national_id),)  # Convert to string to handle number input
    )
    patient = cursor.fetchone()
    conn.close()
    return patient
