from time import time


def damerau_levenshtein(s1, s2):
    d = {}
    l1 = len(s1)
    l2 = len(s2)
    for i in range(-1,l1+1):
        d[(i,-1)] = i+1
    for j in range(-1,l2+1):
        d[(-1,j)] = j+1
    for i in range(l1):
        for j in range(l2):
            if s1[i]==s2[j]:
                cout_substitution=0
            else:
                cout_substitution=1
            d[(i,j)] = min(d[(i-1,j)]+1, # deletion
                           d[(i,j-1)]+1, # insertion
                           d[(i-1,j-1)]+cout_substitution # substitution
                          )
            if i>0 and j>0 and s1[i]==s2[j-1] and s1[i-1]==s2[j]:
                d[(i,j)]=min(d[(i,j)],d[i-2,j-2]+cout_substitution) # transposition
    return d[l1-1,l2-1]

try:
    file2=open("F:/MPE 2/liste_mots_accents.txt","r",encoding="latin_1")
except FileNotFoundError:
    file2=open("E:/MPE 2/liste_mots_accents.txt","r",encoding="latin_1")
dict_base=file2.readlines()
file2.close()

def algorithme_naif(mot):
    a=time()
    N=len(dict_base)
    out=[dict_base[0]]
    min=damerau_levenshtein(mot,out)
    for i in range(N-1):
        d=damerau_levenshtein(mot,dict_base[i])
        if d<min:
            out=[dict_base[i]]
            min=d
        elif d==min:
            out.append(dict_base[i])
    print(time()-a)
    return out

def intersect(a, b):
    return (set(a) & set(b))

def union(a,b):
    return (set(a)|set(b))

def coeffJaccard(mot1,mot2):
    return 1-len(set(mot1)&set(mot2))/len(set(mot1)|set(mot2))


try:
    file2=open("F:/MPE 2/liste_mots_accents.txt","r",encoding="latin_1")
except FileNotFoundError:
    file2=open("E:/MPE 2/liste_mots_accents.txt","r",encoding="latin_1")
dict_acc=file2.readlines()
file2.close()
N_acc=len(dict_acc)
for i in range(N_acc):
    dict_acc[i]=dict_acc[i].strip()
    dict_acc[i]='$'+dict_acc[i]+'$'

def partage(mot):#partage un mot en trigrammes
    n =len(mot)
    trig = []
    for i in range(n-2):
        trig.append(mot[i:i+3])
    return trig

def liste_trigrammes(dict):
    trigrammes=[]
    N=len(dict)
    for j in range(N):
        trigrammes.append(partage(dict[j]))
    return trigrammes

def reference_trig(dict): #renvoie un dictionnaire où les clés sont les trigrammes du dictionnaire et les valeurs associées aux clés sont les mots du dictionnaire contenant la clé
    trigrammes=liste_trigrammes(dict)
    ref_trig_mot = {}
    N=len(dict)
    for i in range(N):
        m=len(trigrammes[i])
        for j in range(m):
            if trigrammes[i][j] in ref_trig_mot.keys():
                ref_trig_mot[trigrammes[i][j]].append(dict[i])
            else:
                ref_trig_mot[trigrammes[i][j]]=[dict[i]]
    return ref_trig_mot

def ajoute_mot_proche(mot,dict_mot_occ):
    if mot in dict_mot_occ.keys():
        dict_mot_occ[mot]+=1
    else:
        dict_mot_occ[mot]=1

def cle(dic,valeur):
    out=[]
    for i in dic.keys():
        if dic[i]==valeur:
            out.append(i)
    return out

#ref_trig_mot=reference_trig(dict_acc)

def correction_trig(mot,dict,existe=False):
    a=time()
    mot2='$'+mot+'$'
    if mot2 in dict and not existe:
        return [mot]
    else:
        mots_occ={}
        trig=partage(mot2)
        mots_proches=[]
        #ref_trig_mot=reference_trig(dict)
        for triplet in trig:
            mots_proches.extend(ref_trig_mot.get(triplet,[]))
        for mot in mots_proches:
            ajoute_mot_proche(mot,mots_occ)
        maxi=max(mots_occ.values())
        closest_words=[]
        for mot in mots_occ.keys():
            if mots_occ[mot] >= maxi-2:
                closest_words.append(mot)
        for word in closest_words:
            if coeffJaccard(word,mot2)>0.8:
                closest_words.remove(word)
        limite=10
        best_matches = sorted(closest_words,key=lambda x:damerau_levenshtein(x,mot2))
        for i in range(len(best_matches[0:limite])):
            n=len(best_matches[i])
            best_matches[i]=best_matches[i][1:n-1]
        #print(time()-a)
        if existe:
            return best_matches[1:limite+1]
        else:
            return best_matches[0:limite]

