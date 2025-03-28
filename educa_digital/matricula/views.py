# matricula/views.py
import secrets
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Enrollment, EnrollmentDocuments
from .serializers import EnrollmentSerializer, EnrollmentDocumentsSerializer
from django.contrib.auth import get_user_model



def generate_random_password():
    """
    Gera uma senha aleatória segura com 8 caracteres.
    """
    return secrets.token_urlsafe(8)

def send_whatsapp_message(phone_number, message):
    """
    Função fictícia para envio de mensagem via WhatsApp.
    Aqui você integraria com o seu provedor (ex.: Twilio, Zenvia, etc.).
    Por enquanto, apenas logamos a mensagem.
    """
    # Exemplo de integração: use uma API externa para enviar a mensagem.
    print(f"Enviando WhatsApp para {phone_number}: {message}")


class EnrollmentCreateView(generics.CreateAPIView):
    """
    Endpoint para criar uma nova matrícula (enrollment).
    
    Se o CPF do aluno já existir, os dados serão atualizados.
    
    Após criar a matrícula, o sistema:
    - Cria um usuário para o perfil do responsável e do aluno (inativos inicialmente);
    - Gera uma senha aleatória para cada um;
    - Envia mensagens via WhatsApp com as informações de acesso.
    
    Os usuários criados deverão redefinir a senha no primeiro acesso.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        request_body=EnrollmentSerializer,
        responses={201: EnrollmentSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()  # Cria a matrícula

        User = get_user_model()

        # --- Criação do usuário para o responsável ---
        responsible_email = enrollment.responsible.email
        responsible_phone = enrollment.responsible.telefone_whatsapp
        if not User.objects.filter(email=responsible_email).exists():
            random_password_resp = generate_random_password()
            responsible_user = User.objects.create_user(
                username=responsible_email,
                email=responsible_email,
                password=random_password_resp,
                is_active=False  # Cria inativo para forçar redefinição de senha
            )
            school_name = enrollment.school_unit.nome if enrollment.school_unit else "a escola"
            message_resp = (
                f"Olá, {enrollment.responsible.nome}, seu cadastro foi concluído com sucesso, enviamos as informações para a administração da {school_name}. "
                f"Acompanhe o processo no sistema www.educadigital.com.br. O seu acesso é, email: {responsible_email} senha: {random_password_resp}, "
                "ao acessar o sistema, você será solicitado a redefinir sua senha. Qualquer dúvida, entre em contato com o suporte!"
            )
            send_whatsapp_message(responsible_phone, message_resp)

        # --- Criação do usuário para o aluno ---
        student_email = enrollment.student.email
        student_phone = enrollment.student.telefone_whatsapp
        if not User.objects.filter(email=student_email).exists():
            random_password_student = generate_random_password()
            student_user = User.objects.create_user(
                username=student_email,
                email=student_email,
                password=random_password_student,
                is_active=False
            )
            school_name = enrollment.school_unit.nome if enrollment.school_unit else "a escola"
            message_student = (
                f"Olá, {enrollment.student.nome}, seu cadastro foi concluído pelo seu responsável {enrollment.responsible.nome}. "
                f"Enviamos as informações para a administração da {school_name}. Acompanhe o processo no sistema www.educadigital.com.br. "
                f"O seu acesso é, email: {student_email} senha: {random_password_student}, ao acessar o sistema, você será solicitado a redefinir sua senha. "
                "Qualquer dúvida, entre em contato com o suporte!"
            )
            send_whatsapp_message(student_phone, message_student)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para recuperar, atualizar ou deletar uma matrícula.
    Identifica a matrícula pelo ID.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema(
        responses={200: EnrollmentSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EnrollmentSerializer,
        responses={200: EnrollmentSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EnrollmentDocumentsView(generics.CreateAPIView):
    """
    Endpoint para enviar os documentos da matrícula.
    
    Os arquivos enviados serão encaminhados para o S3 (configurado via django-storages e boto3).
    
    **Credenciais S3 necessárias (no arquivo .env e settings):**
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_STORAGE_BUCKET_NAME
    - AWS_S3_REGION_NAME
    """
    queryset = EnrollmentDocuments.objects.all()
    serializer_class = EnrollmentDocumentsSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('enrollment', openapi.IN_FORM, description="ID da matrícula", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cartao_sus': openapi.Schema(type=openapi.TYPE_FILE, description="Arquivo do Cartão SUS (opcional)"),
                'laudo_pcd': openapi.Schema(type=openapi.TYPE_FILE, description="Arquivo do Laudo PCD (opcional)"),
                'comprovante_residencia': openapi.Schema(type=openapi.TYPE_FILE, description="Arquivo do Comprovante de Residência"),
                'historico_escolar': openapi.Schema(type=openapi.TYPE_FILE, description="Arquivo do Histórico Escolar"),
            }
        ),
        responses={201: EnrollmentDocumentsSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
