import requests
import json
import os

class JDMClient:
    def __init__(self, cache_file='data/cache_jdm.json'):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def get_relations(self, term_a, relation_type):
        # Clé unique pour le cache
        key = f"{term_a}_{relation_type}"
        
        if key in self.cache:
            return self.cache[key]
        
        # Appel API (url à adapter selon la doc JDM)
        url = f"https://jdm-api.demo.lirmm.fr/v1/relations?node_name={term_a}&rel_name={relation_type}"
        try:
            response = requests.get(url).json()
            # Simplifier la réponse pour ne garder que l'essentiel
            result = response.get('relations', [])
            self.cache[key] = result
            self.save_cache() # Sauvegarde immédiate ou périodique
            return result
        except:
            return []