def correction_choix(mot,dict):
    liste=correction(mot,dict)
    if mot in liste:
        return mot
    else:
        liste=[mot]+liste
    for i in range(len(liste)):
        print(i,':',liste[i])
    choix=input('choix ?')
    return liste[int(choix)]







##
import collections

def coupe_texte(phrase):
    lettres = 'abcdefghijklmnopqrstuvwxyzáàâçéèêëíîïôöùûü-'
    phrase=phrase.lower()
    resultat = []
    mot = ''
    for c in phrase:
        if c in lettres:
            mot = mot + c
        else:
            if mot != '':
                resultat.append(mot)
            mot = ''
    if mot != '':
        resultat.append(mot)
    return resultat

def entrainer(liste_mots):
    dict=collections.defaultdict(lambda: 1) #crée un dictionnaire qui à un mot associe le nombre d'apparitions dans le texte (initialisé à 1)
    for mot in liste_mots:
        dict[mot]+=1
    return dict

file0= open("F:/MPE 2/corpus final utf8.txt","r",encoding="utf8")
#dict = entrainer(coupe_texte(file0.read()))
file0.close()

alphabet='abcdefghijklmnopqrstuvwxyz-'
alphabet_accent = 'abcdefghijklmnopqrstuvwxyzáàâçéèêëíîïôöùûü-'


def dist05(mot): #ensemble des mots où les caractères a,e,i,o,u,c sont remplacés par à,é,ç,... #génère environ 3(n/2) mots
    a_accent="áàâ"
    e_accent="éèêë"
    i_accent="íîï"
    o_accent="ôö"
    u_accent="ùûü"
    n=len(mot)
    partage=[(mot[:i],mot[i:]) for i in range(n+1)]
    remplace = []
    for (a,b) in partage:
        if( b!="") and (b[0] in 'aeiouc'):
            if b[0]=='a':
                for c in a_accent:
                    remplace.append(a+c+b[1:])
            elif b[0]=='e':
                for c in e_accent:
                    remplace.append(a+c+b[1:])
            elif b[0]=='i':
                for c in i_accent:
                    remplace.append(a+c+b[1:])
            elif b[0]=='o':
                for c in o_accent:
                    remplace.append(a+c+b[1:])
            elif b[0]=='u':
                for c in u_accent:
                    remplace.append(a+c+b[1:])
            else:
                remplace.append(a+'ç'+b[1:])
    return set(remplace)

def dist1(mot): #renvoie l'ensemble des mots à une distance 1 de mot #pour un mot de longueur n --> génère environ 45n+44+(3n/2)**2 mots
    n=len(mot)
    partage=[(mot[:i],mot[i:]) for i in range(n+1)]
    supprime =[]
    transpose = []
    remplace = []
    insere = []
    for (a,b) in partage:
        if b!="":
            supprime.append(a+b[1:])
        if len(b)>1:
            transpose.append(a+b[1]+b[0]+b[2:])
        for c in alphabet_accent:
            insere.append(a+c+b)
            if b!="":
                remplace.append(a+c+b[1:])
    liste=[] #liste contenant l'ensemble des mots ayant deux caractères accentués de différence par rapport à mot
    for mot1 in dist05(mot):
        for mot2 in dist05(mot1):
            liste.append(mot2)
    return set(supprime + transpose + remplace + insere + liste)

def dist1_esp(mot): #renvoie l'ensemble des couples (m1,m2) tels que m1 et m2 soient dans le dictionnaire et m=m1+m2 (à un espace près)
    n=len(mot)
    partage=[(mot[:i],mot[i:]) for i in range(n+1)]
    remplace = []
    insere = []
    for (a,b) in partage:
        if (a in dict) and (b in dict):
            insere.append(a+" "+b)
            if b!="":
                remplace.append(a+" "+b[1:])
    return set(remplace+insere)

def dist15_connus(mot): #renvoie 49n*3(n/2) mots
    liste=[]
    for mot1 in dist05(mot):
        for mot2 in dist1(mot1):
            if mot2 in dict:
                liste.append(mot2)
    return set(liste)

def dist2_connus(mot): #renvoie l'ensemble des mots à une distance 2 de mot
    liste=[]
    for mot1 in dist1(mot):
        for mot2 in dist1(mot1):
            if mot2 in dict:
                liste.append(mot2)
    return set(liste)


