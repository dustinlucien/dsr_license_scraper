import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import schedule
import time
import smtplib
from datetime import date
from email.mime.text import MIMEText
from twilio.rest import Client

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'dustin.lucien@gmail.com'
smtp_password = "lnpg wlsw usen gzti"

from_email = 'dustin.lucien@gmail.com'
to_emails = ['dustin.lucien@gmail.com']

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

def check_availability(date_string):
    # Extract necessary form fields and tokens (this depends on the actual form structure)

    date_to_check = date.fromisoformat(date_string)
    
    form_data = {
        'action' : 'wc_bookings_calculate_costs',
        'form': urllib.parse.urlencode({
            'add-premium-pass' : 'false',
            'wc_bookings_field_persons' : '1',
            'wc_bookings_field_duration' : '1',
            'wc_bookings_field_start_date_month' : date_to_check.month,
            'wc_bookings_field_start_date_year' : date_to_check.year,
            'wc_bookings_field_start_date_day' : date_to_check.day,
            'wc_bookings_field_start_date_to_month' : '',
            'wc_bookings_field_start_date_to_year' : date_to_check.year, 
            'wc_bookings_field_start_date_to_day' : '',
            'add-to-cart' : '467',
        }),
        # Include any other hidden fields or tokens if required
    }
    
    #print("form data")
    #print(form_data)
    
    # Submit the form
    form_action_url = "https://douglastonsalmonrun.com/wp-admin/admin-ajax.php"  # Update if different from the main URL
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(form_action_url, data=form_data, headers=headers)

    #print("raw response")
    #print(response.url)
    
    #print("body")
    #print(response.request.body)
    
    #print("headers")
    #print(response.headers)
    #print(response.text)
        
    availability_info = response.json()
    
    #print(availability_info)
    
    if "SUCCESS" in availability_info["result"]:
        return True
    else:
        return False

# Schedule the task
#schedule.every().day.at("08:00").do(check_availability)
#schedule.every().day.at("12:00").do(check_availability)
#schedule.every().day.at("16:00").do(check_availability)
#schedule.every().day.at("20:00").do(check_availability)

# Keep the script running
#while True:
    #schedule.run_pending()
    #time.sleep(1)

dates_to_check = ["2024-10-07", "2024-10-08", "2024-10-09", "2024-10-10"]

for date_to_check in dates_to_check:
    if check_availability(date_to_check):
        #send sms
        #add to email message
        print(f"Passes available on: {date_to_check}")
    else:
        #add to email message
        print(f"No passes available on: {date_to_check}")
