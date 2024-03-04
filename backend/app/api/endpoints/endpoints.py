
from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.api.database.database_connection import get_db
from app.api.models.models import HiredEmployee, Job, Department
import csv
from app.api.endpoints.utils import process_csv_batches


router = APIRouter()

@router.get('/', tags=['Welcome'])
def root():
    return {'message': 'Welcome to Globant Challenge!'}

    
@router.post('/upload-hired_employee-v2/', tags=['Upload File'])
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        await process_csv_batches(file_content=content, db=db)
        return {'message': 'CSV file uploaded and data inserted successfully'}

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

        return {'message': 'CSV file uploaded and data inserted successfully'}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')

@router.post('/upload-hired_employee/', tags=['Upload File'])
async def upload_hired_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        decoded_content = content.decode('utf-8')

        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        rows = list(csv_reader)
        for row in rows:
            name=row[1] if row[1] != '' else None
            datetime=row[2] if row[2] != '' else None
            department_id=row[3] if row[3] != '' else None
            job_id=row[4] if row[4] != '' else None

            print(row[0], name, datetime, department_id, job_id)
            employee = HiredEmployee(id=row[0], name=name, datetime=datetime, department_id=department_id, job_id=job_id)
            db.add(employee)

        db.commit()

        return {'message': 'CSV file uploaded and data inserted successfully'}

    except Exception as e:
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

        return {'message': 'CSV file uploaded and data inserted successfully'}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')