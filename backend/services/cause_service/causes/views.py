from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Causes
from .serializers import CausesSerializer


# Create your views here.
class CauseCreateView(generics.CreateAPIView):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer

class CauseListView(generics.ListAPIView):
    serializer_class = CausesSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Causes.objects.exclude(status='under_review')

class CauseDetailView(generics.RetrieveAPIView):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer
    lookup_field = 'id'

class CauseDeleteView(generics.DestroyAPIView):
    queryset = Causes.objects.all()
    serializer_class = CausesSerializer
    lookup_field = 'id'  # Assuming you want to delete by 'id'