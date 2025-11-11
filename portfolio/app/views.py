from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    """
    if username:
        # View another user's profile
        user = get_object_or_404(User, username=username)
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
