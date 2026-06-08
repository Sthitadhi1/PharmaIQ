from datetime import datetime
import json


def produce_sales_event(region: str, revenue: float):
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'region': region,
        'revenue': revenue
    }
    print(json.dumps(event))
