from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    PermissionSerializer
)


class UserCreateView(generics.CreateAPIView):
    """
    Cria um novo usuário (is_active=False por padrão).

    Exemplo de requisição POST:
    {
      "username": "jose",
      "email": "jose@example.com",
      "first_name": "José",
      "last_name": "Silva",
      "password": "senha123"
    }

    Resposta (201 Created):
    {
      "id": 1,
      "username": "jose",
      "email": "jose@example.com",
      "first_name": "José",
      "last_name": "Silva",
      "is_active": false,
      "is_staff": false,
      "permissions": []
    }
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Visualiza, atualiza ou deleta um usuário específico.
    Também possui endpoints para adicionar/remover permissões.

    - GET /users/<id>/
      Exemplo de resposta:
      {
        "username": "jose",
        "email": "jose@example.com",
        "first_name": "José",
        "last_name": "Silva",
        "is_active": false,
        "is_staff": false,
        "permissions": []
      }

    - PUT/PATCH /users/<id>/
      Exemplo de requisição:
      {
        "username": "jose",
        "email": "jose@example.com",
        "first_name": "José",
        "last_name": "Silva",
        "is_active": true,
        "is_staff": false,
        "password": "nova_senha"
      }

    - DELETE /users/<id>/
      Retorna 204 No Content se bem sucedido.

    - POST /users/<id>/add-permission/
      {
        "permission_id": 10
      }

    - POST /users/<id>/remove-permission/
      {
        "permission_id": 10
      }
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='add-permission')
    def add_permission(self, request, pk=None):
        """
        Adiciona uma permissão ao usuário.

        Exemplo de requisição POST:
        {
          "permission_id": 10
        }
        """
        user = self.get_object()
        permission_id = request.data.get('permission_id')
        try:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.add(permission)
            return Response({'detail': 'Permissão adicionada com sucesso.'})
        except Permission.DoesNotExist:
            return Response({'detail': 'Permissão não encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='remove-permission')
    def remove_permission(self, request, pk=None):
        """
        Remove uma permissão do usuário.

        Exemplo de requisição POST:
        {
          "permission_id": 10
        }
        """
        user = self.get_object()
        permission_id = request.data.get('permission_id')
        try:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.remove(permission)
            return Response({'detail': 'Permissão removida com sucesso.'})
        except Permission.DoesNotExist:
            return Response({'detail': 'Permissão não encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)


class CustomLoginView(APIView):
    """
    Realiza login via JWT. Retorna tokens e dados completos do usuário (incluindo permissões).

    Exemplo de requisição POST:
    {
      "username": "jose",
      "password": "senha123"
    }

    Possíveis respostas:
    - 200 OK (usuário ativo):
      {
        "refresh": "<token_refresh>",
        "access": "<token_access>",
        "user": {
          "id": 1,
          "username": "jose",
          "email": "jose@example.com",
          "first_name": "José",
          "last_name": "Silva",
          "is_active": true,
          "is_staff": false,
          "permissions": ["add_user", "change_user", ...]
        }
      }
    - 401 Unauthorized (credenciais inválidas)
    - 403 Forbidden (usuário inativo)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if not user.is_active:
            return Response({'detail': 'Usuário inativo. Aguardando ativação.'},
                            status=status.HTTP_403_FORBIDDEN)
            
        if user is None:
            return Response({'detail': 'Credenciais inválidas.'},
                            status=status.HTTP_401_UNAUTHORIZED)


        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Serializa todos os dados do usuário (incluindo permissões)
        user_data = UserSerializer(user).data

        return Response({
            'refresh': str(refresh),
            'access': access_token,
            'user': user_data
        }, status=status.HTTP_200_OK)


class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, criar, editar e deletar permissões.

    Exemplos:
    - GET /users/permissions/
      [
        {
          "id": 1,
          "name": "Can add user",
          "codename": "add_user",
          "content_type": 1
        },
        ...
      ]

    - POST /users/permissions/
      {
        "name": "Pode ver relatórios",
        "codename": "can_view_reports",
        "content_type": 1
      }

    - PUT/PATCH /users/permissions/<id>/
    - DELETE /users/permissions/<id>/
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
