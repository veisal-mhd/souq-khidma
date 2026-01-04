from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):
    """
    Modèle pour les transactions de paiement
    """
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('en_escrow', 'En escrow'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('rembourse', 'Remboursé'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('bankily', 'Bankily'),
        ('moov_money', 'Moov Money'),
        ('bamis', 'BAMIS'),
        ('bmci', 'BMCI'),
        ('carte', 'Carte bancaire'),
    ]
    
    service = models.ForeignKey('services.Service', on_delete=models.PROTECT, related_name='transactions')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='commandes')
    prestataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ventes'
    )
    
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    montant_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_prestataire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    
    # Informations de paiement
    reference_paiement = models.CharField(max_length=200, blank=True)
    transaction_id_externe = models.CharField(max_length=200, blank=True)
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes_client = models.TextField(blank=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['client', 'statut']),
            models.Index(fields=['prestataire', 'statut']),
            models.Index(fields=['service', 'statut']),
        ]
    
    def __str__(self):
        return f"Transaction #{self.id} - {self.client.username} -> {self.prestataire.username}"
    
    def calculer_commission(self, taux_commission=None):
        """Calcule la commission et le montant pour le prestataire"""
        from django.conf import settings
        if taux_commission is None:
            taux_commission = getattr(settings, 'PAYMENT_COMMISSION_RATE', 0.05)
        
        self.montant_commission = self.montant_total * Decimal(str(taux_commission))
        self.montant_prestataire = self.montant_total - self.montant_commission
        return self.montant_commission, self.montant_prestataire
    
    def save(self, *args, **kwargs):
        # Calculer la commission si c'est une nouvelle transaction ou si le montant change
        update_fields = kwargs.get('update_fields', None)
        if not self.pk or (update_fields and 'montant_total' in update_fields):
            self.calculer_commission()
        elif not update_fields:
            # Si update_fields n'est pas spécifié, toujours recalculer
            self.calculer_commission()
        super().save(*args, **kwargs)


class AbonnementPremium(models.Model):
    """
    Abonnements premium pour prestataires
    """
    prestataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='abonnements')
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    est_actif = models.BooleanField(default=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'abonnements_premium'
        verbose_name = 'Abonnement Premium'
        verbose_name_plural = 'Abonnements Premium'
    
    def __str__(self):
        return f"Premium - {self.prestataire.username} ({self.date_debut} - {self.date_fin})"

