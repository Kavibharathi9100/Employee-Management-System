


class EmployeeNotFoundException(Exception):
    def __init__(self):
        self.message = "Employee not found"


class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "User already exists"


class InvalidPasswordException(Exception):
    def __init__(self):
        self.message = "Invalid password"

class InvalidSortFieldException(Exception):
    def __init__(self):
        self.message = "Invalid sort field"

class EmailAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "Email already exists"