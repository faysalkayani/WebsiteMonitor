# import smtplib
# import requests
# import os
# import time

# # Function to check if the website is up
# def check_website(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             send_email("Website is up", f"The website {url} is up and running! \n HAPPY MONITORING")
#         else:
#             send_email("Website is down", f"The website {url} is down with status code {response.status_code}.")
#     except requests.RequestException as e:
#         send_email("Website is down", f"The website {url} could not be reached due to an error: {e}")

# # Function to send an email notification
# def send_email(subject, body):
#     # Fetching the secrets from environment variables
#     smtp_user = os.getenv('SMTP_USER')  # Secret SMTP_USER
#     smtp_password = os.getenv('SMTP_PASSWORD')  # Secret SMTP_PASSWORD
#     recipient_email = os.getenv('RECIPIENT_EMAIL')  # Secret RECIPIENT_EMAIL

#     # StackMail SMTP server details
#     smtp_server = "smtp.stackmail.com"
#     smtp_port = 587

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()  # Secure the connection
#         server.login(smtp_user, smtp_password)
#         message = f"Subject: {subject}\n\n{body}"
#         server.sendmail(smtp_user, recipient_email, message)
#         print(f"Email sent to {recipient_email}")
#         server.quit()
#     except Exception as e:
#         print(f"Error sending email: {e}")

# # Main code to monitor the website
# website_url = "http://www.techsacare.com"  # Replace with your website URL

# # Run the check every 5 minutes
# # while True:
#     check_website(website_url)
#     # time.sleep(600)  # Sleep for 600 seconds (10 minutes)




import smtplib
import requests
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Function to check if the website is up
def check_website(url):
    try:
        print(f"Checking website: {url}")
        response = requests.get(url)
        
        # Collect website details
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()  # Response time in seconds
        headers = response.headers
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Response status code: {status_code}")
        
        if status_code == 200:
            body = f"""
            <p>The website <strong>{url}</strong> is up and running!</p>
            <p><strong>Status Code:</strong> {status_code}</p>
            <p><strong>Response Time:</strong> {response_time} seconds</p>
            <p><strong>Last Checked:</strong> {current_time}</p>
            <p><strong>Headers:</strong><br>{format_headers(headers)}</p>
            <p><strong>Happy Monitoring!</strong></p>
            """
            send_email("Website is Up", body)
        else:
            body = f"""
            <p>The website <strong>{url}</strong> is down with status code <strong>{status_code}</strong>.</p>
            <p><strong>Response Time:</strong> {response_time} seconds</p>
            <p><strong>Last Checked:</strong> {current_time}</p>
            <p><strong>Headers:</strong><br>{format_headers(headers)}</p>
            """
            send_email("Website is Down", body)
    except requests.RequestException as e:
        print(f"Error while checking website: {e}")
        body = f"""
        <p>The website <strong>{url}</strong> could not be reached due to an error: {e}</p>
        <p><strong>Last Checked:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        """
        send_email("Website is Down", body)

# Function to format headers into HTML
def format_headers(headers):
    formatted_headers = "<ul>"
    for key, value in headers.items():
        formatted_headers += f"<li><strong>{key}:</strong> {value}</li>"
    formatted_headers += "</ul>"
    return formatted_headers

# Function to send an email notification with HTML content
def send_email(subject, body):
    # Fetching the secrets from environment variables
    smtp_user = os.getenv('SMTP_USER')  # Secret SMTP_USER
    smtp_password = os.getenv('SMTP_PASSWORD')  # Secret SMTP_PASSWORD
    recipient_email = os.getenv('RECIPIENT_EMAIL')  # Secret RECIPIENT_EMAIL

    # StackMail SMTP server details
    smtp_server = "smtp.stackmail.com"
    smtp_port = 587

    # Create the HTML content with CSS
    email_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.5;
                color: #333;
            }}
            .footer {{
                margin-top: 20px;
                text-align: center;
                font-size: 12px;
                color: #888;
            }}
            h2 {{
                color: #2d87f0;
            }}
            p {{
                font-size: 16px;
                color: #555;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                font-size: 14px;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>{subject}</h2>
            </div>
            <div class="content">
                {body}
            </div>
            <div class="footer">
                <p>Website Monitoring Service</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Set up the MIME message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['Subject'] = subject

    # Combine recipient emails into a comma-separated string
    msg['To'] = recipient_email

    # Attach the HTML content
    msg.attach(MIMEText(email_html, 'html'))

    try:
        print("Sending email...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Main code to monitor the website
website_url = "http://www.techsacare.com"  # Replace with your website URL

# Run the check every 5 minutes
# while True:
check_website(website_url)
    # time.sleep(300)  # Sleep for 300 seconds (5 minutes)

