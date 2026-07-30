from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    salary: float
    joining_date: date
    blood_group: str | None = None
    status: str = "Active"


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    status: Optional[str] = None



class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    status: str

    profile_image: Optional[str] = None

    class Config:
        from_attributes = True