from django.contrib import admin
from .models import Transaction, AbonnementPremium


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'prestataire', 'service', 'montant_total', 
                   'montant_commission', 'statut', 'mode_paiement', 'date_creation')
    list_filter = ('statut', 'mode_paiement', 'date_creation')
    search_fields = ('client__username', 'prestataire__username', 'reference_paiement', 'transaction_id_externe')
    readonly_fields = ('date_creation', 'date_paiement', 'date_confirmation')


@admin.register(AbonnementPremium)
class AbonnementPremiumAdmin(admin.ModelAdmin):
    list_display = ('prestataire', 'date_debut', 'date_fin', 'montant_paye', 'est_actif')
    list_filter = ('est_actif', 'date_debut', 'date_fin')
    search_fields = ('prestataire__username',)

