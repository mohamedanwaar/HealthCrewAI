from crewai.tools import tool
from db import get_patient_medical_history, get_patient_by_national_id
import json
from datetime import datetime

@tool
def get_patient_history_tool(national_id: str) -> str:
    """    
    Get complete medical history for a patient using their national ID.
    
    Args:
        national_id: The patient's national ID as a string
        
    Returns:
        str: Plain text medical history descriptions or error message"""
    try:
        # Get patient medical history
        history_entries = get_patient_medical_history(national_id)
        
        if not history_entries:
            return "No medical history found for this patient."
        
        # Format history entries as plain text
        history_text = "Medical History:\n"
        for i, (description, timestamp) in enumerate(history_entries, 1):
            history_text += f"{i}. {description} (Date: {timestamp})\n"
        
        return history_text
        
    except Exception as e:
        return f"Error retrieving history: {str(e)}"


