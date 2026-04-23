import random

def generate_otp():
    return str(random.randint(100000, 999999))

# self serving OTP
# note replace later with Temi API
def send_otp(phone, code):
    print(f"Sending OTP {code} to {phone}")