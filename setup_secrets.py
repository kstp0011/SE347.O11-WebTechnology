import os
import secrets

# Prompt user for secret key
secret_key = secrets.token_hex(16)

# Prompt user for email and password
email = input("Please enter your email address: ")
password = ""
while len(password) != 16:
    password = input('Please enter your 16 character APP_PASSWORD: ')

# Write secret key and credentials to creds.py
with open(os.path.join("musicapp", "creds.py"), "w") as f:
    f.write(f"SECRET_KEY = '{secret_key}'\n")
    f.write(f"MAIL_USERNAME = '{email}'\n")
    f.write(f"MAIL_PASSWORD = '{password}'\n")
