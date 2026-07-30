

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session


from app.models.employee import Employee
from typing import Optional

from app.schemas import employee
class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[Employee]:

        return (
            self.db.query(Employee)
            .filter(Employee.email == email)
            .first()
        )

    def get_by_id(
        self,
        employee_id: int
    ) -> Optional[Employee]:

        return (
            self.db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

    def get_all(
            self,
            search=None,
            department=None,
            status=None,
            min_salary=None,
            max_salary=None,
            sort_by=None,
            order="asc",
            limit=10,
            offset=0
        ) -> list[Employee]:
    
            query = self.db.query(Employee)
    
            if search:
                query = query.filter(
                    or_(
                        Employee.full_name.ilike(f"%{search}%"),
                        Employee.department.ilike(f"%{search}%"),
                        Employee.designation.ilike(f"%{search}%")
                    )
                )
    
            if department:
                query = query.filter(Employee.department == department)
    
            if status:
                query = query.filter(Employee.status == status)
    
            if min_salary is not None:
                query = query.filter(Employee.salary >= min_salary)
    
            if max_salary is not None:
                query = query.filter(Employee.salary <= max_salary)
    
            if sort_by:
                if not hasattr(Employee, sort_by):
                    raise ValueError("Invalid sort field")

                column = getattr(Employee, sort_by)
    
                if order.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))
    
            return (
                query
                .offset(offset)
                .limit(limit)
                .all()
            )

    def create(
        self,
        employee: Employee
    ) -> Employee:

        try:

            self.db.add(employee)

            self.db.commit()

            self.db.refresh(employee)

            return employee

        except Exception:

            self.db.rollback()

            raise

        
    def update(
        self,
        employee: Employee
    ) -> Employee:

        try:

            self.db.commit()

            self.db.refresh(employee)

            return employee

        except Exception:

            self.db.rollback()

            raise

    def update_profile_image(
        self,
        employee: Employee
    ) -> Employee:

        return self.update(employee)

    def delete(
        self,
        employee: Employee
    ) -> None:

        try:

            self.db.delete(employee)

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

    