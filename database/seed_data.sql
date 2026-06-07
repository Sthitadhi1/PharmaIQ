INSERT INTO users (name, email, role) VALUES
('Admin User', 'admin@pharmaiq.com', 'admin');

INSERT INTO patients (age, gender, disease, treatment, risk_score) VALUES
(52, 'Female', 'Diabetes', 'Metformin', 0.0),
(38, 'Male', 'Hypertension', 'Lisinopril', 0.0);

INSERT INTO clinical_trials (patient_id, phase, completion_percentage, dropout_probability) VALUES
(1, 'Phase II', 72.5, 0.0),
(2, 'Phase III', 85.0, 0.0);

INSERT INTO sales_records (medicine_name, region, units_sold, revenue, sales_date) VALUES
('Medicine A', 'North', 4500, 180000.0, '2026-05-01'),
('Medicine B', 'South', 3800, 152000.0, '2026-05-01');

INSERT INTO doctors (specialization, region, prescription_volume, engagement_score) VALUES
('Cardiology', 'West', 980, 89.2),
('Endocrinology', 'East', 740, 72.5);
