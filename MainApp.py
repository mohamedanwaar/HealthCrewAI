import streamlit as st
import sqlite3
from datetime import datetime
import json
import os
import sys

# Add the current directory to Python path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing modules
from db import (
    init_database,
    check_patient_by_national_id,
    create_patient,
    add_medical_history,
    get_patient_medical_history
)

from Agents import (
    create_symptom_extractor_agent,
    create_medical_history_agent,
    create_symptom_evaluator_agent,
    create_medical_report_generator_agent
)

from Tasks import (
    create_symptom_extraction_task,
    create_medical_history_task,
    create_symptom_evaluation_task,
    create_medical_report_task
)

from crewai import Crew
from crewai.crew import Process

# Initialize database
init_database()

# Streamlit page configuration
st.set_page_config(
    page_title="Medical Analysis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        padding: 1rem 0;
        border-bottom: 3px solid #3498db;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #2980b9;
        border-left: 4px solid #3498db;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🏥 AI Medical Analysis System</h1>', unsafe_allow_html=True)

# Initialize session state
if 'patient_registered' not in st.session_state:
    st.session_state.patient_registered = False
if 'show_medical_history_form' not in st.session_state:
    st.session_state.show_medical_history_form = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'crew_results' not in st.session_state:
    st.session_state.crew_results = None

# Sidebar for system information
with st.sidebar:
    st.markdown("### 🔧 System Information")
    st.info("This system uses 4 AI agents working collaboratively:")
    st.markdown("""
    1. **Data Extractor** - Processes patient symptoms
    2. **History Specialist** - Retrieves medical records
    3. **Symptom Evaluator** - Analyzes clinical data
    4. **Report Generator** - Creates final medical report
    """)


# Main content area
def run_medical_crew_analysis(patient_name, patient_age, patient_gender, symptoms, national_id):
    """Run the 4-agent medical analysis system"""

    with st.spinner("🔄 Running AI Medical Analysis..."):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Create agents
            agent1_extractor = create_symptom_extractor_agent()
            agent2_history = create_medical_history_agent()
            agent3_evaluator = create_symptom_evaluator_agent()
            agent4_reporter = create_medical_report_generator_agent()

            # Create tasks
            task1 = create_symptom_extraction_task(
                patient_name=patient_name,
                patient_age=patient_age,
                patient_gender=patient_gender,
                symptoms=symptoms,
                agent=agent1_extractor
            )
            progress_bar.progress(20)
            status_text.text("Creating medical history task...")

            task2 = create_medical_history_task(
                national_id=national_id,
                agent=agent2_history
            )
            progress_bar.progress(40)
            status_text.text("Creating symptom evaluation task...")

            task3 = create_symptom_evaluation_task(agent3_evaluator)
            progress_bar.progress(60)
            status_text.text("Creating report generation task...")

            task4 = create_medical_report_task(agent4_reporter)
            progress_bar.progress(80)
            status_text.text("Running AI analysis...")

            # Create and run crew
            crew = Crew(
                agents=[agent1_extractor, agent2_history, agent3_evaluator, agent4_reporter],
                tasks=[task1, task2, task3, task4],
                verbose=False,
                process=Process.sequential
            )

            result = crew.kickoff()
            progress_bar.progress(100)
            status_text.text("Analysis complete!")

            return str(result)

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            return None


# Main form
st.markdown('<h2 class="section-header">Patient Information</h2>', unsafe_allow_html=True)

with st.form("patient_form"):
    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("👤 Patient Name", placeholder="Enter full name")
        patient_age = st.number_input("🎂 Age", min_value=1, max_value=120, value=30)
        patient_gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])

    with col2:
        national_id = st.text_input("🆔 National ID", placeholder="Enter national ID")
        symptoms = st.text_area("🩺 Current Symptoms",
                                placeholder="Describe your symptoms in detail...",
                                height=100)

    submit_button = st.form_submit_button("🔍 Analyze Patient", use_container_width=True)

if submit_button:
    # Validate inputs
    if not all([patient_name, national_id, symptoms]):
        st.error("⚠️ Please fill in all required fields!")
    else:
        # Check if patient exists
        existing_patient = check_patient_by_national_id(national_id)

        if existing_patient:
            # Patient exists - proceed with analysis
            st.markdown('<div class="info-box">✅ Patient found in database. Proceeding with analysis...</div>',
                        unsafe_allow_html=True)

            # Run the crew analysis
            crew_result = run_medical_crew_analysis(
                patient_name, patient_age, patient_gender, symptoms, national_id
            )

            if crew_result:
                st.session_state.crew_results = crew_result
                st.session_state.analysis_complete = True
                st.rerun()
        else:
            # New patient - show registration form
            st.session_state.show_medical_history_form = True
            st.session_state.temp_patient_data = {
                'name': patient_name,
                'age': patient_age,
                'gender': patient_gender,
                'national_id': national_id,
                'symptoms': symptoms
            }
            st.rerun()

