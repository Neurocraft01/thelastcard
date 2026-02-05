"""
Views for profiles app.
Handles public NFC card profile pages.
"""

import hashlib
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from cards.models import NFCCard


class PublicProfileView(TemplateView):
    """Public profile page for NFC cards."""
    template_name = 'profile/public.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        
        card = get_object_or_404(NFCCard, url_slug=slug)
        context['card'] = card
        
        if card.user and hasattr(card.user, 'profile'):
            context['profile'] = card.user.profile
        else:
            context['profile'] = None
        
        if card.theme:
            context['theme'] = card.theme
        
        # Track the view
        self.track_view(card)
        
        return context
    
    def track_view(self, card):
        """Track profile view analytics."""
        from analytics.models import ProfileAnalytics
        
        request = self.request
        ip = self.get_client_ip(request)
        
        # Hash IP for privacy
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
        
        # Get device info
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        device_type = self.detect_device_type(user_agent)
        
        ProfileAnalytics.objects.create(
            card=card,
            interaction_type=ProfileAnalytics.InteractionType.VIEW,
            visitor_ip_hash=ip_hash,
            user_agent=user_agent,
            referrer=request.META.get('HTTP_REFERER', '')[:200] if request.META.get('HTTP_REFERER') else '',
            device_type=device_type
        )
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
    
    def detect_device_type(self, user_agent):
        """Detect device type from user agent."""
        user_agent = user_agent.lower()
        if 'mobile' in user_agent or 'android' in user_agent and 'mobile' in user_agent:
            return 'MOBILE'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'TABLET'
        elif 'windows' in user_agent or 'macintosh' in user_agent or 'linux' in user_agent:
            return 'DESKTOP'
        return 'OTHER'


class DownloadVCardView(View):
    """Download vCard for contact."""
    
    def get(self, request, slug):
        card = get_object_or_404(NFCCard, url_slug=slug)
        
        if not card.user or not hasattr(card.user, 'profile'):
            return HttpResponse('Profile not found', status=404)
        
        profile = card.user.profile
        vcard_content = profile.generate_vcard()
        
        # Track the download
        self.track_interaction(card, request)
        
        response = HttpResponse(vcard_content, content_type='text/vcard')
        response['Content-Disposition'] = f'attachment; filename="{profile.full_name}.vcf"'
        return response
    
    def track_interaction(self, card, request):
        """Track contact save analytics."""
        from analytics.models import ProfileAnalytics
        
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
        
        ProfileAnalytics.objects.create(
            card=card,
            interaction_type=ProfileAnalytics.InteractionType.CONTACT_SAVE,
            visitor_ip_hash=ip_hash,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )


class QRCodeView(View):
    """Generate and serve QR code for profile."""
    
    def get(self, request, slug):
        card = get_object_or_404(NFCCard, url_slug=slug)
        
        # Check if download is requested
        is_download = request.GET.get('download') == 'true'
        
        # If QR code exists, serve it
        if card.qr_code:
            response = HttpResponse(card.qr_code.read(), content_type='image/png')
            if is_download:
                response['Content-Disposition'] = f'attachment; filename="qr_{slug}.png"'
            else:
                response['Content-Disposition'] = f'inline; filename="qr_{slug}.png"'
            return response
        
        # Generate QR code on the fly
        try:
            import qrcode
            from io import BytesIO
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(card.public_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color='#D4AF37', back_color='white')
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            response = HttpResponse(buffer.getvalue(), content_type='image/png')
            if is_download:
                response['Content-Disposition'] = f'attachment; filename="qr_{slug}.png"'
            else:
                response['Content-Disposition'] = f'inline; filename="qr_{slug}.png"'
            
            # Track QR code interaction
            if is_download:
                self.track_qr_download(card, request)
            
            return response
            
        except ImportError:
            return HttpResponse('QR code generation not available', status=501)
    
    def track_qr_download(self, card, request):
        """Track QR code download analytics."""
        from analytics.models import ProfileAnalytics
        
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]
        
        ProfileAnalytics.objects.create(
            card=card,
            interaction_type='QR_DOWNLOAD',
            visitor_ip_hash=ip_hash,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )


class MobilePreviewView(TemplateView):
    """Mobile-optimized preview of profile."""
    template_name = 'profile/mobile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        
        card = get_object_or_404(NFCCard, url_slug=slug)
        context['card'] = card
        
        if card.user and hasattr(card.user, 'profile'):
            context['profile'] = card.user.profile
        else:
            context['profile'] = None
        
        if card.theme:
            context['theme'] = card.theme
        
        return context
