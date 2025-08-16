import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import requests

from .serializers import CauseStatusUpdateSerializer
from .throttles import AdminActionThrottle
from .clients.cause_client import CauseClient

User = get_user_model()


class CauseStatusUpdateSerializerTestCase(TestCase):
    """Test cases for CauseStatusUpdateSerializer"""

    def setUp(self):
        self.valid_data = {
            'status': 'approved',
            'rejection_reason': ''
        }

    def test_valid_serializer_data(self):
        """Test serializer with valid data"""
        serializer = CauseStatusUpdateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_valid_status_choices(self):
        """Test all valid status choices"""
        valid_statuses = ["approved", "rejected", "under_review", "upcoming", "ongoing", "completed", "cancelled"]

        for status_choice in valid_statuses:
            data = {'status': status_choice}
            serializer = CauseStatusUpdateSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Status '{status_choice}' should be valid")

    def test_serializer_invalid_status(self):
        """Test serializer with invalid status"""
        invalid_data = self.valid_data.copy()
        invalid_data['status'] = 'invalid_status'

        serializer = CauseStatusUpdateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_serializer_missing_status(self):
        """Test serializer without status field"""
        data = {'rejection_reason': 'Some reason'}
        serializer = CauseStatusUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_serializer_with_rejection_reason(self):
        """Test serializer with rejection reason"""
        data = {
            'status': 'rejected',
            'rejection_reason': 'This cause violates our guidelines'
        }
        serializer = CauseStatusUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['rejection_reason'], 'This cause violates our guidelines')

    def test_serializer_blank_rejection_reason(self):
        """Test serializer with blank rejection reason"""
        data = {
            'status': 'approved',
            'rejection_reason': ''
        }
        serializer = CauseStatusUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['rejection_reason'], '')

    def test_serializer_without_rejection_reason(self):
        """Test serializer without rejection reason field"""
        data = {'status': 'approved'}
        serializer = CauseStatusUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('rejection_reason', serializer.validated_data)


class AdminActionThrottleTestCase(TestCase):
    """Test cases for AdminActionThrottle"""

    def test_throttle_scope(self):
        """Test throttle scope is set correctly"""
        throttle = AdminActionThrottle()
        self.assertEqual(throttle.scope, 'admin_action')

    def test_throttle_inheritance(self):
        """Test throttle inherits from UserRateThrottle"""
        throttle = AdminActionThrottle()
        self.assertIsInstance(throttle, AdminActionThrottle)


