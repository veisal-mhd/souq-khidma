# Souq-Khidma

Plateforme de services en Mauritanie connectant clients et prestataires.

## Architecture

- **Backend**: Django REST Framework avec JWT
- **Frontend**: React.js + TailwindCSS
- **Base de données**: PostgreSQL
- **Paiements**: Bankily, Moov Money, BAMIS, BMCI, Cartes bancaires

## Installation

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Structure du projet

```
souq-lkhidme/
├── backend/          # Application Django
├── frontend/         # Application React
└── README.md
```

## Fonctionnalités

- Authentification (email, téléphone, réseaux sociaux)
- Gestion des services
- Messagerie interne
- Paiements intégrés
- Système d'évaluation
- Tableaux de bord clients/prestataires

