# matricula/admin.py
from django.contrib import admin
from .models import (
    StudentProfile, 
    ResponsibleProfile, 
    Address, 
    SchoolUnit, 
    Enrollment, 
    EnrollmentDocuments
)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email')
    search_fields = ('cpf', 'nome')


class ResponsibleProfileAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email')
    search_fields = ('cpf', 'nome')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('cep', 'cidade', 'estado')


class SchoolUnitAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')


class EnrollmentDocumentsInline(admin.StackedInline):
    model = EnrollmentDocuments
    extra = 0


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'etapa', 'situacao', 'created_at')
    list_filter = ('situacao', 'etapa')
    search_fields = ('student__cpf', 'student__nome')
    inlines = [EnrollmentDocumentsInline]

# Registra os modelos no admin
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(ResponsibleProfile, ResponsibleProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(SchoolUnit, SchoolUnitAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
