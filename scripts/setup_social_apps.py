
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_social_apps():
    # Ensure Site exists
    site, created = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'NFC Platform'})
    if not created and site.domain != 'localhost:8000':
        site.domain = 'localhost:8000'
        site.name = 'NFC Platform (Local)'
        site.save()
    
    # Google App
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google',
        defaults={
            'client_id': 'PLACEHOLDER_CLIENT_ID',
            'secret': 'PLACEHOLDER_SECRET_KEY',
        }
    )
    if not google_app.sites.filter(id=site.id).exists():
        google_app.sites.add(site)
    
    # Twitter App
    twitter_app, created = SocialApp.objects.get_or_create(
        provider='twitter',
        name='Twitter',
        defaults={
            'client_id': 'PLACEHOLDER_CLIENT_ID',
            'secret': 'PLACEHOLDER_SECRET_KEY',
        }
    )
    if not twitter_app.sites.filter(id=site.id).exists():
        twitter_app.sites.add(site)
        
    print("Successfully created placeholder Social Apps. Please update keys in Admin Panel.")

if __name__ == '__main__':
    setup_social_apps()
