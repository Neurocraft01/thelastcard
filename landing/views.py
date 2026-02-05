"""
Views for landing pages.
"""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page home view."""
    template_name = 'landing/home.html'


class AboutView(TemplateView):
    """About page view."""
    template_name = 'landing/about.html'


class PricingView(TemplateView):
    """Pricing page view."""
    template_name = 'landing/pricing.html'


class ContactView(TemplateView):
    """Contact page view."""
    template_name = 'landing/contact.html'


class FeaturesView(TemplateView):
    """Features page view."""
    template_name = 'landing/features.html'


class PrivacyView(TemplateView):
    """Privacy policy page view."""
    template_name = 'landing/privacy.html'


class TermsView(TemplateView):
    """Terms of service page view."""
    template_name = 'landing/terms.html'
