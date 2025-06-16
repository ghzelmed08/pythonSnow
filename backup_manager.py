import requests

from requests.auth import HTTPBasicAuth
import os
from urllib.parse import quote
from tkinter import messagebox as mg
print(requests.__version__)
class BackupManager:
    def __init__(self, config, folder, output_filename, table_name, query=None):
        self.config = config
        self.folder = folder
        self.output_filename = output_filename + ".xml"
        self.table_name = table_name
        self.query = (query +"^ORDERBYsys_id ^sys_idSTARTSWITH{0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f}")  or "ORDERBYsys_id ^sys_idSTARTSWITH{0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f}"

    def execute_backup(self):
        # si erreur de donnnée on reçois  un message box d erreur
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

        # Construction de l'URL avec servicenow comme base
        base_url = f"https://{self.config['instance']}.service-now.com/"
        encoded_query = quote(self.query) ##pour encoder en url mais je supprime si ça fonctionne pas comme le cas manuellement parfois
        #encoded_query = self.query
        url = f"{base_url}{self.table_name}_list.do?XML&sysparm_query={encoded_query}"

        # Chemin du output file
        #A verifier avec un print
        output_path = os.path.join(self.folder, self.output_filename)

        try:
            # Envoi de la requête get 
            response = requests.get(
                url,
                auth=HTTPBasicAuth(self.config['user'], self.config['password']),
                stream=True
            )

            # Vérification de la réponse
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                mg.showinfo("Succès", f"Export terminé avec succès!\n 16 Fichiers sauvegardés à:\n{self.folder}")
                return True
            else:
                mg.showerror("Erreur", f"Échec de l'export (Code {response.status_code})\n{response.text}") ####a aajouter un quote si erreur de  escape
                return False

        except Exception as e:
            mg.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
            return False