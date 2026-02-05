"""
Views for analytics app.
"""

import json
import hashlib
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cards.models import NFCCard
from .models import ProfileAnalytics, DailyAnalyticsSummary


@method_decorator(csrf_exempt, name='dispatch')
class TrackInteractionView(View):
    """API endpoint to track profile interactions."""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            interaction_type = data.get('event', 'VIEW').upper()
            metadata = data.get('metadata', {})
            
            card = get_object_or_404(NFCCard, pk=card_id)
            
            # Get visitor info
            ip = self.get_client_ip(request)
            ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            
            ProfileAnalytics.objects.create(
                card=card,
                interaction_type=interaction_type,
                metadata=metadata,
                visitor_ip_hash=ip_hash,
                user_agent=user_agent,
                referrer=metadata.get('referrer', '')[:200] if metadata.get('referrer') else ''
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '0.0.0.0')


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Analytics dashboard view."""
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        from datetime import timedelta
        from django.utils import timezone
        from django.db.models import Sum, Count
        
        # Get user's cards
        if user.is_super_admin:
            cards = NFCCard.objects.all()
        elif user.is_admin and user.organization:
            org_users = user.organization.members.all()
            cards = NFCCard.objects.filter(user__in=org_users)
        else:
            cards = user.cards.all()
        
        context['cards'] = cards
        
        # Get last 30 days analytics
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        analytics = DailyAnalyticsSummary.objects.filter(
            card__in=cards,
            date__gte=thirty_days_ago.date()
        )
        
        totals = analytics.aggregate(
            total_views=Sum('total_views'),
            unique_views=Sum('unique_views'),
            contact_saves=Sum('contact_saves'),
            phone_clicks=Sum('phone_clicks'),
            email_clicks=Sum('email_clicks')
        )
        
        context['totals'] = totals
        context['daily_stats'] = analytics.order_by('date')
        
        return context


class CardAnalyticsView(LoginRequiredMixin, TemplateView):
    """Analytics for a specific card."""
    template_name = 'analytics/card.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_id = self.kwargs.get('card_id')
        card = get_object_or_404(NFCCard, pk=card_id)
        
        # Check permissions
        user = self.request.user
        if not user.is_super_admin:
            if user.is_admin:
                if not (card.user and card.user.organization == user.organization):
                    context['error'] = 'Permission denied'
                    return context
            elif card.user != user:
                context['error'] = 'Permission denied'
                return context
        
        context['card'] = card
        
        from datetime import timedelta
        from django.utils import timezone
        
        # Get last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        context['daily_stats'] = DailyAnalyticsSummary.objects.filter(
            card=card,
            date__gte=thirty_days_ago.date()
        ).order_by('date')
        
        context['recent_views'] = ProfileAnalytics.objects.filter(
            card=card
        ).order_by('-timestamp')[:50]
        
        return context


class ExportAnalyticsView(LoginRequiredMixin, View):
    """Export analytics data as CSV."""
    
    def get(self, request):
        import csv
        from datetime import timedelta
        from django.utils import timezone
        
        user = request.user
        
        # Get user's cards
        if user.is_super_admin:
            cards = NFCCard.objects.all()
        elif user.is_admin and user.organization:
            org_users = user.organization.members.all()
            cards = NFCCard.objects.filter(user__in=org_users)
        else:
            cards = user.cards.all()
        
        # Get last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        analytics = DailyAnalyticsSummary.objects.filter(
            card__in=cards,
            date__gte=thirty_days_ago.date()
        ).order_by('card', 'date')
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="analytics_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Card', 'Date', 'Total Views', 'Unique Views',
            'Contact Saves', 'Phone Clicks', 'Email Clicks',
            'Website Clicks', 'Social Clicks', 'Shares'
        ])
        
        for stat in analytics:
            writer.writerow([
                stat.card.url_slug,
                stat.date,
                stat.total_views,
                stat.unique_views,
                stat.contact_saves,
                stat.phone_clicks,
                stat.email_clicks,
                stat.website_clicks,
                stat.social_clicks,
                stat.shares
            ])
        
        return response
