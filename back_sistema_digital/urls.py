from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="Back Sistema Escolar API",
        default_version='v1',
        description="Documentação da API para o projeto Back Sistema Escolar Digital",
        terms_of_service="www.prodosdigital.com.br",
        contact=openapi.Contact(email="agencia.prodosdigital@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('back_sistema_digital.users.urls')),
    
    # Endpoints para autenticação JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Endpoints para a documentação Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
