import os
import shutil
import configparser
import tkinter as tk
from scripts.window import *
from scripts.helper import *

debug=False #quand True, désactive l'écriture des noms des musiques copiées dans le fichier "music.txt".

"""Prepare le nom de la musique en fonction du nom du dossier."""
def prepareMusicName(currentName) :
    n = False
    result = ""
    for l in range (0,len(currentName)) :
        # On rajoute toutes les caracteres à partir du 1er caractere non numerique.
        if n or currentName[l] not in ["0","1","2","3","4","5","6","7","8","9"," "]:
            n = True
            result = result + currentName[l]

    return result


if __name__ == "__main__":
    nbrCopy=0
    Helper.config = configparser.ConfigParser()
    Helper.config.read("config.ini")
    mus = "" #Nom donné à la musique
    window = Window()

    while (not window.ready):
        # On attend. (-o-)zzZ
        window.update()

    #Test pour vérifier que les dossiers cibles existent
    songs = Helper.config["DIRECTORY"]["levels"] #Chemin des musiques osu!.
    target = Helper.config["DIRECTORY"]["destination"] #Chemin où copier les musiques.
    if not os.access(songs, os.F_OK):
        window.error_not_found(songs)
    if not os.access(target, os.F_OK):
        window.error_not_found(target)

    print("\n##### Début de la copie des musiques #####\n")
    directories = os.listdir(songs) #liste des dossiers de niveau osu!.
    Helper.dirCount = len(directories)
    print("dossier de musiques :", songs)

    for dir in directories :
        print("dossier actuel :", dir)
        window.update_dir_count()

        mus = prepareMusicName(dir)

        with open("music.txt", "a+") as bruh:
            # Ne fait que créer le music.txt si il n'existe pas.
            pass
        lmus = open("music.txt", "r")
        if mus not in lmus.read() :
            lmus.close()
            fichiers = os.listdir(songs+"/"+dir)
            nbr_mp3=0
            num_mp3=1
            for fich in fichiers :
                if "mp3" in fich :nbr_mp3+=1
            for fich in fichiers :
                if "mp3" in fich :
                    shutil.copy(songs+"/"+dir+"/"+fich, target+"/"+mus+(" "+str(num_mp3))*(nbr_mp3>1)+".mp3")
                    num_mp3+=1
                    if not debug:
                        with open("music.txt","a") as lmus:
                            lmus.write(mus+"\n")
    
        else:lmus.close()

        window.update_nbr_copy()

    lmus.close()
    print(str(nbrCopy)+" musiques ont été copiées dans le dossier "+target)

    print("\n##### Copie des musiques terminé avec succès #####\n")
    window.mainloop_final()
