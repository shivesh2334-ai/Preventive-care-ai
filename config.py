import os
from typing import Dict, Any

# API Configuration
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', 'your-claude-api-key-here')

# Application Configuration
APP_CONFIG = {
    'title': 'AI-Powered Preventive Care Risk Assessment',
    'description': 'Comprehensive health risk assessment using AI',
    'version': '1.0.0',
    'author': 'Healthcare AI Team'
}

# Risk Thresholds
RISK_THRESHOLDS = {
    'low': 30,
    'moderate': 60,
    'high': 100
}

# Database Configuration (if using database)
DATABASE_CONFIG = {
    'type': 'sqlite',  # or postgresql, mysql
    'path': 'patient_data.db',
    'echo': False
}

# Security Settings
SECURITY_CONFIG = {
    'encrypt_patient_data': True,
    'session_timeout_minutes': 30,
    'max_file_size_mb': 10
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'app.log'
}
