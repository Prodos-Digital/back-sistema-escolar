from django.contrib import admin
from .models import SchoolUnit

try:
    admin.site.unregister(SchoolUnit)
except admin.sites.NotRegistered:
    pass

class SchoolUnitAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'ativo')
    search_fields = ('nome', 'cnpj')

admin.site.register(SchoolUnit, SchoolUnitAdmin)
