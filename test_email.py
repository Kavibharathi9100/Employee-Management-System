import smtplib

EMAIL = "kavibharathi910@gmail.com"
PASSWORD = "gbdevefgncqbqwwb"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(EMAIL, PASSWORD)

print("Login Successful!")

server.quit()