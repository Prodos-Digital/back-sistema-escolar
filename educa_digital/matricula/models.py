# matricula/models.py
from django.db import models
from educa_digital.escolas.models import SchoolUnit


class StudentProfile(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=50)
    orgao_emissor = models.CharField(max_length=100)
    estado_emissao = models.CharField(max_length=2)
    cartao_sus = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    data_nascimento = models.DateField()
    telefone_whatsapp = models.CharField(max_length=20)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    pcd = models.BooleanField(default=False)
    bolsa_familia = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class ResponsibleProfile(models.Model):
    VINCULO_CHOICES = [
        ('pai', 'Pai'),
        ('mae', 'Mãe'),
        ('tutor', 'Tutor'),
        ('responsavel_legal', 'Responsável Legal'),
        ('avo', 'Avô/Avó'),
        ('outro', 'Outro'),
    ]
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    data_nascimento = models.DateField()
    telefone_whatsapp = models.CharField(max_length=20)
    vinculo = models.CharField(max_length=50, choices=VINCULO_CHOICES)
    genero = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Address(models.Model):
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    ponto_referencia = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.cep} - {self.cidade}"



class Enrollment(models.Model):
    SITUACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
    ]
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    responsible = models.ForeignKey(ResponsibleProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    school_unit = models.ForeignKey(SchoolUnit, on_delete=models.SET_NULL, null=True, blank=True)
    etapa = models.IntegerField(default=1)  # Série: 1, 2, 3, etc.
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='pendente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Matricula: {self.student.nome} - Etapa {self.etapa}"


class EnrollmentDocuments(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    cartao_sus = models.FileField(upload_to='documents/', blank=True, null=True)
    laudo_pcd = models.FileField(upload_to='documents/', blank=True, null=True)
    comprovante_residencia = models.FileField(upload_to='documents/')
    historico_escolar = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"Documentos de {self.enrollment.student.nome}"
