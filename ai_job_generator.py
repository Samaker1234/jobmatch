"""
Module d'IA pour générer des offres d'emploi réalistes
Utilise des templates et de la génération basée sur des profils
"""

import random
from typing import List, Dict
from datetime import datetime, timedelta

class JobOfferAIGenerator:
    """Générateur intelligent d'offres d'emploi"""
    
    def __init__(self):
        self.job_titles = {
            'development': [
                'Développeur Python Senior',
                'Développeur Full Stack',
                'Développeur Backend Node.js',
                'Développeur Frontend React',
                'Développeur Mobile iOS/Android',
                'Ingénieur DevOps',
                'Architecte Solutions Cloud',
                'Développeur Data Engineer',
                'Lead Developer',
                'Développeur Machine Learning',
            ],
            'design': [
                'Designer UX/UI Senior',
                'Product Designer',
                'Motion Designer',
                'Graphiste Web',
                'Designer d\'Interface',
                'Web Designer',
            ],
            'management': [
                'Product Manager',
                'Project Manager',
                'Scrum Master',
                'Chef de Projet Digital',
                'Manager Technique',
                'Technical Lead',
            ],
            'data': [
                'Data Scientist',
                'Data Analyst',
                'Business Intelligence Engineer',
                'Big Data Engineer',
                'Analytics Engineer',
            ],
            'qa': [
                'QA Engineer',
                'Test Automation Engineer',
                'QA Lead',
                'Test Manager',
            ]
        }
        
        self.companies = [
            'TechCorp', 'DataSoft', 'CloudInnovate', 'DigitalWorks',
            'WebDynamics', 'AI Solutions', 'DevStream', 'LogicForce',
            'NexGen Systems', 'ProTech', 'ByteForce', 'CloudBridge'
        ]
        
        self.skills_by_role = {
            'Développeur Python Senior': [
                'Python', 'Django', 'FastAPI', 'PostgreSQL', 'Redis',
                'Docker', 'Kubernetes', 'Git', 'TDD', 'Microservices'
            ],
            'Développeur Full Stack': [
                'React', 'Node.js', 'JavaScript', 'MongoDB', 'PostgreSQL',
                'Docker', 'AWS', 'REST API', 'GraphQL', 'TypeScript'
            ],
            'Designer UX/UI Senior': [
                'Figma', 'Adobe XD', 'Sketch', 'User Research', 'Prototyping',
                'Wireframing', 'Design Systems', 'Accessibility', 'CSS', 'Animation'
            ],
            'Product Manager': [
                'Product Strategy', 'User Research', 'Analytics', 'Agile',
                'Data Analysis', 'Roadmap Planning', 'Stakeholder Management', 'Market Analysis'
            ],
            'Data Scientist': [
                'Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'SQL',
                'Statistics', 'Data Visualization', 'Deep Learning', 'NLP', 'Computer Vision'
            ],
            'QA Engineer': [
                'Test Automation', 'Selenium', 'JUnit', 'TestNG', 'BDD',
                'API Testing', 'Performance Testing', 'SQL', 'CI/CD', 'Agile'
            ]
        }
        
        self.responsibilities = {
            'Développeur Python Senior': [
                'Concevoir et développer des solutions backend scalables',
                'Mentorer les développeurs juniors et leads techniques',
                'Participer aux revues de code et définir les bonnes pratiques',
                'Optimiser les performances et la sécurité des applications',
                'Collaborer avec l\'équipe produit pour définir les spécifications'
            ],
            'Développeur Full Stack': [
                'Développer des applications web modernes et responsives',
                'Concevoir et implémenter les APIs REST',
                'Gérer la base de données et les migrations',
                'Déployer et maintenir les applications en production',
                'Collaborer avec le design et le backend'
            ],
            'Designer UX/UI Senior': [
                'Créer des designs visuels innovants et accessibles',
                'Mener des recherches utilisateurs et des tests',
                'Concevoir les interfaces et les interactions',
                'Construire et maintenir les design systems',
                'Collaborer avec les équipes produit et développement'
            ],
            'Data Scientist': [
                'Développer des modèles prédictifs et analytiques',
                'Analyser les données volumineuses et complexes',
                'Créer des visualisations et des rapports insights',
                'Optimiser les algorithmes de machine learning',
                'Déployer les modèles en production'
            ]
        }
        
        self.benefits = [
            'Télétravail flexible',
            'Horaires flexibles',
            'Formation continue',
            'Assurance maladie premium',
            'Ticket restaurant',
            'Congés illimités',
            'Prime de performance',
            'Stock options',
            'Environnement inclusif',
            'Crèche d\'entreprise',
            'Salle de sport',
            'Séminaires d\'équipe'
        ]
        
        self.experience_levels = ['Débutant', 'Intermédiaire', 'Confirmé', 'Senior', 'Expert']
        self.contract_types = ['CDI', 'CDD 12 mois', 'Stage', 'Freelance']
        self.work_locations = ['Paris', 'Île-de-France', 'Lyon', 'Toulouse', 'Bordeaux', 'Nantes', 'Marseille', 'Remote']
    
    def generate_offer(self, role_type: str = None) -> Dict:
        """Génère une offre d'emploi complète et réaliste"""
        
        # Choisir une catégorie si non spécifiée
        if role_type is None:
            role_type = random.choice(list(self.job_titles.keys()))
        
        # Sélectionner un poste
        job_title = random.choice(self.job_titles.get(role_type, self.job_titles['development']))
        
        # Générer les composantes
        company = random.choice(self.companies)
        salary_min = random.randint(35, 70) * 1000
        salary_max = salary_min + random.randint(10, 30) * 1000
        
        # Déterminer les compétences requises
        required_skills = self.skills_by_role.get(job_title, 
            random.sample([skill for skills in self.skills_by_role.values() 
                          for skill in skills], k=5))
        
        # Déterminer les responsabilités
        responsibilities = self.responsibilities.get(job_title, [
            'Contribuer au développement des projets',
            'Collaborer avec l\'équipe',
            'Assurer la qualité du travail',
            'Participer aux réunions d\'équipe'
        ])
        
        selected_benefits = random.sample(self.benefits, k=random.randint(5, 8))
        experience_level = random.choice(self.experience_levels)
        contract_type = random.choice(self.contract_types)
        location = random.choice(self.work_locations)
        
        # Générer les dates
        posted_date = datetime.now() - timedelta(days=random.randint(0, 30))
        deadline = posted_date + timedelta(days=random.randint(30, 90))
        
        # Créer la description
        description = self._generate_description(job_title, company, responsibilities)
        
        offer = {
            'id': f"JOB_{datetime.now().timestamp()}_{random.randint(1000, 9999)}",
            'title': job_title,
            'company': company,
            'location': location,
            'contract_type': contract_type,
            'experience_level': experience_level,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'description': description,
            'required_skills': required_skills[:7],  # Top 7 skills
            'nice_to_have_skills': required_skills[7:10] if len(required_skills) > 7 else [],
            'responsibilities': responsibilities[:5],
            'benefits': selected_benefits,
            'posted_date': posted_date.strftime('%d/%m/%Y'),
            'application_deadline': deadline.strftime('%d/%m/%Y'),
            'department': self._get_department(role_type),
            'team_size': random.randint(3, 15),
            'remote_percentage': random.choice([0, 50, 100]),
            'generated': True,
            'generated_date': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        
        return offer
    
    def generate_batch(self, count: int = 10, role_type: str = None) -> List[Dict]:
        """Génère un lot d'offres d'emploi"""
        return [self.generate_offer(role_type) for _ in range(count)]
    
    def generate_by_requirements(self, required_skills: List[str], 
                                experience_level: str = None,
                                location: str = None) -> Dict:
        """Génère une offre basée sur des critères spécifiques"""
        
        offer = self.generate_offer()
        
        # Adapter les compétences requises
        offer['required_skills'] = required_skills[:7]
        offer['nice_to_have_skills'] = [s for s in offer['nice_to_have_skills'] 
                                       if s not in required_skills]
        
        # Adapter le niveau d'expérience
        if experience_level:
            offer['experience_level'] = experience_level
        
        # Adapter la localisation
        if location:
            offer['location'] = location
        
        return offer
    
    def _generate_description(self, title: str, company: str, 
                            responsibilities: List[str]) -> str:
        """Génère une description textuelle réaliste"""
        
        description = f"""
{company} recrute un {title} pour rejoindre notre équipe dynamique et innovante.

À propos du rôle:
Nous recherchons un professionnel expérimenté qui rejoindra notre équipe passionnée par la technologie et l'innovation. 
Vous serez au cœur de nos projets ambitieux et contribuerez à façonner l'avenir de notre entreprise.

Vos responsabilités:
"""
        for i, resp in enumerate(responsibilities, 1):
            description += f"\n{i}. {resp}"
        
        description += """

Ce que nous cherchons:
- Une expertise reconnue dans votre domaine
- Une forte capacité d'adaptation et d'apprentissage
- Un esprit d'équipe et une bonne communication
- Une passion pour l'excellence et l'innovation

Ce que nous offrons:
- Un environnement de travail moderne et stimulant
- Des opportunités de développement professionnel
- Une équipe talentueuse et collaborative
- Des outils et ressources de pointe
"""
        
        return description.strip()
    
    def _get_department(self, role_type: str) -> str:
        """Retourne le département basé sur le type de rôle"""
        departments = {
            'development': 'Ingénierie',
            'design': 'Design & UX',
            'management': 'Management',
            'data': 'Data & Analytics',
            'qa': 'Qualité & Testing'
        }
        return departments.get(role_type, 'Général')


# Exemple d'utilisation
if __name__ == "__main__":
    generator = JobOfferAIGenerator()
    
    # Générer une seule offre
    offer = generator.generate_offer()
    print("Offre générée:")
    for key, value in offer.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Générer plusieurs offres
    offers = generator.generate_batch(5)
    print(f"Lot de {len(offers)} offres générées avec succès!")
    for i, offer in enumerate(offers, 1):
        print(f"{i}. {offer['title']} @ {offer['company']} ({offer['location']})")