def mots_connus(liste_mots): #renvoie l'ensemble des mots connus parmi liste_mots
    out=[]
    for mot in liste_mots:
        if mot in dict:
            out.append(mot)
    return set(out)
    
def mots_connus2(liste_mots,dist,n): #renvoie un dictionnaire qui à un mot d associe P(d|m) où m est un mot de longueur n et situé à une distance dist de d
    out={}
    N={0.5:3*n/2} 
    N[1]=45*n+44+(N[0.5])**2 
    N[1.5]=N[0.5]*N[1]
    N[2]=(N[1])**2
    for d in liste_mots:
        a=coupe_texte(d)
        if len(a)>1: #cas où d est un ensemble de deux mots
           out[d]=0.8*dict[a[0]]*(dict[a[1]]/len(dict))/N[dist] #out[d]=(P(m|d1)*P(d1))*(P(m|d2)*P(d2))*constante avec a=(d1,d2)
        if d in dict:
            if dist>1:
                out[d]=0.2/N[dist]*dict[d] #out[d]=P(m|d)*P(d)*constante
            else:
                out[d]=0.8/N[dist]*dict[d]
    return out

def somme_dictionnaires(a,b): #renvoie un dictionnaire composé des clés de a et de b et qui à chaque clé k associe a[k],b[k] ou max(a[k],b[k]) si a[k] et b[k] existent 
    c={}
    for i in list(a.keys())+list(b.keys()):
        if i in c:
            if b[i]>a[i]:
                c[i]=b[i]
        else:
            try:
                c[i]=a[i]
            except KeyError:
                c[i]=b[i]
    return c


def corriger2_proba(mot): #renvoie la liste des 10 mots d ayant la plus forte probabilité P(d|mot)
    n=len(mot)
    a=mots_connus([mot])
    b=mots_connus2(dist05(mot),.5,n)
    c=mots_connus2(dist1(mot)|dist1_esp(mot),1,n)
    d=mots_connus2(dist15_connus(mot),1.5,n)
    e=mots_connus2(dist2_connus(mot),2,n)
    dict_proba=somme_dictionnaires(somme_dictionnaires(b,c),somme_dictionnaires(d,e))
    if a!=set():
        corr_possibles=list(a)
    else:
        corr_possibles=sorted(dict_proba.keys(), key=dict_proba.get, reverse=True)
    if len(corr_possibles)>0:
        return corr_possibles[:10]
    else:
        print("correction non trouvée")
        return []

def corriger(mot): #renvoie l'ensemble des mots 
    a=mots_connus([mot])
    b=mots_connus(dist05(mot))
    c=mots_connus(dist1(mot))
    d=dist15_connus(mot)
    e=dist2_connus(mot)
    if a!=set():
        corr_possibles=list(a)
    else:
        corr_possibles=sorted(b, key=dict.get, reverse=True)+sorted(c, key=dict.get, reverse=True)+sorted(d, key=dict.get, reverse=True)+sorted(e, key=dict.get, reverse=True)
    if len(corr_possibles)>0:
        return list(set(corr_possibles[:10]))
    else:
        print("correction non trouvée")
        return []

def corriger_choix(mot):
    a=time()
    liste=corriger(mot)
    if mot in liste:
        return mot
    else:
        liste=[mot]+liste
    print(time()-a)
    for i in range(len(liste)):
        print(i,':',liste[i])
    print(len(liste),"autre orthographe")
    choix=input('choix ?')
    if int(choix) == len(liste):
        ortho=input("entrer nouveau mot:")
        return ortho
    else:
        return liste[int(choix)]

def correction_proba_choix(mot):
    a=time()
    liste=corriger2_proba(mot)
    if mot in liste:
        dict[mot]+=1
        return mot
    else:
        liste=[mot]+liste
    print(time()-a)
    for i in range(len(liste)):
        print(i,':',liste[i])
    print(len(liste),"autre orthographe")
    choix=input('choix ?')
    if int(choix) == len(liste):
        ortho=input("entrer nouveau mot:")
        ajout=input("l'ajouter au dictionnaire ? (o/n)")
        if ajout=="o":
            dict[ortho]+=1
        return ortho
    else:
        if choix!=0:
            dict[liste[int(choix)]]+=1
        return liste[int(choix)]


