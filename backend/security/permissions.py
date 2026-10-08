ROLE_PERMISSIONS = {
    'ADMIN': ['patient', 'trials', 'sales', 'doctors', 'executive', 'analytics', 'mlops', 'streaming', 'ai'],
    'CLINICAL_ANALYST': ['patient', 'trials', 'analytics'],
    'SALES_ANALYST': ['sales', 'doctors', 'analytics'],
    'EXECUTIVE': ['executive', 'analytics'],
    'DATA_SCIENTIST': ['patient', 'trials', 'sales', 'doctors', 'analytics', 'mlops', 'ai'],
    'BUSINESS_USER': ['sales', 'executive', 'analytics']
}
