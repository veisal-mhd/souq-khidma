from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'telephone', 'password', 'password2', 
                 'role', 'first_name', 'last_name', 'localisation')
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'telephone', 'role', 'first_name', 
                 'last_name', 'profil_photo', 'bio', 'localisation', 'statut_verifie',
                 'is_premium', 'competences', 'note_moyenne', 'nombre_evaluations',
                 'date_inscription')
        read_only_fields = ('id', 'date_inscription', 'note_moyenne', 'nombre_evaluations')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'telephone', 'first_name', 'last_name',
                 'profil_photo', 'bio', 'localisation', 'competences', 'statut_verifie',
                 'is_premium', 'note_moyenne', 'nombre_evaluations')
        read_only_fields = ('id', 'statut_verifie', 'note_moyenne', 'nombre_evaluations')

