from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(GISModelAdmin):
    """
    Admin interface for UserProfile with map widget for location field
    """
    list_display = ['user', 'phone_number', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'home_address']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('home_address', 'phone_number')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
