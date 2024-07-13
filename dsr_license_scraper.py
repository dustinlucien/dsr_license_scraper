import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

# Email configuration
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_user = 'your_email@example.com'
smtp_password = 'your_password'
from_email = 'your_email@example.com'
to_emails = ['email1@example.com', 'email2@example.com']

# SMS configuration
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
twilio_phone_number = '+1234567890'
to_phone_numbers = ['+0987654321', '+1123456789']

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())

def send_sms(body):
    client = Client(account_sid, auth_token)
    for number in to_phone_numbers:
        client.messages.create(body=body, from_=twilio_phone_number, to=number)

def check_availability():
    url = "https://douglastonsalmonrun.com/fishing/"
    session = requests.Session()
    
    # First request to get the initial page and any hidden form fields
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract necessary form fields and tokens (this depends on the actual form structure)
    form_data = {
        'date': '10/8/2024',  # Update according to the form's actual field names
        # Include any other hidden fields or tokens if required
    }
    
    # Submit the form
    form_action_url = "https://douglastonsalmonrun.com/fishing/"  # Update if different from the main URL
    response = session.post(form_action_url, data=form_data)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Parse the relevant part of the page to check availability
    availability_info = soup.find_all("div", class_="availability")

    for info in availability_info:
        if "10/8/2024" in info.text:
            message = "Passes available on 10/8/2024!"
            send_email("Pass Availability Alert", message)
            send_sms(message)
            print(message)
            return
    print("No passes available on 10/8/2024.")

# Schedule the task
schedule.every().day.at("08:00").do(check_availability)
schedule.every().day.at("12:00").do(check_availability)
schedule.every().day.at("16:00").do(check_availability)
schedule.every().day.at("20:00").do(check_availability)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
