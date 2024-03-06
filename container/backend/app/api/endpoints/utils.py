
from io import BytesIO
from fastapi.responses import JSONResponse
import pandas as pd
from sqlalchemy.orm import Session
from app.api.models.alchemy_models import Department, Job, HiredEmployee
from sqlalchemy.orm import Session


def get_departments_util(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Department).offset(skip).limit(limit).all()

def get_jobs_util(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Job).offset(skip).limit(limit).all()

def get_employees_util(db: Session, skip: int = 0, limit: int = 10):
    return db.query(HiredEmployee).offset(skip).limit(limit).all()

async def process_csv_batches(file_content: bytes, db: Session, batch_size: int = 1000):
    try:
        df_chunks = pd.read_csv(BytesIO(file_content), header=None, chunksize = batch_size)
        for chunk in df_chunks:
            await batch_upload_files(data=chunk, db=db)
    except Exception as e:
        return JSONResponse(content={'message': f'Error: {str(e)}'}, status_code=500)
    
async def batch_upload_files(data, db: Session):
    try:
        data_list = data.values.tolist()
        for row in data_list:
            name=row[1] if not pd.isna(row[1]) else None
            datetime=row[2] if not pd.isna(row[2]) else None
            department_id=int(row[3]) if not pd.isna(row[3]) else None
            job_id=int(row[4]) if not pd.isna(row[4]) else None
            print(row[0], name, datetime, department_id, job_id)
            employee = HiredEmployee(id=row[0], name=name, datetime=datetime, department_id=department_id, job_id=job_id)
            db.add(employee)
        db.commit()
        return {'message': f'{len(data)} rows successfully uploaded.'}
    except Exception as e:
        db.rollback()
        return JSONResponse(content={'message': f'Error: {str(e)}'}, status_code=500)