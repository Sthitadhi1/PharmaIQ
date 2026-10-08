FROM python:3.14-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend /app/backend
COPY ml_engine /app/ml_engine
COPY database /app/database
# The datasets every analytics endpoint and the AI assistant read from.
COPY patients.csv clinical_trials.csv pharma_sales.csv doctors.csv /app/

# Bake trained model artifacts into the image so /api/ml/* works out of the box.
RUN cd /app && python -m ml_engine.training.train_all

WORKDIR /app/backend
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
