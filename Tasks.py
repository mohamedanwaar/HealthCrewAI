from crewai import Task
from openpyxl.styles.builtins import output
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class PatientDataOutput(BaseModel):
    """Output Json for agent1_extractor Agent 1"""

    name: str = Field(..., title="Patient full name")
    age: int = Field(..., title="Patient age in years")
    gender: str = Field(..., title="Patient gender")
    symptoms: List[str] = Field(..., title="List of standardized medical symptoms")

class MedicalHistoryOutput(BaseModel):
    """Output schema for Agent 2"""
    patient_info: Dict[str, Any] = Field(..., title="Patient basic information from Agent 1")
    medical_history: List[Dict[str, str]] = Field(..., title="Historical medical records")
    chronic_conditions: List[str] = Field(default=[], title="Identified chronic conditions")
    allergies: List[str] = Field(default=[], title="Known allergies")
class InputData_for_tools(BaseModel):
    """Input schema for tools"""
    national_id: str = Field(..., title="Patient national ID")
def create_symptom_extraction_task(patient_name: str, patient_age: int, 
                                 patient_gender: str, symptoms: str, agent):
    """Simplified task: extract and save basic patient data and symptoms."""
    return Task(
        description=f"""
        PATIENT DATA EXTRACTION TASK

        PATIENT INFO:
        - Name: {patient_name}
        - Age: {patient_age}
        - Gender: {patient_gender}
        - Symptoms: "{symptoms}"

        YOUR TASK:
        1. Extract the name, age, and gender exactly as given.
        2. Analyze the symptoms and return them as a list of clean, medically phrased terms.
        3. Ensure the final output is a valid JSON object with the following structure:

        {{
          "name": "{patient_name}",
          "age": {patient_age},
          "gender": "{patient_gender}",
          "symptoms": ["Symptom 1", "Symptom 2", "Symptom 3"]
        }}

        RULES:
        - Only output a single JSON object.
        - No explanation, no markdown, no comments — just JSON.
        - Symptoms must be clearly written and separated.
        """,
        agent=agent,
        expected_output="A single JSON object with patient name, age, gender, and symptoms",
        output_file="Output/PatientData.json"
    )

def create_medical_history_task(national_id: str, agent):
    """Agent 2 Task: Use Agent 1 output + database tool to generate full medical history profile"""
    return Task(
        description=f"""
    MEDICAL HISTORY PROCESSING TASK

    You are given:
    1. Patient data from a previous agent in structured JSON format.
    2. Access to a tool called `get_patient_history` that accepts a national ID and returns plain text.

    Your steps:
    1. Parse the previous agent's JSON output to extract: name, age, gender, and symptoms.
    2. Use the tool `get_patient_history` with national ID: "{national_id}" to fetch historical medical notes.
    3. From the plain text tool response, extract:
       - Medical events and dates
       - Chronic conditions (e.g., high blood pressure → Hypertension)
       - Allergies (if mentioned)
    4. Combine both Agent 1 data and tool results into this JSON format:

    {{
      "patient_info": {{
        "name": "...",
        "age": ...,
        "gender": "...",
        "current_symptoms": ["...", "..."]
      }},
      "medical_history": [
        {{
          "date": "YYYY-MM-DD",
          "description": "event details"
        }}
      ],
      "chronic_conditions": ["condition1", "condition2"],
      "allergies": ["allergy1", "allergy2"]
    }}

    Rules:
    - If no medical history is found, use empty lists or "None"
    - Only output the final JSON object — no explanation or markdown
    - Always start from the structured JSON provided by Agent 1
    """,
        agent=agent,
        expected_output="A single clean JSON object combining Agent 1 data with patient medical history",
        output_file="Output/agentHistory.json"
    )




def create_symptom_evaluation_task(agent):
    """Agent 3 Task: Auto-uses Agent 2's output to generate clinical summary"""
    return Task(
        description="""
        SYMPTOM EVALUATION TASK - AGENT 3

        CONTEXT:
        You are the third agent in a multi-agent medical system.
        You receive the output from the previous agent (Agent 2) in structured JSON format, containing:
        - Patient info (name, age, gender, symptoms)
        - Medical history (events with dates and descriptions)
        - Chronic conditions
        - Allergies

        YOUR TASK:
        1. Read the previous JSON output
        2. Analyze current symptoms in light of the history
        3. Identify possible (not confirmed) diagnoses
        4. Assess severity and urgency level
        5. Provide recommendations for the doctor:
           - Follow-up actions
           - Suggested tests
           - Precautions based on history/allergies

        OUTPUT FORMAT:
        Return ONLY this valid JSON structure:

        {
          "patient_summary": {
            "name": "...",
            "age": ...,
            "gender": "...",
            "current_symptoms": [...],
            "medical_history_summary": [
              "Short summary of key historical events (1 sentence each)"
            ]
          },
          "clinical_assessment": {
            "symptom_analysis": "Detailed explanation of current symptoms",
            "potential_diagnoses": ["Possible diagnosis 1", "2"],
            "risk_factors": ["Risk 1", "2"],
            "severity_assessment": "low | moderate | high",
            "urgency_level": "routine | urgent | emergent"
          },
          "recommendations": {
            "immediate_actions": ["Action 1", "2"],
            "follow_up_care": ["Follow-up steps"],
            "additional_tests": ["Test 1", "Test 2"],
            "precautions": ["Avoid x due to allergy y"]
          }
        }

        RULES:
        - Do NOT provide confirmed diagnoses
        - Do NOT output markdown or extra explanation — only JSON
        - Start with: "Based on the previous agent's output..."
        """,
        agent=agent,
        expected_output="Final structured JSON with clinical evaluation and guidance",
        output_file="Output/agentSummary.json"
    )

def create_medical_report_task(agent):
    """Agent 4 Task: Generate human-readable medical report"""
    return Task(
        description="""
            REPORT GENERATION TASK - AGENT 4

            INSTRUCTIONS:
            1. You will receive the complete output from Agent 3.
            2. Convert the structured JSON into a complete and styled HTML document.
            3. The HTML must include the following sections:
               - Patient Summary
               - Clinical Assessment
               - Recommendations
            4. Use HTML headings, bold labels, and paragraphs.
            5. Apply minimal but clean styling: use CSS inline or inside <style> tag.
            6. Avoid markdown or plain text — output only HTML.

            OUTPUT FORMAT:
            Output ONLY the final HTML string.
            """,
        agent=agent,
        expected_output="A full HTML report styled and organized based on Agent 3's output",
        output_file="Output/final_report.html"
    )
