# Guide de Déploiement - Application Flask (JobMath)

Ce guide vous montre les étapes nécessaires pour déployer votre application Flask en production. Nous utiliserons **Render**, car c'est une plateforme très populaire, facile à utiliser et qui propose une offre gratuite parfaite pour commencer.

## 1. Prérequis

Avant de commencer le déploiement, assurez-vous d'avoir :
* Un compte **GitHub** (pour héberger votre code).
* Un compte **Render** (https://render.com/).
* Le serveur WSGI `gunicorn` installé dans votre projet.

## 2. Préparation du projet en local

### A. Ajouter Gunicorn
Flask utilise un serveur de développement intégré qui n'est pas conçu pour la production. Nous devons utiliser `gunicorn`.
Assurez-vous qu'il est dans votre fichier `requirements.txt`. Si ce n'est pas le cas, ajoutez-le :
```text
# Dans requirements.txt, ajoutez la ligne suivante :
gunicorn==21.2.0
```

### B. Vérifier les variables d'environnement (.env)
En production, vous ne devez **jamais** envoyer votre fichier `.env` sur GitHub. Vous devrez configurer ces variables manuellement sur la plateforme d'hébergement.
Faites une liste des variables présentes dans votre `.env` (ex: `SECRET_KEY`, `GEMINI_API_KEY`, etc.) pour les avoir à portée de main.

### C. Pousser le code sur GitHub
1. Initialisez un dépôt Git si ce n'est pas fait (`git init`).
2. Assurez-vous d'avoir un fichier `.gitignore` qui ignore le dossier `venv/`, `__pycache__/` et surtout le fichier `.env`.
3. Commitez et poussez votre code sur un nouveau dépôt GitHub.

## 3. Déploiement sur Render

1. Connectez-vous sur **Render.com** et allez dans votre Dashboard.
2. Cliquez sur **"New"** et sélectionnez **"Web Service"**.
3. Choisissez **"Build and deploy from a Git repository"** et connectez votre compte GitHub.
4. Sélectionnez le dépôt de votre projet JobMath.
5. Remplissez les paramètres de configuration :
   * **Name** : `jobmath-app` (ou le nom de votre choix)
   * **Region** : Choisissez la plus proche (ex: Frankfurt pour l'Europe)
   * **Branch** : `main` (ou `master`)
   * **Runtime** : `Python 3`
   * **Build Command** : `pip install -r requirements.txt && prisma generate && prisma db push --accept-data-loss`
   * **Start Command** : `gunicorn app:app` *(Si votre fichier principal s'appelle app.py et que l'instance Flask s'appelle app)*

6. **Variables d'environnement :**
   Descendez jusqu'à la section "Environment Variables" et cliquez sur "Add Environment Variable". 
   Ajoutez **toutes** les variables de votre fichier `.env` local une par une.
   
   **IMPORTANT POUR SUPABASE (Prisma) :**
   Vous devez récupérer vos identifiants sur Supabase (Settings > Database) et ajouter ces deux variables :
   * `DATABASE_URL` : (Utilisez l'URL avec le port `6543` et `?pgbouncer=true` à la fin)
   * `DIRECT_URL` : (Utilisez l'URL avec le port `5432` sans pgbouncer)

7. Cliquez sur le bouton **"Create Web Service"** en bas de la page.

## 4. Finalisation
Render va maintenant récupérer votre code, installer les dépendances et lancer l'application. 
* Vous pouvez suivre l'avancement dans les logs affichés à l'écran.
* Si le déploiement réussit, Render vous fournira une URL (ex: `https://jobmath-app.onrender.com`).
* En cas d'erreur `502` ou `503`, vérifiez les logs de Render pour voir ce qui a échoué (souvent une variable d'environnement manquante ou un problème avec gunicorn).

---
> 💡 **Conseil de sécurité :** Mettez toujours `DEBUG=False` dans vos variables d'environnement en production pour des raisons de sécurité.
