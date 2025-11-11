from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from .models import UserProfile, UserActivityLog


@admin.register(UserProfile)
class UserProfileAdmin(GISModelAdmin):
    """
    Admin interface for UserProfile with map widget for location field
    Staff users can only view/edit their own profile
    Superusers can view/edit all profiles
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
    
    def get_queryset(self, request):
        """
        Filter queryset based on user permissions
        Non-superuser staff can only see their own profile
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Non-superuser staff users only see their own profile
        return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        """
        Non-superuser staff can only change their own profile
        """
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """
        Only superusers can delete profiles
        """
        if request.user.is_superuser:
            return True
        return False
    
    def has_add_permission(self, request):
        """
        Profiles are created automatically, no manual creation
        """
        return False
    
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
        """
        Add custom button to view all users on map in list view
        Only show for superusers since non-superuser staff only see their own profile
        """
        extra_context = extra_context or {}
        # Only superusers get the "View All Users on Map" button
        if request.user.is_superuser:
            extra_context['show_all_on_map_url'] = reverse('map_view')
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make user field readonly for non-superuser staff
        """
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.append('user')
        return readonly
    
    def has_module_permission(self, request):
        """
        Allow access to module if user is in Staff group or is superuser
        """
        if request.user.is_superuser:
            return True
        # Check if user is in Staff group or has view permission
        return (
            request.user.groups.filter(name='Staff').exists() or
            request.user.has_perm('app.view_userprofile')
        )


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing user login/logout activity logs
    Non-superuser staff can only see their own activity logs
    Superusers can see all activity logs
    """
    list_display = ['colored_action', 'username', 'user_link', 'timestamp', 'ip_address', 'short_user_agent']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['username', 'ip_address', 'user__email']
    readonly_fields = ['user', 'username', 'action', 'timestamp', 'ip_address', 'user_agent', 'session_key']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        """
        Filter queryset based on user permissions
        Non-superuser staff can only see their own activity logs
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Non-superuser staff users only see their own logs
        return qs.filter(user=request.user)
    
    # Prevent adding/editing logs manually
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete logs
        return request.user.is_superuser
    
    def has_module_permission(self, request):
        """
        Allow access to activity logs if user is in Staff group or is superuser
        """
        if request.user.is_superuser:
            return True
        # Check if user is in Staff group
        return request.user.groups.filter(name='Staff').exists()
    
    def colored_action(self, obj):
        """Display action with color coding"""
        colors = {
            'login': '#28a745',      # Green
            'logout': '#6c757d',     # Gray
            'failed_login': '#dc3545',  # Red
        }
        color = colors.get(obj.action, '#000')
        icon = {
            'login': '✅',
            'logout': '🚪',
            'failed_login': '❌',
        }.get(obj.action, '•')
        
        return format_html(
            '<span style="color: {}; font-weight: 600;">{} {}</span>',
            color,
            icon,
            obj.get_action_display()
        )
    colored_action.short_description = 'Action'
    colored_action.admin_order_field = 'action'
    
    def user_link(self, obj):
        """Link to user's profile in admin"""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return format_html('<span style="color: #999;">User Deleted</span>')
    user_link.short_description = 'User Account'
    user_link.admin_order_field = 'user'
    
    def short_user_agent(self, obj):
        """Display shortened user agent"""
        if not obj.user_agent:
            return '-'
        ua = obj.user_agent
        # Shorten user agent for display
        if len(ua) > 50:
            return ua[:50] + '...'
        return ua
    short_user_agent.short_description = 'Browser/Device'
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('action', 'username', 'user', 'timestamp')
        }),
        ('Session Details', {
            'fields': ('ip_address', 'session_key')
        }),
        ('Browser Information', {
            'fields': ('user_agent',),
            'classes': ('collapse',)
        }),
    )


# Unregister the default User admin and register custom one
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin that restricts non-superuser staff to only see themselves
    """
    
    def get_queryset(self, request):
        """
        Filter queryset based on user permissions
        Non-superuser staff can only see their own user account
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Non-superuser staff users only see themselves
        return qs.filter(pk=request.user.pk)
    
    def has_change_permission(self, request, obj=None):
        """
        Non-superuser staff can only change their own account
        """
        if request.user.is_superuser:
            return True
        if obj is not None and obj != request.user:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """
        Only superusers can delete user accounts
        """
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """
        Only superusers can add users via admin
        Regular users should use the signup page
        """
        return request.user.is_superuser
