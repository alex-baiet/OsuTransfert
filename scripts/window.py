import tkinter as tk
from tkinter.constants import NSEW;
import tkinter.ttk as ttk;
from scripts.helper import *
import time

class Window:
    def __init__(self):

        self.ready = False

        self.__dirNbr = 0
        self.__nbrCopy = 0
        self.__buttonPressedRecent = False
        self.__nextMaj = 0
        self.__start = 0
        self.__estimatedTime = ""

        # Création de la fenêtre.
        self.__win = tk.Tk()
        #self.__win.minsize(320, 240)

        # Création des input pour indiquer les dossiers cibles.
        self.__labelTargetDir = tk.Label(self.__win, text="Dossier des niveaux :")
        self.__labelTargetDir.grid(column=0, row=0)

        self.__entryTargetDir = tk.Entry(self.__win, width=50)
        self.__entryTargetDir.grid(column=1, row=0)

        self.__labelDestDir = tk.Label(self.__win, text="Dossier destination :")
        self.__labelDestDir.grid(column=0, row=1)

        self.__entryDestDir = tk.Entry(self.__win, width=50)
        self.__entryDestDir.grid(column=1, row=1)
        
        self.__answerPan = tk.PanedWindow(self.__win)
        self.__answerPan.grid(columnspan=2, row=2)
        
        self.__butSaveDir = tk.Button(self.__answerPan, text="Sauvegarder", command=self.__targets_save)
        self.__butSaveDir.grid(column=0, row=0, padx=5)
        
        self.__butResetDir = tk.Button(self.__answerPan, text="Réinitialiser", command=self.__targets_reset)
        self.__butResetDir.grid(column=1, row=0, padx=5)

        self.__sep = ttk.Separator(self.__win, orient="horizontal")
        self.__sep.grid(column=0, columnspan=2, row=4, sticky=NSEW, pady=10)
        
        self.__textLoad = None
        self.__targets_reset()

        # Création du texte de chargement.
        self.__textLoad= tk.StringVar()
        self.__textLoad.set("En attente d'une action.\n")
        self.__labelLoad = tk.Label(self.__win, textvariable=self.__textLoad)
        self.__labelLoad.grid(column=0, columnspan=2, row=5)

        self.__textCopy = tk.StringVar()
        self.__textCopy.set(str(self.__nbrCopy)+" musiques copiées.")
        self.__labelCopy = tk.Label(self.__win, textvariable=self.__textCopy)
        self.__labelCopy.grid(column=0, columnspan=2, row=6)

        # Initialisation de la barre de chargement.
        self.__bar = ttk.Progressbar(self.__win)
        self.__bar.grid(column=0, columnspan=2, row=7, sticky=NSEW, pady=5, padx=5)

        # Création du bouton principal.
        self.__button = tk.Button(self.__win, text="Commencer", command=self.__set_ready)
        self.__button.grid(column=0, columnspan=2, row=8, sticky=NSEW, pady=5, padx=5)

        self.__win.update()

    def update_dir_count(self):
        # Maj estimation du temps
        if (self.__nextMaj <= time.perf_counter()):
            self.__nextMaj += 1
            res = (int)((time.perf_counter() - self.__start) / self.__dirNbr * (Helper.dirCount - self.__dirNbr))
            self.__estimatedTime = " (Temps estimé :"+ (str(res // 60)+"min" if res>=60 else "") +str(res%60)+"s" +")"

        # Affichage compteur
        self.__dirNbr += 1
        self.__textLoad.set("Traitement en cours..." + self.__estimatedTime + "\ndossier " + str(self.__dirNbr) + " / " + str(Helper.dirCount))
        self.__bar["value"] = self.__dirNbr
        self.__bar["maximum"] = Helper.dirCount
        #self.__win.update_idletasks()
        self.__win.update()

    def update_nbr_copy(self):
        self.__nbrCopy += 1
        self.__textCopy.set(str(self.__nbrCopy) + " musiques copiées.")
        #self.__win.update_idletasks()
        self.__win.update()

    def update(self):
        if (self.__buttonPressedRecent and self.__nextMaj+1 < time.perf_counter()):
            self.__textLoad.set("En attente d'une action.\n")

        self.__win.update()

    def error_not_found(self, directory: str):
        self.__textLoad.set("Le dossier " + directory + " n'existe pas.\nRelancer le programme en indiquant un bon chemin.")
        self.__labelLoad["fg"] = "red"
        self.__win.update()
        time.sleep(5)
        exit()

    def mainloop_final(self):
        self.__textLoad.set("Terminé.\ndossier " + str(self.__dirNbr) + " / " + str(Helper.dirCount))
        self.__button["text"] = "Quitter"
        self.__button["state"] = "normal"
        self.__button["command"] = self.__quit

        self.__win.mainloop()

    def __set_ready(self):
        self.ready = True
        self.__button["text"] = "En cours..."
        self.__button["state"] = "disabled"
        self.__butSaveDir["state"] = "disabled"
        self.__butResetDir["state"] = "disabled"
        self.__textLoad.set("Traitement en cours...\n")

        self.__start = time.perf_counter()
        self.__nextMaj = time.perf_counter() + 1

    def __quit(self):
        self.__win.quit()

    def __targets_save(self):
        Helper.config.set("DIRECTORY", "levels", self.__entryTargetDir.get())
        Helper.config.set("DIRECTORY", "destination", self.__entryDestDir.get())
        self.__pressed_button()

        with open("config.ini", "w") as config_file:
            Helper.config.write(config_file)

        self.__textLoad.set("Sauvegardé !\n")

    def __targets_reset(self):
        self.__entryTargetDir.delete(0, tk.END)
        self.__entryTargetDir.insert(0, Helper.config["DIRECTORY"]["levels"])
        self.__entryDestDir.delete(0, tk.END)
        self.__entryDestDir.insert(0, Helper.config["DIRECTORY"]["destination"])
        self.__pressed_button()

        if (self.__textLoad != None):
            self.__textLoad.set("Réinitialisé !\n")

    def __pressed_button(self):
        self.__buttonPressedRecent = True
        self.__nextMaj = time.perf_counter()
