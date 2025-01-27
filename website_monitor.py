import smtplib
import requests
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# List of recipient emails
recipient_emails = [
    "s.abdullah@techsasoft.net",
    "ehsan.raza@techsasoft.net",
    "M.Usman@techsasoft.net",
    "aqib.javaid@techsasoft.net",
    "m.hamza@techsasoft.net",
    "mohsin.raza@techsasoft.net",
    "shaheryar.ayub@techsasoft.net",
    "aqsa.qureshi@techsasoft.net",
    "haider.naseem@techsasoft.net",
    "sarmad.khan@techsasoft.net",
    "saaim.raza@techsasoft.net",
    "atif.rashid@techsasoft.net",
    "ahmad.nawaz@techsasoft.net",
    "faisal.ahmed@techsasoft.net"
]

# Join the list into a comma-separated string and use it in the email
recipient_email = ", ".join(recipient_emails)

# Dictionary to track the previous status of websites (True for UP, False for DOWN)
previous_status = {}

# List of websites to monitor
website_urls = [
    "http://qa.techsacare.com",   
    "http://mobile.techsacare.com",  
    "https://techsacare.com/"      
]

# Initialize previous_status with True for all websites (assume they are UP initially)
for url in website_urls:
    previous_status[url] = True

# Function to convert GMT to Pakistan Standard Time (PKT)
def convert_gmt_to_local(gmt_time_str, time_zone="Asia/Karachi"):
    # Define the time zone you want to convert to (Pakistan Standard Time)
    local_tz = pytz.timezone(time_zone)
    
    gmt_time = datetime.strptime(gmt_time_str, "%a, %d %b %Y %H:%M:%S GMT")
    gmt_time = pytz.utc.localize(gmt_time)
    local_time = gmt_time.astimezone(local_tz)
    
    # Format the time to a string (e.g., '2025-01-22 13:14:15')
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

# Function to check that web is up
def check_website(url):
    global previous_status
    try:
        logging.info("Checking website: {}".format(url))  
        response = requests.get(url)
        
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()  # Response time in seconds
        headers = response.headers
        
        # Get current time in PKT
        current_time = datetime.now(pytz.timezone("Asia/Karachi")).strftime("%Y-%m-%d %H:%M:%S")
        
        logging.info("Response status code: {}".format(status_code))  # Using .format() instead of f-string
        logging.info("Last Checked Time (PKT): {}".format(current_time))  # Debug log
        
        # Determine if the website is UP or DOWN
        is_up = (status_code == 200)
        
        # Check the previous status of the website
        prev_status = previous_status.get(url, None)

        # Debug logs for status transition
        logging.info("Previous Status: {}".format(prev_status))
        logging.info("Current Status: {}".format(is_up))

        # If the website was previously DOWN and is now UP, send an email
        if is_up and prev_status is False:
            body = """
            <p>The website <strong>{}</strong> is back up with status code <strong>{}</strong>.</p>
            <p><strong>Response Time:</strong> {} seconds</p>
            <p><strong>Last Checked:</strong> {}</p>
            <p><strong>Headers:</strong><br>{}</p>
            """.format(url, status_code, response_time, current_time, format_headers(headers))
            send_email("Website is Back Up", body)
            logging.info("Website {} is back up. Email sent.".format(url))

        # If the website is DOWN and was not DOWN previously (including first-time DOWN), send an email
        elif not is_up and (prev_status is None or prev_status is not False):
            body = """
            <p>The website <strong>{}</strong> is down with status code <strong>{}</strong>.</p>
            <p><strong>Response Time:</strong> {} seconds</p>
            <p><strong>Last Checked:</strong> {}</p>
            <p><strong>Headers:</strong><br>{}</p>
            """.format(url, status_code, response_time, current_time, format_headers(headers))
            send_email("Website is Down", body)
            logging.info("Website {} is down. Email sent.".format(url))
        
        # Update the status in the dictionary
        previous_status[url] = is_up

    except requests.RequestException as e:
        logging.error("Error while checking website: {}".format(e))  # Using .format() instead of f-string
        body = """
        <p>The website <strong>{}</strong> could not be reached due to an error: {}</p>
        <p><strong>Last Checked:</strong> {}</p>
        """.format(url, e, datetime.now(pytz.timezone("Asia/Karachi")).strftime("%Y-%m-%d %H:%M:%S"))
        send_email("Website is Down", body)
        logging.error("Failed to check website {}. Email sent.".format(url))

# Function to format headers into HTML
def format_headers(headers):
    formatted_headers = "<ul>"
    
    for key, value in headers.items():
        if key.lower() == "date":  # Convert the 'Date' header to local PKT time
            local_time = convert_gmt_to_local(value)  # Convert to PKT
            formatted_headers += "<li><strong>{}:</strong> {}</li>".format(key, local_time)
        else:
            formatted_headers += "<li><strong>{}:</strong> {}</li>".format(key, value)
    
    formatted_headers += "</ul>"
    return formatted_headers

# Function to send an email notification with HTML content
def send_email(subject, body):
    logging.info("Preparing to send email with subject: {}".format(subject))
    # Fetch SMTP credentials from environment variables
    smtp_user = os.getenv("SMTP_USER")  # Fetch email from environment variable
    smtp_password = os.getenv("SMTP_PASSWORD")  # Fetch password from environment variable

    if not smtp_user or not smtp_password:
        logging.error("SMTP credentials are not set in environment variables.")
        return

    # Gmail SMTP server details (adjust if using a different provider)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the HTML content with CSS
    email_html = """
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
                <h2>{}</h2>
            </div>
            <div class="content">
                {}
            </div>
            <div class="footer">
                <p>Website Monitoring Service</p>
            </div>
        </div>
    </body>
    </html>
    """.format(subject, body)

    # Set up the MIME message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['Subject'] = subject

    # Combine recipient emails into a comma-separated string
    msg['To'] = recipient_email

    # Attach the HTML content
    msg.attach(MIMEText(email_html, 'html'))

    try:
        logging.info("Sending email...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient_email.split(", "), msg.as_string())
        logging.info("Email sent to {}".format(recipient_email))  # Using .format() instead of f-string
        server.quit()
    except Exception as e:
        logging.error("Error sending email: {}".format(e))  # Using .format() instead of f-string

# Main code to monitor the websites
for url in website_urls:
    check_website(url)
