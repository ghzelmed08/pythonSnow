import requests
from requests.auth import HTTPBasicAuth
import os
from tkinter import messagebox as mg

print(requests.__version__)

class BackupManager:
    def __init__(self, config, folder, output_filename, table_name, query=None, logger=None):
        self.config = config
        self.folder = folder
        self.output_filename = output_filename
        self.table_name = table_name
        self.logger = logger or print  # Utilise `print`  si logger n'est pas passé dans les paramètres de backup manager
        # Si query est fournie, l'ajouter, sinon utiliser seulement le tri par défaut
        if query and query.strip():
            self.base_query = f"{query}^ORDERBYsys_id"
        else:
            self.base_query = "ORDERBYsys_id"
        
        # Les 16 caractères hexadécimaux pour créer 16 fichiers
        self.hex_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    def execute_backup(self):
        print("DEBUT execute_backup")
        
        # Validation des données
        if not self.config:
            mg.showerror("Erreur", "Configuration d'authentification manquante")
            return False
        if not self.folder:
            mg.showerror("Erreur", "Dossier de destination non sélectionné")
            return False
        if not self.output_filename:
            mg.showerror("Erreur", "Nom du fichier de sortie non spécifié")
            return False
        if not self.table_name:
            mg.showerror("Erreur", "Table cible non spécifiée")
            return False

        # Construction de l'URL de base
        base_url = f"https://{self.config['instance']}.service-now.com/"
        self.logger(f"URL de base: {base_url}")
        
        successful_files = 0
        failed_files = 0
        
        # Créer 16 fichiers, un pour chaque caractère hexadécimal
        for i, hex_char in enumerate(self.hex_chars):
            self.logger(f"Traitement fichier {i+1}/16 pour caractère '{hex_char}'")
            
            # Construction de la query pour ce caractère spécifique
            query_for_char = f"{self.base_query}^sys_idSTARTSWITH{hex_char}"
            
            # URL complète pour cette requête - SANS ENCODAGE
            url = f"{base_url}{self.table_name}_list.do?XML&sysparm_query={query_for_char}"
            self.logger(f"url finale debugg {url}")
            
            # Nom du fichier pour une boucle 
            filename = f"{self.output_filename}_{i+1:02d}.xml"  # export_01.xml, export_02.xml, etc.
            output_path = os.path.join(self.folder, filename)
            
            self.logger(f"Téléchargement du fichier {i+1}/16: {filename}")
            self.logger(f"Query finale: {query_for_char}")
            self.logger(f"URL complète: {url}")
            
            # Envoi de la requête GET avec python basé sur les exemples servicenow
            response = requests.get(
                url,
                auth=HTTPBasicAuth(self.config['user'], self.config['password']),
                stream=True,
                timeout=360  # Timeout de 360 secondes
            )
            
            self.logger(f"Réponse reçue: Status  {response.status_code}")
            
            # Vérification de la réponse (non 200 c une erreur et pas possible 201 car c un get)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # Filtrer les chunks vides
                            f.write(chunk)
                
                # Vérifier que le fichier a été créé et n'est pas vide
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    successful_files += 1
                    self.logger(f"OK Fichier {filename} créé avec succès")
                else:
                    failed_files += 1
                    self.logger(f"X Fichier {filename} vide ou non créé")
                    
            else:
                failed_files += 1
                self.logger(f"X Échec pour {filename} (Code {response.status_code}): {response.text[:200]}")
                
        self.logger(f"Résumé: {successful_files} réussis, {failed_files} échoués")
                
        # Affichage du résultat final avec nombre reel de fichier crée(debugger la creation)
        if successful_files > 0:
            message = f"Export terminé!\n{successful_files} fichiers créés avec succès"
            if failed_files > 0:
                message += f"\n{failed_files} fichiers ont échoué"
            message += f"\nFichiers sauvegardés dans:\n{self.folder}"
            mg.showinfo("Résultat", message)
            self.logger(f"\n Résultat {message}")
            return True
        else:
            mg.showerror("Erreur", f"Aucun fichier n'a pu être créé.\n{failed_files} tentatives ont échoué.")
            self.logger(f"Erreur. Aucun fichier n'a pu être créé.\n{failed_files} tentatives ont échoué.")
            return False