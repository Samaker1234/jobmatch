#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service d'intégration Gemini API pour la génération d'offres et l'analyse de CV
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import logging

# Charger le fichier .env en PREMIER
load_dotenv()

from config import Config

logger = logging.getLogger(__name__)

class GeminiService:
    """Service pour interagir avec Gemini API"""
    
    def __init__(self):
        """Initialise le service Gemini"""
        self.enabled = False
        try:
            # Check if enabled in config
            if not Config.GEMINI_ENABLED:
                logger.info("ℹ Service Gemini désactivé dans la configuration")
                return

            api_key = Config.GEMINI_API_KEY
            model_name = Config.GEMINI_MODEL or 'gemini-1.5-flash'
            
            if not api_key:
                logger.error("✗ GEMINI_API_KEY manquante dans Config")
                return

            genai.configure(api_key=api_key)
            
            # System instruction for consistency
            system_instruction = "Vous êtes l'Assistant JobMatch, expert en recrutement. Répondez en français de manière concise et professionnelle."
            
            try:
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
                # Test connectivity
                # self.model.generate_content("hello", generation_config={"max_output_tokens": 1})
            except Exception as model_err:
                logger.warning(f"⚠ Erreur avec le modèle {model_name}, tentative avec gemini-1.5-flash")
                self.model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=system_instruction
                )
                
            self.enabled = True
            logger.info(f"✓ Service Gemini prêt avec success")
        except Exception as e:
            logger.error(f"✗ Erreur d'initialisation Gemini : {str(e)}")
    
    def extract_text_from_image(self, image_data: bytes, mime_type: str = "image/jpeg") -> str:
        """
        Extrait le texte d'une image (offre d'emploi) via Gemini Vision
        """
        if not self.enabled:
            return ""
            
        try:
            # Prepare multimodal content
            contents = [
                {
                    "mime_type": mime_type,
                    "data": image_data
                },
                "Veuillez extraire tout le texte pertinent de cette offre d'emploi. Ignorez les publicités ou les éléments d'interface utilisateur non pertinents. Fournissez uniquement le texte de l'offre."
            ]
            
            response = self.model.generate_content(contents)
            return response.text.strip()
        except Exception as e:
            logger.error(f"✗ Erreur OCR Gemini : {str(e)}")
            return ""

    def extract_text_from_pdf_ai(self, pdf_bytes: bytes) -> str:
        """
        Extrait le texte d'un PDF complexe ou scanné via les capacités multimodales de Gemini 1.5
        """
        if not self.enabled:
            return ""
            
        try:
            # Gemini 1.5 supporte les PDF directement
            print(">>> DEBUG GEMINI: Envoi du PDF à l'API...")
            contents = [
                {
                    "mime_type": "application/pdf",
                    "data": pdf_bytes
                },
                "Veuillez extraire tout le texte de ce CV de manière structurée et fidèle. Fournissez uniquement le texte extrait."
            ]
            
            response = self.model.generate_content(contents)
            print(">>> DEBUG GEMINI: Réponse reçue de l'API.")
            text = response.text.strip()
            if text:
                logger.info("✓ Texte extrait du PDF via Gemini AI (Fallback)")
            else:
                logger.warning("⚠ Gemini a retourné un texte vide pour le PDF")
            return text
        except Exception as e:
            logger.error(f"✗ Erreur extraction PDF via Gemini : {str(e)}")
            return ""
    
    def generate_job_offers(self, job_title: str, company: str, skills: list, experience_level: str = "Senior") -> dict:
        """
        Génère une offre d'emploi détaillée avec Gemini
        
        Args:
            job_title: Titre du poste
            company: Nom de l'entreprise
            skills: Liste des compétences requises
            experience_level: Niveau d'expérience requis
        
        Returns:
            dict contenant l'offre générée
        """
        if not self.enabled:
            return {"error": "Service Gemini non disponible"}
        
        try:
            skills_str = ", ".join(skills)
            
            prompt = f"""
            Générez une offre d'emploi professionnelle et attrape en français pour le poste suivant:
            
            Titre du poste: {job_title}
            Entreprise: {company}
            Compétences requises: {skills_str}
            Niveau d'expérience: {experience_level}
            
            Formatez la réponse en JSON avec les clés suivantes:
            - title: Titre du poste
            - company: Nom de l'entreprise
            - description: Description détaillée (200-300 mots)
            - requirements: Liste des compétences requises
            - nice_to_have: Compétences appréciées (liste)
            - salary_range: Fourchette salariale estimée
            - job_type: Type de contrat (CDI, CDD, Stage, Freelance)
            - location: Localisation (télétravail possible)
            - benefits: Avantages proposés (liste)
            
            Répondez UNIQUEMENT avec du JSON valide, sans texte supplémentaire.
            """
            
            response = self.model.generate_content(prompt)
            
            # Essayer de parser la réponse JSON
            try:
                # Nettoyer la réponse potentiellement encadrée de ```json
                text = response.text
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                offer_data = json.loads(text)
                logger.info(f"✓ Offre générée pour {job_title} chez {company}")
                return offer_data
            except json.JSONDecodeError as e:
                logger.error(f"Erreur JSON parsing: {str(e)}")
                logger.error(f"Réponse brute: {response.text}")
                return {"error": "Format de réponse invalide", "raw": response.text}
        
        except Exception as e:
            logger.error(f"✗ Erreur génération offre : {str(e)}")
            return {"error": str(e)}
    
    def analyze_cv_compatibility(self, cv_text: str, job_offer: str) -> dict:
        """
        Analyse la compatibilité d'un CV avec une offre d'emploi
        
        Args:
            cv_text: Texte du CV
            job_offer: Description de l'offre d'emploi
        
        Returns:
            dict contenant l'analyse de compatibilité
        """
        if not self.enabled:
            return {"error": "Service Gemini non disponible"}
        
        try:
            prompt = f"""
            Analysez la compatibilité entre ce CV et cette offre d'emploi. Soyez rigoureux et analytique.
            
            CV:
            {cv_text[:3000]}  # Limiter la taille pour ne pas dépasser les limites API
            
            Offre d'emploi:
            {job_offer[:2000]}
            
            Fournissez une analyse au format JSON avec:
            - compatibility_score: Score de 0 à 100
            - overall_assessment: Évaluation générale (Excellent, Bon, Moyen, Faible)
            - matching_skills: Compétences correspondantes trouvées
            - missing_skills: Compétences manquantes importantes
            - experience_match: Évaluation de l'expérience (texte court)
            - strengths: Points forts du candidat (liste)
            - recommendations: Recommandations pour améliorer le profil
            - cultural_fit: Évaluation du potentiel d'intégration
            - insight: Analyse détaillée et conseil (200 mots max)
            
            Répondez UNIQUEMENT avec du JSON valide.
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                text = response.text
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                analysis_data = json.loads(text)
                logger.info(f"✓ Analyse de compatibilité effectuée (score: {analysis_data.get('compatibility_score', 'N/A')})")
                return analysis_data
            except json.JSONDecodeError as e:
                logger.error(f"Erreur JSON parsing analyse: {str(e)}")
                return {"error": "Format de réponse invalide", "raw": response.text}
        
        except Exception as e:
            logger.error(f"✗ Erreur analyse CV : {str(e)}")
            return {"error": str(e)}
    
    def enhance_cv(self, cv_text: str, job_title: str = None) -> dict:
        """
        Suggère des améliorations pour un CV basé sur un poste cible
        
        Args:
            cv_text: Texte du CV
            job_title: Titre du poste visé (optionnel)
        
        Returns:
            dict contenant les suggestions d'amélioration
        """
        if not self.enabled:
            return {"error": "Service Gemini non disponible"}
        
        try:
            job_context = f"pour le poste de {job_title}" if job_title else ""
            
            prompt = f"""
            Vous êtes un expert en recrutement et en optimisation de CV. Analysez ce CV {job_context} 
            et proposez des améliorations concrètes et constructives.
            
            CV actuel:
            {cv_text[:3000]}
            
            Fournissez en JSON:
            - score_actuel: Score de professionnalisme (0-100)
            - points_forts: Points forts du CV
            - points_faibles: Points à améliorer
            - suggestions_specifiques: Liste des amélioration concrètes
            - exemple_modifications: Exemples de texte révisé pour les sections clés
            - mots_cles_manquants: Mots-clés à ajouter
            - priorites: Améliorations par ordre de priorité
            
            Soyez positif mais rigoureux.
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                text = response.text
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                suggestions = json.loads(text)
                logger.info(f"✓ Suggestions CV générées")
                return suggestions
            except json.JSONDecodeError as e:
                logger.error(f"Erreur JSON parsing suggestions: {str(e)}")
                return {"error": "Format de réponse invalide"}
        
        except Exception as e:
            logger.error(f"✗ Erreur suggestions CV : {str(e)}")
            return {"error": str(e)}
    
    def chat(self, message: str, history: list = None) -> str:
        """
        Gère une interaction conversationnelle avec Gemini
        """
        if not self.enabled:
            return "Le service d'IA est actuellement désactivé."
            
        if not message:
            return ""
        
        try:
            # Utiliser le chat avec historique si disponible
            if history:
                chat_session = self.model.start_chat(history=history)
                response = chat_session.send_message(message)
            else:
                # Premier message (le contexte est déjà dans system_instruction)
                response = self.model.generate_content(message)
            
            return response.text
            
        except Exception as e:
            logger.error(f"✗ Erreur Chat Gemini : {str(e)}")
            # On retourne un message plus explicite pour débugger
            if "finish_reason: SAFETY" in str(e):
                return "Désolé, je ne peux pas répondre à cette question pour des raisons de sécurité."
            return f"Je rencontre une difficulté technique ({str(e)[:50]}...). Réessayez ?"

    def optimize_cv_and_structure(self, cv_text: str, job_offer_text: str = None) -> dict:
        """
        Méthode "Turbo" : Valide, extrait et optimise un CV en UN SEUL appel Gemini.
        Génère une structure de données complète prête pour l'affichage et le PDF.
        """
        if not self.enabled:
            return {"error": "Service Gemini non disponible"}
            
        try:
            context = f"en fonction de cette offre d'emploi : {job_offer_text[:1500]}" if job_offer_text else "de manière générale pour le marché actuel"
            
            prompt = f"""
            Vous êtes un expert en recrutement international. Votre mission est de transformer ce CV brut en un profil d'exception {context}.
            
            TEXTE DU CV :
            {cv_text[:4000]}
            
            ÉTAPE 1 : VALIDEZ s'il s'agit bien d'un CV.
            ÉTAPE 2 : EXTRAIRE et CORRIGER les informations (orthographe, tournures de phrases).
            ÉTAPE 3 : OPTIMISER les descriptions d'expériences en utilisant des verbes d'action et des résultats quantifiables.
            
            RÉPONDEZ UNIQUEMENT AU FORMAT JSON avec cette structure précise :
            {{
                "is_valid": true,
                "reason_invalid": "",
                "cv_data": {{
                    "nom": "NOM",
                    "prenom": "Prénom",
                    "email": "email@example.com",
                    "telephone": "0600000000",
                    "localisation": "Ville, Pays",
                    "titre_professionnel": "Titre optimisé",
                    "experiences": [
                        {{
                            "titre": "Poste",
                            "entreprise": "Entreprise",
                            "periode": "Dates",
                            "taches": ["Réalisation optimisée 1", "Résultat quantifiable 2"]
                        }}
                    ],
                    "formations": [
                        {{
                            "titre": "Diplôme",
                            "etablissement": "École",
                            "periode": "Dates"
                        }}
                    ],
                    "competences": ["Compétence 1", "Compétence 2"],
                    "langues": ["Langue (Niveau)"]
                }},
                "suggestions": ["Suggestion stratégique 1", "Suggestion stratégique 2"],
                "score_optimisation": 95
            }}
            """
            
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Nettoyage JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].strip()
                
            result = json.loads(text)
            logger.info(f"✓ CV optimisé et structuré en un seul appel (Turbo Mode)")
            return result
            
        except Exception as e:
            logger.error(f"✗ Erreur Turbo Optimization : {str(e)}")
            return {"error": str(e)}

    def is_cv_valid(self, text: str) -> dict:
        """
        Vérifie si le texte fourni ressemble à un CV (Expériences, Diplômes, Compétences).
        """
        if not self.enabled:
            return {"valid": True} # On laisse passer si le service est désactivé
            
        try:
            prompt = f"""
            Analysez très rapidement ce texte et déterminez s'il s'agit d'un Curriculum Vitae (CV) ou d'un profil professionnel. 
            Un CV contient généralement: expériences professionnelles, formation/diplômes, compétences, contact.
            
            Texte à analyser (extrait):
            {text[:2000]}
            
            Répondez UNIQUEMENT en JSON avec ce format:
            {{
                "is_cv": true/false,
                "reason": "Une courte explication si false (en français)"
            }}
            """
            
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Nettoyage JSON
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].strip()
                
            data = json.loads(raw_text)
            return {
                "valid": data.get("is_cv", False),
                "reason": data.get("reason", "Le document ne semble pas être un CV professionnel.")
            }
        except Exception as e:
            logger.error(f"Erreur lors de la validation du CV: {str(e)}")
            # En cas d'erreur IA, on laisse passer pour ne pas bloquer l'utilisateur
            return {"valid": True}
    
    def optimize_cv_for_job_offer(self, cv_text: str, job_offer_text: str) -> dict:
        """
        Optimise le CV en fonction d'une offre d'emploi spécifique.
        
        Args:
            cv_text: Texte du CV
            job_offer_text: Description complète de l'offre d'emploi
        
        Returns:
            dict contenant l'analyse et les suggestions d'optimisation
        """
        if not self.enabled:
            return {"error": "Service Gemini non disponible"}
        
        try:
            if not cv_text or len(cv_text) < 100:
                return {"error": "CV invalide (minimum 100 caractères)"}
            
            if not job_offer_text or len(job_offer_text) < 50:
                return {"error": "Offre d'emploi invalide"}
            
            prompt = f"""
            Vous êtes un expert en recrutement et optimisation de CV. Votre tâche est d'optimiser le CV en fonction de l'offre d'emploi.
            
            OFFRE D'EMPLOI:
            {job_offer_text[:2000]}
            
            CV ACTUEL:
            {cv_text[:3000]}
            
            Analysez et optimisez le CV pour correspondre au maximum à l'offre d'emploi.
            
            Fournissez une réponse en JSON avec la structure suivante:
            {{
                "score_matching": <nombre entre 0-100>,
                "keywords_found": [liste des mots-clés de l'offre présents dans le CV],
                "keywords_missing": [liste des mots-clés essentiels manquants],
                "competences_requises": [compétences requises par l'offre],
                "competences_presentes": [compétences du CV correspondant aux exigences],
                "competences_manquantes": [compétences à ajouter ou développer],
                "suggestions": [
                    {{
                        "section": "nom de la section (Expériences, Compétences, etc)",
                        "suggestion": "description de l'amélioration proposée",
                        "exemple": "texte proposé ou modification concrète",
                        "priorite": "haute/moyenne/basse"
                    }}
                ],
                "sections_a_ajouter": [sections manquantes qui renforceraient le CV],
                "cv_optimise": "Version révisée du CV optimisée pour l'offre",
                "resume_optimisation": "Résumé des changements effectués"
            }}
            
            Soyez très concret et proposez des modifications réelles du texte du CV.
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                text = response.text.strip()
                
                # Nettoyage JSON
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                result = json.loads(text)
                logger.info(f"✓ CV optimisé pour l'offre d'emploi")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"Erreur JSON parsing optimisation CV: {str(e)}")
                return {"error": "Format de réponse invalide", "raw": response.text[:500]}
        
        except Exception as e:
            logger.error(f"✗ Erreur optimisation CV : {str(e)}")
            return {"error": str(e)}


# Instance globale du service
gemini_service = GeminiService()
