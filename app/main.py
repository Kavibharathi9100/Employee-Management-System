from fastapi import FastAPI
from app.middleware.logging_middleware import LoggingMiddleware
from sqlalchemy import text
from app.database.database import Base, engine
from app.models.user import User
from app.models.employee import Employee   # NEW
from app.api.employee import router as employee_router
from app.api.user import router as user_router
from fastapi.staticfiles import StaticFiles
from app.exceptions.handlers import register_exception_handlers
from app.api.auth import router as auth_router
from app.models.password_reset import PasswordReset

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="Enterprise HRMS Backend API",
    version="1.0.0"
)
app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)
app.include_router(user_router)
app.include_router(employee_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Employee Management System API is Running"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

@app.get("/db-check")
def database_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "success",
            "message": "Database connected successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)