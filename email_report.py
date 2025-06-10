import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from check_dmv import get_active_locations  # Importing the function to check appointment locations

# Load environment variables from .env file (where I keep my email credentials)
load_dotenv()

# Grab my email credentials and recipient email from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email(body):
    # Set up sender, recipient, and password for the SMTP server
    sender = EMAIL_ADDRESS
    recipient = RECIPIENT_EMAIL
    password = EMAIL_PASSWORD

    # Create the email content as plain text
    msg = MIMEText(body)
    msg['Subject'] = 'NCDMV Appointment Availability'  # Subject line of the email
    msg['From'] = sender
    msg['To'] = recipient

    # Connect securely to Gmail's SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)  # Log in using my credentials
        server.sendmail(sender, recipient, msg.as_string())  # Send the email
        print(f"Email sent to {recipient}")

if __name__ == "__main__":
    # First, get the list of active locations from the scraper
    locations = get_active_locations()
    
    # Build the email body depending on whether any appointments were found
    if locations:
        body = "The following locations have appointments available:\n\n" + "\n".join(locations)
    else:
        body = "No locations currently have available appointments."

    # Finally, send the email with the constructed message body
    send_email(body)
