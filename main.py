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

root = tk.Tk()
folder = tk.StringVar(root)
config = {}
query_parm =tk.StringVar(root)
##function to return pathname
def getFolder():
    global folder
    path_name = fl.askdirectory(title ="choisissez un dossier pour le ficher de sauvegarde")
    if(path_name):
        print(f"dossier choisi : {path_name}")
        folder = path_name
        return
###function to call  config window
def call_config():
    config  =cf(root,setConfig)
    config.focus()###Donner le focus à la nouvelle fenetre


###function for callBack
def setConfig(jsonCfg):
    global config
    config = jsonCfg
    print(f"ceci s'affiche veut dire on a recu la bonne configuration {config}")


##function for btn start

def beginBackUp():
    table = table_var.get()
    user = config["user"]
    password = config["password"]
    output_file = ouput_file_name.get()
    query = query_parm.get()
    instance = config["instance"]
    backup_cli(instance, user, password, table, output_file, query)



def backup_cli(instance, user, password, table, output_file, query=None):
    """Exemple d'utilisation en ligne de commande"""
    manager = BackupManager(
        config={'instance': instance, 'user': user, 'password': password},
        folder='.',  # Dossier courant
        output_filename=output_file,
        table_name=table,
        query=query
    )
    return manager.execute_backup()


###################
###################
###FUNCTION ----END
####################
####################


######GRAPHIQUE and FRAMES#####
#########################################################################################################
##Titre de la fenêtre
root.title("Backup data ")
###Declaration de variables
#Variable pour le nom de la table
table_var = tk.StringVar(root)
#variable pour le nom du fichier output
ouput_file_name = tk.StringVar(root)
#variable pour nom de l'instance
url_instance = tk.StringVar()
#Defie window size
root.geometry('800x500+400+50')
username  = tk.StringVar()
#Configurer le layout du conteneur principal
root.columnconfigure(0,weight=1)
##############################################
#################FRAMES#######################
##############################################
#Configurer les  quatres frames
frame_1 = ttk.Frame(root, padding=(20,50,20,0))
frame_1.grid(column=0,row=0,sticky="EW")
#frame_11 pour ajouter la query oublié 

frame_11 = ttk.Frame(root,padding=(15,10, 15,5))
frame_11.grid(column=0,row=1,sticky="EW")
frame_11.columnconfigure(0,weight=1)
#frame_2 pour les label
frame_2 = ttk.Frame(root,padding=(15,10, 15,5))
frame_2.grid(column=0,row=2,sticky="EW")
frame_2.columnconfigure(0,weight=1)


#frame_3 pour les zones de texte
frame_3 = ttk.Frame(root,padding=(15,10,15,5))
frame_3.grid(column=0,row=3,sticky="EW")
######
#frame_4 pour le boution demarrer sauvegarde
frame_4 = ttk.Frame(root,padding=(15,10,15,5))
frame_4.grid(column=0,row=4,sticky="EW",columnspan=3)
###########################################################################################
##############################################################################################

#Adding controls to frame_1
####
frame_1.columnconfigure(0,weight=2)
frame_1.columnconfigure(1,weight=1)
frame_1.columnconfigure(2,weight=1)
btn_configure = ttk.Button(frame_1,text="Configure Authentification",padding=(10,15,5,15),command=call_config)
btn_configure.grid(row=0,column=0,sticky="W")
lbl_table = ttk.Label(frame_1,foreground="blue",background="grey",text="Selectionnez la table cible: ")
lbl_table.grid(row=0,column=1)
#adding text zone for table
txt_table = ttk.Entry(frame_1,foreground="black",width=40,background="green",textvariable=table_var)
txt_table.grid(row=0,column=2)
###END of frame_1###

#####
#Adding controls to frame_2
#####
frame_2.columnconfigure(0,weight=2)
frame_2.columnconfigure(1,weight=1)
frame_2.columnconfigure(2,weight=1)
#label pour le bouton output folder
lbl_output_fd = ttk.Label(frame_2,foreground="blue",background="grey", text="Selectionner le dossier d'extraction ")
lbl_output_fd.grid(column=1,row=0)
#Adding btn to get folder destination

btn_fd =ttk.Button(frame_2,text="Dossier",width=20,command=getFolder)
btn_fd.grid(column=2,row=0)

####
##Adding controls to frame 3 
### textzone and button
frame_3.columnconfigure(0,weight=2)
frame_3.columnconfigure(1,weight=1)
frame_3.columnconfigure(2,weight=1)
#label pour le nom du fichier
lbl_file_name = ttk.Label(frame_3,foreground="blue",background="grey",text="Choisir le nom du fihcier xml de sortie",)
lbl_file_name.grid(column=1,row=0,pady=20)
#Adding text zone for output filename
txt_file_name = ttk.Entry(frame_3,textvariable=ouput_file_name,background="green",foreground="blue",width=40)
txt_file_name.grid(column=2,row=0, pady=50,sticky="E")

###End of frame_3

####
##Adding controls to frame  
frame_4.columnconfigure(0,weight=2)
frame_4.columnconfigure(1,weight=1)
frame_3.columnconfigure(2,weight=1)
btn_start = ttk.Button(frame_4, text="Débuter la sauvegarde" ,padding=(15,10,15,10), width=25,command=beginBackUp)
btn_start.grid(column=0,row=0, sticky="S",pady=30)

###################
##############END of FRame_4################
##################

####
##Adding controls to frame_11
### textzone and button
frame_11.columnconfigure(0,weight=2)
frame_11.columnconfigure(1,weight=1)
frame_11.columnconfigure(2,weight=1)
#label pour le nom du fichier
lbl_query = ttk.Label(frame_11,foreground="blue",background="grey",text="saisir la query  sans ajouter sysparm_query=")
lbl_query.grid(column=1,row=0,pady=29)
#Adding text zone for output filename
txt_query = ttk.Entry(frame_11,textvariable=query_parm,background="green",foreground="blue",width=40)
txt_query.grid(column=2,row=0)

###End of frame_3

root.mainloop()
