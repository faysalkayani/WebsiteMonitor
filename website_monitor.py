import smtplib
import requests
import time

# Function to check if the website is up
def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            send_email("Website is up", f"The website {url} is up and running! \n Welcome jeee")
        else:
            send_email("Website is down", f"The website {url} is down with status code {response.status_code}.")
    except requests.RequestException as e:
        send_email("Website is down", f"The website {url} could not be reached due to an error: {e}")

# Function to send an email notification
def send_email(subject, body):
    # StackMail SMTP server details
    smtp_server = "smtp.stackmail.com"
    smtp_port = 587
    sender_email = "faisal.ahmed@techsasoft.net"  # Replace with your email
    sender_password = "Killer@420"  # Replace with your email password (or App Password if 2FA enabled)
    recipient_email = "faisalkiani06@gmail.com"  # Replace with the recipient's email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, recipient_email, message)
        print(f"Email sent to {recipient_email}")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Main code to monitor the website
website_url = "http://www.techsacare.com"  # Replace with your website URL

# Run the check every 5 minutes
while True:
    check_website(website_url)
    time.sleep(300)  # Sleep for 300 seconds (5 minutes)
