import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================================
# EMAIL SENDING SERVICE
# =========================================
def send_real_email(to_email: str, subject: str, content: str) -> tuple[bool, str]:
    """Sends an email using SMTP and returns a success boolean and error message."""
    
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")

    # Validate that required credentials exist
    if not all([smtp_user, smtp_pass, sender_email]):
        return False, "SMTP credentials missing in environment variables."

    # Construct the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "plain"))

    try:
        # Connect to SMTP server and send
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        
        return True, ""
    except Exception as e:
        return False, str(e)