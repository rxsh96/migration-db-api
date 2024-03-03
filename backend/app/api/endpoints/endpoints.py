from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.api.database.database_connection import get_db
from app.api.models.models import HiredEmployee, Job, Department
import csv


router = APIRouter()

@router.get('/', tags=['Welcome'])
def root():
    return {'message': 'Welcome to Globant Challenge!'}

@router.post('/upload-hired_employee/', tags=['Hired Employees'])
async def upload_hired_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        decoded_content = content.decode('utf-8')

        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        rows = list(csv_reader)

        for row in rows:
            print(row)
            employee = HiredEmployee(id=row[0], name=row[1], datetime=row[2], department_id=row[3], job_id=row[4])
            db.add(employee)

        db.commit()

        return {'message': 'CSV file uploaded and data inserted successfully'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
