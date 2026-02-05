import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from themes.models import Theme

User = get_user_model()

def create_superuser():
    email = 'admin@example.com'
    password = 'admin'
    if not User.objects.filter(email=email).exists():
        print(f"Creating superuser: {email}")
        User.objects.create_superuser(email=email, password=password)
    else:
        print(f"Superuser {email} already exists")

def create_default_themes():
    themes = [
        {
            'name': 'Modern Dark',
            'slug': 'modern-dark',
            'theme_type': 'SYSTEM',
            'primary_color': '#6366F1',
            'background_color': '#0F172A',
            'text_color': '#F8FAFC',
            'dark_mode': True,
        },
        {
            'name': 'Clean Light',
            'slug': 'clean-light',
            'theme_type': 'SYSTEM',
            'primary_color': '#4F46E5',
            'background_color': '#FFFFFF',
            'text_color': '#1E293B',
            'dark_mode': False,
        },
        {
            'name': 'Gradient Blue',
            'slug': 'gradient-blue',
            'theme_type': 'SYSTEM',
            'primary_color': '#3B82F6',
            'background_gradient': 'linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)',
            'text_color': '#1E3A8A',
            'dark_mode': False,
        }
    ]

    for theme_data in themes:
        Theme.objects.get_or_create(
            slug=theme_data['slug'],
            defaults=theme_data
        )
    print(f"Created {len(themes)} default themes")

if __name__ == '__main__':
    create_superuser()
    create_default_themes()
