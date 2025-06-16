import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fl

class CONFIG_AUTH(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.config(
            background="white",          # Fond blanc
            padx=20,             # Marge horizontale 20 pixel
            pady=25,             # Marge verticale 25 pixel
            relief="groove"     # Bordure 
        )
        self.geometry("500x350+400+50") #garder la même config de positionnement qaue la fenêtre parent
        self.grab_set() #mettre en premier plan et interdire les actions sur root
        self.instance_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.cgf ={}
        self.callback = callback
        self.configure()
        
    def configure(self):
        #configure actual window
        self.columnconfigure(0, weight=1)
        
        ##adding control and frames
        ##frame_01
        frame_01 = ttk.Frame(self, padding=(15,10,15,10))
        frame_01.grid(column=0, row=0, sticky="EW")
        frame_01.columnconfigure(0, weight=2)
        frame_01.columnconfigure(1, weight=1)
        #Adding label for instance
        label_instance = ttk.Label(frame_01, background="grey", padding=(10,10,15,10), width=30, text="lien de l'instance")
        label_instance.grid(column=0, row=0, sticky="E")
        #Adding Entry for instance
        input_instance = ttk.Entry(frame_01, background="white", width=40, textvariable=self.instance_var)
        input_instance.grid(column=1, row=0, sticky="W")

        #######
        ####Frame_02
        #######
        frame_02 = ttk.Frame(self, padding=(15,10,15,10))
        frame_02.grid(column=0, row=1, sticky="EW")
        frame_02.columnconfigure(0, weight=2)
        frame_02.columnconfigure(1, weight=1)
        #Adding label for instuserance
        label_user = ttk.Label(frame_02, background="grey", padding=(10,10,15,10), width=30, text="Nomde l'utilisateur")
        label_user.grid(column=0, row=0, sticky="E")
        #Adding Entry for user
        input_user = ttk.Entry(frame_02, background="white", width=40, textvariable=self.user_var)
        input_user.grid(column=1, row=0, sticky="W")
        ####END FRAME 02 ####
        ########################

        ######Frame03#####
        #################
        #######
        frame_03 = ttk.Frame(self, padding=(15,10,15,10))
        frame_03.grid(column=0, row=2, sticky="EW")
        frame_03.columnconfigure(0, weight=2)
        frame_03.columnconfigure(1, weight=1)
        #Adding label for password
        label_password = ttk.Label(frame_03, background="grey", padding=(10,10,15,10), width=30, text="Mot de passe")
        label_password.grid(column=0, row=0, sticky="E")
        #Adding Entry for password
        input_password = ttk.Entry(frame_03, background="white", width=40, textvariable=self.password_var, show="*")
        input_password.grid(column=1, row=0, sticky="W")
        ####END FRAME 03 ####
        ########################

        ######Frame04#####
        #################
        #######
        frame_04 = ttk.Frame(self, padding=(15,10,15,10))
        frame_04.grid(column=0, row=3, sticky="EW")
        frame_04.columnconfigure(0, weight=1)
       
        #Adding button Sauvegarder 
        btn_save = ttk.Button(frame_04, text="Sauvegarder", padding=(20,15,20,10), width=20, command=self.sauvegarder)
        btn_save.grid(column=0, row=0, padx=30, pady=20, sticky="W")
        
        #Adding button Annuler
        btn_cancel = ttk.Button(frame_04, text="Annuler", padding=(20,15,20,10), width=20, command=self.annuler)
        btn_cancel.grid(column=1, row=0, padx=30, pady=20, sticky="E")
        ####END FRAME 04 ####
        ########################

    ######function command to save json obj
    def sauvegarder(self):
        print("sauvegarde effectué")
        print("Instance:", self.instance_var.get())
        print("Utilisateur:", self.user_var.get())
        ### Not secure  : print("Mot de passe:", self.password_var.get())
        self.cgf={
            "user" : self.instance_var.get(),
            "password" : self.password_var.get(),
            "instance" :self.instance_var.get()
        }

        return
    
    ########function to cancel and close the actual window
    def annuler(self):
        self.destroy()