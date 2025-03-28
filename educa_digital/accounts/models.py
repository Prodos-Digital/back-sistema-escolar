# profile/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

USER_TYPE_CHOICES = [
    ('aluno', 'Aluno'),
    ('responsavel', 'Responsável'),
    ('professor', 'Professor'),
    ('admin', 'Administrador'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    # Adicione outros campos específicos do perfil conforme necessário, por exemplo:
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    # ...

    def __str__(self):
        return f"{self.user.email} - {self.tipo_usuario}"
