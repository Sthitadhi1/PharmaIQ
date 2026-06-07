CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    treatment VARCHAR(255),
    risk_score FLOAT DEFAULT 0.0
);

CREATE TABLE clinical_trials (
    trial_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    phase VARCHAR(50) NOT NULL,
    completion_percentage FLOAT DEFAULT 0.0,
    dropout_probability FLOAT DEFAULT 0.0,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE sales_records (
    sales_id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    units_sold INT DEFAULT 0,
    revenue FLOAT DEFAULT 0.0,
    sales_date DATE
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    specialization VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    prescription_volume INT DEFAULT 0,
    engagement_score FLOAT DEFAULT 0.0
);
