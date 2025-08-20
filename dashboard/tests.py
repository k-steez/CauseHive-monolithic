import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CachedReportData
from .serializers import CachedReportDataSerializer


class CachedReportDataModelTestCase(TestCase):
    """Test cases for CachedReportData model"""

    def setUp(self):
        self.report_data = {
            'report_type': 'dashboard_metrics',
            'data': {'total_users': 100, 'total_causes': 50},
            'generated_at': timezone.now()
        }
        self.report = CachedReportData.objects.create(**self.report_data)

    def test_report_creation(self):
        """Test report model creation"""
        self.assertIsInstance(self.report.id, uuid.UUID)
        self.assertEqual(self.report.report_type, self.report_data['report_type'])
        self.assertEqual(self.report.data, self.report_data['data'])
        self.assertEqual(self.report.generated_at, self.report_data['generated_at'])

    def test_report_string_representation(self):
        """Test report string representation"""
        expected = f"{self.report.report_type} report at {self.report.generated_at}"
        self.assertEqual(str(self.report), expected)

    def test_report_unique_constraint(self):
        """Test report unique constraint on report_type and generated_at"""
        # Try to create another report with same type and time
        with self.assertRaises(Exception):  # Should raise IntegrityError
            CachedReportData.objects.create(
                report_type=self.report_data['report_type'],
                data={'different': 'data'},
                generated_at=self.report_data['generated_at']
            )

    def test_report_different_times(self):
        """Test that reports with same type but different times can coexist"""
        new_time = timezone.now() + timedelta(hours=1)
        new_report = CachedReportData.objects.create(
            report_type=self.report_data['report_type'],
            data={'new': 'data'},
            generated_at=new_time
        )
        self.assertNotEqual(self.report.id, new_report.id)

    def test_report_different_types(self):
        """Test that reports with different types can coexist"""
        new_report = CachedReportData.objects.create(
            report_type='user_list',
            data={'users': []},
            generated_at=self.report_data['generated_at']
        )
        self.assertNotEqual(self.report.id, new_report.id)


