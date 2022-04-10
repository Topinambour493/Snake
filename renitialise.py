import pickle

def sauvegarde(variable,fichier):
    """cette fonction permet de sauvegarder une variable dans un fichier"""
    outfile = open(fichier,'wb')
    pickle.dump(variable,outfile)
    outfile.close()

sauvegarde(0,"meilleur_score")