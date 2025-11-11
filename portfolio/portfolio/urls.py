"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import (
    UserProfileViewSet, UserViewSet, profile_view, profile_edit,
    map_view, user_locations_geojson
)

# Create a router for REST API endpoints
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Login/logout for browsable API
    
    # Profile pages
    path('', profile_view, name='profile_view'),  # Default home page
    path('profile/', profile_view, name='profile_view'),  # Profile view
    path('profile/edit/', profile_edit, name='profile_edit'),  # Profile edit
    path('profile/<str:username>/', profile_view, name='profile_view_user'),  # View other user's profile
    
    # Map pages
    path('map/', map_view, name='map_view'),  # Full-screen map view
    path('map/api/locations/', user_locations_geojson, name='user_locations_geojson'),  # GeoJSON API
]
