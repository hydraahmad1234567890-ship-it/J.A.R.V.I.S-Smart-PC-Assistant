import os
import smtplib
from email.mime.text import MIMEText
from core.tools import register_tool

@register_tool(
    name="send_email",
    description="Sends an email using SMTP. Requires environment variables: SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASS.",
    parameters=[
        {"name": "to_email", "type": "string", "required": True},
        {"name": "subject", "type": "string", "required": True},
        {"name": "body", "type": "string", "required": True}
    ],
    requires_confirmation=True
)
def send_email(to_email: str, subject: str, body: str) -> str:
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")
    
    if not all([smtp_server, smtp_port, email_user, email_pass]):
        return "🔴 Error: SMTP configuration is missing in environment variables."
        
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = to_email
        
        with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            
        return f"📧 Email sent successfully to {to_email}."
    except Exception as e:
        return f"🔴 Email Error: {str(e)}"