def correction_trig_choix(mot,dict):
    liste=correction_trig(mot,dict)
    if mot in liste:
        return mot
    else:
        liste=[mot]+liste
    for i in range(len(liste)):
        print(i,':',liste[i])
    print(len(liste)," autre recherche")
    choix=input('choix ?')
    if int(choix) == len(liste):
        return correction_proba_choix(mot)
    else:
        return liste[int(choix)]

##
def algorithme_final(mot):
    if len(mot)<7:
        return correction_proba_choix(mot)
    else:
        return correction_trig_choix(mot,dict_acc)


file2=open("F:/MPE 2/fautes.txt","r",encoding="latin_1")
fichier_fautes=file2.readlines()
file2.close()
N_fautes=len(fichier_fautes)
for i in range(N_fautes):
    fichier_fautes[i]=fichier_fautes[i].strip()

# fichier_fautes de la forme:
# mot1         |envelloppe
# mot1_correct |enveloppe
# mot2         |rhytme
# mot2_correct |rythme
# ...

def test_efficacite():
    n=len(fichier_fautes)//2
    nb_corrections=0
    a=time()
    for i in range(n):
        mot=fichier_fautes[2*i]
        mot_correct=fichier_fautes[2*i+1]
        print(mot_correct)
        if len(mot)<7:
            prop=corriger2_proba(mot)
            if mot_correct in prop:
                nb_corrections+=1
            else:
                print("non trouvé")
        else:
            prop=correction_trig(mot,dict_acc)
            if mot_correct in prop:
                nb_corrections+=1
            elif mot_correct in corriger2_proba(mot):
                nb_corrections+=1
            else:
                print("non trouvé")
        print(nb_corrections)
    print(time()-a)
    print(nb_corrections,n)
    return nb_corrections/n

import sqlite3
from sqlite3 import OperationalError

def inserer(chaine,caractere,rang): #insere caractere pour que chaine[rang]=caractere
    return chaine[:rang]+caractere+chaine[rang:]

def supprimer(chaine,rang):
    return chaine[:rang]+chaine[(rang+1):]


def liste_phrases(texte):
    n=len(texte)
    debut_phrase=0
    phrases=[]
    for i in range(n):
        if texte[i] in ['.','!','?']:
            phrases.append(texte[debut_phrase:i+1].capitalize())
            debut_phrase=i+2
    return phrases

def corr_syntaxe(chaine): #vérifier tous les aspects typographiques, les espaces insécables, les guillemets, les espaces surnuméraires
    chaine=chaine.strip()
    n=len(chaine)
    i=0
    while i<n:
        while chaine[i:i+2]=='  ':
            chaine=supprimer(chaine,i)
            n-=1
        if chaine[i] in [".",",",")"]:
            try:
                if chaine[i+1]!=' ':
                    chaine=inserer(chaine,' ',i+1)
                    n+=1
            except IndexError:
                ()
            if chaine[i-1]==' ':
                chaine=supprimer(chaine,i-1)
                n-=1
        elif chaine[i] in ['!','?',';',':']:
            try:
                if chaine[i+1]!=' ':
                    chaine=inserer(chaine,' ',i+1)
                    n+=1
            except IndexError:
                ()
            if chaine[i-1]!=' ':
                chaine=inserer(chaine,' ',i)
                n+=1
        elif chaine[i] == "'":
            if chaine[i+1]==' ':
                chaine=supprimer(chaine,i+1)
                n-=1
            if chaine[i-1]==' ':
                chaine=supprimer(chaine,i-1)
                n-=1
        elif chaine[i] == '(':
            if chaine[i+1]==' ':
                chaine=supprimer(chaine,i+1)
                n-=1
            if chaine[i-1]!=' ':
                chaine=inserer(chaine,' ',i)
                n+=1
        i+=1
    return liste_phrases(chaine)

            

from tkinter import *
from tkinter.messagebox import *

# class MyByeButton(Button):
#     def __init__(self, parent=None, **config):
#         Button.__init__(self, parent, config)
#         self.pack()
#         self.config(command=self.callback)
#     def callback(self):
#         print('bye...')
#         self.destroy()

def avancer_curseur(actuel,n):
    return actuel+" + "+str(n)+' chars'

def reculer_curseur(actuel,n):
    return actuel+" - "+str(n)+' chars'

def reperer(mot,index): #renvoie l'indice de la première apparition de mot après index
    n=len(mot)
    index2=avancer_curseur(index,n)
    while txt.get(index,index2)!=mot:
        index=avancer_curseur(index,1)
        index2=avancer_curseur(index2,1)
    return index

