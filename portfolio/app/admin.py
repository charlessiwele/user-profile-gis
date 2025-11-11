from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(GISModelAdmin):
    """
    Admin interface for UserProfile with map widget for location field
    """
    list_display = ['user', 'phone_number', 'created_at', 'updated_at', 'view_on_map_button']
    search_fields = ['user__username', 'user__email', 'phone_number', 'home_address']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'view_on_map_link']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('home_address', 'phone_number')
        }),
        ('Location', {
            'fields': ('location', 'view_on_map_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def view_on_map_button(self, obj):
        """Button in list view to view user's location on map"""
        if obj.location:
            url = reverse('map_view') + f'?user_id={obj.user.id}'
            return format_html(
                '<a href="{}" target="_blank" style="'
                'display: inline-block; '
                'padding: 5px 10px; '
                'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                'color: white; '
                'text-decoration: none; '
                'border-radius: 4px; '
                'font-size: 12px; '
                'font-weight: 600;'
                '">📍 View on Map</a>',
                url
            )
        return format_html('<span style="color: #999;">No location set</span>')
    view_on_map_button.short_description = 'Map'
    
    def view_on_map_link(self, obj):
        """Link in change form to view user's location on map"""
        if obj.location:
            url = reverse('map_view') + f'?user_id={obj.user.id}'
            return format_html(
                '<a href="{}" target="_blank" style="'
                'display: inline-block; '
                'padding: 10px 20px; '
                'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                'color: white; '
                'text-decoration: none; '
                'border-radius: 8px; '
                'font-size: 14px; '
                'font-weight: 600; '
                'margin-top: 10px;'
                '">📍 View This User on Map</a>',
                url
            )
        return format_html('<span style="color: #999; font-style: italic;">Location not set. Add coordinates above to enable map view.</span>')
    view_on_map_link.short_description = 'Map View'
    
    def changelist_view(self, request, extra_context=None):
        """Add custom button to view all users on map in list view"""
        extra_context = extra_context or {}
        extra_context['show_all_on_map_url'] = reverse('map_view')
        return super().changelist_view(request, extra_context=extra_context)
