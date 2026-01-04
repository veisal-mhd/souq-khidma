"""
Commande Django pour initialiser les catégories de services
Usage: python manage.py init_categories
"""
from django.core.management.base import BaseCommand
from services.models import Categorie


class Command(BaseCommand):
    help = 'Initialise les catégories de services de base'

    def handle(self, *args, **options):
        categories = [
            {'nom': 'Plomberie', 'description': 'Services de plomberie et réparation', 'icone': '🔧'},
            {'nom': 'Électricité', 'description': 'Services électriques et installations', 'icone': '⚡'},
            {'nom': 'Nettoyage', 'description': 'Services de nettoyage et ménage', 'icone': '🧹'},
            {'nom': 'Jardinage', 'description': 'Services de jardinage et paysagisme', 'icone': '🌳'},
            {'nom': 'Peinture', 'description': 'Services de peinture et rénovation', 'icone': '🎨'},
            {'nom': 'Menuiserie', 'description': 'Services de menuiserie et ébénisterie', 'icone': '🪵'},
            {'nom': 'Mécanique', 'description': 'Services de mécanique automobile', 'icone': '🔩'},
            {'nom': 'Informatique', 'description': 'Services informatiques et support technique', 'icone': '💻'},
            {'nom': 'Cuisine', 'description': 'Services de cuisine et restauration', 'icone': '👨‍🍳'},
            {'nom': 'Transport', 'description': 'Services de transport et livraison', 'icone': '🚗'},
            {'nom': 'Coiffure', 'description': 'Services de coiffure et beauté', 'icone': '✂️'},
            {'nom': 'Cours', 'description': 'Services de cours et formation', 'icone': '📚'},
        ]

        created_count = 0
        for cat_data in categories:
            categorie, created = Categorie.objects.get_or_create(
                nom=cat_data['nom'],
                defaults={
                    'description': cat_data['description'],
                    'icone': cat_data['icone']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Catégorie créée: {categorie.nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Catégorie existante: {categorie.nom}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n{created_count} catégorie(s) créée(s) avec succès!')
        )

