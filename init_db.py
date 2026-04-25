import json
from app import app, db
from models import JobOffer

def seed_data():
    with app.app_context():
        # Check if we already have data to avoid duplicates
        if JobOffer.query.first():
            print("Database already contains job offers. Skipping seed.")
            return

        offers = [
            {
                "title": "Développeur Fullstack Python/React",
                "company": "TechVision AI",
                "location": "Paris (75)",
                "salary": "55k - 70k €",
                "contract_type": "CDI",
                "description": "Nous recherchons un développeur passionné par l'IA et les interfaces modernes pour rejoindre notre équipe core.",
                "requirements": json.dumps(["Python 3.10+", "React", "Flask/FastAPI", "PostgreSQL", "Docker"]),
                "is_generated": False
            },
            {
                "title": "Data Scientist Senior",
                "company": "DataVista Solutions",
                "location": "Lyon (69) / Télétravail",
                "salary": "60k - 85k €",
                "contract_type": "CDI",
                "description": "Rejoignez une équipe de pointe travaillant sur des modèles LLM personnalisés pour le secteur financier.",
                "requirements": json.dumps(["NLP", "PyTorch", "Transformers", "SQL", "Pandas", "Scikit-Learn"]),
                "is_generated": False
            },
            {
                "title": "Ingénieur DevOps",
                "company": "CloudNative Corp",
                "location": "Bordeaux (33)",
                "salary": "50k - 65k €",
                "contract_type": "CDI",
                "description": "Optimisez nos pipelines CI/CD et gérez notre infrastructure Kubernetes sur GCP.",
                "requirements": json.dumps(["Kubernetes", "Terraform", "CI/CD", "AWS/GCP", "Linux"]),
                "is_generated": False
            },
            {
                "title": "UX/UI Designer Premium",
                "company": "CreativeMind Studio",
                "location": "Full Remote",
                "salary": "45k - 60k €",
                "contract_type": "Freelance",
                "description": "Concevez des interfaces d'exception avec un focus sur le glassmorphism et les micro-animations.",
                "requirements": json.dumps(["Figma", "Adobe XD", "Design System", "Prototyping"]),
                "is_generated": False
            }
        ]
        
        for offer_data in offers:
            offer = JobOffer(**offer_data)
            db.session.add(offer)
        
        db.session.commit()
        print(f"Successfully seeded {len(offers)} job offers.")

if __name__ == "__main__":
    seed_data()
