import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body, smtp_server="smtp.gmail.com", smtp_port=587):
    """
    Send an email using SMTP.

    Parameters:
    - sender_email: your email address
    - sender_password: your email password or app password
    - recipient_email: recipient email address
    - subject: email subject line
    - body: email body (plain text)
    - smtp_server: SMTP server address (default Gmail)
    - smtp_port: SMTP server port (default 587)
    """

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
