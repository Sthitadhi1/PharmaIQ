"""Train every model the API serves.

Run from the repository root:
    python -m ml_engine.training.train_all
"""
from ml_engine.training import (
    train_doctor_model,
    train_patient_model,
    train_sales_model,
    train_trial_model,
)


def main():
    for train in (train_patient_model, train_trial_model, train_sales_model, train_doctor_model):
        train()
        print()


if __name__ == '__main__':
    main()
