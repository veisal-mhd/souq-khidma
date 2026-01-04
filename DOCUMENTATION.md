# Documentation Technique - Souq-Khidma

## Architecture

### Backend (Django)
- **Framework**: Django 4.2.7 + Django REST Framework
- **Authentification**: JWT (Simple JWT)
- **Base de données**: PostgreSQL
- **Cache**: Redis
- **Tâches asynchrones**: Celery

### Frontend (React)
- **Framework**: React 18.2.0
- **Styling**: TailwindCSS 3.3.6
- **Routing**: React Router DOM 6.20.0
- **HTTP Client**: Axios
- **State Management**: React Query

## Installation

### Prérequis
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis (optionnel pour le cache)

### Backend

1. Créer un environnement virtuel :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la base de données :
```bash
# Créer la base de données PostgreSQL
createdb souq_khidma

# Copier le fichier .env.example vers .env et le configurer
cp .env.example .env
# Éditer .env avec vos paramètres

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsupesruser
```

4. Lancer le serveur :
```bash
python manage.py runserver
```

### Frontend

1. Installer les dépendances :
```bash
cd frontend
npm install
```

2. Configurer l'URL de l'API :
```bash
cp .env.example .env
# Éditer .env avec l'URL de l'API backend
```

3. Lancer le serveur de développement :
```bash
npm start
```

## Structure de la base de données

### Tables principales

- **users**: Utilisateurs (clients et prestataires)
- **services**: Services proposés
- **categories**: Catégories de services
- **transactions**: Transactions de paiement
- **reviews**: Avis et évaluations
- **conversations**: Conversations entre utilisateurs
- **messages**: Messages dans les conversations
- **notifications**: Notifications utilisateur
- **abonnements_premium**: Abonnements premium

## API Endpoints

### Authentification
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/token/refresh/` - Rafraîchir le token
- `GET /api/auth/profile/` - Profil utilisateur
- `PATCH /api/auth/profile/` - Mettre à jour le profil

### Services
- `GET /api/services/` - Liste des services (avec filtres)
- `GET /api/services/{id}/` - Détails d'un service
- `POST /api/services/` - Créer un service (prestataire)
- `PATCH /api/services/{id}/` - Modifier un service
- `GET /api/services/categories/` - Liste des catégories
- `GET /api/services/mes_services/` - Mes services (prestataire)

### Transactions
- `GET /api/transactions/` - Liste des transactions
- `POST /api/transactions/` - Créer une transaction
- `GET /api/transactions/mes_commandes/` - Mes commandes (client)
- `GET /api/transactions/mes_ventes/` - Mes ventes (prestataire)
- `POST /api/transactions/{id}/confirmer_paiement/` - Confirmer le paiement
- `POST /api/transactions/{id}/confirmer_service/` - Confirmer le service

### Paiements
- `POST /api/payments/initier/` - Initier un paiement
- `POST /api/payments/verifier/` - Vérifier un paiement

### Avis
- `GET /api/reviews/` - Liste des avis
- `POST /api/reviews/` - Créer un avis
- `POST /api/reviews/{id}/signaler/` - Signaler un avis

### Messagerie
- `GET /api/messaging/conversations/` - Liste des conversations
- `GET /api/messaging/conversations/avec_utilisateur/?user_id={id}` - Conversation avec un utilisateur
- `GET /api/messaging/messages/` - Messages d'une conversation
- `POST /api/messaging/messages/` - Envoyer un message

### Notifications
- `GET /api/notifications/` - Liste des notifications
- `POST /api/notifications/{id}/marquer_lue/` - Marquer comme lue
- `POST /api/notifications/marquer_toutes_lues/` - Marquer toutes comme lues

## Intégration des paiements

Les services de paiement sont implémentés dans `backend/payments/services.py`. Pour chaque service (Bankily, Moov Money, etc.), il faut :

1. Obtenir les clés API auprès du prestataire
2. Configurer les variables d'environnement dans `.env`
3. Implémenter les méthodes `process_payment` et `verify_payment` avec les vraies API

### Services supportés
- Bankily
- Moov Money
- BAMIS
- BMCI
- Cartes bancaires (Stripe/GIMTEL)

## Déploiement

### Backend
- Utiliser Gunicorn comme serveur WSGI
- Configurer Nginx comme reverse proxy
- Utiliser PostgreSQL en production
- Configurer les variables d'environnement
- Activer HTTPS

### Frontend
- Build de production : `npm run build`
- Servir avec Nginx ou un CDN
- Configurer l'URL de l'API en production

## Sécurité

- Mots de passe hashés avec bcrypt
- JWT pour l'authentification
- CORS configuré
- Protection CSRF
- Validation des entrées
- Escrow pour les paiements

## Fonctionnalités futures

- Application mobile (React Native)
- Notifications push
- Système de publicité
- Analytics avancés
- Intégration complète des APIs de paiement

