"""
Custom error handlers and utility views for the NFC Platform.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods


@never_cache
@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """
    Health check endpoint for monitoring services (e.g., Render, AWS, etc.)
    Returns 200 if the application and database are healthy.
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=503)


def handler404(request, exception):
    """Custom 404 error page."""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Custom 500 error page."""
    return render(request, 'errors/500.html', status=500)
