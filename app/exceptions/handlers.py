from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.exceptions.custom_exceptions import (
    EmployeeNotFoundException,
    UserAlreadyExistsException,
    InvalidPasswordException,
    InvalidSortFieldException
)


def register_exception_handlers(app: FastAPI):

    # ==========================
    # Employee Not Found
    # ==========================
    @app.exception_handler(EmployeeNotFoundException)
    async def employee_not_found_handler(
        request: Request,
        exc: EmployeeNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "status_code": 404,
                "message": exc.message,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # ==========================
    # User Already Exists
    # ==========================
    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "status_code": 409,
                "message": exc.message,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # ==========================
    # Invalid Password
    # ==========================
    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_handler(
        request: Request,
        exc: InvalidPasswordException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "status_code": 401,
                "message": exc.message,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    @app.exception_handler(InvalidSortFieldException)
    async def invalid_sort_field_handler(
        request: Request,
        exc: InvalidSortFieldException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "status_code": 400,
                "message": exc.message,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # ==========================
    # HTTP Exception
    # ==========================
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status_code": exc.status_code,
                "message": exc.detail,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # ==========================
    # Global Exception
    # ==========================
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status_code": 500,
                "message": "Internal Server Error",
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        )