class CachedReportDataSerializerTestCase(TestCase):
    """Test cases for CachedReportDataSerializer"""

    def setUp(self):
        self.report = CachedReportData.objects.create(
            report_type='dashboard_metrics',
            data={'total_users': 100, 'total_causes': 50},
            generated_at=timezone.now()
        )

    def test_serializer_fields(self):
        """Test serializer includes all fields"""
        serializer = CachedReportDataSerializer(self.report)
        expected_fields = ['id', 'report_type', 'data', 'generated_at']
        for field in expected_fields:
            self.assertIn(field, serializer.data)

    def test_serializer_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'report_type': 'user_list',
            'data': {'users': [{'id': 1, 'name': 'Test'}]},
            'generated_at': timezone.now()
        }
        serializer = CachedReportDataSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_create_report(self):
        """Test serializer creates report correctly"""
        data = {
            'report_type': 'donations_list',
            'data': {'donations': [{'id': 1, 'amount': 100}]},
            'generated_at': timezone.now()
        }
        serializer = CachedReportDataSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        report = serializer.save()

        self.assertIsInstance(report, CachedReportData)
        self.assertEqual(report.report_type, data['report_type'])
        self.assertEqual(report.data, data['data'])


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
)
class DashboardViewsTestCase(APITestCase):
    """Test cases for Dashboard views"""

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

    @patch('dashboard.views.generate_fresh_report')
    def test_dashboard_metrics_with_cached_data(self, mock_generate):
        """Test dashboard metrics with cached data"""
        # Create cached report data
        report = CachedReportData.objects.create(
            report_type='dashboard_metrics',
            data={'total_users': 100, 'total_causes': 50},
            generated_at=timezone.now()
        )

        response = self.client.get('/admin/dashboard/metrics/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_users'], 100)
        self.assertEqual(response.data['total_causes'], 50)
        mock_generate.delay.assert_not_called()

    @patch('dashboard.views.generate_fresh_report')
    def test_dashboard_metrics_without_cached_data(self, mock_generate):
        """Test dashboard metrics without cached data"""
        response = self.client.get('/admin/dashboard/metrics/')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('No report data available', response.data['detail'])
        mock_generate.delay.assert_called_once()

    @patch('dashboard.views.generate_fresh_report')
    def test_dashboard_metrics_with_old_cached_data(self, mock_generate):
        """Test dashboard metrics with old cached data"""
        # Create old cached report data (more than 1 hour ago)
        old_time = timezone.now() - timedelta(hours=2)
        CachedReportData.objects.create(
            report_type='dashboard_metrics',
            data={'total_users': 100, 'total_causes': 50},
            generated_at=old_time
        )

        response = self.client.get('/admin/dashboard/metrics/')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('No report data available', response.data['detail'])
        mock_generate.delay.assert_called_once()

    def test_dashboard_metrics_unauthorized(self):
        """Test dashboard metrics without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/admin/dashboard/metrics/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('dashboard.views.generate_fresh_report')
    def test_admin_users_list_with_cached_data(self, mock_generate):
        """Test admin users list with cached data"""
        report = CachedReportData.objects.create(
            report_type='user_list',
            data={'users': [{'id': 1, 'name': 'Test User'}]},
            generated_at=timezone.now()
        )

        response = self.client.get('/admin/dashboard/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        mock_generate.delay.assert_not_called()

    @patch('dashboard.views.generate_fresh_report')
    def test_admin_donations_list_with_cached_data(self, mock_generate):
        """Test admin donations list with cached data"""
        report = CachedReportData.objects.create(
            report_type='donations_list',
            data={'donations': [{'id': 1, 'amount': 100}]},
            generated_at=timezone.now()
        )

        response = self.client.get('/admin/dashboard/donations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['donations']), 1)
        mock_generate.delay.assert_not_called()

    @patch('dashboard.views.generate_fresh_report')
    def test_admin_causes_list_with_cached_data(self, mock_generate):
        """Test admin causes list with cached data"""
        report = CachedReportData.objects.create(
            report_type='causes_list',
            data={'causes': [{'id': 1, 'name': 'Test Cause'}]},
            generated_at=timezone.now()
        )

        response = self.client.get('/admin/dashboard/causes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['causes']), 1)
        mock_generate.delay.assert_not_called()


class DashboardTasksTestCase(TestCase):
    """Test cases for Dashboard tasks"""
    @patch('dashboard.utils.requests.get')
    def test_generate_fresh_report(self, mock_get):
        """Test generate fresh report task"""
        # Mock the requests.get responses
        mock_responses = [
            # Users response
            MagicMock(
                status_code=200,
                json=lambda: {'users': [{'id': 1, 'email': 'test@example.com'}]}
            ),
            # Donations list response (first call)
            MagicMock(
                status_code=200,
                json=lambda: {'results': [{'id': 1, 'amount': 100}]}
            ),
            # Donations stats response (first call)
            MagicMock(
                status_code=200,
                json=lambda: {'total_amount': 1000, 'count': 10}
            ),
            # Withdrawal requests response
            MagicMock(
                status_code=200,
                json=lambda: [{'id': 1, 'amount': 500}]
            ),
            # Withdrawals stats response
            MagicMock(
                status_code=200,
                json=lambda: {'total_withdrawn': 5000, 'count': 5}
            ),
            # Causes response
            MagicMock(
                status_code=200,
                json=lambda: {'results': [{'id': 1, 'title': 'Test Cause'}], 'count': 1}
            ),
            # Payments response
            MagicMock(
                status_code=200,
                json=lambda: {'results': [{'id': 1, 'amount': 200}], 'count': 1}
            ),
            # Donations list response (second call)
            MagicMock(
                status_code=200,
                json=lambda: {'results': [{'id': 1, 'amount': 100}]}
            ),
            # Donations stats response (second call)
            MagicMock(
                status_code=200,
                json=lambda: {'total_amount': 1000, 'count': 10}
            ),
        ]

        mock_get.side_effect = mock_responses

        # Call the task
        from .tasks import generate_fresh_report
        result = generate_fresh_report()

        # Verify the task completed successfully
        self.assertIsNone(result)  # Task returns None on success

        # Verify that CachedReportData objects were created
        self.assertTrue(CachedReportData.objects.filter(report_type='dashboard_metrics').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='users_list').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='donations_list').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='donations_stats').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='causes_list').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='payments_list').exists())
        self.assertTrue(CachedReportData.objects.filter(report_type='withdrawals_stats').exists())

        # Verify the number of API calls
        self.assertEqual(mock_get.call_count, 9)  # Total number of API calls in the task