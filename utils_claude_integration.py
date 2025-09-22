import anthropic
from typing import Dict, Any
import json

class ClaudeIntegration:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def get_risk_insights(self, patient_data: Dict, risk_results: Dict) -> str:
        """Get AI-powered clinical insights from Claude"""
        prompt = self._create_analysis_prompt(patient_data, risk_results)
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"AI analysis temporarily unavailable. Error: {str(e)}"
    
    def _create_analysis_prompt(self, patient_data: Dict, risk_results: Dict) -> str:
        return f"""
        As a preventive care specialist, analyze this patient's risk profile and provide clinical insights:

        Patient Profile:
        - Age: {patient_data['age']}, Gender: {patient_data['gender']}
        - BMI: {patient_data['bmi']:.1f}
        - BP: {patient_data['systolic_bp']}/{patient_data['diastolic_bp']} mmHg
        - HbA1c: {patient_data['hba1c']}%
        - Total Cholesterol: {patient_data['total_cholesterol']} mg/dL
        - LDL: {patient_data['ldl_cholesterol']} mg/dL
        - Family History: Diabetes={patient_data.get('family_diabetes', False)}, 
          Hypertension={patient_data.get('family_hypertension', False)}
        - Personal History: Gestational Diabetes={patient_data.get('diabetes_history', False)}

        Risk Assessment Results:
        - Hypertension: {risk_results['hypertension']['risk_percentage']:.1f}%
        - Diabetes: {risk_results['diabetes']['risk_percentage']:.1f}%
        - Kidney Disease: {risk_results['kidney_disease']['risk_percentage']:.1f}%
        - Stroke: {risk_results['stroke']['risk_percentage']:.1f}%
        - Heart Disease: {risk_results['heart_disease']['risk_percentage']:.1f}%

        Please provide:
        1. Key clinical insights about interconnected risks
        2. Priority interventions based on risk profile
        3. Specific recommendations for this patient
        4. Timeline for reassessment

        Focus on evidence-based recommendations and explain the rationale.
        """

    def get_personalized_recommendations(self, patient_data: Dict, condition: str) -> str:
        """Get personalized recommendations for specific conditions"""
        prompt = f"""
        Provide personalized prevention recommendations for {condition} based on this patient profile:
        
        {json.dumps(patient_data, indent=2)}
        
        Include specific, actionable recommendations for:
        1. Lifestyle modifications
        2. Monitoring parameters
        3. When to seek medical attention
        4. Evidence-based preventive measures
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=800,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Recommendations temporarily unavailable. Error: {str(e)}"
