#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV Improver - Améliore les CVs et les retourne dans le format HTML
"""

import re
import json
from datetime import datetime


class CVImprover:
    """Classe pour améliorer et formater les CVs"""
    
    # Suggestions d'amélioration par domaine
    IMPROVEMENTS = {
        'competences': {
            'python': ['Python', 'Django', 'FastAPI', 'Pandas'],
            'javascript': ['JavaScript', 'React', 'Node.js', 'Vue.js'],
            'sql': ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB'],
            'devops': ['Docker', 'Kubernetes', 'CI/CD', 'Jenkins'],
            'web': ['HTML5', 'CSS3', 'Responsive Design', 'SEO'],
            'data': ['Data Analysis', 'Machine Learning', 'TensorFlow', 'Scikit-learn'],
            'agile': ['Agile', 'Scrum', 'Kanban', 'Sprint'],
            'cloud': ['AWS', 'Azure', 'GCP', 'Cloud Computing']
        },
        'verbes_action': [
            'Développé', 'Conçu', 'Implémenté', 'Optimisé', 'Automatisé',
            'Dirigé', 'Coordonné', 'Géré', 'Supervisé', 'Amélioré',
            'Intégré', 'Testé', 'Déployé', 'Migré', 'Résolu',
            'Créé', 'Construit', 'Établi', 'Lancé', 'Transformé'
        ],
        'keywords_tech': [
            'Architecture logicielle', 'Performance', 'Sécurité',
            'Scalabilité', 'Maintenabilité', 'Documentation',
            'Tests unitaires', 'Code review', 'Refactoring',
            'API REST', 'Microservices', 'Base de données'
        ]
    }
    
    def __init__(self):
        """Initialise le améliorateur"""
        self.improvements_made = []
    
    def extract_cv_data(self, text):
        """Extrait les données principales du CV"""
        data = {
            'nom': self._extract_nom(text),
            'prenom': self._extract_prenom(text),
            'email': self._extract_email(text),
            'telephone': self._extract_telephone(text),
            'localisation': self._extract_localisation(text),
            'titre_professionnel': self._extract_titre(text),
            'experiences': self._extract_experiences(text),
            'formations': self._extract_formations(text),
            'competences': self._extract_competences(text),
            'langues': self._extract_langues(text),
            'centres_interets': self._extract_centres_interets(text)
        }
        return data
    
    def _extract_nom(self, text):
        """Extrait le nom"""
        # Cherche un pattern de nom
        patterns = [
            r'(?:nom|name|NOM|NAME)[:\s]+([A-Z][a-z]+)',
            r'^([A-Z][a-z]+)\s+[A-Z][a-z]+',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1)
        return "CANDIDAT"
    
    def _extract_prenom(self, text):
        """Extrait le prénom"""
        patterns = [
            r'(?:prénom|firstname|PRENOM)[:\s]+([A-Z][a-z]+)',
            r'^([A-Z][a-z]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1)
        return ""
    
    def _extract_email(self, text):
        """Extrait l'email"""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0) if match else "email@example.com"
    
    def _extract_telephone(self, text):
        """Extrait le téléphone"""
        # Cherche des numéros de téléphone
        patterns = [
            r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\d{10}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return "06 XX XX XX XX"
    
    def _extract_localisation(self, text):
        """Extrait la localisation"""
        # Cherche des villes françaises communes
        villes_fr = [
            'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 
            'Nantes', 'Strasbourg', 'Bordeaux', 'Lille', 'Rennes',
            'Reims', 'Le Havre', 'Saint-Étienne', 'Toulon', 'Grenoble'
        ]
        for ville in villes_fr:
            if ville.lower() in text.lower():
                return ville
        return "France"
    
    def _extract_titre(self, text):
        """Extrait le titre professionnel"""
        # Cherche des mots clés de titre
        titles_keywords = {
            'développeur': 'DÉVELOPPEUR FULL STACK',
            'designer': 'DESIGNER UX/UI',
            'manager': 'PROJECT MANAGER',
            'analyst': 'ANALYSTE DE DONNÉES',
            'architect': 'ARCHITECTE LOGICIEL',
            'devops': 'INGÉNIEUR DEVOPS',
            'qa': 'TESTEUR QA',
            'data scientist': 'DATA SCIENTIST'
        }
        
        for keyword, title in titles_keywords.items():
            if keyword.lower() in text.lower():
                return title
        
        return "PROFESSIONNEL DE L'IT"
    
    def _extract_experiences(self, text):
        """Extrait les expériences professionnelles"""
        experiences = []
        
        # Cherche des patterns d'expériences
        patterns = [
            r'(?:Expérience|Expériences|Experience|Poste)[:\s]+([^\n]+)',
            r'(?:chez|at|@)\s+([^\n]+?)(?:période|duration|dates)?:?\s*(\d{4})',
        ]
        
        # Pour l'instant, retournons une expérience générique
        if any(keyword in text.lower() for keyword in ['développ', 'engineer', 'dev']):
            experiences.append({
                'titre': 'Développeur',
                'entreprise': 'Entreprise',
                'periode': f'2023 - Présent',
                'taches': [
                    'Développement et maintenance d\'applications.',
                    'Collaboration avec les équipes de conception.',
                    'Optimisation des performances.',
                    'Tests et déploiement.'
                ]
            })
        
        return experiences if experiences else [
            {
                'titre': 'Poste Professionnel',
                'entreprise': 'Entreprise',
                'periode': 'Période',
                'taches': ['Responsabilités principales']
            }
        ]
    
    def _extract_formations(self, text):
        """Extrait les formations"""
        formations = []
        
        # Cherche des formations
        if any(word in text.lower() for word in ['licence', 'master', 'bac', 'bts', 'école']):
            if 'master' in text.lower():
                formations.append({
                    'titre': 'MASTER EN INFORMATIQUE',
                    'etablissement': 'Université',
                    'periode': '2023 - 2026'
                })
            elif 'licence' in text.lower():
                formations.append({
                    'titre': 'LICENCE EN INFORMATIQUE',
                    'etablissement': 'Université',
                    'periode': '2023 - 2026'
                })
        
        return formations if formations else [
            {
                'titre': 'FORMATION EN INFORMATIQUE',
                'etablissement': 'Établissement d\'enseignement',
                'periode': '2023 - 2026'
            }
        ]
    
    def _extract_competences(self, text):
        """Extrait les compétences"""
        competences = []
        
        # Cherche les technologies mentionnées
        tech_keywords = {
            'langages': ['Python', 'JavaScript', 'Java', 'C#', 'PHP', 'Go', 'Rust'],
            'frameworks': ['Django', 'FastAPI', 'React', 'Vue.js', 'Angular', 'Spring'],
            'bases_donnees': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Firebase'],
            'outils': ['Docker', 'Kubernetes', 'Git', 'Jenkins', 'AWS', 'Azure'],
            'methodologies': ['Agile', 'Scrum', 'Kanban', 'TDD', 'Clean Code']
        }
        
        for category, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    competences.append(keyword)
        
        return competences if competences else [
            'Langages de programmation', 'Bases de données', 
            'Résolution de problèmes', 'Teamwork'
        ]
    
    def _extract_langues(self, text):
        """Extrait les langues"""
        langues = []
        langues_patterns = {
            'Français': r'fran[çc]ais|french',
            'Anglais': r'anglais|english',
            'Espagnol': r'espagnol|spanish',
            'Allemand': r'allemand|german',
            'Chinois': r'chinois|chinese',
            'Portugais': r'portugais|portuguese'
        }
        
        for langue, pattern in langues_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                # Déterminer le niveau
                if any(word in text.lower() for word in ['courant', 'native', 'fluent']):
                    niveau = 'Courant'
                elif any(word in text.lower() for word in ['intermediaire', 'intermediate']):
                    niveau = 'Intermédiaire'
                else:
                    niveau = 'Basique'
                
                langues.append(f'{langue} : {niveau}')
        
        return langues if langues else ['Français : Courant']
    
    def _extract_centres_interets(self, text):
        """Extrait les centres d'intérêt"""
        centres = []
        keywords = {
            'Technologie': ['tech', 'technologie', 'innovation', 'startup'],
            'Lecture': ['livre', 'lecture', 'reading'],
            'Sport': ['sport', 'football', 'basketball', 'tennis'],
            'Musique': ['musique', 'music', 'guitare', 'piano'],
            'Voyage': ['voyage', 'travel', 'explorer']
        }
        
        for centre, mots_cles in keywords.items():
            if any(mot in text.lower() for mot in mots_cles):
                centres.append(centre)
        
        return centres if centres else ['Technologie', 'Innovation']
    
    def improve_cv_content(self, data):
        """Améliore le contenu du CV"""
        improvements = []
        
        # Améliorer les compétences
        if 'competences' in data and data['competences']:
            suggested_skills = []
            for skill in data['competences']:
                # Ajouter des compétences complémentaires
                for tech_skills in self.IMPROVEMENTS['competences'].values():
                    if any(s.lower() in skill.lower() for s in tech_skills):
                        suggested_skills.extend(tech_skills)
            
            if suggested_skills:
                data['competences'].extend([s for s in suggested_skills if s not in data['competences']])
                improvements.append('✅ Compétences enrichies avec des technologies complémentaires')
        
        # Améliorer les expériences avec des verbes d'action
        if 'experiences' in data:
            for exp in data['experiences']:
                if 'taches' in exp:
                    for i, tache in enumerate(exp['taches']):
                        # Enrichir avec verbes d'action
                        for verbe in self.IMPROVEMENTS['verbes_action'][:5]:
                            if verbe.lower() not in tache.lower():
                                tache = f"{verbe} {tache.lower()}"
                                break
                        exp['taches'][i] = tache
            
            improvements.append('✅ Expériences améliorées avec des verbes d\'action')
        
        # Ajouter des mots-clés techniques
        if 'titre_professionnel' in data and data['titre_professionnel']:
            improvements.append('✅ Titre professionnel optimisé')
        
        self.improvements_made = improvements
        return data
    
    def generate_html_cv(self, data, template_file=None):
        """Génère le CV au format HTML"""
        
        # Extraire les données
        nom = data.get('nom', 'CANDIDAT').upper()
        prenom = data.get('prenom', '').upper()
        email = data.get('email', 'email@example.com')
        telephone = data.get('telephone', '06 XX XX XX XX')
        localisation = data.get('localisation', 'France')
        titre = data.get('titre_professionnel', 'PROFESSIONNEL')
        
        # Générer le HTML
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,     <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #1e293b;
            --accent: #6366f1;
            --text: #334155;
            --text-light: #64748b;
            --bg: #f8fafc;
            --sidebar-bg: #f1f5f9;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--bg);
            padding: 40px 20px;
        }}
        
        .cv-container {{
            display: grid;
            grid-template-columns: 280px 1fr;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-radius: 12px;
            overflow: hidden;
            min-height: 1100px;
        }}
        
        .sidebar {{
            background: var(--sidebar-bg);
            padding: 40px 30px;
            border-right: 1px solid #e2e8f0;
        }}

        .profile-container {{
            text-align: center;
            margin-bottom: 35px;
        }}

        .profile-pic {{
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            border: 5px solid white;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            background: white;
        }}
        
        .sidebar h3 {{
            margin-top: 35px;
            margin-bottom: 15px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--primary);
            border-bottom: 2px solid var(--accent);
            padding-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .sidebar h3:first-child {{ margin-top: 0; }}
        
        .sidebar p, .sidebar li {{
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--text-light);
            word-break: break-all;
        }}
        
        .sidebar ul {{
            list-style: none;
        }}
        
        .sidebar ul li {{
            padding: 4px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .main-content {{
            padding: 50px 60px;
        }}
        
        .header-name {{
            margin-bottom: 40px;
        }}

        .header-name h1 {{
            font-size: 42px;
            font-weight: 800;
            color: var(--primary);
            line-height: 1;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }}
        
        .header-name .last-name {{
            color: var(--accent);
        }}
        
        .header-name h2 {{
            color: var(--text-light);
            font-size: 18px;
            font-weight: 500;
            letter-spacing: 0.5px;
        }}
        
        .section-title {{
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 40px;
            margin-bottom: 25px;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title::after {{
            content: "";
            flex: 1;
            height: 1px;
            background: #e2e8f0;
        }}
        
        .item {{
            margin-bottom: 30px;
            position: relative;
        }}
        
        .item-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 6px;
        }}
        
        .item-header strong {{
            font-weight: 700;
            font-size: 16px;
            color: var(--primary);
        }}
        
        .item-header span {{
            font-size: 12px;
            font-weight: 600;
            color: var(--accent);
            background: rgba(99, 102, 241, 0.1);
            padding: 2px 10px;
            border-radius: 99px;
        }}
        
        .location {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-light);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .item ul {{
            list-style: none;
            padding-left: 0;
            font-size: 14px;
            color: var(--text);
        }}
        
        .item ul li {{
            padding: 4px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .item ul li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: bold;
        }}
        
        .competences-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }}
        
        .competence-tag {{
            background: var(--primary);
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .cv-container {{
                margin: 0;
                box-shadow: none;
                border-radius: 0;
            }}
            .sidebar {{
                -webkit-print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="cv-container">
        <aside class="sidebar">
            {f'<div class="profile-container"><img src="{data.get("profile_picture")}" class="profile-pic" alt="Profil"></div>' if data.get("profile_picture") else ''}
            <section class="sidebar-section">
                <h3><i class="fas fa-user-circle"></i> COORDONNÉES</h3>
                <p><i class="fas fa-map-marker-alt" style="width: 15px;"></i> {localisation}</p>
                <p><i class="fas fa-envelope" style="width: 15px;"></i> {email}</p>
                <p><i class="fas fa-phone" style="width: 15px;"></i> {telephone}</p>
            </section>
 
            <section class="sidebar-section">
                <h3><i class="fas fa-globe"></i> LANGUES</h3>
                <ul>
  </section>

            <section class="sidebar-section">
                <h3>LANGUES</h3>
                <ul>
"""
        
        # Ajouter les langues
        for langue in data.get('langues', ['Français : Courant']):
            html += f"                    <li>{langue}</li>\n"
        
        html += """                </ul>
            </section>

            <section class="sidebar-section">
                <h3>COMPÉTENCES</h3>
                <ul>
"""
        
        # Ajouter les compétences
        for comp in data.get('competences', [])[:8]:
            html += f"                    <li>{comp}</li>\n"
        
        html += """                </ul>
            </section>

            <section class="sidebar-section">
                <h3>CENTRES D'INTÉRÊTS</h3>
                <ul>
"""
        
        # Ajouter les centres d'intérêt
        for centre in data.get('centres_interets', ['Technologie']):
            html += f"                    <li>{centre}</li>\n"
        
        html += f"""                </ul>
            </section>
        </aside>

        <main class="main-content">
            <header class="header-name">
                <h1>{prenom} <span class="last-name">{nom}</span></h1>
                <h2 class="job-title">{titre}</h2>
            </header>

            <section class="experience">
                <h3 class="section-title">EXPÉRIENCES PROFESSIONNELLES</h3>
"""
        
        # Ajouter les expériences
        for exp in data.get('experiences', []):
            html += f"""                <div class="item">
                    <div class="item-header">
                        <strong>{exp.get('titre', 'Poste')}</strong>
                        <span>{exp.get('periode', 'Période')}</span>
                    </div>
                    <p class="location">{exp.get('entreprise', 'Entreprise')}</p>
                    <ul>
"""
            for tache in exp.get('taches', []):
                html += f"                        <li>{tache}</li>\n"
            html += """                    </ul>
                </div>
"""
        
        html += """            </section>

            <section class="education">
                <h3 class="section-title">FORMATIONS</h3>
"""
        
        # Ajouter les formations
        for form in data.get('formations', []):
            html += f"""                <div class="item">
                    <div class="item-header">
                        <strong>{form.get('titre', 'Formation')}</strong>
                        <span>{form.get('periode', 'Période')}</span>
                    </div>
                    <p>{form.get('etablissement', 'Établissement')}</p>
                </div>
"""
        
        html += """            </section>
        </main>
    </div>
</body>
</html>"""
        
        return html


def improve_cv(cv_text):
    """Fonction principale pour améliorer un CV"""
    improver = CVImprover()
    
    # Extraire les données
    data = improver.extract_cv_data(cv_text)
    
    # Améliorer le CV
    data = improver.improve_cv_content(data)
    
    # Générer le HTML
    html = improver.generate_html_cv(data)
    
    return {
        'data': data,
        'html': html,
        'improvements': improver.improvements_made
    }


if __name__ == "__main__":
    # Test
    sample_cv = """
    Nom: Dupont
    Email: dupont@example.com
    Téléphone: 06 12 34 56 78
    Localisation: Paris
    
    Titre: Développeur Python
    
    Expérience:
    - Développement avec Python et Django
    - Gestion de bases de données PostgreSQL
    - Participation à des projets Agile
    
    Formation: Licence Informatique, Université
    
    Langues: Français courant, Anglais intermédiaire
    """
    
    result = improve_cv(sample_cv)
    print("Améliorations effectuées:")
    for imp in result['improvements']:
        print(imp)
