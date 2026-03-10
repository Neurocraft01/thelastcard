from .models import AuthSettings

def auth_settings(request):
    """Expose global auth settings to templates."""
    try:
        settings = AuthSettings.load()
    except Exception:
        settings = None
    return {'auth_settings': settings}
