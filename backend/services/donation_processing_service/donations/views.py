from django.db.models import Sum, Count
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_201_CREATED

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user_id = getattr(request, 'user_id', None)
        data['user_id'] = user_id # Caters for anonymous donations

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if user and hasattr(user, 'id') and user.is_authenticated:
            return Donation.objects.filter(user_id=user.id)
        # Anonymous users have no history
        return Donation.objects.none()

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_donations = queryset.count()
        total_amount = queryset.aggregate(Sum('amount'))['total_amount'] or 0
        return Response({
            'total_amount': total_amount,
            'total_donations': total_donations,
        })