export type Patient = {
  patient_id: number;
  name: string;
  age: number;
  gender: string;
  disease: string;
  risk_score: number;
};

export type ClinicalTrial = {
  trial_id: number;
  patient_id: number;
  phase: string;
  location: string;
  completion_rate: number;
  dropout_probability: number;
};

export type SalesRecord = {
  sales_id: number;
  medicine: string;
  region: string;
  units_sold: number;
  revenue: number;
  date: string;
};

export type Doctor = {
  doctor_id: number;
  name: string;
  specialization: string;
  region: string;
  prescription_volume: number;
  patient_count: number;
  engagement_score: number;
};
