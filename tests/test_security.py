from app.core.security import hash_password, verify_password

password = "Kavi123"

hashed = hash_password(password)

print("Original Password:", password)
print("Hashed Password:", hashed)

print("Verify Correct Password:",
      verify_password("Kavi123", hashed))

print("Verify Wrong Password:",
      verify_password("WrongPassword", hashed))