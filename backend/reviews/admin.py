from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'prestataire', 'service', 'note', 'est_approuve', 'date_creation')
    list_filter = ('note', 'est_approuve', 'est_signale', 'date_creation')
    search_fields = ('client__username', 'prestataire__username', 'commentaire')
    readonly_fields = ('date_creation', 'date_modification')

