#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 01:41:59 2020

@author: chendeb
"""

import http.client
import time
import numpy as np
import  math
from timeit import default_timer as timer

CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'

servergame="chendeb.free.fr"


def jouerWEB(idjeu,monid,tour,jeu,server=servergame):
    conn = http.client.HTTPConnection(server)
    req=conn.request("GET", "/Puissance6?status=JeJoue&idjeu="+idjeu+"&idjoueur="+monid+"&tour="+str(tour)+"&jeu="+str(jeu))
    r1 = conn.getresponse()
    return (r1.status, r1.reason)  

def getJeuAdv(idjeu,idAdv,tour,server=servergame):
    conn = http.client.HTTPConnection(server)
    req=conn.request("GET", "/Puissance6?status=GetJeuAdv&idjeu="+idjeu+"&idjoueur="+idAdv+"&tour="+str(tour))
    r1 = conn.getresponse()
    advJeu=None
    if(r1.status==200):
        temp=r1.read()
        print(temp)
        if(temp.decode('UTF-8')!='PASENCOREJOUE'):
            advJeu=int(temp)
    return advJeu  

def loopToGetJeuAdv( inetvalle,idjeu,idAdv,tour,server=servergame):
    advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    while(advJeu==None):
        time.sleep(inetvalle)
        advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    return advJeu

def remplirGrille(joueur, jeu):
    for i in range(grilleDim-1,-1,-1):
        if(grille[i][jeu]==0):
            grille[i][jeu]=joueur
            break

def returnGrille(joueur, board, action):
    for i in range(12-1,-1,-1):
        if(board[i][action]==0):
            board[i][action]=joueur
            return board,i,action

def action_win(board,player,r,c) :
    countR = 0
    countC = 0
    countDP = 0
    countDN = 0
    for i in range(-3,4):
        if c-i >= 0 and c-i <= 11 :
            if board[r][c-i] == player : countR = countR + 1
            else :countR = 0
        if r-i>=6 and r-i <= 11 :
            if board[r-i][c] == player : countC = countC + 1
            else : countC = 0
        if c+i>= 0 and c+i <= 11 and r-i >= 6 and r-i <=11 : 
            if board[r-i][c+i] == player : countDP = countDP + 1
            else : countDP = 0
        if c-i>=0 and c-i<= 11 and r-i >= 6 and r-i<=11:
            if board[r-i][c-i] == player : countDN = countDN + 1
            else : countDN = 0
        if countC >= 4 or countR >= 4  or countDN >= 4 or countDP >= 4:
            return True
    return False
    
        
            
def printGrille():
    for i in range(grilleDim):
        print("|",end=' ')
        for j in range(grilleDim):
            if(grille[i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif grille[i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(grilleDim):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(grilleDim):
        print(i%10+1,end=" ")
        print("|",end=' ')
    print()
    
def scorecell(board,r,c,player,opponent):
    score = 0
    if board[r][c] == player:  
        #horizontal     
        if c<9:
            if board[r][c]==board[r][c+1] and board[r][c+2] != opponent and board[r][c+3] != opponent:
                score += 4
                if board[r][c]==board[r][c+3] or board[r][c]==board[r][c+2]:
                    score +=20

        #vertical
        if r>8:
            if board[r][c]==board[r-1][c] and board[r-2][c] != opponent and board[r-3][c] != opponent:
                score += 4
                if board[r][c]==board[r-2][c] :
                    score +=20
                    if c<9:
                        if board[r][c]==board[r-1][c+3] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+1] :
                            score +=500
                    if c>2:
                        if board[r][c]==board[r-1][c-3] and board[r][c]==board[r-2][c-2] and board[r][c]==board[r-3][c-1] :
                            score +=500



        #diag positiv
        if r>8 and c<9 :
            if board[r][c]==board[r-1][c+1] and board[r-2][c+2] != opponent and board[r-3][c+3] != opponent :
                score += 8
                #cluster win
                if board[r][c]==board[r][c+1] and board[r][c]==board[r-1][c] and board[r-1][c+2] != opponent and board[r-2][c] != opponent and board[r-2][c+1] != opponent:
                    score+=500

                #3 in diag pos
                if board[r][c]==board[r-3][c+3] or board[r][c]==board[r-2][c+2] :
                    score +=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c+3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c+1]:
                        score+=500
                    #triangle win pos
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c+1] and board[r-2][c+3] ==0 and board[r][c]==board[r-2][c+2]:
                        score+=500

        #diag negativ
        if r>8 and c>2 :
            if board[r][c]==board[r-1][c-1] and board[r-2][c-2] != opponent and board[r-3][c-3] != opponent and r>8 and c>3 :
                score += 8
                if board[r][c]==board[r-3][c-3] or board[r][c]==board[r-2][c-2] :
                    score +=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c-3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c-1]:
                        score+=500
                    #triangle win neg
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c-1] and board[r-2][c-3] ==0:
                        score+=500


    if board[r][c] == opponent:  
        #horizontal
        if c<9:     
            if board[r][c]==board[r][c+1] and board[r][c+2] != player and board[r][c+3] != player:
                score -= 4
                if board[r][c]==board[r][c+3] or board[r][c]==board[r][c+2]  :
                    score -=20
        #vertical
        if r>8:
            if board[r][c]==board[r-1][c] and board[r-2][c] != player and board[r-3][c] != player:
                score -= 4
                if board[r][c]==board[r-2][c]:
                    score -=20
                    if c<9:
                        if board[r][c]==board[r-1][c+3] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+1] :
                            score -=500
        #diag positiv
        if r>8 and c<9 :        
            if board[r][c]==board[r-1][c+1] and board[r-2][c+2] != player and board[r-3][c+3] != player :
                score -= 8
                #cluster win
                if board[r][c]==board[r][c+1] and board[r][c]==board[r-1][c] and board[r-1][c+2] != opponent and board[r-2][c] != opponent and board[r-2][c+1] != opponent:
                    score-=500
                #3 in diag pos
                if board[r][c]==board[r-3][c+3] or board[r][c]==board[r-2][c+2] :
                    score -=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c+3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c+1]:
                        score-=500
                    #triangle win pos
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c+1] and board[r-2][c+3] ==0:
                        score-=500
                        
        #diag negativ
        if r>8 and c>2 :
            if board[r][c]==board[r-1][c-1] and board[r-2][c-2] != player and board[r-3][c-3] != player :
                score -= 8
                if board[r][c]==board[r-3][c-3] or board[r][c]==board[r-2][c-2]  :
                    score -=50
                    #pos win 2 1 2
                    if board[r][c]==board[r-3][c-3] and board[r][c]==board[r-3][c] and board[r][c]==board[r-3][c-1]:
                        score-=500
                    #triangle win neg
                    if board[r][c]==board[r-2][c] and board[r][c]==board[r-2][c-1] and board[r-2][c-3] ==0:
                        score-=500
    return score
        

def utility(board, player, opponent):
    #print(board)
    score = 0
    # Check horizontal locations for win
    for c in range(12):
        for r in range(11,5,-1):
            if board[r][c]!=0:
                score += scorecell(board,r,c,player,opponent)
    return score

def actionPossible(board):
    listeActions = []
    for i in range(12):
        if board[6][i] == 0 :
            listeActions.append(i)
    return listeActions

def winning_move2(board):
    for c in range(12):
        for r in range(11,5,-1):
            if board[r][c] != 0:
                if c < 9 :
                    if board[r][c] == board[r][c+1] and board[r][c] == board[r][c+2] and  board[r][c] == board[r][c+3]:
                        return True
                if r > 8 :
                    if board[r][c] == board[r-1][c] and board[r][c] == board[r-2][c] and  board[r][c] == board[r-3][c]:
                        return True
                if r > 8 and c < 9:
                    if board[r][c] == board[r-1][c+1] and board[r][c] == board[r-2][c+2] and  board[r][c] == board[r-3][c+3]:
                        return True
                if r < 8 and c > 3:
                    if board[r][c] == board[r-1][c-1] and board[r][c] == board[r-2][c-2] and  board[r][c] == board[r-3][c-3]:
                        return True
    return False


def minmax(board, depth, alpha, beta, maxplayer,player,opponent):
    list_action = actionPossible(board)
    if depth <= 0:
        t=()
        for ligne in board:
            t+=tuple(ligne)
        h=hash(t)
        if h in dict:
            value = dict[h]
        else:
            value = utility(board,player,opponent)
            dict[h]=value
        return value
    if maxplayer==True:
        value = -math.inf
        for actions in list_action:
            testboard = board.copy()
            lastboard,r,c = returnGrille(player,testboard,actions)
            if action_win(lastboard,player,r,c)==True:
                alpha = 5000
                return 5000+depth
            value = max(value,minmax(lastboard,depth-1,alpha,beta,False,player,opponent))
            alpha = max(alpha,value)
            if alpha>=beta :
                break
        return value
    else:
        value = math.inf
        for actions in list_action:
            testboard = board.copy()
            lastboard,r,c = returnGrille(opponent,testboard,actions)
            if action_win(lastboard,opponent,r,c)==True:
                beta = -5000
                return -5000-depth
            value = min(value,minmax(lastboard,depth-1,alpha,beta,True,player,opponent))
            beta = min(beta,value)
            if alpha>=beta :
                break
        return value

def bestmoove(board,player,opponent,profondeur):
    a = timer()
    listresult=[]
    action_list=actionPossible(board)
    for actions in action_list:
        testboard=board.copy()
        lastboard,r,c = returnGrille(player,testboard,actions)
        if action_win(lastboard,player,r,c)==True:
            print(timer()-a)
            return c
        listresult.append(minmax(lastboard,profondeur,-math.inf,math.inf,False,player,opponent))
    finalaction = action_list[listresult.index(max(listresult))]
    print(timer()-a)
    print(listresult)
    return finalaction


dict = {}       



#############################################################
#                                                           #
#  Vous n'avez qu'a remplacer les deux methodes monjeu et   #
#      appliqueJeuAdv  selon votre IA                       #
#                                                           #
#  Bien definir un idjeu pour l'id de la partie de jeu      #
#  votre nom et celui du joueur distant                     #
#  puis bien préciser si vous commencer le jeu True,        #
#  False signifie que le joueurDistant qui commence.        #
#                                                           #
#                                                           #
#############################################################



grilleDim=12
grille=np.zeros((grilleDim,grilleDim),dtype=np.byte)



#idjeu est un id unique, si vous abondonnez une partie, pensez à créer un nouveau idjeu
idjeu="ID65165195618841916553123456651234567652123456789012"
idjoueurLocal="Jeremy"
idjoueurDistant="Tristan"

# bien préviser si vous commencer le jeu ou c'est l'adversaire qui commence
joueurLocalquiCommence=True



#cette methode est à remplacer par votre une fonction IA qui propose le jeu
def monjeu():
    #print(utility(grille,1))
    testgrille = grille.copy()
    return bestmoove(testgrille,joueurLocal,joueurDistant,3)
    #return int(input("vueillez saisir la colonne de votre jeu entre 0 et "+ str(grilleDim-1) +" : "))

def jeuadvlocal():
    #print(utility(grille,1))
    #testgrille = grille.copy()
    #return bestmoove(testgrille,1,2)
    testgrille = grille.copy()
    return bestmoove(testgrille,1,2,4)
    #return int(input("vueillez saisir la colonne de votre jeu entre 0 et "+ str(grilleDim-1) +" : "))


# cette fonction est à remplacer une qui saisie le jeu de l'adversaire à votre IA
def appliqueJeuAdv(jeu):
    print("jeu de l'adversair est ", jeu)




if(joueurLocalquiCommence):
    joueurLocal=2
    joueurDistant=1
else:
    joueurLocal=1
    joueurDistant=2
    
sommetempsjeu = 0    
tour=0
while(True):
    
    if(joueurLocalquiCommence):
        if tour ==0:
            a = timer()
            jeu=5
            temps = timer() - a
            sommetempsjeu += temps
            print(temps)
            print("Je joue en 6")
        elif tour ==1:
            a = timer()
            jeu = jeuAdv
            sommetempsjeu += (timer()-a)
            print("Je joue en " + str(jeu+1) )
            print(timer()-a)
        else :
            a = timer()
            jeu=monjeu()
            sommetempsjeu += timer()-a
            print(timer()-a)
            print("Je joue en " + str(jeu+1) )
        #jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        print(str(sommetempsjeu), "s : temps final" )
        remplirGrille(joueurLocal,jeu)
        printGrille()
        jeuAdv=input("vueillez saisir la colonne de votre jeu entre 0 et "+ str(grilleDim-1) +" : ")
        jeuAdv = int(jeuAdv) -1
        #c'est ce jeu qu'on doit transmettre à notre IA
        #appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
    else:
        #jeuAdv=loopToGetJeuAdv( 5,idjeu,idjoueurDistant,tour)
        #c'est ce jeu qu'on doit transmettre à notre IA
        jeuAdv=input("vueillez saisir la colonne de votre jeu entre 0 et "+ str(grilleDim-1) +" : ")
        jeuAdv = int(jeuAdv) -1
        #appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
        if tour ==0:
            a = timer()
            jeu=jeuAdv
            sommetempsjeu += (timer()-a)
            print("Je joue en " + str(jeu+1) )
            print(timer()-a)
        else :
            a = timer()
            jeu=monjeu()
            sommetempsjeu += (timer()-a)
            print("Je joue en " + str(jeu+1) )
            print(str(sommetempsjeu), "s : temps final" )
        jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        remplirGrille(joueurLocal,jeu)
        printGrille()
        
    tour+=1        
       
    
    
