from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File

from app.auth.roles import require_role
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services.employee_service import EmployeeService
from app.auth.oauth2 import get_current_user
from app.dependencies.employee_dependencies import get_employee_service
from typing import Optional
import os
import shutil
import uuid
from app.exceptions.custom_exceptions import EmployeeNotFoundException


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# -------------------------------------------------------
# Create Employee
# -------------------------------------------------------
@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    return service.create_employee(employee)


# -------------------------------------------------------
# Get All Employees
# -------------------------------------------------------
@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(
    search: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of employees to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of employees to skip"
    ),
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_all_employees(
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


# -------------------------------------------------------
# Get Employee By ID
# -------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service)
):
    employee = service.get_employee(employee_id)
    if not employee:
        raise EmployeeNotFoundException()
    return employee


# -------------------------------------------------------
# Update Employee
# -------------------------------------------------------
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    current_user: User = Depends(require_role(["admin", "manager"])),
    service: EmployeeService = Depends(get_employee_service)
):
    return service.update_employee(
        employee_id,
        employee
    )


# -------------------------------------------------------
# Upload Profile Photo
# -------------------------------------------------------
@router.post("/{employee_id}/upload-photo")
def upload_profile_photo(
    employee_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(["admin", "manager"])),
    service: EmployeeService = Depends(get_employee_service)
):

    employee = service.get_employee(employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are allowed"
        )

    extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    upload_dir = "uploads/profile_images"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    service.upload_profile_image(employee_id, file_path)

    return {
        "message": "Profile image uploaded successfully",
        "image_url": f"/uploads/profile_images/{filename}"
    }


# -------------------------------------------------------
# Delete Employee
# -------------------------------------------------------
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    current_user: User = Depends(require_role(["admin"])),
    service: EmployeeService = Depends(get_employee_service)
):
    return service.delete_employee(employee_id)