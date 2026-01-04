from django.contrib import admin
from .models import Categorie, Service, Forfait


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prestataire', 'categorie', 'prix', 'disponibilite', 'est_actif', 'date_creation')
    list_filter = ('categorie', 'disponibilite', 'est_actif', 'est_sponsorise', 'date_creation')
    search_fields = ('titre', 'description', 'prestataire__username')
    readonly_fields = ('date_creation', 'date_modification', 'nombre_vues', 'nombre_commandes')


@admin.register(Forfait)
class ForfaitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'service', 'prix', 'duree', 'est_actif')
    list_filter = ('est_actif',)
    search_fields = ('nom', 'service__titre')

