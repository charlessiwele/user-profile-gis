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


# Signal to automatically create/update user profile when user is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
