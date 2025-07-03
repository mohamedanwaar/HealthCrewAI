# 🏥 AI Medical Analysis System

An intelligent medical analysis system powered by CrewAI that automates patient data processing, medical history retrieval, and clinical assessment. The system generates comprehensive medical reports to assist healthcare providers in making informed clinical decisions.

## 📌 Features

- 🤖 Multi-agent system using CrewAI framework
- 👤 Patient data extraction and standardization
- 📋 Medical history retrieval and analysis
- 🔍 Symptom evaluation and clinical assessment
- 📊 Professional HTML medical report generation
- 💾 SQLite database for patient records
- 🎯 Risk assessment and urgency classification
- 📈 Chronic condition identification
- 🔄 Sequential workflow automation
- 🖥️ Streamlit-based user interface

## 📸 GUI Screenshots

### Patient Information Form
![Patient Form](https://via.placeholder.com/800x400/3498db/ffffff?text=Patient+Information+Form)

### Medical History Registration
![Medical History](https://via.placeholder.com/800x400/e74c3c/ffffff?text=Medical+History+Registration)

### AI Analysis Results
![Analysis Results](https://via.placeholder.com/800x400/27ae60/ffffff?text=AI+Analysis+Results)

### Medical Report Display
![Medical Report](https://via.placeholder.com/800x400/f39c12/ffffff?text=Medical+Report+Display)

## 📂 Project Structure

```
ai-medical-analysis-system/
├── 🐍 Agents.py             # Agent definitions and configurations
├── 📋 Tasks.py              # Task definitions and data models
├── 🛠️ Tools.py              # Database tools and utilities
├── 🖥️ MainApp.py            # Streamlit GUI implementation
├── 💾 db.py                 # Database operations and schema
├── 📝 requirements.txt      # Project dependencies
├── 📄 .env                  # Environment variables
├── 🗄️ medical_assistant.db  # SQLite database
└── 📁 Output/               # Generated reports directory
    ├── PatientData.json     # Agent 1 output
    ├── agentHistory.json    # Agent 2 output
    ├── agentSummary.json    # Agent 3 output
    └── final_report.html    # Agent 4 output
```

## 🛠 Installation

### **1️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **2️⃣ Set Up Environment Variables**

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key
# Or for OpenRouter
OPENAI_API_KEY=your_openrouter_api_key
```

### **3️⃣ Initialize Database**

The system will automatically create the SQLite database on first run, but you can manually initialize it:

```bash
python -c "from db import init_database; init_database()"
```

## 🖥️ Running the Project

### **1. Start the Streamlit GUI**

```bash
streamlit run MainApp.py
```

### **2. Access the Application**

Open your browser and navigate to:
```
http://localhost:8501
```

## 🔧 How It Works

### **CrewAI Structure**

The system utilizes four specialized AI agents working in sequence:

1. **Medical Data Extractor Agent**: Processes patient information and symptoms
- Output: `PatientData.json`

   ```json
    {
  "name": "Mohamed Rashed",
  "age": 21,
  "gender": "Male",
  "symptoms": ["Fatigue", "Daily headaches"]
    }
   ```

2. **Medical History Specialist Agent**: Retrieves and analyzes patient medical history
- Output: `agentHistory.json`

   ```json
   {
  "patient_info": {
    "name": "Mohamed Rashed",
    "age": 21,
    "gender": "Male",
    "current_symptoms": ["Fatigue", "Daily headaches"]
  },
  "medical_history": [
    {
      "date": "2025-06-29",
      "description": "Diagnosed with high blood pressure during routine checkup. Prescribed amlodipine 5mg daily."
    }
  ],
  "chronic_conditions": ["Hypertension"],
  "allergies": []
    }

   ```


3. **Medical Symptom Evaluator Agent**: Analyzes clinical data and provides assessment
- Output: `agentSummary.json`

    ```json
    {
    "patient_summary": {
        "name": "Mohamed Rashed",
        "age": 21,
        "gender": "Male",
        "current_symptoms": ["Fatigue", "Daily headaches"],
        "medical_history_summary": [
        "Diagnosed with hypertension in June 2025 and prescribed amlodipine"
        ]
    },
    "clinical_assessment": {
        "symptom_analysis": "Patient presents with persistent fatigue and daily headaches, which could be related to his known hypertension or possible medication side effects. The symptoms may also suggest secondary hypertension causes or other underlying conditions.",
        "potential_diagnoses": ["Hypertensive encephalopathy", "Medication side effects", "Sleep disorder"],
        "risk_factors": ["Young age hypertension", "Possible uncontrolled BP", "Chronic medication use"],
        "severity_assessment": "moderate",
        "urgency_level": "urgent"
    },
    "recommendations": {
        "immediate_actions": ["BP measurement", "Medication review"],
        "follow_up_care": ["24-hour BP monitoring", "Sleep evaluation"],
        "additional_tests": ["Renal function tests", "Thyroid function tests", "Electrolyte panel"],
        "precautions": []
    }
    }
    ```


4. **Medical Report Generator Agent**: Creates professional HTML medical reports
   - Output: `final_report.html`
   - Styled HTML report with comprehensive medical information

### **File Breakdown**

- **Agents.py**: Defines the four specialized medical agents and their configurations
- **Tasks.py**: Contains task definitions and Pydantic data models for structured output
- **Tools.py**: Implements database tools for patient history retrieval
- **MainApp.py**: Implements the Streamlit-based user interface
- **db.py**: Handles SQLite database operations and patient record management
- **requirements.txt**: Lists all project dependencies

## 🎮 Running the Application

### **1️⃣ Start the GUI**

Launch the Streamlit interface:
```bash
streamlit run MainApp.py
```

### **2️⃣ Patient Registration/Analysis**

#### **For Existing Patients:**
1. Enter patient information (Name, Age, Gender, National ID, Symptoms)
2. Click "Analyze Patient"
3. System retrieves existing medical history and performs analysis

#### **For New Patients:**
1. Enter patient information
2. System prompts for medical history registration
3. Provide detailed medical history
4. Click "Register & Analyze"

### **3️⃣ View Results**

After analysis, the system generates:
1. **Patient Data Extraction** (saved as `PatientData.json`)
2. **Medical History Analysis** (saved as `agentHistory.json`)
3. **Clinical Assessment** (saved as `agentSummary.json`)
4. **Professional Medical Report** (saved as `final_report.html`)

All output files are available in the `Output` directory.

## 🗄️ Database Schema

### **Patients Table**
```sql
CREATE TABLE patients (
    national_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Medical History Table**
```sql
CREATE TABLE medical_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    national_id TEXT NOT NULL,
    description TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (national_id) REFERENCES patients (national_id)
);
```

## 🔑 Key Features

### **Multi-Agent Collaboration**
- **Agent 1**: Extracts and standardizes patient data
- **Agent 2**: Retrieves and analyzes medical history
- **Agent 3**: Performs clinical assessment and risk evaluation
- **Agent 4**: Generates professional medical reports

### **Intelligent Analysis**
- Symptom standardization and medical terminology
- Chronic condition identification
- Allergy detection and precautions
- Risk factor assessment
- Urgency level classification

### **Professional Output**
- Structured JSON data for each analysis step
- Comprehensive HTML medical reports
- Clinical recommendations and follow-up actions
- Risk assessment and safety precautions

## 🚀 Advanced Features

### **Patient Management**
- Automatic patient registration
- Medical history tracking
- National ID-based patient identification
- Historical data preservation

### **Clinical Decision Support**
- Evidence-based symptom analysis
- Differential diagnosis suggestions
- Risk stratification
- Treatment recommendations

### **Report Generation**
- Professional HTML formatting
- Comprehensive clinical summaries
- Actionable recommendations
- Risk factor documentation

## 🔧 Configuration

### **LLM Configuration**
The system supports multiple LLM providers:
- OpenAI GPT models
- OpenRouter models
- Custom API endpoints

### **Database Configuration**
- SQLite database for local storage
- Automatic schema initialization
- Data integrity constraints
- Foreign key relationships

## 📊 Output Examples

### **Patient Data JSON**
```json
{
  "name": "Sarah Johnson",
  "age": 28,
  "gender": "Female",
  "symptoms": ["migraine", "nausea", "photophobia"]
}
```

### **Clinical Assessment**
```json
{
  "clinical_assessment": {
    "symptom_analysis": "Classic migraine presentation with aura symptoms",
    "potential_diagnoses": ["Migraine with aura", "Tension headache"],
    "severity_assessment": "moderate",
    "urgency_level": "routine"
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


---

**🏥 AI Medical Analysis System | Powered by CrewAI Multi-Agent Framework** 