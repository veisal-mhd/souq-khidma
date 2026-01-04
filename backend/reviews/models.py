from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Modèle pour les avis et évaluations
    """
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='reviews')
    transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE, related_name='review', null=True, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_donnees')
    prestataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_recues')
    
    note = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    commentaire = models.TextField(max_length=1000, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Modération
    est_approuve = models.BooleanField(default=True)
    est_signale = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'
        ordering = ['-date_creation']
        unique_together = [['client', 'service']]  # Un client ne peut évaluer qu'une fois par service
        indexes = [
            models.Index(fields=['prestataire', 'note']),
            models.Index(fields=['service', 'note']),
        ]
    
    def __str__(self):
        return f"Avis {self.note}/5 - {self.client.username} pour {self.prestataire.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour la note moyenne du prestataire
        self.update_prestataire_rating()
    
    def delete(self, *args, **kwargs):
        prestataire = self.prestataire
        super().delete(*args, **kwargs)
        # Recalculer la note moyenne après suppression
        self.update_prestataire_rating_for_user(prestataire)
    
    def update_prestataire_rating(self):
        """Met à jour la note moyenne et le nombre d'évaluations du prestataire"""
        from django.db.models import Avg, Count
        stats = Review.objects.filter(
            prestataire=self.prestataire,
            est_approuve=True
        ).aggregate(
            moyenne=Avg('note'),
            total=Count('id')
        )
        
        self.prestataire.note_moyenne = stats['moyenne'] or 0
        self.prestataire.nombre_evaluations = stats['total'] or 0
        self.prestataire.save(update_fields=['note_moyenne', 'nombre_evaluations'])
    
    @staticmethod
    def update_prestataire_rating_for_user(prestataire):
        """Met à jour la note moyenne pour un prestataire donné"""
        from django.db.models import Avg, Count
        stats = Review.objects.filter(
            prestataire=prestataire,
            est_approuve=True
        ).aggregate(
            moyenne=Avg('note'),
            total=Count('id')
        )
        
        prestataire.note_moyenne = stats['moyenne'] or 0
        prestataire.nombre_evaluations = stats['total'] or 0
        prestataire.save(update_fields=['note_moyenne', 'nombre_evaluations'])

