import requests
import json
import os
import time

class JDMClient:
    def __init__(self, cache_path="data/jdm_cache.json"):
        self.cache_path = cache_path
        self.api_url = "https://jdm-api.demo.lirmm.fr/schema" # URL de base
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=4, ensure_ascii=False)

    def get_info(self, term):
        """Récupère toutes les informations d'un terme (POS, relations, etc.)"""
        if term in self.cache:
            return self.cache[term]

        print(f"--- Requête JDM pour : '{term}' ---")
        # Note: Dans une vraie implémentation, on utilise l'endpoint spécifique
        # Ici on simule l'appel à l'API JDM (adapté à leur structure)
        try:
            # On demande les relations sortantes du terme
            params = {'term': term, 'relations': 'out'}
            # Attention : adapte l'URL selon la doc exacte (ex: /node-light/)
            # Pour l'exercice, on va structurer ce qu'on attend
            response = requests.get(f"https://jdm-api.demo.lirmm.fr/node-light/{term}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.cache[term] = data
                self.save_cache()
                return data
        except Exception as e:
            print(f"Erreur API JDM: {e}")
        
        return None

    def get_pos(self, term):
        """Extrait spécifiquement les natures grammaticales (relation r_pos / type 4)"""
        data = self.get_info(term)
        pos_found = []
        if data and 'relations' in data:
            for rel in data['relations']:
                # Le type 4 dans JDM correspond souvent à r_pos
                if rel['type'] == 4 or rel['type'] == "r_pos":
                    pos_found.append(rel['node_dest'])
        return pos_found