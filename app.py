import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from utils.risk_calculator import RiskCalculator
from utils.data_validator import DataValidator
from utils.claude_integration import ClaudeIntegration
import config

# Page configuration
st.set_page_config(
    page_title="AI-Powered Preventive Care Risk Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.risk-card {
    padding: 1rem;
    margin: 0.5rem;
    border-radius: 10px;
    border-left: 5px solid;
}
.high-risk { border-left-color: #ff4444; background-color: #ffe6e6; }
.moderate-risk { border-left-color: #ffaa00; background-color: #fff4e6; }
.low-risk { border-left-color: #00cc44; background-color: #e6ffe6; }
</style>
""", unsafe_allow_html=True)

class PreventiveCareApp:
    def __init__(self):
        self.risk_calculator = RiskCalculator()
        self.data_validator = DataValidator()
        self.claude_integration = ClaudeIntegration(config.CLAUDE_API_KEY)
        
    def main(self):
        st.markdown('<h1 class="main-header">🏥 AI-Powered Preventive Care Risk Assessment</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Choose a page", 
                                   ["Patient Assessment", "Risk Analysis", "Prevention Plans", "About"])
        
        if page == "Patient Assessment":
            self.patient_assessment_page()
        elif page == "Risk Analysis":
            self.risk_analysis_page()
        elif page == "Prevention Plans":
            self.prevention_plans_page()
        else:
            self.about_page()
    
    def patient_assessment_page(self):
        st.header("📝 Patient Information Input")
        
        with st.form("patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Information")
                patient_id = st.text_input("Patient ID", value="78901")
                name = st.text_input("Name", value="Sarah Johnson")
                age = st.number_input("Age", min_value=18, max_value=100, value=45)
                gender = st.selectbox("Gender", ["Female", "Male", "Other"])
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
                
                st.subheader("Lifestyle Factors")
                smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
                alcohol = st.selectbox("Alcohol Consumption", 
                                     ["None", "Occasional", "Moderate", "Heavy"])
                exercise = st.selectbox("Exercise Level", 
                                      ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
                diet = st.selectbox("Diet Pattern", 
                                  ["Standard", "Mediterranean", "Plant-based", "Low-carb", "Other"])
            
            with col2:
                st.subheader("Medical History")
                diabetes_history = st.checkbox("Gestational Diabetes")
                depression_history = st.checkbox("Depression/Mental Health Issues")
                
                st.subheader("Family History")
                family_diabetes = st.checkbox("Family History - Diabetes")
                family_hypertension = st.checkbox("Family History - Hypertension") 
                family_cancer = st.selectbox("Family Cancer History", 
                                           ["None", "Breast", "Prostate", "Lung", "Colorectal", "Other"])
                
                st.subheader("Vital Signs")
                systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=200, value=128)
                diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=120, value=82)
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=150, value=72)
                
                st.subheader("Laboratory Results")
                fasting_glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=300, value=97)
                hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=15.0, value=5.7, step=0.1)
                total_cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=201)
                ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=300, value=120)
                hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=54)
                
            submitted = st.form_submit_button("Calculate Risk Assessment")
            
            if submitted:
                # Validate data
                patient_data = {
                    'patient_id': patient_id,
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'bmi': weight / ((height/100)**2),
                    'smoking': smoking,
                    'alcohol': alcohol,
                    'exercise': exercise,
                    'diet': diet,
                    'diabetes_history': diabetes_history,
                    'depression_history': depression_history,
                    'family_diabetes': family_diabetes,
                    'family_hypertension': family_hypertension,
                    'family_cancer': family_cancer,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                    'heart_rate': heart_rate,
                    'fasting_glucose': fasting_glucose,
                    'hba1c': hba1c,
                    'total_cholesterol': total_cholesterol,
                    'ldl_cholesterol': ldl_cholesterol,
                    'hdl_cholesterol': hdl_cholesterol
                }
                
                if self.data_validator.validate_patient_data(patient_data):
                    st.session_state.patient_data = patient_data
                    st.success("✅ Patient data saved successfully!")
                    st.info("🔍 Go to 'Risk Analysis' to see the assessment results.")
                else:
                    st.error("❌ Please check your input data for errors.")
    
    def risk_analysis_page(self):
        st.header("📊 Risk Analysis Results")
        
        if 'patient_data' not in st.session_state:
            st.warning("⚠️ Please complete patient assessment first.")
            return
        
        patient_data = st.session_state.patient_data
        
        # Calculate risks
        with st.spinner("🧠 AI is analyzing patient data..."):
            risk_results = self.risk_calculator.calculate_all_risks(patient_data)
            ai_insights = self.claude_integration.get_risk_insights(patient_data, risk_results)
        
        # Display patient summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Patient", patient_data['name'])
            st.metric("Age", f"{patient_data['age']} years")
        with col2:
            st.metric("BMI", f"{patient_data['bmi']:.1f}")
            st.metric("Blood Pressure", f"{patient_data['systolic_bp']}/{patient_data['diastolic_bp']}")
        with col3:
            st.metric("HbA1c", f"{patient_data['hba1c']}%")
            st.metric("Total Cholesterol", f"{patient_data['total_cholesterol']} mg/dL")
        
        # Risk visualization
        st.subheader("🎯 10-15 Year Risk Predictions")
        
        # Create risk gauge charts
        fig = go.Figure()
        
        conditions = ['Hypertension', 'Diabetes', 'Kidney Disease', 'Stroke', 'Heart Disease']
        risk_values = [risk_results[condition.lower().replace(' ', '_')]['risk_percentage'] 
                      for condition in conditions]
        
        colors = ['red' if r >= 60 else 'orange' if r >= 30 else 'green' for r in risk_values]
        
        fig = px.bar(x=conditions, y=risk_values, color=risk_values,
                    color_continuous_scale=['green', 'orange', 'red'],
                    title="Risk Assessment by Condition")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed risk cards
        st.subheader("📋 Detailed Risk Assessment")
        
        for condition in conditions:
            condition_key = condition.lower().replace(' ', '_')
            risk_data = risk_results[condition_key]
            risk_level = self._get_risk_level(risk_data['risk_percentage'])
            
            with st.container():
                st.markdown(f"""
                <div class="risk-card {risk_level.lower()}-risk">
                    <h4>{condition}</h4>
                    <p><strong>Risk Score:</strong> {risk_data['risk_percentage']:.1f}% over 10-15 years</p>
                    <p><strong>Risk Level:</strong> {risk_level}</p>
                    <p><strong>Key Factors:</strong> {', '.join(risk_data['key_factors'])}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # AI-powered insights
        if ai_insights:
            st.subheader("🤖 AI-Powered Clinical Insights")
            st.markdown(ai_insights)
        
        # Recommended investigations
        st.subheader("🔬 Recommended Investigations")
        investigations = self._get_recommended_investigations(patient_data, risk_results)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Immediate Tests:**")
            for test in investigations['immediate']:
                st.write(f"• {test}")
        
        with col2:
            st.markdown("**Follow-up Tests:**")
            for test in investigations['followup']:
                st.write(f"• {test}")
    
    def prevention_plans_page(self):
        st.header("🛡️ Personalized Prevention Plans")
        
        if 'patient_data' not in st.session_state:
            st.warning("⚠️ Please complete patient assessment first.")
            return
        
        patient_data = st.session_state.patient_data
        
        # Generate prevention recommendations
        prevention_plan = self._generate_prevention_plan(patient_data)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Lifestyle", "Medical", "Screening", "Follow-up"])
        
        with tab1:
            st.subheader("🏃‍♀️ Lifestyle Modifications")
            st.write("**Exercise Recommendations:**")
            for rec in prevention_plan['lifestyle']['exercise']:
                st.write(f"• {rec}")
            
            st.write("**Dietary Guidelines:**")
            for rec in prevention_plan['lifestyle']['diet']:
                st.write(f"• {rec}")
            
            st.write("**Stress Management:**")
            for rec in prevention_plan['lifestyle']['stress']:
                st.write(f"• {rec}")
        
        with tab2:
            st.subheader("💊 Medical Interventions")
            for intervention in prevention_plan['medical']:
                st.write(f"• {intervention}")
        
        with tab3:
            st.subheader("🔍 Screening Schedule")
            screening_df = pd.DataFrame(prevention_plan['screening'])
            st.dataframe(screening_df)
        
        with tab4:
            st.subheader("📅 Follow-up Timeline")
            for followup in prevention_plan['followup']:
                st.write(f"• {followup}")
    
    def about_page(self):
        st.header("ℹ️ About This Application")
        st.markdown("""
        ## AI-Powered Preventive Care Risk Assessment
        
        This application uses advanced AI and evidence-based medical guidelines to assess 
        patient risk for major health conditions and provide personalized prevention strategies.
        
        ### Features:
        - 🧠 Claude AI integration for intelligent risk analysis
        - 📊 Comprehensive risk assessment for 6 major conditions
        - 🎯 Personalized prevention recommendations
        - 📱 User-friendly interface with data validation
        - 🔒 Secure patient data handling
        
        ### Risk Conditions Assessed:
        1. **Hypertension** - Based on current BP, family history, lifestyle factors
        2. **Type 2 Diabetes** - Incorporating HbA1c, family history, BMI
        3. **Kidney Disease** - Considering diabetes/hypertension risk
        4. **Stroke** - Cardiovascular risk factors assessment
        5. **Ischemic Heart Disease** - Comprehensive cardiac risk evaluation
        6. **Cancer** - Family history and age-appropriate screening
        
        ### Technology Stack:
        - **Frontend:** Streamlit
        - **AI Integration:** Claude API
        - **Visualization:** Plotly
        - **Data Processing:** Pandas, NumPy
        
        ### Disclaimer:
        This tool is for educational and screening purposes only. Always consult with 
        healthcare professionals for medical decisions.
        """)
    
    def _get_risk_level(self, risk_percentage):
        if risk_percentage >= 60:
            return "HIGH"
        elif risk_percentage >= 30:
            return "MODERATE"
        else:
            return "LOW"
    
    def _get_recommended_investigations(self, patient_data, risk_results):
        investigations = {
            'immediate': [],
            'followup': []
        }
        
        # Based on risk levels and patient data
        if patient_data['hba1c'] >= 5.7:
            investigations['immediate'].extend(['Oral Glucose Tolerance Test', 'Fasting Insulin'])
        
        if patient_data['systolic_bp'] >= 130:
            investigations['immediate'].extend(['24-hour BP monitoring', 'ECG'])
        
        if patient_data['age'] >= 45:
            investigations['immediate'].extend(['Lipid Profile', 'Kidney Function Tests'])
        
        if patient_data['family_cancer'] == 'Breast':
            investigations['followup'].extend(['BRCA Gene Testing', 'Enhanced MRI Screening'])
        
        investigations['followup'].extend([
            'Annual HbA1c monitoring',
            'Cardiovascular risk assessment',
            'Cancer screening as per guidelines'
        ])
        
        return investigations
    
    def _generate_prevention_plan(self, patient_data):
        plan = {
            'lifestyle': {
                'exercise': [
                    'Increase to 150 minutes moderate aerobic activity per week',
                    'Add 2 days of strength training',
                    'Continue yoga practice for stress management',
                    'Include high-intensity interval training once weekly'
                ],
                'diet': [
                    'Implement structured meal timing',
                    'Follow Mediterranean or DASH diet pattern',
                    'Reduce sodium intake to <2300mg/day',
                    'Increase fiber intake to 25-30g/day',
                    'Limit processed foods and added sugars'
                ],
                'stress': [
                    'Continue regular yoga practice',
                    'Consider mindfulness meditation',
                    'Ensure 7-8 hours quality sleep',
                    'Work-life balance strategies'
                ]
            },
            'medical': [
                'Consider low-dose aspirin for cardiovascular prevention',
                'Monitor blood pressure regularly',
                'Vitamin D supplementation assessment',
                'Annual flu vaccination',
                'Consider statin therapy evaluation'
            ],
            'screening': [
                {'Test': 'Mammography', 'Frequency': 'Annual', 'Next Due': '2024-12-01'},
                {'Test': 'HbA1c', 'Frequency': '6 months', 'Next Due': '2024-08-01'},
                {'Test': 'Lipid Profile', 'Frequency': 'Annual', 'Next Due': '2024-12-01'},
                {'Test': 'Blood Pressure', 'Frequency': 'Monthly', 'Next Due': '2024-03-01'},
                {'Test': 'Colonoscopy', 'Frequency': '10 years', 'Next Due': '2029-01-01'}
            ],
            'followup': [
                'Primary care follow-up in 3 months',
                'Endocrinologist consultation for diabetes prevention',
                'Nutritionist consultation for meal planning',
                'Annual comprehensive physical examination',
                'Quarterly lifestyle progress review'
            ]
        }
        
        return plan

if __name__ == "__main__":
    app = PreventiveCareApp()
    app.main()
