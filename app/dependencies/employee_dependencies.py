from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService


def get_employee_repository(
    db: Session = Depends(get_db),
) -> EmployeeRepository:
    return EmployeeRepository(db)


def get_employee_service(
    repository: EmployeeRepository = Depends(get_employee_repository),
) -> EmployeeService:
    return EmployeeService(repository)