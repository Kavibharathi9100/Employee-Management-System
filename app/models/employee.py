from sqlalchemy import Column, Integer, String, Float, Date

from app.database.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String(20), unique=True, nullable=False)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    phone = Column(String(20))

    department = Column(String(100))

    blood_group = Column(String(10), nullable=True)

    designation = Column(String(100))

    salary = Column(Float)

    joining_date = Column(Date)

    status = Column(String(20), default="Active")

    profile_image = Column(String(255), nullable=True)