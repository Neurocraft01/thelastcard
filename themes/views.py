"""
Views for themes app.
"""

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Theme


class ThemeListView(ListView):
    """List available themes."""
    model = Theme
    template_name = 'themes/list.html'
    context_object_name = 'themes'
    
    def get_queryset(self):
        return Theme.objects.filter(is_active=True, is_public=True)


class ThemeDetailView(DetailView):
    """Theme detail view."""
    model = Theme
    template_name = 'themes/detail.html'
    context_object_name = 'theme'


class ThemePreviewView(TemplateView):
    """Preview a theme with sample content."""
    template_name = 'themes/preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        theme = get_object_or_404(Theme, slug=slug)
        context['theme'] = theme
        
        # Sample profile data for preview
        context['sample_profile'] = {
            'full_name': 'John Smith',
            'designation': 'Product Designer',
            'company': 'TechCorp Inc.',
            'bio': 'Passionate about creating beautiful and functional digital experiences.',
            'phone': '+1 (555) 123-4567',
            'email': 'john@example.com',
            'website': 'https://johnsmith.design',
            'location': 'San Francisco, CA',
            'social_links': {
                'linkedin': 'https://linkedin.com/in/johnsmith',
                'twitter': 'https://twitter.com/johnsmith',
                'github': 'https://github.com/johnsmith',
                'instagram': 'https://instagram.com/johnsmith',
            }
        }
        
        return context
