import numpy as np
from typing import Dict, List, Any
import json

class RiskCalculator:
    def __init__(self):
        self.load_risk_models()
    
    def load_risk_models(self):
        """Load evidence-based risk models and coefficients"""
        # Simplified risk models based on established guidelines
        self.risk_models = {
            'hypertension': {
                'base_risk': 0.1,
                'age_factor': 0.02,
                'bmi_factor': 0.03,
                'family_history_factor': 0.15,
                'current_bp_factor': 0.25
            },
            'diabetes': {
                'base_risk': 0.08,
                'age_factor': 0.015,
                'bmi_factor': 0.04,
                'family_history_factor': 0.20,
                'gestational_diabetes_factor': 0.30,
                'hba1c_factor': 0.35
            }
            # Add other models...
        }
    
    def calculate_hypertension_risk(self, patient_data: Dict) -> Dict:
        """Calculate hypertension risk using evidence-based factors"""
        model = self.risk_models['hypertension']
        
        # Base risk
        risk = model['base_risk']
        
        # Age factor
        if patient_data['age'] > 45:
            risk += (patient_data['age'] - 45) * model['age_factor']
        
        # BMI factor
        if patient_data['bmi'] > 25:
            risk += (patient_data['bmi'] - 25) * model['bmi_factor']
        
        # Family history
        if patient_data.get('family_hypertension', False):
            risk += model['family_history_factor']
        
        # Current BP status
        if patient_data['systolic_bp'] > 120:
            risk += (patient_data['systolic_bp'] - 120) * model['current_bp_factor'] / 100
        
        risk_percentage = min(risk * 100, 95)  # Cap at 95%
        
        return {
            'risk_percentage': risk_percentage,
            'risk_level': self._categorize_risk(risk_percentage),
            'key_factors': self._identify_key_factors_hypertension(patient_data),
            'recommendations': self._get_hypertension_recommendations(patient_data)
        }
    
    def calculate_diabetes_risk(self, patient_data: Dict) -> Dict:
        """Calculate Type 2 diabetes risk"""
        model = self.risk_models['diabetes']
        
        risk = model['base_risk']
        
        # Age factor
        if patient_data['age'] > 40:
            risk += (patient_data['age'] - 40) * model['age_factor']
        
        # BMI factor
        if patient_data['bmi'] > 23:  # Lower threshold for diabetes
            risk += (patient_data['bmi'] - 23) * model['bmi_factor']
        
        # Family history
        if patient_data.get('family_diabetes', False):
            risk += model['family_history_factor']
        
        # Gestational diabetes history
        if patient_data.get('diabetes_history', False):
            risk += model['gestational_diabetes_factor']
        
        # HbA1c factor (most important)
        if patient_data['hba1c'] >= 5.7:
            risk += (patient_data['hba1c'] - 5.7) * model['hba1c_factor']
        
        risk_percentage = min(risk * 100, 95)
        
        return {
            'risk_percentage': risk_percentage,
            'risk_level': self._categorize_risk(risk_percentage),
            'key_factors': self._identify_key_factors_diabetes(patient_data),
            'recommendations': self._get_diabetes_recommendations(patient_data)
        }
    
    def calculate_kidney_disease_risk(self, patient_data: Dict) -> Dict:
        """Calculate chronic kidney disease risk"""
        # Base risk is low, but increases with diabetes and hypertension risk
        base_risk = 0.05
        
        # Get diabetes and hypertension risks
        diabetes_risk = self.calculate_diabetes_risk(patient_data)['risk_percentage'] / 100
        hypertension_risk = self.calculate_hypertension_risk(patient_data)['risk_percentage'] / 100
        
        # Kidney disease risk increases with these conditions
        risk = base_risk + (diabetes_risk * 0.3) + (hypertension_risk * 0.2)
        
        # Age factor
        if patient_data['age'] > 50:
            risk += (patient_data['age'] - 50) * 0.01
        
        risk_percentage = min(risk * 100, 80)
        
        return {
            'risk_percentage': risk_percentage,
            'risk_level': self._categorize_risk(risk_percentage),
            'key_factors': ['Diabetes risk', 'Hypertension risk', 'Age'],
            'recommendations': self._get_kidney_recommendations(patient_data)
        }
    
    def calculate_stroke_risk(self, patient_data: Dict) -> Dict:
        """Calculate stroke risk using modified risk factors"""
        base_risk = 0.03
        
        # Multiple cardiovascular risk factors
        risk = base_risk
        
        # Age (major factor)
        if patient_data['age'] > 45:
            risk += (patient_data['age'] - 45) * 0.015
        
        # Hypertension (strongest factor)
        if patient_data['systolic_bp'] > 140:
            risk += 0.25
        elif patient_data['systolic_bp'] > 120:
            risk += 0.1
        
        # Diabetes/Prediabetes
        if patient_data['hba1c'] >= 6.5:
            risk += 0.2
        elif patient_data['hba1c'] >= 5.7:
            risk += 0.1
        
        # Cholesterol
        if patient_data['ldl_cholesterol'] > 130:
            risk += 0.08
        
        # Gender (women have different risk profile)
        if patient_data['gender'] == 'Female' and patient_data['age'] > 45:
            risk += 0.05
        
        risk_percentage = min(risk * 100, 90)
        
        return {
            'risk_percentage': risk_percentage,
            'risk_level': self._categorize_risk(risk_percentage),
            'key_factors': self._identify_stroke_factors(patient_data),
            'recommendations': self._get_stroke_recommendations(patient_data)
        }
    
    def calculate_heart_disease_risk(self, patient_data: Dict) -> Dict:
        """Calculate ischemic heart disease risk"""
        # Use simplified Framingham-based approach
        base_risk = 0.04
        
        risk = base_risk
        
        # Age and gender specific risks
        if patient_data['gender'] == 'Female':
            if patient_data['age'] > 45:
                risk += (patient_data['age'] - 45) * 0.012
        else:
            if patient_data['age'] > 35:
                risk += (patient_data['age'] - 35) * 0.015
        
        # Cholesterol ratios
        total_hdl_ratio = patient_data['total_cholesterol'] / patient_data['hdl_cholesterol']
        if total_hdl_ratio > 5:
            risk += 0.15
        elif total_hdl_ratio > 4:
            risk += 0.08
        
        # Blood pressure
        if patient_data['systolic_bp'] > 140:
            risk += 0.2
        elif patient_data['systolic_bp'] > 130:
            risk += 0.1
        
        # Diabetes/Prediabetes
        if patient_data['hba1c'] >= 6.5:
            risk += 0.25
        elif patient_data['hba1c'] >= 5.7:
            risk += 0.12
        
        risk_percentage = min(risk * 100, 90)
        
        return {
            'risk_percentage': risk_percentage,
            'risk_level': self._categorize_risk(risk_percentage),
            'key_factors': self._identify_heart_disease_factors(patient_data),
            'recommendations': self._get_heart_disease_recommendations(patient_data)
        }
    
    def calculate_all_risks(self, patient_data: Dict) -> Dict:
        """Calculate all risk assessments"""
        return {
            'hypertension': self.calculate_hypertension_risk(patient_data),
            'diabetes': self.calculate_diabetes_risk(patient_data),
            'kidney_disease': self.calculate_kidney_disease_risk(patient_data),
            'stroke': self.calculate_stroke_risk(patient_data),
            'heart_disease': self.calculate_heart_disease_risk(patient_data)
        }
    
    def _categorize_risk(self, risk_percentage: float) -> str:
        if risk_percentage >= 60:
            return "HIGH"
        elif risk_percentage >= 30:
            return "MODERATE"
        else:
            return "LOW"
    
    def _identify_key_factors_hypertension(self, patient_data: Dict) -> List[str]:
        factors = []
        if patient_data['systolic_bp'] > 130:
            factors.append("Elevated blood pressure")
        if patient_data['bmi'] > 25:
            factors.append("Overweight BMI")
        if patient_data.get('family_hypertension'):
            factors.append("Family history")
        if patient_data['age'] > 45:
            factors.append("Age factor")
        return factors
    
    def _identify_key_factors_diabetes(self, patient_data: Dict) -> List[str]:
        factors = []
        if patient_data['hba1c'] >= 5.7:
            factors.append("Prediabetic HbA1c")
        if patient_data.get('diabetes_history'):
            factors.append("Gestational diabetes history")
        if patient_data.get('family_diabetes'):
            factors.append("Family history")
        if patient_data['bmi'] > 25:
            factors.append("BMI")
        return factors
    
    def _identify_stroke_factors(self, patient_data: Dict) -> List[str]:
        factors = []
        if patient_data['systolic_bp'] > 130:
            factors.append("Blood pressure")
        if patient_data['hba1c'] >= 5.7:
            factors.append("Glucose control")
        if patient_data['ldl_cholesterol'] > 100:
            factors.append("Cholesterol")
        if patient_data['age'] > 45:
            factors.append("Age")
        return factors
    
    def _identify_heart_disease_factors(self, patient_data: Dict) -> List[str]:
        factors = []
        if patient_data['total_cholesterol'] / patient_data['hdl_cholesterol'] > 4:
            factors.append("Cholesterol ratio")
        if patient_data['systolic_bp'] > 130:
            factors.append("Blood pressure")
        if patient_data['hba1c'] >= 5.7:
            factors.append("Glucose levels")
        return factors
    
    # Add recommendation methods for each condition
    def _get_hypertension_recommendations(self, patient_data: Dict) -> List[str]:
        return [
            "DASH diet implementation",
            "Regular aerobic exercise",
            "Weight management",
            "Sodium restriction",
            "Stress management"
        ]
    
    def _get_diabetes_recommendations(self, patient_data: Dict) -> List[str]:
        return [
            "Structured meal planning",
            "Regular glucose monitoring",
            "Weight loss program",
            "Diabetes prevention program",
            "Regular physical activity"
        ]
    
    def _get_kidney_recommendations(self, patient_data: Dict) -> List[str]:
        return [
            "Blood pressure control",
            "Diabetes prevention",
            "Annual kidney function tests",
            "Adequate hydration",
            "Avoid nephrotoxic medications"
        ]
    
    def _get_stroke_recommendations(self, patient_data: Dict) -> List[str]:
        return [
            "Blood pressure management",
            "Cholesterol control",
            "Regular cardio exercise",
            "Antiplatelet therapy consideration",
            "Stroke symptom education"
        ]
    
    def _get_heart_disease_recommendations(self, patient_data: Dict) -> List[str]:
        return [
            "Cardiac risk factor modification",
            "Regular exercise program",
            "Heart-healthy diet",
            "Cholesterol management",
            "Regular cardiac screening"
        ]
