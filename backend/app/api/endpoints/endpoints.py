
from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.api.database.database_connection import get_db
from app.api.models.models import Job, Department
import csv
from app.api.endpoints.utils import process_csv_batches


router = APIRouter()

@router.get('/', tags=['Welcome'])
def root():
    return {'message': 'Welcome to Globant Challenge!'}

    
@router.post('/upload-hired_employees/', tags=['Upload File'])
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        await process_csv_batches(file_content=content, db=db)
        return {'message': f'CSV file {file.filename} uploaded and data inserted successfully'}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
    

@router.post('/upload-departments/', tags=['Upload File'])
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        decoded_content = content.decode('utf-8')
        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        rows = list(csv_reader)
        for row in rows:
            print(row)
            department = Department(id=row[0], department=row[1])
            db.add(department)
        db.commit()
        return {'message': f'CSV file {file.filename} uploaded and data inserted successfully'}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')


@router.post('/upload-jobs/', tags=['Upload File'])
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        decoded_content = content.decode('utf-8')
        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        rows = list(csv_reader)
        for row in rows:
            print(row)
            job = Job(id=row[0], job=row[1])
            db.add(job)
        db.commit()
        return {'message': f'CSV file {file.filename} uploaded and data inserted successfully'}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')