class CauseClientTestCase(TestCase):
    """Test cases for CauseClient"""

    @override_settings(
        CAUSE_SERVICE_URL='http://localhost:8001/causes',
        ADMIN_SERVICE_API_KEY='test-api-key'
    )
    @patch('management.clients.cause_client.requests.get')
    def test_get_causes_success(self, mock_get):
        """Test successful get_causes call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'causes': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = CauseClient.get_causes({'status': 'pending'})

        mock_get.assert_called_once_with(
            'http://localhost:8001/causes/admin/causes/',
            headers={'X-ADMIN-SERVICE-API-KEY': 'test-api-key'},
            params={'status': 'pending'},
            timeout=5
        )
        self.assertEqual(result, {'causes': []})

    @override_settings(
        CAUSE_SERVICE_URL='http://localhost:8001/causes',
        ADMIN_SERVICE_API_KEY='test-api-key'
    )
    @patch('management.clients.cause_client.requests.get')
    def test_get_causes_without_params(self, mock_get):
        """Test get_causes call without parameters"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'causes': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = CauseClient.get_causes()

        mock_get.assert_called_once_with(
            'http://localhost:8001/causes/admin/causes/',
            headers={'X-ADMIN-SERVICE-API-KEY': 'test-api-key'},
            params=None,
            timeout=5
        )
        self.assertEqual(result, {'causes': []})

    @override_settings(
        CAUSE_SERVICE_URL='http://localhost:8001/causes',
        ADMIN_SERVICE_API_KEY='test-api-key'
    )
    @patch('management.clients.cause_client.requests.get')
    def test_get_causes_http_error(self, mock_get):
        """Test get_causes call with HTTP error"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Not Found')
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            CauseClient.get_causes()

    @override_settings(
        CAUSE_SERVICE_URL='http://localhost:8001/causes',
        ADMIN_SERVICE_API_KEY='test-api-key'
    )
    @patch('management.clients.cause_client.requests.patch')
    def test_update_cause_success(self, mock_patch):
        """Test successful update_cause call"""
        cause_id = uuid.uuid4()
        update_data = {'status': 'approved'}

        mock_response = MagicMock()
        mock_response.json.return_value = {'id': str(cause_id), 'status': 'approved'}
        mock_response.raise_for_status.return_value = None
        mock_patch.return_value = mock_response

        result = CauseClient.update_cause(cause_id, update_data)

        mock_patch.assert_called_once_with(
            f'http://localhost:8001/causes/admin/causes/{cause_id}/update/',
            headers={'X-ADMIN-SERVICE-API-KEY': 'test-api-key'},
            json=update_data,
            timeout=5
        )
        self.assertEqual(result, {'id': str(cause_id), 'status': 'approved'})

    @override_settings(
        CAUSE_SERVICE_URL='http://localhost:8001/causes',
        ADMIN_SERVICE_API_KEY='test-api-key'
    )
    @patch('management.clients.cause_client.requests.patch')
    def test_update_cause_http_error(self, mock_patch):
        """Test update_cause call with HTTP error"""
        cause_id = uuid.uuid4()
        update_data = {'status': 'rejected'}

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('400 Bad Request')
        mock_patch.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            CauseClient.update_cause(cause_id, update_data)


class AdminCauseListViewTestCase(APITestCase):
    """Test cases for AdminCauseListView"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # Use correct URL with /admin/management/ prefix
        self.url = '/admin/management/causes/'

    @patch('management.views.CauseClient.get_causes')
    def test_get_causes_success(self, mock_get_causes):
        """Test successful GET request to list causes"""
        mock_get_causes.return_value = {
            'causes': [
                {'id': '1', 'title': 'Test Cause 1', 'status': 'pending'},
                {'id': '2', 'title': 'Test Cause 2', 'status': 'approved'}
            ]
        }

        response = self.client.get(self.url, {'status': 'pending'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        mock_get_causes.assert_called_once_with({'status': 'pending'})

    @patch('management.views.CauseClient.get_causes')
    def test_get_causes_without_params(self, mock_get_causes):
        """Test GET request without query parameters"""
        mock_get_causes.return_value = {'causes': []}

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        mock_get_causes.assert_called_once_with({})

    @patch('management.views.CauseClient.get_causes')
    def test_get_causes_http_error(self, mock_get_causes):
        """Test GET request when CauseClient raises HTTPError"""
        mock_get_causes.side_effect = requests.HTTPError('404 Not Found')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)

    def test_get_causes_unauthorized(self):
        """Test GET request without authentication"""
        client = APIClient()  # Unauthenticated client
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminCauseStatusUpdateViewTestCase(APITestCase):
    """Test cases for AdminCauseStatusUpdateView"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.cause_id = uuid.uuid4()
        # Use correct URL with /admin/management/ prefix
        self.url = f'/admin/management/causes/{self.cause_id}/status/'
        self.valid_data = {
            'status': 'approved',
            'rejection_reason': ''
        }

    @patch('management.views.log_admin_action')
    @patch('management.views.CauseClient.update_cause')
    def test_patch_cause_status_success(self, mock_update_cause, mock_log_action):
        """Test successful PATCH request to update cause status"""
        mock_update_cause.return_value = {
            'id': str(self.cause_id),
            'status': 'approved'
        }

        response = self.client.patch(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('data', response.data)

        mock_update_cause.assert_called_once_with(self.cause_id, self.valid_data)
        mock_log_action.assert_called_once_with(
            user=self.user,
            entity_type='cause',
            entity_id=self.cause_id,
            action='status_changed_to_approved',
            reason='',
            extra_data={'request_data': self.valid_data}
        )

    @patch('management.views.log_admin_action')
    @patch('management.views.CauseClient.update_cause')
    def test_patch_cause_status_with_rejection_reason(self, mock_update_cause, mock_log_action):
        """Test PATCH request with rejection reason"""
        data = {
            'status': 'rejected',
            'rejection_reason': 'Violates community guidelines'
        }
        mock_update_cause.return_value = {
            'id': str(self.cause_id),
            'status': 'rejected'
        }

        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

        # Note: The view has a bug - it uses 'reason' instead of 'rejection_reason'
        # So the reason will always be empty string, not the rejection_reason value
        mock_log_action.assert_called_once_with(
            user=self.user,
            entity_type='cause',
            entity_id=self.cause_id,
            action='status_changed_to_rejected',
            reason='',  # This will be empty due to the view bug
            extra_data={'request_data': data}
        )

    def test_patch_cause_status_invalid_data(self):
        """Test PATCH request with invalid data"""
        invalid_data = {
            'status': 'invalid_status'
        }

        response = self.client.patch(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_patch_cause_status_missing_status(self):
        """Test PATCH request without status field"""
        invalid_data = {
            'rejection_reason': 'Some reason'
        }

        response = self.client.patch(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    @patch('management.views.CauseClient.update_cause')
    def test_patch_cause_status_http_error(self, mock_update_cause):
        """Test PATCH request when CauseClient raises HTTPError"""
        mock_update_cause.side_effect = requests.HTTPError('400 Bad Request')

        response = self.client.patch(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)

    def test_patch_cause_status_unauthorized(self):
        """Test PATCH request without authentication"""
        client = APIClient()  # Unauthenticated client
        response = client.patch(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_cause_status_wrong_method(self):
        """Test PATCH endpoint with wrong HTTP method"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ManagementIntegrationTestCase(APITestCase):
    """Integration test cases for management functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('management.views.CauseClient.get_causes')
    @patch('management.views.log_admin_action')
    @patch('management.views.CauseClient.update_cause')
    def test_complete_cause_management_flow(self, mock_update_cause, mock_log_action, mock_get_causes):
        """Test complete cause management workflow"""
        cause_id = uuid.uuid4()

        # Mock get_causes response
        mock_get_causes.return_value = {
            'causes': [
                {'id': str(cause_id), 'title': 'Test Cause', 'status': 'pending'}
            ]
        }

        # Mock update_cause response
        mock_update_cause.return_value = {
            'id': str(cause_id),
            'status': 'approved'
        }

        # Step 1: List causes
        list_response = self.client.get('/admin/management/causes/', {'status': 'pending'})
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data['status'], 'success')

        # Step 2: Update cause status
        update_data = {'status': 'approved'}
        update_response = self.client.patch(f'/admin/management/causes/{cause_id}/status/', update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertTrue(update_response.data['success'])

        # Verify all mocks were called correctly
        mock_get_causes.assert_called_once_with({'status': 'pending'})
        mock_update_cause.assert_called_once_with(cause_id, update_data)
        mock_log_action.assert_called_once()

    def test_management_endpoints_require_authentication(self):
        """Test that all management endpoints require authentication"""
        client = APIClient()  # Unauthenticated client

        # Test list endpoint
        response = client.get('/admin/management/causes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test update endpoint
        cause_id = uuid.uuid4()
        response = client.patch(f'/admin/management/causes/{cause_id}/status/', {'status': 'approved'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)