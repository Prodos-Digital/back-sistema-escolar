from django.contrib.auth.models import User, Permission
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir detalhes do usuário,
    incluindo lista de permissões personalizadas.
    """
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'permissions'
        ]

    def get_permissions(self, obj):
        """
        Retorna a lista de 'codename' das permissões associadas ao usuário.
        """
        return [perm.codename for perm in obj.user_permissions.all()]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar novos usuários (por padrão, is_active=False).

    Exemplo de requisição POST (criação de usuário):
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
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False  # por padrão, desativado
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualizar dados do usuário, incluindo
    is_active (ativar/desativar) e is_staff (opcional).

    Exemplo de requisição PUT/PATCH:
    {
      "username": "jose",
      "email": "jose@example.com",
      "first_name": "José",
      "last_name": "Silva",
      "is_active": true,
      "is_staff": false,
      "password": "nova_senha"
    }

    Resposta (200 OK):
    {
      "username": "jose",
      "email": "jose@example.com",
      "first_name": "José",
      "last_name": "Silva",
      "is_active": true,
      "is_staff": false
      ...
    }
    """
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'password'
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar permissões.

    Exemplo de requisição POST (criar permissão):
    {
      "name": "Pode ver relatórios",
      "codename": "can_view_reports",
      "content_type": 1
    }

    Exemplo de resposta GET (listar permissões):
    [
      {
        "id": 1,
        "name": "Pode ver relatórios",
        "codename": "can_view_reports",
        "content_type": 1
      },
      ...
    ]
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
