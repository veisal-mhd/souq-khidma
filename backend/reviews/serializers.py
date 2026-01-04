from rest_framework import serializers
from .models import Review
from services.serializers import ServiceSerializer
from accounts.serializers import UserSerializer
# AJOUT : Import du modèle Service pour le queryset
from services.models import Service

class ReviewSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        # CORRECTION : Remplacer None par Service.objects.all()
        queryset=Service.objects.all(),
        source='service',
        write_only=True,
        required=False
    )
    client = UserSerializer(read_only=True)
    prestataire = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'service', 'service_id', 'transaction', 'client', 'prestataire',
            'note', 'commentaire', 'date_creation', 'date_modification',
            'est_approuve', 'est_signale'
        )
        read_only_fields = ('id', 'date_creation', 'date_modification', 'est_approuve', 'est_signale')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On peut garder ceci pour filtrer dynamiquement si nécessaire
        if self.context.get('request'):
            self.fields['service_id'].queryset = Service.objects.all()
    
    def validate(self, attrs):
        # Vérifier qu'un client ne peut évaluer qu'une fois par service
        if self.instance is None:  # Nouvelle création
            service = attrs.get('service')
            # Protection au cas où service_id n'est pas fourni
            if service:
                client = self.context['request'].user
                if Review.objects.filter(client=client, service=service).exists():
                    raise serializers.ValidationError(
                        "Vous avez déjà évalué ce service."
                    )
        return attrs


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('service', 'note', 'commentaire', 'transaction')
    
    def create(self, validated_data):
        service = validated_data['service']
        validated_data['client'] = self.context['request'].user
        validated_data['prestataire'] = service.prestataire
        return super().create(validated_data)