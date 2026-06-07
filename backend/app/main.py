from fastapi import FastAPI
from app.routes import auth, patients, clinical, sales, doctors, analytics

app = FastAPI(title='PharmaIQ API', version='0.1.0')

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(patients.router, prefix='', tags=['patients'])
app.include_router(clinical.router, prefix='', tags=['clinical'])
app.include_router(sales.router, prefix='', tags=['sales'])
app.include_router(doctors.router, prefix='', tags=['doctors'])
app.include_router(analytics.router, prefix='/analytics', tags=['analytics'])

@app.get('/')
def root():
    return {'message': 'Welcome to PharmaIQ API'}
