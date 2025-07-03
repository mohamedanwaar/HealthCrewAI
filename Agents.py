
import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.llm import LLM
from Tools import get_patient_history_tool

load_dotenv()

def create_llm():
    """Create LLM instance with Ollama configuration."""
    # api_key = os.environ.get("OPENAI_API_KEY")
    return LLM(
    model="openrouter/deepseek/deepseek-chat-v3-0324:free",  
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  # make sure this is set properly
)



def create_symptom_extractor_agent():
    """Agent 1 - Extract and structure patient information into clean JSON format"""
    return Agent(
        role="Medical Data Extractor",
        goal="Extract and structure patient information into clean JSON format",
        backstory="""You are a specialized medical data extraction agent. Your expertise is in taking raw patient 
        information (name, age, gender, symptoms) and converting it into structured, clean JSON format. You convert 
        patient-reported symptoms into proper medical terminology when possible. You are precise and only output 
        valid JSON objects with standardized medical terms.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
        handle_tool_error=lambda error: f"Error executing tool: {str(error)}. Please try again or inform the user."
    )

def create_medical_history_agent():
    """Agent 2 - Retrieve and combine patient medical history with Agent 1's output"""
    return Agent(
        role="Medical History Specialist",
        goal="Retrieve patient medical history and combine with structured patient data",
        backstory="""You are a medical history specialist agent. Your expertise is in accessing patient medical 
        records from the database and combining them with current patient information. You analyze patient metadata, 
        symptoms, and historical data to provide comprehensive medical profiles including chronic conditions, 
        allergies, and previous treatments. You always begin with 'Based on the previous agent's output' and only 
        output valid JSON objects. When you encounter errors or failures, you provide detailed reasoning explaining 
        what went wrong and why.""",
        verbose=False,
        allow_delegation=False,
        llm=create_llm(),
        tools=[get_patient_history_tool],
        handle_tool_error=lambda error: f"Tool execution failed: {str(error)}. I attempted to use the tool but encountered this error. Please provide detailed reasoning for this failure."
    )

def create_symptom_evaluator_agent():
    """Agent 3 - Analyze patient's data and generate clinical summary for the doctor."""
    return Agent(
        role="Medical Symptom Evaluator",
        goal="Analyze patient history and current symptoms to assist doctor with insights",
        backstory="""
        You are a clinical evaluator agent working alongside a doctor. Your job is to read the structured output 
        from Agent 2, including current symptoms and medical history, and provide a helpful, structured summary. 
        You never make final diagnoses but help the doctor with possible conditions, risk levels, and suggestions.
        You begin with: 'Based on the previous agent's output...' and you always return structured JSON only.
        """,
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),  # Use your LLM setup (Ollama or OpenRouter)
        handle_tool_error=lambda e: f"Tool failed: {str(e)}"
    )

def create_medical_report_generator_agent():
    """Agent 4 - Generate human-readable medical report for healthcare providers"""
    return Agent(
        role="Medical Report Generator",
        goal="Generate a clean and professional HTML medical report from structured JSON assessment",
        backstory="""You are a medical documentation assistant. Your job is to convert structured clinical 
            summaries into clear, readable, styled HTML reports for doctors. Focus on clarity, structure, 
            and proper medical presentation.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm()
    )