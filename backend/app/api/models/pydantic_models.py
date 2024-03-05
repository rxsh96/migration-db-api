from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

class DepartmentBase(BaseModel):
    department: str

class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    job: str

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True

class HiredEmployeeBase(BaseModel):
    name: Optional[str] = None
    datetime: datetime
    department_id: Optional[int] = None
    job_id: Optional[int] = None

class HiredEmployee(HiredEmployeeBase):
    id: int

    class Config:
        orm_mode = True


class DepartmentJobSummary(BaseModel):
    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int

class DepartmentJobSummaryList(BaseModel):
    data: List[DepartmentJobSummary]


class DepartmentHiredSummary(BaseModel):
    id: int
    department: str
    hired: int

class DepartmentHiredSummaryList(BaseModel):
    data: List[DepartmentHiredSummary]