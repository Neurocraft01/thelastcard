
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from accounts.models import AuthSettings

def disable_google_login():
    """Disable Google Login via the AuthSettings singleton."""
    try:
        settings = AuthSettings.load()
        settings.enable_google_login = False
        settings.save()
        print("SUCCESS: Google Login has been disabled.")
        print("The buttons will no longer appear on Login/Register pages.")
        print("To re-enable, go to Admin Panel > Authentication Settings.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    disable_google_login()
