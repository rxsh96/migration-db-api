from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.database_connection import get_db
from app.api.endpoints.utils import get_departments_util, get_employees_util, get_jobs_util
from app.api.models.pydantic_models import Department, DepartmentHiredSummary, DepartmentHiredSummaryList, DepartmentJobSummary, DepartmentJobSummaryList, Job, HiredEmployee
from sqlalchemy.sql import text

router = APIRouter()

@router.get('/', tags=['Get Methods'])
def root():
    return {'message': 'Welcome to Globant Challenge!'}

@router.get("/departments/", response_model=list[Department], tags=['Get Methods'])
def get_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    departments = get_departments_util(db, skip=skip, limit=limit)
    return departments

@router.get("/jobs/", response_model=list[Job], tags=['Get Methods'])
def get_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = get_jobs_util(db, skip=skip, limit=limit)
    return jobs

@router.get("/employees/", response_model=list[HiredEmployee], tags=['Get Methods'])
def get_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = get_employees_util(db, skip=skip, limit=limit)
    return employees

@router.get('/hired-avg/', response_model = DepartmentHiredSummaryList, tags=['Get Methods'])
def get_hired_average(year: int, db: Session = Depends(get_db)):
    try:
        query_results = db.execute(text('''
                WITH hired_employee_counting AS 
                (
                    SELECT 
                        d.id, 
                        d.department, 
                        COUNT(1) AS hired
                    FROM hired_employees he
                    INNER JOIN departments d
                        ON he.department_id = d.id
                    WHERE EXTRACT(YEAR FROM he.datetime) = :year
                    GROUP BY d.id, d.department
                ), hired_employee_average AS 
                (
                    SELECT AVG(hec.hired) AS avg_hired_employees
                    FROM hired_employee_counting AS hec
                ) 
                SELECT hec.*
                FROM hired_employee_counting hec, hired_employee_average hea
                WHERE hec.hired > hea.avg_hired_employees
                ORDER BY hec.hired DESC'''
                ), {"year": year})
        
        response_data = []
        for row in query_results:
            id=row.id
            department=row.department
            hired=row.hired
            response_data.append(DepartmentHiredSummary(id=id, department=department, hired=hired))

        return DepartmentHiredSummaryList(data=response_data)
    
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')


@router.get("/job-summary", response_model=DepartmentJobSummaryList, tags=['Get Methods'])
def get_department_job_summary(year: int, db: Session = Depends(get_db)):
    try:
        query_results = db.execute(text('''SELECT
                department,
                job,
                SUM(CASE WHEN quarter = 1 THEN num_employees_hired ELSE 0 END) AS q1,
                SUM(CASE WHEN quarter = 2 THEN num_employees_hired ELSE 0 END) AS q2,
                SUM(CASE WHEN quarter = 3 THEN num_employees_hired ELSE 0 END) AS q3,
                SUM(CASE WHEN quarter = 4 THEN num_employees_hired ELSE 0 END) AS q4
            FROM (
                    SELECT
                        d.department,
                        j.job,
                        EXTRACT(QUARTER FROM h.datetime) AS quarter,
                        COUNT(*) AS num_employees_hired
                    FROM hired_employees h
                    JOIN departments d 
                        ON h.department_id = d.id
                    JOIN jobs j 
                        ON h.job_id = j.id
                    WHERE
                        EXTRACT(YEAR FROM h.datetime) = :year
                    GROUP BY
                        d.department,
                        j.job,
                        EXTRACT(QUARTER FROM h.datetime)
                ) AS quarters_counter
            GROUP BY
                department,
                job
            ORDER BY
                department,
                job
        '''), {"year": year})

        response_data = []
        for row in query_results:
            department=row.department
            job=row.job
            q1=row.q1
            q2=row.q2
            q3=row.q3
            q4=row.q4
            response_data.append(DepartmentJobSummary(department=department, job=job, q1=q1, q2=q2, q3=q3, q4=q4))

        return DepartmentJobSummaryList(data=response_data)

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')