import smtplib
import requests
import os
import time

# Function to check if the website is up
def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            send_email("Website is up", f"The website {url} is up and running! \n HAPPY MONITORING")
        else:
            send_email("Website is down", f"The website {url} is down with status code {response.status_code}.")
    except requests.RequestException as e:
        send_email("Website is down", f"The website {url} could not be reached due to an error: {e}")

# Function to send an email notification
def send_email(subject, body):
    # Fetching the secrets from environment variables
    smtp_user = os.getenv('SMTP_USER')  # Secret SMTP_USER
    smtp_password = os.getenv('SMTP_PASSWORD')  # Secret SMTP_PASSWORD
    recipient_email = os.getenv('RECIPIENT_EMAIL')  # Secret RECIPIENT_EMAIL

    # StackMail SMTP server details
    smtp_server = "smtp.stackmail.com"
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_user, smtp_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(smtp_user, recipient_email, message)
        print(f"Email sent to {recipient_email}")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Main code to monitor the website
website_url = "http://www.techsacare.com"  # Replace with your website URL

# Run the check every 5 minutes
# while True:
    check_website(website_url)
    # time.sleep(600)  # Sleep for 600 seconds (10 minutes)
