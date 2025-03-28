
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario')
    search_fields = ('user__email', 'user__username')

admin.site.register(UserProfile, UserProfileAdmin)
