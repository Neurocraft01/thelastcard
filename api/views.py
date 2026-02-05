"""
API views using Django REST Framework.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from cards.models import NFCCard
from themes.models import Theme
from analytics.models import ProfileAnalytics


class ProfileAPIView(APIView):
    """Get current user's profile."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if hasattr(user, 'profile'):
            profile = user.profile
            return Response({
                'full_name': profile.full_name,
                'bio': profile.bio,
                'company': profile.company,
                'designation': profile.designation,
                'phone_primary': profile.phone_primary,
                'email_public': profile.email_public,
                'website': profile.website,
                'location': profile.location,
                'social_links': profile.social_links,
                'completion_percentage': profile.completion_percentage,
            })
        return Response({'error': 'Profile not found'}, status=404)


class ProfileUpdateAPIView(APIView):
    """Update current user's profile."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'full_name': user.email.split('@')[0]}
        )
        
        # Update fields
        allowed_fields = [
            'full_name', 'first_name', 'last_name', 'bio',
            'company', 'designation', 'department',
            'phone_primary', 'phone_secondary', 'email_public', 'website',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code',
            'social_links', 'custom_fields'
        ]
        
        for field in allowed_fields:
            if field in request.data:
                setattr(profile, field, request.data[field])
        
        profile.save()
        
        return Response({
            'status': 'success',
            'completion_percentage': profile.completion_percentage
        })


class CardListAPIView(APIView):
    """List user's cards."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cards = NFCCard.objects.filter(user=request.user)
        return Response([
            {
                'id': str(card.id),
                'url_slug': card.url_slug,
                'status': card.status,
                'is_active': card.is_active,
                'public_url': card.public_url,
                'view_count': card.view_count,
            }
            for card in cards
        ])


class CardDetailAPIView(APIView):
    """Get card details."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        card = get_object_or_404(NFCCard, pk=pk, user=request.user)
        return Response({
            'id': str(card.id),
            'card_uid': card.card_uid,
            'url_slug': card.url_slug,
            'status': card.status,
            'is_active': card.is_active,
            'public_url': card.public_url,
            'theme_id': str(card.theme.id) if card.theme else None,
            'created_at': card.created_at.isoformat(),
        })


class TrackEventAPIView(APIView):
    """Track analytics event."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        import hashlib
        
        card_id = request.data.get('card_id')
        event_type = request.data.get('event', 'VIEW').upper()
        metadata = request.data.get('metadata', {})
        
        try:
            card = NFCCard.objects.get(pk=card_id)
            
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
            
            ProfileAnalytics.objects.create(
                card=card,
                interaction_type=event_type,
                metadata=metadata,
                visitor_ip_hash=ip_hash,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
            )
            
            return Response({'status': 'success'})
        except NFCCard.DoesNotExist:
            return Response({'error': 'Card not found'}, status=404)


class AnalyticsSummaryAPIView(APIView):
    """Get analytics summary for user's cards."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from django.db.models import Sum
        from django.utils import timezone
        from datetime import timedelta
        from analytics.models import DailyAnalyticsSummary
        
        cards = NFCCard.objects.filter(user=request.user)
        
        # Last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        stats = DailyAnalyticsSummary.objects.filter(
            card__in=cards,
            date__gte=thirty_days_ago.date()
        ).aggregate(
            total_views=Sum('total_views'),
            unique_views=Sum('unique_views'),
            contact_saves=Sum('contact_saves'),
            phone_clicks=Sum('phone_clicks'),
            email_clicks=Sum('email_clicks')
        )
        
        return Response(stats)


class ThemeListAPIView(APIView):
    """List available themes."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        themes = Theme.objects.filter(is_active=True, is_public=True)
        return Response([
            {
                'id': str(theme.id),
                'name': theme.name,
                'slug': theme.slug,
                'description': theme.description,
                'primary_color': theme.primary_color,
                'is_premium': theme.is_premium,
                'dark_mode': theme.dark_mode,
            }
            for theme in themes
        ])
