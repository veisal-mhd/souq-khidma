from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Categorie(models.Model):
    """
    Catégories de services (Plomberie, Électricité, Nettoyage, etc.)
    """
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Service(models.Model):
    """
    Modèle pour les services proposés par les prestataires
    """
    DISPONIBILITE_CHOICES = [
        ('disponible', 'Disponible'),
        ('indisponible', 'Indisponible'),
        ('en_conges', 'En congés'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='services')
    prestataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE_CHOICES, default='disponible')
    est_actif = models.BooleanField(default=True)
    est_sponsorise = models.BooleanField(default=False)
    
    # Images du service
    image_principale = models.ImageField(upload_to='services/', null=True, blank=True)
    
    # Promotion
    prix_promotion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_debut_promotion = models.DateTimeField(null=True, blank=True)
    date_fin_promotion = models.DateTimeField(null=True, blank=True)
    
    # Localisation
    ville = models.CharField(max_length=100, blank=True)
    quartier = models.CharField(max_length=100, blank=True)
    
    # Statistiques
    nombre_vues = models.IntegerField(default=0)
    nombre_commandes = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['categorie', 'disponibilite']),
            models.Index(fields=['prestataire', 'est_actif']),
            models.Index(fields=['ville', 'quartier']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.prestataire.username}"
    
    @property
    def prix_actuel(self):
        """Retourne le prix actuel (promotion si applicable)"""
        if self.prix_promotion and self.est_en_promotion:
            return self.prix_promotion
        return self.prix
    
    @property
    def est_en_promotion(self):
        """Vérifie si le service est actuellement en promotion"""
        from django.utils import timezone
        if not self.prix_promotion:
            return False
        now = timezone.now()
        if self.date_debut_promotion and now < self.date_debut_promotion:
            return False
        if self.date_fin_promotion and now > self.date_fin_promotion:
            return False
        return True


class Forfait(models.Model):
    """
    Forfaits de services (ex: 5 heures de ménage)
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='forfaits')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duree = models.IntegerField(help_text="Durée en heures", null=True, blank=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'forfaits'
        verbose_name = 'Forfait'
        verbose_name_plural = 'Forfaits'
    
    def __str__(self):
        return f"{self.nom} - {self.service.titre}"

