from django.urls import path
from .views import ImageHashListCreateView, ImageHashDetailView

urlpatterns = [
    path('image-hashes/', ImageHashListCreateView.as_view(), name='image-hash-list'),
    path('image-hashes/<int:pk>/', ImageHashDetailView.as_view(), name='image-hash-detail'),
]
