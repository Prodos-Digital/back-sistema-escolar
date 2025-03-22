from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserCreateView,
    UserDetailView,
    CustomLoginView,
    PermissionViewSet
)

router = DefaultRouter()
router.register(r'permissions', PermissionViewSet, basename='permissions')

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # Rotas para o ViewSet de permissões
    path('', include(router.urls)),
]
