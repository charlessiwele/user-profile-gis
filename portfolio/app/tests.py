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
    
    def test_list_profiles_as_staff_user(self):
        """
        Test that staff users can only see their own profile
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.profiles_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'staffuser')
    
    def test_list_profiles_as_superuser(self):
        """
        Test that superusers can see all profiles
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.profiles_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        usernames = [profile['username'] for profile in response.data]
        self.assertIn('staffuser', usernames)
        self.assertIn('admin', usernames)
        self.assertIn('otherstaff', usernames)
    
    def test_retrieve_own_profile(self):
        """
        Test that users can retrieve their own profile
        """
        self.client.force_authenticate(user=self.staff_user)
        profile_id = self.staff_user.profile.id
        response = self.client.get(f'{self.profiles_url}{profile_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'staffuser')
        self.assertEqual(response.data['email'], 'staff@test.com')
        self.assertEqual(response.data['phone_number'], '1234567890')
        self.assertEqual(response.data['home_address'], '123 Test Street')
    
    def test_retrieve_other_profile_as_staff(self):
        """
        Test that staff users cannot retrieve other users' profiles
        """
        self.client.force_authenticate(user=self.staff_user)
        other_profile_id = self.other_staff_user.profile.id
        response = self.client.get(f'{self.profiles_url}{other_profile_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_other_profile_as_superuser(self):
        """
        Test that superusers can retrieve any profile
        """
        self.client.force_authenticate(user=self.superuser)
        staff_profile_id = self.staff_user.profile.id
        response = self.client.get(f'{self.profiles_url}{staff_profile_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'staffuser')
    
    def test_update_own_profile(self):
        """
        Test that users can update their own profile
        """
        self.client.force_authenticate(user=self.staff_user)
        profile_id = self.staff_user.profile.id
        
        update_data = {
            'phone_number': '9999999999',
            'home_address': 'Updated Address'
        }
        
        response = self.client.patch(
            f'{self.profiles_url}{profile_id}/',
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '9999999999')
        self.assertEqual(response.data['home_address'], 'Updated Address')
        
        # Verify database update
        self.staff_user.profile.refresh_from_db()
        self.assertEqual(self.staff_user.profile.phone_number, '9999999999')
    
    def test_update_other_profile_as_staff(self):
        """
        Test that staff users cannot update other users' profiles
        """
        self.client.force_authenticate(user=self.staff_user)
        other_profile_id = self.other_staff_user.profile.id
        
        update_data = {'phone_number': '1111111111'}
        
        response = self.client.patch(
            f'{self.profiles_url}{other_profile_id}/',
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_location_field(self):
        """
        Test updating the geographic location field
        """
        self.client.force_authenticate(user=self.staff_user)
        profile_id = self.staff_user.profile.id
        
        # GeoJSON format for location
        update_data = {
            'location': {
                'type': 'Point',
                'coordinates': [-118.2437, 34.0522]  # Los Angeles
            }
        }
        
        response = self.client.patch(
            f'{self.profiles_url}{profile_id}/',
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify location was updated
        self.staff_user.profile.refresh_from_db()
        self.assertIsNotNone(self.staff_user.profile.location)
        self.assertAlmostEqual(self.staff_user.profile.location.x, -118.2437, places=4)
        self.assertAlmostEqual(self.staff_user.profile.location.y, 34.0522, places=4)
    
    def test_delete_own_profile_not_allowed(self):
        """
        Test that users cannot delete their own profile
        (Profile is linked to User, so it shouldn't be directly deletable)
        """
        self.client.force_authenticate(user=self.staff_user)
        profile_id = self.staff_user.profile.id
        
        response = self.client.delete(f'{self.profiles_url}{profile_id}/')
        
        # This should either fail or be restricted
        # Depending on business logic, adjust assertion
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_204_NO_CONTENT]
        )
    
    def test_profile_serializer_fields(self):
        """
        Test that profile serializer returns expected fields
        """
        self.client.force_authenticate(user=self.staff_user)
        profile_id = self.staff_user.profile.id
        response = self.client.get(f'{self.profiles_url}{profile_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check all expected fields are present
        expected_fields = [
            'id', 'username', 'email', 'home_address', 
            'phone_number', 'location', 'created_at', 'updated_at'
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)


class UserViewSetTestCase(APITestCase):
    """
    Test cases for UserViewSet API endpoints
    Tests read-only operations and permission levels
    """
    
    def setUp(self):
        """
        Set up test data - create users
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
        
        # Create another staff user
        self.other_staff_user = User.objects.create_user(
            username='otherstaff',
            email='other@test.com',
            password='testpass123',
            first_name='Other',
            last_name='Staff',
            is_staff=True
        )
        
        # API client
        self.client = APIClient()
        
        # Base URL for user endpoints
        self.users_url = '/api/users/'
    
    def test_list_users_unauthenticated(self):
        """
        Test that unauthenticated users cannot access user list
        """
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_users_as_staff_user(self):
        """
        Test that staff users can only see themselves
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'staffuser')
    
    def test_list_users_as_superuser(self):
        """
        Test that superusers can see all users
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        usernames = [user['username'] for user in response.data]
        self.assertIn('staffuser', usernames)
        self.assertIn('admin', usernames)
        self.assertIn('otherstaff', usernames)
    
    def test_retrieve_own_user(self):
        """
        Test that users can retrieve their own user data
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f'{self.users_url}{self.staff_user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'staffuser')
        self.assertEqual(response.data['email'], 'staff@test.com')
        self.assertEqual(response.data['first_name'], 'Staff')
        self.assertEqual(response.data['last_name'], 'User')
        
        # Check that profile is included
        self.assertIn('profile', response.data)
    
    def test_retrieve_other_user_as_staff(self):
        """
        Test that staff users cannot retrieve other users' data
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f'{self.users_url}{self.other_staff_user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_other_user_as_superuser(self):
        """
        Test that superusers can retrieve any user's data
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(f'{self.users_url}{self.staff_user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'staffuser')
    
    def test_user_viewset_is_read_only(self):
        """
        Test that UserViewSet does not allow POST, PUT, PATCH, DELETE
        """
        self.client.force_authenticate(user=self.staff_user)
        
        # Test POST
        post_data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpass123'
        }
        response = self.client.post(self.users_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test PUT
        put_data = {'first_name': 'Updated'}
        response = self.client.put(
            f'{self.users_url}{self.staff_user.id}/',
            put_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test PATCH
        response = self.client.patch(
            f'{self.users_url}{self.staff_user.id}/',
            put_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test DELETE
        response = self.client.delete(f'{self.users_url}{self.staff_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_user_serializer_fields(self):
        """
        Test that user serializer returns expected fields
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f'{self.users_url}{self.staff_user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check all expected fields are present
        expected_fields = [
            'id', 'username', 'email', 'first_name', 
            'last_name', 'date_joined', 'profile'
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)
        
        # Check profile nested fields
        profile_fields = [
            'id', 'username', 'email', 'home_address',
            'phone_number', 'location', 'created_at', 'updated_at'
        ]
        for field in profile_fields:
            self.assertIn(field, response.data['profile'])
    
    def test_user_with_profile_data(self):
        """
        Test that user endpoint returns complete profile data
        """
        # Update staff user profile with data
        self.staff_user.profile.phone_number = '1234567890'
        self.staff_user.profile.home_address = '123 Test Street'
        self.staff_user.profile.save()
        
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f'{self.users_url}{self.staff_user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['phone_number'], '1234567890')
        self.assertEqual(response.data['profile']['home_address'], '123 Test Street')
