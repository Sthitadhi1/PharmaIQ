from datetime import datetime
import json


def produce_patient_event(patient_id: int, status: str):
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'patient_id': patient_id,
        'status': status
    }
    print(json.dumps(event))
