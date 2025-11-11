from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import UserActivityLog


def get_client_ip(request):
    """
    Get the client's IP address from the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Get the user agent (browser/device info) from the request
    """
    return request.META.get('HTTP_USER_AGENT', '')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Signal handler to log successful user logins
    """
    UserActivityLog.objects.create(
        user=user,
        username=user.username,
        action='login',
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
        session_key=request.session.session_key
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    Signal handler to log user logouts
    """
    if user:  # user can be None if session expired
        UserActivityLog.objects.create(
            user=user,
            username=user.username,
            action='logout',
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            session_key=request.session.session_key if hasattr(request, 'session') else None
        )


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """
    Signal handler to log failed login attempts
    """
    username = credentials.get('username', 'unknown')
    UserActivityLog.objects.create(
        user=None,  # No user object for failed logins
        username=username,
        action='failed_login',
        ip_address=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else '',
        session_key=None
    )

