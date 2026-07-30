import json

from app.core.logger import logger
from app.exceptions.custom_exceptions import (
    EmployeeNotFoundException,
    EmailAlreadyExistsException,
    InvalidSortFieldException,
)
from app.models.employee import Employee
from app.redis.redis_client import redis_client
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:

    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    # -----------------------------
    # Create Employee
    # -----------------------------
    def create_employee(
        self,
        employee_data: EmployeeCreate
    ) -> Employee:

        existing = self.repository.get_by_email(employee_data.email)

        if existing:
            logger.warning(
                "Duplicate email attempted: %s",
                employee_data.email
            )
            raise EmailAlreadyExistsException()

        employee = Employee(
            employee_id=employee_data.employee_id,
            full_name=employee_data.full_name,
            email=employee_data.email,
            phone=employee_data.phone,
            department=employee_data.department,
            designation=employee_data.designation,
            salary=employee_data.salary,
            joining_date=employee_data.joining_date,
            blood_group=employee_data.blood_group,
            status=employee_data.status,
        )

        logger.info(
            "Creating employee with email: %s",
            employee.email
        )

        created_employee = self.repository.create(employee)

        # Clear employee cache
        redis_client.delete("employees")
        logger.info("Employee cache cleared")

        logger.info(
            "Employee created successfully. ID: %s",
            created_employee.id
        )

        return created_employee

    # -----------------------------
    # Update Employee
    # -----------------------------
    def update_employee(
        self,
        employee_id: int,
        employee_data: EmployeeUpdate
    ) -> Employee:

        employee = self.repository.get_by_id(employee_id)

        if not employee:
            logger.warning(
                "Employee not found. ID: %s",
                employee_id
            )
            raise EmployeeNotFoundException()

        logger.info(
            "Updating employee. ID: %s",
            employee_id
        )

        update_data = employee_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(employee, key, value)

        updated_employee = self.repository.update(employee)

        # Clear employee cache
        redis_client.delete("employees")
        logger.info("Employee cache cleared")

        logger.info(
            "Employee updated successfully. ID: %s",
            employee_id
        )

        return updated_employee

    # -----------------------------
    # Upload Profile Image
    # -----------------------------
    def upload_profile_image(
        self,
        employee_id: int,
        file_path: str
    ) -> Employee:

        employee = self.get_employee(employee_id)

        logger.info(
            "Uploading profile image for Employee ID: %s",
            employee_id
        )

        employee.profile_image = file_path

        updated_employee = self.repository.update_profile_image(employee)

        # Clear employee cache
        redis_client.delete("employees")
        logger.info("Employee cache cleared")

        logger.info(
            "Profile image uploaded successfully for Employee ID: %s",
            employee_id
        )

        return updated_employee

    # -----------------------------
    # Delete Employee
    # -----------------------------
    def delete_employee(
        self,
        employee_id: int
    ) -> dict:

        employee = self.repository.get_by_id(employee_id)

        if not employee:
            logger.warning(
                "Employee not found. ID: %s",
                employee_id
            )
            raise EmployeeNotFoundException()

        logger.info(
            "Deleting employee. ID: %s",
            employee_id
        )

        self.repository.delete(employee)

        # Clear employee cache
        redis_client.delete("employees")
        logger.info("Employee cache cleared")

        logger.info(
            "Employee deleted successfully. ID: %s",
            employee_id
        )

        return {
            "message": "Employee deleted successfully"
        }

    # -----------------------------
    # Get Employee
    # -----------------------------
    def get_employee(
        self,
        employee_id: int
    ) -> Employee:

        logger.info(
            "Fetching employee. ID: %s",
            employee_id
        )

        employee = self.repository.get_by_id(employee_id)

        if not employee:
            logger.warning(
                "Employee not found. ID: %s",
                employee_id
            )
            raise EmployeeNotFoundException()

        logger.info(
            "Employee fetched successfully. ID: %s",
            employee_id
        )

        return employee

    # -----------------------------
    # Get All Employees
    # -----------------------------
    def get_all_employees(
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
    ):

        CACHE_KEY = "employees"

        # Check Redis Cache
        cached: str | None = redis_client.get(CACHE_KEY)

        if cached:
            logger.info("Employee list fetched from Redis Cache")
            return json.loads(cached)

        logger.info(
            "Fetching employees from PostgreSQL | search=%s | department=%s | status=%s",
            search,
            department,
            status
        )
        try:
            employees = self.repository.get_all(
                search=search,
                department=department,
                status=status,
                min_salary=min_salary,
                max_salary=max_salary,
                sort_by=sort_by,
                order=order,
                limit=limit,
                offset=offset
            )
        except ValueError:
            raise InvalidSortFieldException()
        
        

        # Convert Employee objects to JSON-serializable dictionaries
        employee_list = [
            {
                "id": emp.id,
                "employee_id": emp.employee_id,
                "full_name": emp.full_name,
                "email": emp.email,
                "phone": emp.phone,
                "department": emp.department,
                "designation": emp.designation,
                "salary": emp.salary,
                "joining_date": str(emp.joining_date),
                "status": emp.status,
                "profile_image": emp.profile_image,
            }
            for emp in employees
        ]

        # Store in Redis with 60-second TTL
        redis_client.setex(
            CACHE_KEY,
            60,
            json.dumps(employee_list)
        )

        logger.info("Employee list stored in Redis Cache")

        return employee_list