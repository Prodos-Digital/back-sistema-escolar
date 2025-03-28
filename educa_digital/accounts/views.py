# profile/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para recuperar ou atualizar o perfil do usuário autenticado.
    
    O perfil deverá ser criado ou atualizado explicitamente via esse endpoint.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Busca o perfil associado ao usuário autenticado.
        # Caso não exista, pode optar por criar automaticamente ou retornar erro.
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
