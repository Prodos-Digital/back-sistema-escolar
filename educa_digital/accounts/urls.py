# profile/urls.py
from django.urls import path
from .views import UserProfileDetailView

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='profile-detail'),
]
