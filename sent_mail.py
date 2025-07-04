
import os
import django
# Removed unused import

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FraudDetection.settings")
django.setup()

from detection.models import Transaction, FraudData

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Example model transaction

# Function to send email
def send_email(to_email, subject, body):
    try:
        # Email configuration
        sender_email = "sableshankar198@gmail.com"
        sender_password = "enlntioeeqxefzqd"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))  # Set content type to 'html'

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Check and send email if needed
def check_and_send_email(transaction):
    subject = "Fraud Transaction Alert"
    body = """
    <html>
    <head></head>
    <body>
        <p>Dear user,</p>
        <p>There is a fraud detected by our system. Here are the details regarding your transaction:</p>
        <table border="1" style="border-collapse: collapse; width: 50%;">
            <tr>
                <th style="text-align: left; padding: 8px;">Date</th>
                <td style="padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="text-align: left; padding: 8px;">Remark</th>
                <td style="padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="text-align: left; padding: 8px;">Credit</th>
                <td style="padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="text-align: left; padding: 8px;">Debit</th>
                <td style="padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="text-align: left; padding: 8px;">Balance</th>
                <td style="padding: 8px;">{}</td>
            </tr>
        </table>
        <p>Thank you for using our service.</p>
        <p>Best regards,<br/>Fraud Detection Team</p>
    </body>
    </html>
    """.format(transaction.date, transaction.remark, transaction.credit, transaction.debit, transaction.balance)
    send_email(transaction.user.email, subject, body)
    transaction.is_message_sent = True  # Update the status after sending the email
    transaction.save()

# Example usage
if __name__ == "__main__":
    # Example transaction
    fraud_data_details = FraudData.objects.all().values_list('fraud_description')
    
                 
    transactions = Transaction.objects.filter(is_fraud=False)
    for transaction in transactions:
        for fraud in fraud_data_details:
            if fraud[0] in transaction.remark:
                print("Fraud data found: ", fraud)
                print(transaction)
                transaction.is_fraud = True
                transaction.save()
                break

    transactions = Transaction.objects.filter(is_fraud=True, is_message_sent=False)  # Replace with your transaction ID
    for transaction in transactions:
        print("Transaction: ", transaction)
        check_and_send_email(transaction)