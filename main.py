import tkinter as tk
import json
from tkinter import ttk
from tkinter import filedialog as fl
from tkinter import messagebox as mg 
from config_auth import CONFIG_AUTH 
root = tk.Tk()
folder = ""
config = {}

print("Version chargée :", CONFIG_AUTH.__name__)
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
    config  =CONFIG_AUTH(callback=setconfig)
    config.focus()###Donner le focus à la nouvelle fenetre


###function for callBack
def setconfig(jsonCfg):
    global config
    config = jsonCfg
    ######jsConfig  = json.loads(config) cause une erreur
    print(f"ceci s'affiche veut dire on a recu la bonne configuration {jsonCfg}")
   ## print(json.dumps(config,indent=3))
   



    
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
root.geometry('600x500+400+50')
username  = tk.StringVar()
#Configurer le layout du conteneur principal
root.columnconfigure(0,weight=1)

#Configurer les  quatres frames
frame_1 = ttk.Frame(root, padding=(20,50,20,0))
frame_1.grid(column=0,row=0,sticky="EW")

#frame_2 pour les label
frame_2 = ttk.Frame(root,padding=(15,10, 15,5))
frame_2.grid(column=0,row=1,sticky="EW")
frame_2.columnconfigure(0,weight=1)


#frame_3 pour les zones de texte
frame_3 = ttk.Frame(root,padding=(15,10,15,5))
frame_3.grid(column=0,row=2,sticky="EW")
######
#frame_4 pour le boution demarrer sauvegarde
frame_4 = ttk.Frame(root,padding=(15,10,15,5))
frame_4.grid(column=0,row=3,sticky="EW",columnspan=3)
######

#Adding controls to frame_1
####
frame_1.columnconfigure(0,weight=2)
frame_1.columnconfigure(1,weight=1)
frame_1.columnconfigure(2,weight=1)
btn_configure = ttk.Button(frame_1,text="Configure Authentification",padding=(10,15,5,15),command=call_config)
btn_configure.grid(row=0,column=0,sticky="WE")
lbl_table = ttk.Label(frame_1,foreground="blue",background="green",text="Selectionnez la table cible: ")
lbl_table.grid(row=0,column=1)
#adding text zone for table
txt_table = ttk.Entry(frame_1,foreground="black",width=20,background="green",textvariable=table_var)
txt_table.grid(row=0,column=2)
###END of frame_1###

#####
#Adding controls to frame_2
#####
frame_2.columnconfigure(0,weight=2)
frame_2.columnconfigure(1,weight=1)
frame_2.columnconfigure(2,weight=1)
#label pour le bouton output folder
lbl_output_fd = ttk.Label(frame_2,foreground="blue",background="green", text="Selectionner le dossier d'extraction ")
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
lbl_file_name = ttk.Label(frame_3,foreground="blue",background="green",text="Choisir le nom du fihcier xml de sortie")
lbl_file_name.grid(column=1,row=2)
#Adding text zone for output filename
txt_file_name = ttk.Entry(frame_3,textvariable=ouput_file_name,background="green",foreground="blue",width=20)
txt_file_name.grid(column=2,row=0)

###End of frame_3

####
##Adding controls to frame  
frame_4.columnconfigure(0,weight=2)
frame_4.columnconfigure(1,weight=1)
frame_3.columnconfigure(2,weight=1)
btn_start = ttk.Button(frame_4, text="Débuter la sauvegarde" ,padding=(15,10,15,10), width=25)
btn_start.grid(column=0,row=0, sticky="EW")

###################
##############END of FRame_4################
##################


root.mainloop()
