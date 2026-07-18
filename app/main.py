from fastapi import FastAPI
from sqlalchemy import text
from app.database.database import Base, engine
from app.models.user import User
from app.api.user import router as user_router
# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="Enterprise HRMS Backend API",
    version="1.0.0"
)
app.include_router(user_router)
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