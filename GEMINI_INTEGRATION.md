# Intégration Gemini API - Guide d'utilisation

## 🤖 Vue d'ensemble

L'API Gemini (Google) a été intégrée à JobMatch pour :
1. **Générer des offres d'emploi** automatiquement et intelligemment
2. **Analyser la compatibilité CV ↔ Offre** avec expertise IA
3. **Suggérer des améliorations** pour optimiser les CVs

## 🔑 Configuration de la clé API

```python
# Dans config.py (ne pas committer la clé dans le dépôt)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')  # <votre_GEMINI_API_KEY_ici>
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')
GEMINI_ENABLED = bool(os.environ.get('GEMINI_ENABLED', '1'))
```

La clé API est automatiquement chargée depuis `config.py` ou la variable d'environnement `GEMINI_API_KEY`.

## 📡 Endpoints API disponibles

### 1. Generate Job Offer (Générer une offre d'emploi)

**Endpoint:** `POST /api/generate-job-offer`

**Payload:**
```json
{
  "job_title": "Développeur Python Senior",
  "company": "TechCorp",
  "skills": ["Python", "Django", "PostgreSQL", "Docker"],
  "experience_level": "Senior"
}
```

**Réponse:**
```json
{
  "success": true,
  "offer": {
    "title": "Développeur Python Senior",
    "company": "TechCorp",
    "description": "Description détaillée...",
    "requirements": ["Python", "Django", ...],
    "nice_to_have": ["Kubernetes", "GraphQL"],
    "salary_range": "60000-85000€",
    "job_type": "CDI",
    "location": "Paris, Télétravail possible",
    "benefits": ["Assurance santé", "RTT", ...]
  },
  "generated_at": "2026-02-09T10:30:00"
}
```

### 2. Analyze CV Compatibility (Analyse avancée)

**Endpoint:** `POST /api/analyze-compatibility-ai`

**Payload:**
```json
{
  "cv_text": "Contenu complet du CV (texte extrait)...",
  "job_offer": "Description détaillée de l'offre d'emploi..."
}
```

**Réponse:**
```json
{
  "success": true,
  "analysis": {
    "compatibility_score": 87,
    "overall_assessment": "Excellent",
    "matching_skills": ["Python", "Django", "PostgreSQL"],
    "missing_skills": ["Kubernetes", "GraphQL"],
    "experience_match": "Les 8 ans d'expérience correspondent parfaitement",
    "strengths": ["Expert Python", "Leadership prouvé", "Expérience startup"],
    "recommendations": ["Améliorer connaissance Kubernetes", "Certifications AWS"],
    "cultural_fit": "Très bon fit avec culture d'entreprise",
    "insight": "Candidate exceptionnelle avec 87% de compatibilité..."
  },
  "generated_at": "2026-02-09T10:30:00"
}
```

### 3. Enhance CV (Améliorer un CV)

**Endpoint:** `POST /api/enhance-cv`

**Payload:**
```json
{
  "cv_text": "Contenu du CV à améliorer...",
  "job_title": "Développeur Python Senior" [optionnel]
}
```

**Réponse:**
```json
{
  "success": true,
  "suggestions": {
    "score_actuel": 72,
    "points_forts": ["Expérience diverse", "Projets numériques"],
    "points_faibles": ["Manque de mots-clés techniques", "Peu de chiffres"],
    "suggestions_specifiques": [
      "Ajouter 'Machine Learning' ou 'AI' si applicable",
      "Quantifier les résultats (réduction coûts de X%, augmentation de Y%)",
      "Mentionner des frameworks spécifiques"
    ],
    "exemple_modifications": {
      "avant": "Développement d'applications web",
      "apres": "Conception et développement d'applications web avec Django REST Framework, desservant 10K+ utilisateurs mensuels"
    },
    "mots_cles_manquants": ["Microservices", "CI/CD", "Docker", "Kubernetes"],
    "priorites": ["Ajouter métriques", "Spécifier technologies", "Enrichir descriptions"]
  },
  "generated_at": "2026-02-09T10:30:00"
}
```

## 🧪 Exemples de test

### Test avec curl

