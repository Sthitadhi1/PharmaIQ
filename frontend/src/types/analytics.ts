export type NameValue = { name: string; value: number };

export type Overview = {
  total_patients: number;
  high_risk_patients: number;
  high_risk_pct: number;
  trial_participants: number;
  active_trial_participants: number;
  trial_dropout_rate: number;
  total_revenue: number;
  revenue_forecast_3m: number;
  recent_growth_pct: number;
  total_doctors: number;
  avg_engagement: number;
  high_value_doctors: number;
  last_updated: string;
};

export type PatientAnalytics = {
  total_patients: number;
  high_risk_patients: number;
  high_risk_pct: number;
  avg_age: number;
  avg_adherence: number;
  diabetic_pct: number;
  risk_distribution: NameValue[];
  by_age_group: Array<{ age_group: string; patients: number; high_risk: number; high_risk_pct: number }>;
  by_risk_level: Array<{
    risk_level: string;
    patients: number;
    avg_adherence: number;
    avg_admissions: number;
    avg_cholesterol: number;
    avg_blood_pressure: number;
  }>;
  by_gender: Array<{ gender: string; patients: number; high_risk: number }>;
};

export type TrialGroup = { participants: number; dropouts: number; dropout_rate: number; completion_rate: number };

export type TrialAnalytics = {
  participants: number;
  active_participants: number;
  dropouts: number;
  dropout_rate: number;
  completion_rate: number;
  avg_duration_days: number;
  high_side_effect_participants: number;
  by_phase: Array<TrialGroup & { phase: string }>;
  by_side_effects: Array<TrialGroup & { side_effects: string }>;
  by_duration: Array<TrialGroup & { duration_group: string }>;
  by_age_group: Array<TrialGroup & { age_group: string }>;
};

export type SalesGroup = { revenue: number; units: number; marketing: number; roi: number; share_pct: number };

export type SalesForecast = {
  method: string;
  monthly_trend: number;
  forecast: Array<{ month: string; revenue: number }>;
  next_3_months_revenue: number;
};

export type SalesAnalytics = {
  total_revenue: number;
  total_units: number;
  total_marketing: number;
  roi: number;
  recent_growth_pct: number;
  period: { start: string; end: string };
  monthly: Array<{ month: string; revenue: number; units: number; marketing: number; complete: boolean }>;
  by_region: Array<SalesGroup & { region: string }>;
  by_medicine: Array<SalesGroup & { medicine: string }>;
  forecast: SalesForecast;
};

export type DoctorGroup = { doctors: number; avg_engagement: number; sales: number; prescriptions: number };

export type DoctorAnalytics = {
  total_doctors: number;
  avg_engagement: number;
  total_sales_generated: number;
  high_value_doctors: number;
  segments: Array<DoctorGroup & { segment: string }>;
  by_specialization: Array<DoctorGroup & { specialization: string }>;
  by_region: Array<DoctorGroup & { region: string }>;
  top_doctors: Array<{
    doctor_id: number;
    specialization: string;
    region: string;
    engagement_score: number;
    sales_generated: number;
    segment: string;
  }>;
};

export type Recommendation = { area: string; text: string };

export type MonitoringStatus = {
  models: Array<{ name: string; metric: string; accuracy: string; value: number | null; status: string; trained_at: string | null; drift: string }>;
  data_drift: { dataset: string; feature: string; method: string; psi: number; status: string };
};

export type AnomalyResult = {
  type: string;
  anomaly: boolean;
  count: number;
  records_checked: number;
  method: string;
  message: string;
  items: Array<Record<string, string | number>>;
};
