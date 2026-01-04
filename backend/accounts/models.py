from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec support pour clients et prestataires
    """
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('prestataire', 'Prestataire'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    telephone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format de téléphone invalide")],
        unique=True,
        null=True,
        blank=True
    )
    profil_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    localisation = models.CharField(max_length=200, blank=True)
    statut_verifie = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    date_premium = models.DateTimeField(null=True, blank=True)
    
    # Champs pour prestataires
    competences = models.JSONField(default=list, blank=True)
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    nombre_evaluations = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_prestataire(self):
        return self.role == 'prestataire'
    
    @property
    def is_client(self):
        return self.role == 'client'

