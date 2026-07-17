from fastapi import FastAPI

app = FastAPI(
    title="Employee Management System",
    description="Enterprise HRMS Backend API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Employee Management System API is Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }