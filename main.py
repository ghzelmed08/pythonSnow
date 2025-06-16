import tkinter as tk
import json
import requests

from requests.auth import HTTPBasicAuth
import os
from urllib.parse import quote
from tkinter import ttk
from tkinter import filedialog as fl
from tkinter import messagebox as mg 
from config_auth import CONFIG_AUTH as cf
from backup_manager import BackupManager  
from xml_combiner import XMLCombiner

root = tk.Tk()
folder = ""  # CORRECTION: Utiliser une chaîne simple au lieu de StringVar
config = {}
query_parm = tk.StringVar(root)

##function to return pathname
def getFolder():
    global folder
    path_name = fl.askdirectory(title="Choisissez un dossier pour le fichier de sauvegarde")
    if path_name:
        print(f"Dossier choisi : {path_name}")
        folder = path_name
        # Optionnel: afficher le dossier sélectionné dans l'interface
        lbl_folder_selected.config(text=f"Dossier: {os.path.basename(path_name)}")
        return folder

###function to call config window
def call_config():
    config_window = cf(root, setConfig)
    config_window.focus()  # Donner le focus à la nouvelle fenêtre

###function for callBack
def setConfig(jsonCfg):
    global config
    config = jsonCfg
    print(f"Configuration reçue: {config}")

##function for btn start
def beginBackUp():
    print("DEBUT beginBackUp")
    
    # Validation des champs requis
    if not config:
        mg.showerror("Erreur", "Veuillez d'abord configurer l'authentification")
        return
    
    if not folder:
        mg.showerror("Erreur", "Veuillez sélectionner un dossier de destination")
        return
    
    table = table_var.get().strip()
    if not table:
        mg.showerror("Erreur", "Veuillez spécifier le nom de la table")
        return
    
    output_file = ouput_file_name.get().strip()
    if not output_file:
        mg.showerror("Erreur", "Veuillez spécifier le nom du fichier de sortie")
        return

    
    query = query_parm.get().strip()  # Peut être vide si pas de specic
    
    # Lancement de la sauvegarde
    print("Début de la sauvegarde:")
    print(f"- Table: {table}")
    print(f"- Dossier: {folder}")
    print(f"- Fichier: {output_file}")
    print(f"- Query: {query if query else 'Aucune query spécifique'}")
    
    result=  backup_cli(config["instance"], config["user"], config["password"], table, output_file, query)
    if  (not  result) :
        mg.showerror("Erreur", "Problème de la creation des fichiers d'exports. ")
        return
    #Sinon combiner les fichiers
    combiner = XMLCombiner(folder,table,output_file) 
    success = combiner.combine()
    
    if success:
         mg.showinfo("Succès", f"Sauvegarde terminée avec succès!\nFichier généré: {output_file}.xml")
         table = ""
    else:
         mg.showerror("Erreur", "Problème lors de la combinaison des fichiers XML.")
         

def backup_cli(instance, user, password, table, output_file, query=None):
    """Fonction de sauvegarde"""
    print("DEBUT backup_cli")
    
    manager = BackupManager(
        config={'instance': instance, 'user': user, 'password': password},
        folder=folder,  # CORRECTION: Utiliser la variable globale folder
        output_filename=output_file,
        table_name=table,
        query=query
    )
    
    print("Appel de execute_backup")
    result = manager.execute_backup()
    print(f"Résultat: {result}")
    return result

###################
# INTERFACE GRAPHIQUE
###################

##Titre de la fenêtre
root.title("Backup Data ServiceNow")

###Déclaration de variables
#Variable pour le nom de la table
table_var = tk.StringVar(root)
#variable pour le nom du fichier output
ouput_file_name = tk.StringVar(root)
#variable pour nom de l'instance
url_instance = tk.StringVar()
#Définir la taille de la fenêtre
root.geometry('800x600+400+50')
username = tk.StringVar()

#Configurer le layout du conteneur principal
root.columnconfigure(0, weight=1)