```bash
# Tester la génération d'offre
curl -X POST http://localhost:5000/api/generate-job-offer \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Data Scientist",
    "company": "StartupIA",
    "skills": ["Python", "Machine Learning", "TensorFlow", "SQL"],
    "experience_level": "Mid"
  }'

# Tester l'analyse de compatibilité
curl -X POST http://localhost:5000/api/analyze-compatibility-ai \
  -H "Content-Type: application/json" \
  -d '{
    "cv_text": "Diplômé en informatique. 5 ans d'\''expérience en Python...",
    "job_offer": "Recherchons Data Scientist avec expertise Python, ML et TensorFlow..."
  }'
```

### Test avec Python

```python
import requests
import json

API_BASE = "http://localhost:5000"

# Tester la génération d'offre
response = requests.post(
    f"{API_BASE}/api/generate-job-offer",
    json={
        "job_title": "Frontend Developer",
        "company": "TechCorp",
        "skills": ["React", "TypeScript", "CSS3", "REST API"],
        "experience_level": "Mid"
    }
)
print(json.dumps(response.json(), indent=2))

# Tester l'analyse de CV
response = requests.post(
    f"{API_BASE}/api/analyze-compatibility-ai",
    json={
        "cv_text": "Contenu du CV...",
        "job_offer": "Offre d'emploi..."
    }
)
print(json.dumps(response.json(), indent=2))
```

### Test avec JavaScript/Frontend

```javascript
// Générer une offre
async function generateJobOffer() {
    const response = await fetch('/api/generate-job-offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            job_title: 'Product Manager',
            company: 'Innovation Inc',
            skills: ['Product Strategy', 'Analytics', 'Agile'],
            experience_level: 'Senior'
        })
    });
    
    const data = await response.json();
    console.log('Generated Offer:', data.offer);
}

// Analyser compatible de CV
async function analyzeCompatibility() {
    const response = await fetch('/api/analyze-compatibility-ai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cv_text: "Mon CV...",
            job_offer: "L'offre d'emploi..."
        })
    });
    
    const data = await response.json();
    console.log('Compatibility Analysis:', data.analysis);
}
```

## 📊 Intégration dans le dashboard

Le endpoint `/api/analyze` existant a été enrichi avec Gemini :

```javascript
// L'analyse existante inclut maintenant les données Gemini
if (response.ai_powered && response.gemini_analysis) {
    // Afficher les résultats enrichis par Gemini
    displayGeminiAnalysis(response.gemini_analysis);
}
```

## 🔒 Gestion des erreurs

Les endpoints retournent les erreurs appropriées :

```json
{
  "error": "Service Gemini non disponible",
  "status": 503
}
```

#### Codes d'erreur:
- **400**: Données invalides ou manquantes
- **500**: Erreur lors du traitement avec Gemini
- **503**: Service Gemini non disponible/configuré

## 📝 Fichiers modifiés/créés

- ✅ `config.py` - Ajout de la configuration Gemini
- ✅ `gemini_service.py` - Nouveau service d'intégration Gemini
- ✅ `app.py` - 3 nouveaux endpoints + enrichissement du `/api/analyze` existant
- ✅ `requirements.txt` - Ajout de `google-generativeai`

## 🚀 Prochaines étapes

1. **Frontend UI** - Créer des formulaires pour utiliser les nouveaux endpoints
2. **Dashboard** - Afficher les analyses Gemini dans le dashboard
3. **Sauvegarde** - Persister les analyses générées en base de données
4. **Cache** - Implémenter un cache pour réduire les appels API
5. **Monitoring** - Logger et monitorer l'utilisation de l'API Gemini

## ❓ FAQ

**Q: Gérer les limites de taux de l'API Gemini?**
R: Gemini API a des limites gratuit. Implémentez un rate limiter si besoin :
```python
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/api/generate-job-offer', methods=['POST'])
@limiter.limit("5 per minute")
def generate_job_offer():
    ...
```

**Q: Comment utiliser une clé API différente?**
R: Définissez la variable d'environnement avant de lancer l'app :
```bash
set GEMINI_API_KEY=votre_cle_ici
python app.py
```

**Q: Peut-on utiliser d'autres modèles Gemini?**
R: Oui, modifiez dans `config.py` :
```python
GEMINI_MODEL = 'gemini-pro-vision'  # Pour l'analyse d'images
```

**Q: Performance pour les gros CVs?**
R: Le service limite à 3000 caractères pour les CVs et 2000 pour les offres pour éviter les timeouts.
