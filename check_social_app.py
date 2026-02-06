
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nfc_platform.settings")
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print(f"Current SITE_ID: {settings.SITE_ID}")

print("\nExisting Sites:")
for site in Site.objects.all():
    print(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print("\nExisting SocialApps:")
for app in SocialApp.objects.all():
    print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
    print(f"  Linked Sites: {[s.id for s in app.sites.all()]}")

if not SocialApp.objects.filter(provider='google').exists():
    print("\nWARNING: No SocialApp found for provider 'google'")

try:
    current_site = Site.objects.get(id=settings.SITE_ID)
    google_app = SocialApp.objects.filter(provider='google', sites=current_site).first()
    if not google_app:
        print(f"\nERROR: No Google SocialApp linked to current site (ID: {settings.SITE_ID})")
    else:
        print(f"\nSUCCESS: Found Google SocialApp linked to current site: {google_app}")
except Site.DoesNotExist:
    print(f"\nERROR: Site with ID {settings.SITE_ID} does not exist")
