# Guide de Démarrage Rapide - Souq-Khidma

## Installation rapide

### 1. Backend Django

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env à partir de .env.example
# (Copier et configurer avec vos paramètres)

# Créer la base de données PostgreSQL
createdb souq_khidma

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

Le backend sera accessible sur `http://localhost:8000`

### 2. Frontend React

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Créer le fichier .env à partir de .env.example
# Configurer REACT_APP_API_URL=http://localhost:8000/api

# Lancer le serveur de développement
npm start
```

Le frontend sera accessible sur `http://localhost:3000`

## Premiers pas

1. **Créer un compte** : Allez sur `/register` et créez un compte (client ou prestataire)

2. **Se connecter** : Utilisez `/login` pour vous connecter

3. **Explorer les services** : Allez sur `/services` pour voir les services disponibles

4. **Pour les prestataires** :
   - Créez des services via l'API ou l'interface admin
   - Gérez vos services depuis le tableau de bord

5. **Pour les clients** :
   - Parcourez les services
   - Commandez un service
   - Effectuez le paiement

## Configuration de la base de données

Assurez-vous que PostgreSQL est installé et en cours d'exécution :

```bash
# Créer la base de données
createdb souq_khidma

# Ou via psql
psql -U postgres
CREATE DATABASE souq_khidma;
```

## Configuration des paiements

Les intégrations de paiement nécessitent des clés API réelles. Pour le développement, les services retournent des réponses simulées.

Pour la production :
1. Obtenez les clés API auprès de chaque prestataire (Bankily, Moov Money, etc.)
2. Configurez-les dans le fichier `.env` du backend
3. Implémentez les vraies intégrations dans `backend/payments/services.py`

## Accès à l'administration Django

1. Créez un superutilisateur : `python manage.py createsuperuser`
2. Accédez à : `http://localhost:8000/admin`
3. Connectez-vous avec les identifiants du superutilisateur

## Structure des URLs API

- Authentification : `/api/auth/`
- Services : `/api/services/`
- Transactions : `/api/transactions/`
- Paiements : `/api/payments/`
- Avis : `/api/reviews/`
- Messagerie : `/api/messaging/`
- Notifications : `/api/notifications/`

## Dépannage

### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est en cours d'exécution
- Vérifiez les paramètres dans `.env` (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

### Erreur CORS
- Vérifiez que `CORS_ALLOWED_ORIGINS` dans `settings.py` inclut l'URL du frontend

### Erreur de migration
- Supprimez les migrations (sauf `__init__.py`) et recréez-les :
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## Prochaines étapes

1. Configurer les vraies intégrations de paiement
2. Ajouter des catégories de services via l'admin
3. Personnaliser le design avec TailwindCSS
4. Ajouter des fonctionnalités supplémentaires selon vos besoins

