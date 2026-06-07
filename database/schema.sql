CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    disease VARCHAR(100),
    treatment_history TEXT,
    risk_score FLOAT
);

CREATE TABLE clinical_trials (
    trial_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    phase VARCHAR(50),
    location VARCHAR(100),
    completion_rate FLOAT,
    dropout_probability FLOAT,
    side_effects TEXT,
    treatment_duration INT,
    previous_missed_visits INT
);

CREATE TABLE sales (
    sales_id SERIAL PRIMARY KEY,
    medicine VARCHAR(100),
    region VARCHAR(100),
    units_sold INT,
    revenue FLOAT,
    date DATE
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    region VARCHAR(100),
    prescription_volume INT,
    patient_count INT,
    engagement_score FLOAT
);
