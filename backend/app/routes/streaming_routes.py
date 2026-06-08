from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.streaming.kafka_producer import KafkaProducerClient

router = APIRouter(prefix='/api/stream', tags=['Streaming'])


class PatientEvent(BaseModel):
    patient_id: int
    status: str


class SalesEvent(BaseModel):
    region: str
    revenue: float


@router.post('/patient-event')
def publish_patient_event(event: PatientEvent):
    producer = KafkaProducerClient(topic='patient_updates')
    success = producer.send(f'patient_id={event.patient_id}&status={event.status}')
    if not success:
        raise HTTPException(status_code=503, detail='Kafka producer unavailable')
    return {'status': 'sent', 'topic': 'patient_updates', 'payload': event.dict()}


@router.post('/sales-event')
def publish_sales_event(event: SalesEvent):
    producer = KafkaProducerClient(topic='sales_events')
    success = producer.send(f'region={event.region}&revenue={event.revenue}')
    if not success:
        raise HTTPException(status_code=503, detail='Kafka producer unavailable')
    return {'status': 'sent', 'topic': 'sales_events', 'payload': event.dict()}
