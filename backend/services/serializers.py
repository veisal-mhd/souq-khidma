from rest_framework import serializers
from .models import Categorie, Service, Forfait
from accounts.serializers import UserSerializer


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'nom', 'description', 'icone')


class ForfaitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forfait
        fields = ('id', 'nom', 'description', 'prix', 'duree', 'est_actif')


class ServiceSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        source='categorie',
        write_only=True,
        required=False
    )
    prestataire = UserSerializer(read_only=True)
    prix_actuel = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    est_en_promotion = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Service
        fields = (
            'id', 'titre', 'description', 'prix', 'prix_actuel', 'prix_promotion',
            'categorie', 'categorie_id', 'prestataire', 'date_creation',
            'date_modification', 'disponibilite', 'est_actif', 'est_sponsorise',
            'image_principale', 'date_debut_promotion', 'date_fin_promotion',
            'ville', 'quartier', 'nombre_vues', 'nombre_commandes', 'est_en_promotion'
        )
        read_only_fields = ('date_creation', 'date_modification', 'nombre_vues', 'nombre_commandes')


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'titre', 'description', 'prix', 'prix_promotion', 'categorie',
            'disponibilite', 'image_principale', 'date_debut_promotion',
            'date_fin_promotion', 'ville', 'quartier'
        )
    
    def create(self, validated_data):
        validated_data['prestataire'] = self.context['request'].user
        return super().create(validated_data)

