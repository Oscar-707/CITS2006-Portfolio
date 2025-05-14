import pyotp
import smtplib
from email.message import EmailMessage

# Mailtrap SMTP settings (use the credentials provided in your Mailtrap dashboard)
MAILTRAP_SMTP_SERVER = 'xxxxxxxxx'
MAILTRAP_SMTP_PORT = 2525
MAILTRAP_USERNAME = 'xxxxxxxxx'  # Found in Mailtrap
MAILTRAP_PASSWORD = 'xxxxxxxxx'  # Found in Mailtrap

# Generate a TOTP code (for OTP MFA)
totp = pyotp.TOTP(pyotp.random_base32())
otp_code = totp.now()

# Send OTP email via Mailtrap SMTP
def send_otp_email(to_email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Your One-Time Password'
    msg['From'] = 'your_email@example.com'  # This can be a placeholder email
    msg['To'] = to_email
    msg.set_content(f'Your OTP is: {code}')

    # Send the email through Mailtrap SMTP
    with smtplib.SMTP(MAILTRAP_SMTP_SERVER, MAILTRAP_SMTP_PORT) as smtp:
        smtp.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
        smtp.send_message(msg)

# Example: Sending OTP to a user
recipient_email = input("Enter your email address: ")
send_otp_email(recipient_email, otp_code)

# Simulate OTP verification process
user_input = input("Enter the OTP you received: ")

if totp.verify(user_input, valid_window=1):
    print("Success! OTP verified.")
else:
    print("Invalid OTP.")
