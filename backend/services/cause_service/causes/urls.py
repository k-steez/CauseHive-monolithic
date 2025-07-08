from django.urls import path
from .views import CauseCreateView, CauseDeleteView, CauseListView, CauseDetailView

urlpatterns = [
    path('create/', CauseCreateView.as_view(), name='event_create'),
    path('list/', CauseListView.as_view(), name='event_list'),
    path('delete/<uuid:id>/', CauseDeleteView.as_view(), name='event_delete'),
    path('details/<uuid:id>/', CauseDetailView.as_view(), name='cause_detail'),
]

