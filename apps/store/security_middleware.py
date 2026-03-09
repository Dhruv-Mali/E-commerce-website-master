"""Security middleware for additional protection"""
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=()'
        )
        
        return response

class RateLimitMiddleware(MiddlewareMixin):
    """Rate limiting middleware"""
    
    def process_request(self, request):
        from django.core.cache import cache
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Rate limit key
        cache_key = f'rate_limit_{ip}'
        requests = cache.get(cache_key, 0)
        
        # Allow 100 requests per minute
        if requests > 100:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return HttpResponseForbidden("Rate limit exceeded")
        
        cache.set(cache_key, requests + 1, 60)
        return None

class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """Detect and prevent SQL injection attempts"""
    
    SQL_KEYWORDS = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'SELECT', 'EXEC', 'EXECUTE']
    
    def process_request(self, request):
        # Check GET parameters
        for key, value in request.GET.items():
            if self._contains_sql_injection(str(value)):
                logger.warning(f"Potential SQL injection detected from IP: {request.META.get('REMOTE_ADDR')}")
                return HttpResponseForbidden("Invalid request")
        
        return None
    
    def _contains_sql_injection(self, value):
        """Check if value contains SQL injection patterns"""
        value_upper = value.upper()
        for keyword in self.SQL_KEYWORDS:
            if keyword in value_upper and any(char in value for char in ['--', ';', '/*', '*/']):
                return True
        return False

class XSSProtectionMiddleware(MiddlewareMixin):
    """Detect and prevent XSS attempts"""
    
    XSS_PATTERNS = ['<script', 'javascript:', 'onerror=', 'onload=', '<iframe', '<object', '<embed']
    
    def process_request(self, request):
        # Check GET parameters
        for key, value in request.GET.items():
            if self._contains_xss(str(value)):
                logger.warning(f"Potential XSS detected from IP: {request.META.get('REMOTE_ADDR')}")
                return HttpResponseForbidden("Invalid request")
        
        return None
    
    def _contains_xss(self, value):
        """Check if value contains XSS patterns"""
        value_lower = value.lower()
        for pattern in self.XSS_PATTERNS:
            if pattern in value_lower:
                return True
        return False