##############################################
# FRAMES
##############################################
#Configurer les frames
frame_1 = ttk.Frame(root, padding=(20,20,20,10))
frame_1.grid(column=0, row=0, sticky="EW")

#frame_11 pour la query
frame_11 = ttk.Frame(root, padding=(15,10,15,10))
frame_11.grid(column=0, row=1, sticky="EW")

#frame_2 pour le dossier
frame_2 = ttk.Frame(root, padding=(15,10,15,10))
frame_2.grid(column=0, row=2, sticky="EW")

#frame_3 pour le nom du fichier
frame_3 = ttk.Frame(root, padding=(15,10,15,10))
frame_3.grid(column=0, row=3, sticky="EW")

#frame_4 pour le bouton de démarrage
frame_4 = ttk.Frame(root, padding=(15,20,15,20))
frame_4.grid(column=0, row=4, sticky="EW")

###########################################################################################
# CONTENU DES FRAMES
###########################################################################################

#Adding controls to frame_1
frame_1.columnconfigure(0, weight=1)
frame_1.columnconfigure(1, weight=1)
frame_1.columnconfigure(2, weight=2)

btn_configure = ttk.Button(frame_1, text="Configurer l'authentification", padding=(10,10,10,10), command=call_config)
btn_configure.grid(row=0, column=0, sticky="W", padx=(0,10))

lbl_table = ttk.Label(frame_1, text="Nom de la table:")
lbl_table.grid(row=0, column=1, sticky="E", padx=(0,5))

txt_table = ttk.Entry(frame_1, width=30, textvariable=table_var)
txt_table.grid(row=0, column=2, sticky="W")

#Adding controls to frame_11 (Query)
frame_11.columnconfigure(0, weight=1)
frame_11.columnconfigure(1, weight=2)

lbl_query = ttk.Label(frame_11, text="Query personnalisée (optionnel):")
lbl_query.grid(column=0, row=0, sticky="E", padx=(0,5))

txt_query = ttk.Entry(frame_11, textvariable=query_parm, width=50)
txt_query.grid(column=1, row=0, sticky="W")

#Adding controls to frame_2 (Dossier)
frame_2.columnconfigure(0, weight=1)
frame_2.columnconfigure(1, weight=1)
frame_2.columnconfigure(2, weight=1)

lbl_output_fd = ttk.Label(frame_2, text="Dossier de destination:")
lbl_output_fd.grid(column=0, row=0, sticky="E", padx=(0,5))

btn_fd = ttk.Button(frame_2, text="Parcourir...", command=getFolder)
btn_fd.grid(column=1, row=0, padx=(5,10))

lbl_folder_selected = ttk.Label(frame_2, text="Aucun dossier sélectionné", foreground="gray")
lbl_folder_selected.grid(column=2, row=0, sticky="W")

#Adding controls to frame_3 (Nom du fichier)
frame_3.columnconfigure(0, weight=1)
frame_3.columnconfigure(1, weight=2)

lbl_file_name = ttk.Label(frame_3, text="Nom du fichier de base:")
lbl_file_name.grid(column=0, row=0, sticky="E", padx=(0,5))

txt_file_name = ttk.Entry(frame_3, textvariable=ouput_file_name, width=30)
txt_file_name.grid(column=1, row=0, sticky="W")

# Note explicative
lbl_note = ttk.Label(frame_3, text="Note: 16 fichiers seront créés (nom_01.xml à nom_16.xml)", 
                     foreground="blue", font=("TkDefaultFont", 8))
lbl_note.grid(column=1, row=1, sticky="W", pady=(5,0))

#Adding controls to frame_4 (Bouton de démarrage)
frame_4.columnconfigure(0, weight=1)

btn_start = ttk.Button(frame_4, text="Débuter la sauvegarde", padding=(20,10,20,10), command=beginBackUp)
btn_start.grid(column=0, row=0)

root.mainloop()