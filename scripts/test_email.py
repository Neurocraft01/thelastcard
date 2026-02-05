
import os
import sys
import django
from decouple import config

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.core.mail import send_mail

def test_email():
    print("--- Email Configuration Test ---")
    print(f"Backend: {config('EMAIL_BACKEND')}")
    print(f"Host: {config('EMAIL_HOST')}")
    print(f"User: {config('EMAIL_HOST_USER')}")
    
    recipient = config('EMAIL_HOST_USER')
    print(f"Attempting to send test email to: {recipient}")
    
    try:
        send_mail(
            subject='Test Token from NFC Platform',
            message='This is a test email to verify your SMTP configuration. If you read this, it works!',
            from_email=config('DEFAULT_FROM_EMAIL'),
            recipient_list=[recipient],
            fail_silently=False,
        )
        print("\nSUCCESS: Email sent successfully!")
        print("Please check your inbox (and spam folder).")
    except Exception as e:
        print(f"\nFAILURE: Could not send email.")
        print(f"Error details: {e}")

if __name__ == '__main__':
    test_email()
