from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile model with additional details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    home_address = models.TextField(blank=True, null=True, help_text="Full home address")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number")
    location = gis_models.PointField(blank=True, null=True, help_text="Geographic location (longitude, latitude)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class UserActivityLog(models.Model):
    """
    Model to track user login and logout activity
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('failed_login', 'Failed Login'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    username = models.CharField(max_length=150, help_text="Username (stored even if user is deleted)")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True, help_text="Browser/device information")
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    class Meta:
        verbose_name = 'User Activity Log'
        verbose_name_plural = 'User Activity Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_action_display()} at {self.timestamp}"


# Signal to automatically create/update user profile when user is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
