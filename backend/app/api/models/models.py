from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.api.database.base_class import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    employees = relationship('HiredEmployee', back_populates='department')

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    
    employees = relationship('HiredEmployee', back_populates='job')

class HiredEmployee(Base):
    __tablename__ = 'hired_employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    datetime = Column(String, index=True, nullable=False)

    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)

    department = relationship('Department', back_populates='employees')
    job = relationship('Job', back_populates='employees')
