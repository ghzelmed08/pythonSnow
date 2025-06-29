import tkinter as tk
import json
import requests

from requests.auth import HTTPBasicAuth
import os
from urllib.parse import quote
from tkinter import ttk
from tkinter import filedialog as fl
from tkinter import messagebox as mg 
from tkinter.scrolledtext import ScrolledText  # Pour la zone de log avec scroll
from config_auth import CONFIG_AUTH as cf
from backup_manager import BackupManager  
from xml_combiner import XMLCombiner

root = tk.Tk()
folder = ""  # CORRECTION: Utiliser une chaîne simple au lieu de StringVar
config = {}
query_parm = tk.StringVar(root)

## fonction pour afficher les logs dans la console ET dans la zone graphique
def log(msg):
    print(msg)  # Affiche aussi dans la console
    log_output.configure(state="normal")
    log_output.insert(tk.END, msg + "\n")
    log_output.see(tk.END)  # Scroll automatique vers le bas
    log_output.configure(state="disabled")

## function to return pathname
def getFolder():
    global folder
    path_name = fl.askdirectory(title="Choisissez un dossier pour le fichier de sauvegarde")
    if path_name:
        log(f"Dossier choisi : {path_name}")
        folder = path_name
        # Optionnel: afficher le dossier sélectionné dans l'interface
        lbl_folder_selected.config(text=f"Dossier: {os.path.basename(path_name)}")
        return folder

### function to call config window
def call_config():
    config_window = cf(root, setConfig)
    config_window.focus()  # Donner le focus à la nouvelle fenêtre

### function for callBack
def setConfig(jsonCfg):
    global config
    config = jsonCfg
    log(f"Configuration reçue: {config}")

## function for btn start
def beginBackUp():
    log("DEBUT beginBackUp")
    
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
    log("Début de la sauvegarde:")
    log(f"- Table: {table}")
    log(f"- Dossier: {folder}")
    log(f"- Fichier: {output_file}")
    log(f"- Query: {query if query else 'Aucune query spécifique'}")
    
    result = backup_cli(config["instance"], config["user"], config["password"], table, output_file, query)
    if not result:
        mg.showerror("Erreur", "Problème de la création des fichiers d'exports.")
        log("❌ Échec de la création des fichiers d’export.")
        return

    # Sinon combiner les fichiers
    combiner = XMLCombiner(folder, table, output_file, logger=log) 
    success = combiner.combine()
    
    if success:
        mg.showinfo("Succès", f"Sauvegarde terminée avec succès!\nFichier généré: {output_file}.xml")
        log("✅ Sauvegarde terminée avec succès.")
    else:
        mg.showerror("Erreur", "Problème lors de la combinaison des fichiers XML.")
        log("❌ Erreur lors de la combinaison des fichiers XML.")

## Fonction de backup
def backup_cli(instance, user, password, table, output_file, query=None):
    """Fonction de sauvegarde"""
    log("DEBUT backup_cli")
    
    manager = BackupManager(
        config={'instance': instance, 'user': user, 'password': password},
        folder=folder,  # Utiliser la variable globale folder
        output_filename=output_file,
        table_name=table,
        query=query,
        logger=log
    )
    
    log("Appel de execute_backup")
    result = manager.execute_backup()
    log(f"Résultat: {result}")
    return result

###################
# INTERFACE GRAPHIQUE
###################

## Titre de la fenêtre
root.title("Backup Data ServiceNow")

### Déclaration de variables
table_var = tk.StringVar(root)              # Nom de la table
ouput_file_name = tk.StringVar(root)        # Nom du fichier output
url_instance = tk.StringVar()
username = tk.StringVar()
root.geometry('800x600+400+50')             # Taille de la fenêtre

# Configurer le layout du conteneur principal
root.columnconfigure(0, weight=1)

##############################################
# FRAMES
##############################################

# frame_1 : config + nom table
frame_1 = ttk.Frame(root, padding=(20, 20, 20, 10))
frame_1.grid(column=0, row=0, sticky="EW")

# frame_11 : query
frame_11 = ttk.Frame(root, padding=(15, 10, 15, 10))
frame_11.grid(column=0, row=1, sticky="EW")

# frame_2 : dossier de destination
frame_2 = ttk.Frame(root, padding=(15, 10, 15, 10))
frame_2.grid(column=0, row=2, sticky="EW")

# frame_3 : nom de fichier
frame_3 = ttk.Frame(root, padding=(15, 10, 15, 10))
frame_3.grid(column=0, row=3, sticky="EW")

# frame_4 : bouton lancement
frame_4 = ttk.Frame(root, padding=(15, 20, 15, 20))
frame_4.grid(column=0, row=4, sticky="EW")

# frame_5 : zone de log
frame_5 = ttk.Frame(root, padding=(15, 10, 15, 10))
frame_5.grid(column=0, row=5, sticky="NSEW")
root.rowconfigure(5, weight=1)

###########################################################################################
# CONTENU DES FRAMES
###########################################################################################

# frame_1
frame_1.columnconfigure(0, weight=1)
frame_1.columnconfigure(1, weight=1)
frame_1.columnconfigure(2, weight=2)

btn_configure = ttk.Button(frame_1, text="Configurer l'authentification", padding=(10,10,10,10), command=call_config)
btn_configure.grid(row=0, column=0, sticky="W", padx=(0,10))

lbl_table = ttk.Label(frame_1, text="Nom de la table:")
lbl_table.grid(row=0, column=1, sticky="E", padx=(0,5))

txt_table = ttk.Entry(frame_1, width=30, textvariable=table_var)
txt_table.grid(row=0, column=2, sticky="W")

# frame_11 (query personnalisée)
frame_11.columnconfigure(0, weight=1)
frame_11.columnconfigure(1, weight=2)

lbl_query = ttk.Label(frame_11, text="Query personnalisée (optionnel):")
lbl_query.grid(column=0, row=0, sticky="E", padx=(0,5))

txt_query = ttk.Entry(frame_11, textvariable=query_parm, width=50)
txt_query.grid(column=1, row=0, sticky="W")

# frame_2 (dossier)
frame_2.columnconfigure(0, weight=1)
frame_2.columnconfigure(1, weight=1)
frame_2.columnconfigure(2, weight=1)

lbl_output_fd = ttk.Label(frame_2, text="Dossier de destination:")
lbl_output_fd.grid(column=0, row=0, sticky="E", padx=(0,5))

btn_fd = ttk.Button(frame_2, text="Parcourir...", command=getFolder)
btn_fd.grid(column=1, row=0, padx=(5,10))

lbl_folder_selected = ttk.Label(frame_2, text="Aucun dossier sélectionné", foreground="gray")
lbl_folder_selected.grid(column=2, row=0, sticky="W")

# frame_3 (nom fichier)
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

# frame_4 (bouton de démarrage)
frame_4.columnconfigure(0, weight=1)

btn_start = ttk.Button(frame_4, text="Débuter la sauvegarde", padding=(20,10,20,10), command=beginBackUp)
btn_start.grid(column=0, row=0)

# frame_5 (zone de log avec scroll)
log_output = ScrolledText(frame_5, height=12, wrap="word", state="disabled", font=("Courier", 9))
log_output.pack(fill="both", expand=True)

# Lancer l'application
root.mainloop()
