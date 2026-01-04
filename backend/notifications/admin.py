from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_notification', 'titre', 'est_lue', 'date_creation')
    list_filter = ('type_notification', 'est_lue', 'date_creation')
    search_fields = ('titre', 'message', 'utilisateur__username')
    readonly_fields = ('date_creation', 'date_lecture')

