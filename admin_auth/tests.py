import uuid
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model, authenticate
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from PIL import Image
import io

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserManagerTestCase(TestCase):
    """Test cases for UserManager"""

    def setUp(self):
        self.user_manager = User.objects
        self.user_data = {
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test user creation"""
        user = self.user_manager.create_user(
            email=self.user_data['email'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            password=self.user_data['password']
        )
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        """Test user creation without email raises error"""
        with self.assertRaises(ValueError):
            self.user_manager.create_user(email='')

    def test_create_superuser(self):
        """Test superuser creation"""
        user = self.user_manager.create_superuser(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)


class UserModelTestCase(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, 'admin@example.com')
        self.assertEqual(self.user.first_name, 'Admin')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Admin')

    def test_user_default_values(self):
        """Test user default values"""
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_active)
        self.assertIsNotNone(self.user.date_joined)

    def test_user_uuid_field(self):
        """Test user UUID field"""
        self.assertIsInstance(self.user.id, uuid.UUID)


class UserProfileModelTestCase(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )
        # Get the profile that was created automatically by signal
        self.profile = self.user.profile

    def test_profile_creation(self):
        """Test profile creation via signal"""
        self.assertIsInstance(self.profile, UserProfile)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str_representation(self):
        """Test profile string representation"""
        expected_str = f"Profile of {self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.profile), expected_str)

    def test_profile_full_name_property(self):
        """Test profile full name property"""
        expected_full_name = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(self.profile.full_name, expected_full_name)

    def test_profile_uuid_field(self):
        """Test profile UUID field"""
        self.assertIsInstance(self.profile.id, uuid.UUID)

    def test_profile_default_values(self):
        """Test profile default values"""
        self.assertIsNone(self.profile.phone_number)
        self.assertIsNone(self.profile.address)
        self.assertIsNotNone(self.profile.updated_at)

    def test_profile_update(self):
        """Test profile update"""
        self.profile.phone_number = '+1234567890'
        self.profile.address = '123 Test St'
        self.profile.save()

        self.assertEqual(self.profile.phone_number, '+1234567890')
        self.assertEqual(self.profile.address, '123 Test St')


class UserSerializerTestCase(TestCase):
    """Test cases for UserSerializer"""

    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password2': 'testpass123',
            'is_superuser': True
        }

    def test_valid_serializer_data(self):
        """Test serializer with valid data"""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_create_user(self):
        """Test serializer creates user correctly"""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
        self.assertTrue(user.check_password(self.valid_data['password']))

    def test_serializer_password_mismatch(self):
        """Test serializer with password mismatch"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        serializer = UserSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())  # Validation happens in create()

        # The error should be raised when calling save()
        with self.assertRaises(Exception):
            serializer.save()

    def test_serializer_duplicate_email(self):
        """Test serializer with duplicate email"""
        # Create a user first
        User.objects.create_user(
            email='test@example.com',
            first_name='Existing',
            last_name='User',
            password='testpass123'
        )

        serializer = UserSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_serializer_invalid_email(self):
        """Test serializer with invalid email"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_serializer_short_password(self):
        """Test serializer with short password"""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'short'
        invalid_data['password2'] = 'short'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


class UserProfileSerializerTestCase(TestCase):
    """Test cases for UserProfileSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_profile_serializer_fields(self):
        """Test profile serializer fields"""
        serializer = UserProfileSerializer(instance=self.profile)
        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('user', data)
        self.assertIn('full_name', data)
        self.assertIn('phone_number', data)
        self.assertIn('address', data)
        self.assertIn('updated_at', data)

    def test_profile_serializer_data(self):
        """Test profile serializer data"""
        serializer = UserProfileSerializer(instance=self.profile)
        data = serializer.data
        self.assertEqual(data['phone_number'], None)
        self.assertEqual(data['address'], None)
        self.assertEqual(data['full_name'], 'Test User')

    def test_profile_serializer_valid_image(self):
        """Test profile serializer with valid image"""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile(
            'test.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )

        # Test with data validation - only test the image field validation
        serializer = UserProfileSerializer()
        validated_image = serializer.validate_profile_picture(image_file)
        self.assertEqual(validated_image, image_file)

    def test_profile_serializer_invalid_image(self):
        """Test profile serializer with invalid image type"""
        # Create a test text file
        text_file = SimpleUploadedFile(
            'test.txt',
            b'This is not an image',
            content_type='text/plain'
        )

        # Test with data validation - only test the image field validation
        serializer = UserProfileSerializer()
        with self.assertRaises(Exception):
            serializer.validate_profile_picture(text_file)


class UserViewsTestCase(APITestCase):
    """Test cases for user views"""

    def setUp(self):
        self.client = APIClient()
        # Use correct URLs with /admin/ prefix
        self.register_url = '/admin/auth/signup/'
        self.login_url = '/admin/auth/login/'
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password2': 'testpass123',
            'is_superuser': True
        }

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

        # Verify user was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])

    def test_register_user_invalid_data(self):
        """Test user registration with invalid data"""
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'

        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)

    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email"""
        # Create a user first
        User.objects.create_user(
            email='test@example.com',
            first_name='Existing',
            last_name='User',
            password='testpass123'
        )

        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_success(self):
        """Test successful login"""
        # Create a user first
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], user.email)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_inactive_user(self):
        """Test login with inactive user"""
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        user.is_active = False
        user.save()

        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetTestCase(APITestCase):
    """Test cases for password reset functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        # Use correct URL with /admin/ prefix
        self.request_reset_url = '/admin/password-reset/'

    @patch('admin_auth.views.send_mail')
    @patch('admin_auth.views.render_to_string')
    @override_settings(FRONTEND_URL='http://localhost:3000')
    def test_request_password_reset_success(self, mock_render_to_string, mock_send_mail):
        """Test successful password reset request"""
        mock_render_to_string.return_value = '<html>Reset your password</html>'
        mock_send_mail.return_value = 1

        data = {'email': 'test@example.com'}
        response = self.client.post(self.request_reset_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_mail.assert_called_once()

    def test_request_password_reset_no_email(self):
        """Test password reset request without email"""
        data = {}
        response = self.client.post(self.request_reset_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_request_password_reset_user_not_found(self):
        """Test password reset request for non-existent user"""
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.request_reset_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check if response has data attribute (for DRF responses)
        if hasattr(response, 'data'):
            self.assertIn('error', response.data)


class UserProfileViewsTestCase(APITestCase):
    """Test cases for user profile views"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        """Test getting user profile"""
        # Use correct URL with /admin/ prefix
        url = '/admin/profile/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], None)
        self.assertEqual(response.data['address'], None)

    def test_update_user_profile(self):
        """Test updating user profile"""
        # Use correct URL with /admin/ prefix
        url = '/admin/profile/'
        data = {
            'phone_number': '+0987654321',
            'address': '456 New St'
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '+0987654321')
        self.assertEqual(response.data['address'], '456 New St')

        # Verify database was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, '+0987654321')
        self.assertEqual(self.profile.address, '456 New St')


class AdminAuthIntegrationTestCase(TestCase):
    """Integration test cases for admin auth functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )

    def test_user_profile_creation_signal(self):
        """Test that user profile is created automatically"""
        # The profile should be created automatically via signal
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_user_authentication_flow(self):
        """Test complete user authentication flow"""
        # Test user can authenticate using Django's authenticate function
        authenticated_user = authenticate(
            email='admin@example.com',
            password='testpass123'
        )
        self.assertEqual(authenticated_user, self.user)

    def test_user_permissions(self):
        """Test user permissions"""
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

    def test_user_profile_relationship(self):
        """Test user profile relationship"""
        profile = self.user.profile
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.full_name, 'Admin User')