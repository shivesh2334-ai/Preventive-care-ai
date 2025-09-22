# AI-Powered Preventive Care Risk Assessment

A comprehensive web application that uses AI to assess patient risk for major health conditions and provide personalized prevention strategies.

## Features

- 🧠 **AI-Powered Analysis**: Integration with Claude AI for intelligent risk assessment
- 📊 **Comprehensive Risk Assessment**: Evaluates risk for 6 major health conditions
- 🎯 **Personalized Recommendations**: Evidence-based prevention strategies
- 📱 **User-Friendly Interface**: Intuitive Streamlit-based web application
- 🔒 **Secure Data Handling**: Patient data protection and validation

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/preventive-care-ai.git
   cd preventive-care-ai

   **Create virtual environment :** 
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install dependencies**
pip install -r requirements.txt

**Set up environment variables:**
cp .env.example .env
# Edit .env file and add your Claude API key

**Start the application:**
streamlit run app.py

**Risk Calculator API**
from utils.risk_calculator import RiskCalculator

calculator = RiskCalculator()
risk_results = calculator.calculate_all_risks(patient_data)


**Claude Integration API**
from utils.claude_integration import ClaudeIntegration

claude = ClaudeIntegration(api_key)
insights = claude.get_risk_insights(patient_data, risk_results)


**Testing**
pytest tests/
**Streamlit Cloud Deployment**
git add .
git commit -m "Initial deployment"
git push origin main




