# Guide d'obtention de la clé (Mot de passe d'application Google)

Pour que votre application puisse envoyer des emails de récupération via Gmail, vous ne pouvez pas utiliser votre mot de passe habituel. Vous devez générer un **Mot de passe d'application**.

## Étapes :

1.  **Activer la Validation en deux étapes** :
    *   Allez sur votre [Compte Google](https://myaccount.google.com/).
    *   Sécurité -> Validation en deux étapes.
    *   Suivez les étapes pour l'activer si ce n'est pas déjà fait.

2.  **Générer le Mot de passe d'application** :
    *   Revenez dans l'onglet **Sécurité**.
    *   Dans la barre de recherche en haut, tapez "**Mots de passe d'application**".
    *   Si l'option n'apparaît pas, assurez-vous que la validation en 2 étapes est bien active.
    *   Donnez un nom à l'application (ex: "JobMatch" ou "AgriOrbit").
    *   Cliquez sur **Créer**.

3.  **Copier la clé** :
    *   Un code de **16 caractères** s'affiche dans un encadré jaune.
    *   Copiez ce code (sans les espaces).

4.  **Mettre à jour le fichier .env** :
    *   Ouvrez votre fichier `flask_app/.env`.
    *   Remplacez `votre_mot_de_passe_app_ici` par cette clé de 16 caractères.

```env
MAIL_PASSWORD=votre_cle_de_16_caracteres_ici
```

---
**Note** : Ne partagez jamais cette clé. Elle donne un accès direct à l'envoi d'emails via votre compte.
