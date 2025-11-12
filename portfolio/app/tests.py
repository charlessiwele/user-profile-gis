from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile


class UserProfileViewSetTestCase(APITestCase):
    """
    Test cases for UserProfileViewSet API endpoints
    Tests CRUD operations and permission levels
    """
    
    def setUp(self):
        """
        Set up test data - create users and profiles
        """
        # Create regular staff user
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='testpass123',
            first_name='Staff',
            last_name='User',
            is_staff=True
        )
        
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        
        # Create another staff user for testing permissions
        self.other_staff_user = User.objects.create_user(
            username='otherstaff',
            email='other@test.com',
            password='testpass123',
            first_name='Other',
            last_name='Staff',
            is_staff=True
        )
        
        # Update profiles with test data
        self.staff_user.profile.phone_number = '1234567890'
        self.staff_user.profile.home_address = '123 Test Street'
        self.staff_user.profile.location = Point(-122.4194, 37.7749)  # San Francisco
        self.staff_user.profile.save()
        
        self.superuser.profile.phone_number = '0987654321'
        self.superuser.profile.home_address = '456 Admin Avenue'
        self.superuser.profile.location = Point(-74.0060, 40.7128)  # New York
        self.superuser.profile.save()
        
        self.other_staff_user.profile.phone_number = '5555555555'
        self.other_staff_user.profile.home_address = '789 Other Road'
        self.other_staff_user.profile.save()
        
        # API client
        self.client = APIClient()
        
        # Base URL for profile endpoints
        self.profiles_url = '/api/profiles/'
    
    def test_list_profiles_unauthenticated(self):
        """
        Test that unauthenticated users cannot access profile list
        """
        response = self.client.get(self.profiles_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