# Show medical history form for new patients
if st.session_state.show_medical_history_form:
    st.markdown('<h2 class="section-header">New Patient Registration</h2>', unsafe_allow_html=True)
    st.markdown(
        '<div class="warning-box">📝 This is a new patient. Please provide medical history before analysis.</div>',
        unsafe_allow_html=True)

    with st.form("medical_history_form"):
        st.markdown("### Patient Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Name", value=st.session_state.temp_patient_data['name'], disabled=True)
        with col2:
            st.number_input("Age", value=st.session_state.temp_patient_data['age'], disabled=True)
        with col3:
            st.text_input("Gender", value=st.session_state.temp_patient_data['gender'], disabled=True)

        st.markdown("### Medical History")
        medical_history = st.text_area(
            "📋 Enter Medical History",
            placeholder="Enter any previous medical conditions, surgeries, medications, allergies, etc.",
            height=150,
            help="Provide detailed medical history including chronic conditions, previous treatments, medications, and known allergies."
        )

        col1, col2 = st.columns(2)
        with col1:
            register_button = st.form_submit_button("✅ Register & Analyze", use_container_width=True)
        with col2:
            cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)

    if register_button:
        if medical_history.strip():
            # Register new patient
            patient_id = create_patient(
                st.session_state.temp_patient_data['name'],
                st.session_state.temp_patient_data['national_id'],
                st.session_state.temp_patient_data['age'],
                st.session_state.temp_patient_data['gender']
            )

            if patient_id:
                # Add medical history
                add_medical_history(st.session_state.temp_patient_data['national_id'], medical_history)

                st.success("✅ Patient registered successfully!")

                # Run analysis
                crew_result = run_medical_crew_analysis(
                    st.session_state.temp_patient_data['name'],
                    st.session_state.temp_patient_data['age'],
                    st.session_state.temp_patient_data['gender'],
                    st.session_state.temp_patient_data['symptoms'],
                    st.session_state.temp_patient_data['national_id']
                )

                if crew_result:
                    st.session_state.crew_results = crew_result
                    st.session_state.analysis_complete = True
                    st.session_state.show_medical_history_form = False
                    st.rerun()
            else:
                st.error("❌ Error registering patient. National ID may already exist.")
        else:
            st.error("⚠️ Please provide medical history information.")

    if cancel_button:
        st.session_state.show_medical_history_form = False
        st.rerun()

# Display analysis results
if st.session_state.analysis_complete and st.session_state.crew_results:
    st.markdown('<h2 class="section-header">🎯 AI Analysis Results</h2>', unsafe_allow_html=True)

    # # Show the raw crew results
    # with st.expander("📊 Detailed Analysis Output", expanded=True):
    #     st.text_area("Analysis Results", st.session_state.crew_results, height=400)

    # Try to extract and display the HTML report if it exists
    try:
        # Check if final report file exists
        report_file_path = "Output/final_report.html"
        if os.path.exists(report_file_path):
            with open(report_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            st.markdown('<h3 class="section-header">📋 Medical Report</h3>', unsafe_allow_html=True)
            st.components.v1.html(html_content, height=600, scrolling=True)
        else:
            st.info("📄 HTML report file not generated. Showing text results above.")
    except Exception as e:
        st.warning(f"Could not load HTML report: {str(e)}")

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.crew_results = None
            st.session_state.show_medical_history_form = False
            st.rerun()

    with col2:
        if st.button("💾 Save Report", use_container_width=True):
            # Save results to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"medical_report_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(st.session_state.crew_results)
            st.success(f"Report saved as {filename}")

    with col3:
        if st.button("📊 View Patient History", use_container_width=True):
            if 'temp_patient_data' in st.session_state:
                national_id = st.session_state.temp_patient_data['national_id']
                history = get_patient_medical_history(national_id)
                if history:
                    st.markdown("### Patient Medical History")
                    for i, (description, timestamp) in enumerate(history, 1):
                        st.write(f"{i}. **{timestamp}**: {description}")
                else:
                    st.info("No medical history found.")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #7f8c8d; padding: 1rem;">'
    '🏥 AI Medical Analysis System | Powered by CrewAI Multi-Agent Framework'
    '</div>',
    unsafe_allow_html=True
)