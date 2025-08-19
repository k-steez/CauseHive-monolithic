# notifications/tests.py

import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AdminNotification
from .serializers import AdminNotificationSerializer


class AdminNotificationModelTestCase(TestCase):
    """Test cases for AdminNotification model"""

    def setUp(self):
        self.notification_data = {
            'notif_type': 'cause_pending',
            'entity_id': 'test-entity-123',
            'message': 'Test notification message',
            'is_read': False
        }
        self.notification = AdminNotification.objects.create(**self.notification_data)

    def test_notification_creation(self):
        """Test notification model creation"""
        self.assertIsInstance(self.notification.id, uuid.UUID)
        self.assertEqual(self.notification.notif_type, self.notification_data['notif_type'])
        self.assertEqual(self.notification.entity_id, self.notification_data['entity_id'])
        self.assertEqual(self.notification.message, self.notification_data['message'])
        self.assertEqual(self.notification.is_read, self.notification_data['is_read'])
        self.assertIsNotNone(self.notification.created_at)

    def test_notification_string_representation(self):
        """Test notification string representation"""
        expected = f"{self.notification.notif_type} - {self.notification.entity_id} - {self.notification.message[:30]}"
        self.assertEqual(str(self.notification), expected)

    def test_notification_notif_type_choices(self):
        """Test notification type choices"""
        valid_types = ['cause_pending']
        for notif_type in valid_types:
            notification = AdminNotification.objects.create(
                notif_type=notif_type,
                entity_id=f'test-entity-{notif_type}',
                message=f'Test message for {notif_type}'
            )
            self.assertEqual(notification.notif_type, notif_type)

    def test_notification_default_values(self):
        """Test notification default values"""
        notification = AdminNotification.objects.create(
            notif_type='cause_pending',
            entity_id='test-entity-default',
            message='Test message'
        )
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)

    def test_notification_mark_as_read(self):
        """Test marking notification as read"""
        self.assertFalse(self.notification.is_read)
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)


class AdminNotificationSerializerTestCase(TestCase):
    """Test cases for AdminNotificationSerializer"""

    def setUp(self):
        self.notification = AdminNotification.objects.create(
            notif_type='cause_pending',
            entity_id='test-entity-123',
            message='Test notification message',
            is_read=False
        )

    def test_serializer_fields(self):
        """Test serializer includes all fields"""
        serializer = AdminNotificationSerializer(self.notification)
        expected_fields = ['id', 'notif_type', 'entity_id', 'message', 'is_read', 'created_at']
        for field in expected_fields:
            self.assertIn(field, serializer.data)

    def test_serializer_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'notif_type': 'cause_pending',
            'entity_id': 'test-entity-456',
            'message': 'Another test message',
            'is_read': True
        }
        serializer = AdminNotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_create_notification(self):
        """Test serializer creates notification correctly"""
        data = {
            'notif_type': 'cause_pending',
            'entity_id': 'test-entity-789',
            'message': 'Test message for creation',
            'is_read': False
        }
        serializer = AdminNotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        notification = serializer.save()

        self.assertIsInstance(notification, AdminNotification)
        self.assertEqual(notification.notif_type, data['notif_type'])
        self.assertEqual(notification.entity_id, data['entity_id'])
        self.assertEqual(notification.message, data['message'])


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
)
class AdminNotificationViewsTestCase(APITestCase):
    """Test cases for AdminNotification views"""

    def setUp(self):
        self.client = APIClient()
        # Create a test user for authentication
        from admin_auth.models import User
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.notification = AdminNotification.objects.create(
            notif_type='cause_pending',
            entity_id='test-entity-123',
            message='Test notification message',
            is_read=False
        )

    def test_list_notifications(self):
        """Test listing notifications"""
        response = self.client.get('/admin/notifications/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['notif_type'], 'cause_pending')

    def test_list_notifications_unauthorized(self):
        """Test listing notifications without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/admin/notifications/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_notification_read(self):
        """Test marking notification as read"""
        self.assertFalse(self.notification.is_read)

        response = self.client.patch(f'/admin/notifications/{self.notification.id}/mark-read/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Notification marked as read')

        # Verify notification was marked as read
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_mark_notification_read_unauthorized(self):
        """Test marking notification as read without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.patch(f'/admin/notifications/{self.notification.id}/mark-read/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_nonexistent_notification_read(self):
        """Test marking non-existent notification as read"""
        fake_id = uuid.uuid4()
        response = self.client.patch(f'/admin/notifications/{fake_id}/mark-read/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminNotificationIntegrationTestCase(APITestCase):
    """Integration test cases for AdminNotification"""

    def setUp(self):
        self.client = APIClient()
        from admin_auth.models import User
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_notification_lifecycle(self):
        """Test complete notification lifecycle"""
        # 1. Create notification
        notification = AdminNotification.objects.create(
            notif_type='cause_pending',
            entity_id='test-entity-lifecycle',
            message='Test lifecycle notification',
            is_read=False
        )

        # 2. List notifications
        list_response = self.client.get('/admin/notifications/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertFalse(list_response.data[0]['is_read'])

        # 3. Mark as read
        mark_read_response = self.client.patch(f'/admin/notifications/{notification.id}/mark-read/')
        self.assertEqual(mark_read_response.status_code, status.HTTP_200_OK)

        # 4. Verify it's marked as read
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

        # 5. List again to verify the change
        list_response_2 = self.client.get('/admin/notifications/')
        self.assertEqual(list_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response_2.data), 1)
        self.assertTrue(list_response_2.data[0]['is_read'])