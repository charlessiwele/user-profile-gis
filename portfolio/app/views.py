from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from .forms import UserForm, UserProfileForm


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user profiles
    Allows CRUD operations on user profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter to show only the authenticated user's profile for non-staff users
        """
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for users with their profiles
    Read-only access to user data
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter to show only the authenticated user for non-staff users
        """
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


# Template-based views for profile pages

@login_required
def profile_view(request, username=None):
    """
    Display user profile page
    Users can only view their own profile unless they are superuser
    """
    if username:
        # View another user's profile
        user = get_object_or_404(User, username=username)
        
        # Permission check: only superusers can view other users' profiles
        if request.user != user and not request.user.is_superuser:
            messages.error(
                request, 
                'You do not have permission to view other users\' profiles. '
                'Only superusers can view all profiles.'
            )
            return redirect('profile_view')  # Redirect to their own profile
    else:
        # View own profile
        user = request.user
    
    profile = user.profile
    
    # Check if viewing own profile
    is_own_profile = (request.user == user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': is_own_profile,
    }
    
    return render(request, 'app/profile_view.html', context)


@login_required
def profile_edit(request):
    """
    Edit user profile page with forms for User and UserProfile
    """
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'app/profile_edit.html', context)


@login_required
def map_view(request):
    """
    Full-screen map view for displaying user locations
    Supports filtering by user_id parameter
    """
    user_id = request.GET.get('user_id')
    
    # Convert 'None' string or empty values to actual None
    if user_id in ['None', '', None]:
        user_id = None
    
    context = {
        'user_id': user_id or '',  # Pass empty string instead of None to avoid 'None' in JS
        'show_all': user_id is None,
    }
    
    return render(request, 'app/map_view.html', context)


@login_required
def user_locations_geojson(request):
    """
    API endpoint that returns user locations in GeoJSON format
    Supports filtering by user_id parameter
    """
    user_id = request.GET.get('user_id')
    
    # Filter profiles based on user_id parameter
    # Handle case where user_id might be 'None' string or empty
    if user_id and user_id != 'None' and user_id.strip():
        try:
            user_id = int(user_id)
            profiles = UserProfile.objects.filter(
                user_id=user_id,
                location__isnull=False
            ).select_related('user')
        except (ValueError, TypeError):
            # Invalid user_id, show based on user permissions
            if request.user.is_staff:
                profiles = UserProfile.objects.filter(
                    location__isnull=False
                ).select_related('user')
            else:
                profiles = UserProfile.objects.filter(
                    user=request.user,
                    location__isnull=False
                ).select_related('user')
    else:
        # Show all users with locations (for staff) or just the current user (for regular users)
        if request.user.is_staff:
            profiles = UserProfile.objects.filter(
                location__isnull=False
            ).select_related('user')
        else:
            profiles = UserProfile.objects.filter(
                user=request.user,
                location__isnull=False
            ).select_related('user')
    
    # Build GeoJSON FeatureCollection
    features = []
    for profile in profiles:
        if profile.location:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [profile.location.x, profile.location.y]  # [longitude, latitude]
                },
                'properties': {
                    'username': profile.user.username,
                    'full_name': profile.user.get_full_name() or profile.user.username,
                    'email': profile.user.email,
                    'phone_number': profile.phone_number or 'Not provided',
                    'home_address': profile.home_address or 'Not provided',
                    'user_id': profile.user.id,
                }
            }
            features.append(feature)
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(geojson)
