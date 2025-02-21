import json
import os
import re

from fastapi import Request

class TranslationManager:
    def __init__(self):
        self.translations_folder = os.path.join(os.path.dirname(__file__), '../translations')
        self.translations = {}

    def load_translations(self):
        """
            Permet de charger les différentes trads disponible
        """
        print("[TranslationManager] Loading....")
        for filename in os.listdir(self.translations_folder):
            if filename.endswith(".json"):
                language = filename.split(".")[0]
                with open(os.path.join(self.translations_folder, filename), "r", encoding="utf-8") as f:
                    self.translations[language] = json.load(f)
        print("[TranslationManager] Done.")

    def get(self, language: str, key: str, **kwargs):
        """
            Permet de retourner la traduction en fonction de la langue et la clé
        """
        if language not in self.translations:
            language = "fr"

        translation = self.translations[language].get(key, key)
        return translation.format(**kwargs)

    def get_language(self, request: Request):
        """
            Permet de retourner la langue prioritaire en fonction des en-têtes de la requête http
        """

        accept_language = request.headers.get("Accept-Language", "fr").lower()

        # On split les langues de l'en-tête Accept-Language pour extraire les préférences de langue
        languages = accept_language.split(",")
        language_q_pairs = []

        # On récupère les langues et leurs score de priorité
        for lang in languages:
            parts = lang.split(";")
            language = parts[0].strip()
            q_value = 1.0
            if len(parts) > 1:
                match = re.match(r"q=([0-9\.]+)", parts[1])
                if match:
                    q_value = float(match.group(1))
            language_q_pairs.append((language, q_value))

        # On trie les langages en fonction du score q
        sorted_languages = sorted(language_q_pairs, key=lambda x: x[1], reverse=True)

        # On retourne la première langue dans la liste triée (la plus prioritaire)
        best_language = sorted_languages[0][0].split("-")[0]

        # Liste des langues supportées
        supported_languages = self.translations.keys()

        if best_language not in supported_languages:
            return "fr"

        return best_language
