def sauvegarde(variable,fichier):
    """cette fonction permet de sauvegarder une variable dans un fichier"""
    outfile = open(fichier,'wb')
    pickle.dump(variable,outfile)
    outfile.close()

def recupere(fichier):
    """cette fonction renvoie une variable venant d'un fichier"""
    infile = open(fichier,'rb')
    variable = pickle.load(infile)
    infile.close()
    return variable

def carre_plein(centre,t,couleur):
    while t>-1:
        x1,y1=(centre[0]+t,centre[1]-t)
        x2,y2=(centre[0]+t,centre[1]+t)
        x3,y3=(centre[0]-t,centre[1]+t)
        x4,y4=(centre[0]-t,centre[1]-t)
        pygame.draw.line(screen,couleur,(x1,y1),(x2,y2),1)
        pygame.draw.line(screen,couleur,(x2,y2),(x3,y3),1)
        pygame.draw.line(screen,couleur,(x3,y3),(x4,y4),1)
        pygame.draw.line(screen,couleur,(x4,y4),(x1,y1),1)
        t=t-1

def carre(centre,t,couleur):
    x1,y1=(centre[0]+t,centre[1]-t)
    x2,y2=(centre[0]+t,centre[1]+t)
    x3,y3=(centre[0]-t,centre[1]+t)
    x4,y4=(centre[0]-t,centre[1]-t)
    pygame.draw.line(screen,couleur,(x1,y1),(x2,y2),1)
    pygame.draw.line(screen,couleur,(x2,y2),(x3,y3),1)
    pygame.draw.line(screen,couleur,(x3,y3),(x4,y4),1)
    pygame.draw.line(screen,couleur,(x4,y4),(x1,y1),1)


def avance_snake():
    global pomme,score,direction_snake
    direction_snake=direction_provisoire
    tete=snake[0]
    if direction_snake=="gauche":
        nv_tete=[tete[0]-1,tete[1]]
    elif direction_snake=="droite":
        nv_tete=[tete[0]+1,tete[1]]
    elif direction_snake=="haut":
        nv_tete=[tete[0],tete[1]-1]
    else:
        nv_tete=[tete[0],tete[1]+1]
    snake.insert(0,nv_tete)
    if nv_tete==pomme:
        score+=1
        pomme=nv_pomme()
        affiche_snake(vert)
    else:
        del snake[-1]
        tete=snake[0]
        if 0<=tete[0]<=taille_carré_jeu-1 and 0<=tete[1]<=taille_carré_jeu-1 and tete not in snake[1:]:
            affiche_snake(blanc)
        else:
            affiche_snake(rouge)
            if score>meilleur_score:
                sauvegarde(score,"meilleur_score")
            pygame.display.flip()
            return True
    pygame.display.flip()
    return False

def nv_pomme():
    while True:
        nouv_pomme=[random.randrange(taille_carré_jeu),random.randrange(taille_carré_jeu)]
        if nouv_pomme not in snake:
            return nouv_pomme


def affiche_pomme(couleur_pomme):
    carre_plein((bord+1+taille_morceau//2+pomme[0]*taille_morceau,cartouche_haut+bord+1+taille_morceau//2+pomme[1]*taille_morceau),taille_morceau//2,couleur_pomme)

def affiche_snake(couleur_snake):
    for morceau in snake:
        carre_plein((bord+1+taille_morceau//2+morceau[0]*taille_morceau,cartouche_haut+bord+1+taille_morceau//2+morceau[1]*taille_morceau),taille_morceau//2,couleur_snake)

def change_direction_snake():
    global direction_provisoire
    pygame.key.set_repeat(220,100)
    for event in pygame.event.get():
        if event.type == QUIT:
            window.blit(credits,(0,0))
            pygame.display.flip()
            pygame.time.delay(3500)
            pygame.quit()
            exit(0)
        if event.type == KEYDOWN :
            if event.key == K_DOWN and direction_snake!="haut":
                direction_provisoire="bas"
            if event.key == K_LEFT and direction_snake!="droite":
                direction_provisoire="gauche"
            if event.key == K_RIGHT and direction_snake!="gauche":
                direction_provisoire="droite"
            if event.key == K_UP and direction_snake!="bas":
                direction_provisoire="haut"
        if event.type== MOUSEBUTTONDOWN :
            X,Y=event.pos
            if (596<X<646) and (10<Y<48):
                soon()



def affichage_score():
    text=font.render(str(score),1,blanc)
    window.blit(text,(510,33))

def affichage_meilleur_score():
    text=font.render(str(meilleur_score),1,blanc)
    window.blit(text,(105,33))


#définition de la fonction soon qui permet d'arreter ou de remetrre le son et de changer le bouton en conséquence
def soon():
    global musique
    if musique==1:
        pygame.mixer.music.pause()
        musique=0
    else:
        pygame.mixer.music.unpause()
        musique=1

#définition de la fonction qui affiche le bouton son ou no_son par rapport à l'ancien
def bouton():
    if musique==1:
        window.blit(son,(596,10))
    else:
        window.blit(no_son,(596,10))

def actualisation_image():
    window.blit(fond,(0,0))
    carre((taille_fenetre[0]//2,taille_fenetre[0]//2+cartouche_haut),taille_fenetre[0]//2-bord,jaune)
    bouton()
    affiche_pomme(vert)
    affichage_score()
    affichage_meilleur_score()

#INITIALISATION
taille_carré_jeu=20
taille_morceau=30
vert=(0,255,0)
rouge=(255,0,0)
bleu=(0,0,255)
jaune=(255,255,0)
noir=(0,0,0)
blanc=(255,255,255)
cartouche_haut=50
bord=30


import time
import random
import pickle
import pygame
from pygame.locals import *
pygame.init() # initialisation de pygame
#construit la fenêtre(taille en pixels : ici 640x480)
taille_fenetre=(662, 712)
window= pygame.display.set_mode(taille_fenetre)
screen = pygame.display.get_surface()
#chargement des images
fond=pygame.image.load("images\fond.png").convert()
son = pygame.image.load("images\son.png").convert_alpha()
no_son = pygame.image.load("images\no_son.png").convert_alpha()
credits=pygame.image.load("images\credits.png").convert()
#chargement de la musique
pygame.mixer.music.load("dj-snake-magenta-riddim.mp3")
#choix de la typographie des textes
font=pygame.font.SysFont("Calibri",50,bold=True,italic=False)


#lancement de la musique
pygame.mixer.music.play(loops=-1)
musique=1
while True:
    #début d'une partie
    direction_snake="bas"
    direction_provisoire="bas"
    snake=[[taille_carré_jeu//2,0]]
    score=0
    meilleur_score=recupere("meilleur_score")
    pomme=nv_pomme()
    actualisation_image()
    fin=False
    while fin==False:
        fin=avance_snake()
        actualisation_image()
        pygame.time.delay(125)
        change_direction_snake()





