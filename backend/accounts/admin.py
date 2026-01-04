from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'telephone', 'role', 'statut_verifie', 'is_premium', 'date_inscription')
    list_filter = ('role', 'statut_verifie', 'is_premium', 'is_active', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'telephone', 'profil_photo', 'bio', 'localisation', 
                      'statut_verifie', 'is_premium', 'date_premium', 'competences',
                      'note_moyenne', 'nombre_evaluations')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'telephone', 'email')
        }),
    )

