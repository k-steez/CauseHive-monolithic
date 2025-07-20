from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import Donation
from .serializers import DonationSerializer

class DonationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    # Allow any user to view donations
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned donations to a given user,
        by filtering against a `user_id` query parameter in the URL.
        e.g., /api/donations/?user_id=some-uuid
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_donations = queryset.count()
        total_amount = queryset.aggregate(Sum('amount'))['total_amount'] or 0
        return Response({
            'total_amount': total_amount,
            'total_donations': total_donations,
        })