def remplacer():
    texte=txt.get('1.0', END+'-1c')
    liste_mots = coupe(texte)
    n=len(liste_mots[0])
    a="rien"
    index="1.0"
    index2 = avancer_curseur(index,n)
    txt.delete(index,index2)
    txt.insert(index,a)

def corr2():
    texte=txt.get('1.0', END+'-1c')
    liste_mots = coupe(texte)
    index = '1.0'
    for i in range(len(liste_mots)):
        mot=liste_mots[i]
        if mot[0] not in alphabet:
            index=reperer(liste_mots[i+1],index)
        else:
            a=correction_choix(mot,dict_acc)
            n=len(mot)
            index2 = avancer_curseur(index,n)
            bool=i>0 and liste_mots[i-1]=='.'
            if mot!=a or bool:
                txt.delete(index,index2)
                if bool:
                    a=a.capitalize()
                txt.insert(index,a)
            index=avancer_curseur(index,len(a)+1)

def corr_sel():
    texte=txt.get(SEL_FIRST,SEL_LAST)
    liste_mots = coupe(texte)
    index_f = float(SEL_FIRST)
    index=str(index_f)
    for i in range(len(liste_mots)):
        mot=liste_mots[i]
        if mot[0] not in alphabet:
            index=reperer(liste_mots[i+1],index)
        else:
            a=algorithme_final(mot)
            n=len(mot)
            index2 = avancer_curseur(index,n)
            if mot!=a:
                txt.delete(index,index2)
                txt.insert(index,a)
            index=avancer_curseur(index,len(a)+1)

def corr3():
    texte=txt.get('1.0', END+'-1c')
    liste_mots = coupe_texte(texte)
    index = '1.0'
    for i in range(len(liste_mots)):
        mot=liste_mots[i]
        if mot[0] not in alphabet:
            index=reperer(liste_mots[i+1],index)
        else:
            a=corriger_choix(mot)
            n=len(mot)
            index2 = avancer_curseur(index,n)
            if mot!=a:
                txt.delete(index,index2)
                txt.insert(index,a)
            index=avancer_curseur(index,len(a)+1)    

def corr4():
    texte=txt.get('1.0', END+'-1c')
    liste_mots = coupe_texte(texte)
    index = '1.0'
    for i in range(len(liste_mots)):
        mot=liste_mots[i]
        if mot[0] not in alphabet:
            index=reperer(liste_mots[i+1],index)
        else:
            a=algorithme_final(mot)
            n=len(mot)
            index2 = avancer_curseur(index,n)
            if mot!=a:
                txt.delete(index,index2)
                txt.insert(index,a)
            index=avancer_curseur(index,len(a)+1)
        root.update()


def synt(): #fonction de correction syntaxique similaire à corr_syntaxe mais adaptée à Tkinter
    index='1.0'
    while txt.compare(index,'<','end'):
        while txt.get(index,avancer_curseur(index,2))=='  ':
            txt.delete(index)
        if txt.get(index) in [".",",",")"]:
            if txt.get(avancer_curseur(index,1))!=' ':
                txt.insert(avancer_curseur(index,1),' ')
            if txt.get(reculer_curseur(index,1))==' ':
                txt.delete(reculer_curseur(index,1))
        elif txt.get(index) in ['!','?',';',':']:
            if txt.get(avancer_curseur(index,1))!=' ':
                txt.insert(avancer_curseur(index,1),' ')
            if txt.get(reculer_curseur(index,1))!=' ':
                txt.insert(index,' ')
        elif txt.get(index) == "'":
            while txt.get(avancer_curseur(index,1))==' ':
                txt.delete(avancer_curseur(index,1))
            if txt.get(reculer_curseur(index,1))==' ':
                txt.delete(reculer_curseur(index,1))
        elif txt.get(index) == '(':
            if txt.get(avancer_curseur(index,1))==' ':
                txt.delete(avancer_curseur(index,1))
            if txt.get(reculer_curseur(index,1))!=' ':
                txt.insert(index,' ')
        index=avancer_curseur(index,1)



root = Tk()
root.title('Correcteur orthographique et syntaxique')
txt = Text(root, height=10, width=100, wrap=WORD)
txt.pack(side=TOP)
#Button(root, text='corr2', command=corr2).pack(side=LEFT)
Button(root, text='correction orthographique', command=corr4).pack(side=LEFT)
Button(root, text='correction orthographique de la sélection', command=corr_sel).pack(side=LEFT)
Button(root, text='correction syntaxique', command=synt).pack(side=LEFT)
mainloop()
