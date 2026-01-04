from rest_framework import serializers
from .models import Transaction, AbonnementPremium
from services.serializers import ServiceSerializer
from accounts.serializers import UserSerializer
from services.models import Service

class TransactionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True,
        required=False
    )
    client = UserSerializer(read_only=True)
    prestataire = UserSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'service', 'service_id', 'client', 'prestataire',
            'montant_total', 'montant_commission', 'montant_prestataire',
            'statut', 'mode_paiement', 'reference_paiement', 'transaction_id_externe',
            'date_creation', 'date_paiement', 'date_confirmation', 'notes_client'
        )
        read_only_fields = (
            'id', 'date_creation', 'date_paiement', 'date_confirmation',
            'montant_commission', 'montant_prestataire'
        )

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('service', 'montant_total', 'mode_paiement', 'notes_client')
    
    def create(self, validated_data):
        service = validated_data['service']
        validated_data['client'] = self.context['request'].user
        validated_data['prestataire'] = service.prestataire
        validated_data['statut'] = 'en_attente'
        
        transaction = super().create(validated_data)
        transaction.calculer_commission()
        transaction.save()
        
        return transaction

class AbonnementPremiumSerializer(serializers.ModelSerializer):
    prestataire = UserSerializer(read_only=True)
    
    class Meta:
        model = AbonnementPremium
        fields = ('id', 'prestataire', 'date_debut', 'date_fin', 'montant_paye', 'est_actif')
        read_only_fields = ('id', 'date_debut', 'est_actif')