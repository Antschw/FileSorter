from pathlib import Path

p = Path( __file__ ).absolute() # Création d'un objet chemin avec la méthode Path
extension = input("Indiquez l'extension des fichiers à trier : ")
nom_fichier = input("Indiquez le nom à donner aux fichier : ")
cond_aj = input("Indiquez une condition d'exclusion (chiffre surplus) : ") # Cette condition exclue tous les chiffres placés après la condition d'ajout, si pas de chiffre en trop laisser vide
if extension == "stop":
    exit()

liste_num = []  # Initialisation de la liste des numéros contenus dans les noms des fichiers
pre_val_digit = False   # Initialisation sur faux du booléen qui indique si la valeur précédemment testée est un entier 

for f in p.parent.glob("*."+extension):    # Boucle sur tous les fichiers avec l'extension .txt contenus dans le fichier parent du chemin p
    b=0
    for i in f.stem:    # Boucle sur le nom de chaque fichier avec la méthode .stem pour négliger l'extension
        if not pre_val_digit :  # Si la valeure précédemment testée n'est pas un entier
            numero_str = "" # Initialisation du charactère chiffre relevé dans le nom du fichier à str vide 
        if i.isdigit(): # Si le i-ème caractère est un entier
            if not pre_val_digit:   # Si le i précédente n'était pas un entier
                numero_str = i  # On enregistre le charactère chiffre actuel
                liste_num.append(int(numero_str))   # On l'ajoute à la liste des chiffres présent dans les noms de fichier sous forme d'entier
                pre_val_digit = True    # On indique pour le prochain tour de boucle qu'on vient de rencontrer un chiffre au cas ou ce serai un nombre à plusieurs chiffres
                if b == len(f.stem)-1:  # Si on arrive au dernier élément du nom de f 
                    pre_val_digit = False   # On indique au programme qu'on change de fichier donc que la valeur précédente n'est plus un chiffre même si ça l'est
            else : 
                liste_num.remove(int(numero_str))   #   Si on a déjà rencontré un chiffre au caractère i-1 on le retire de la liste
                numero_str = numero_str + i # On forme le nombre grâce à la concaténation des str i-1 et i
                liste_num.append(int(numero_str))   # On ajoute ce nouveau nombre à notre liste
                if b == len(f.stem)-1:
                    pre_val_digit = False
        else : 
            if pre_val_digit:
                pre_val_digit = False   # On réinitialise à faux dans le cas ou le caratère rencontrer n'est pas un chiffre
                break
            pre_val_digit = False
        b+=1
    numero_str = ""

liste_ep = sorted(liste_num,)   # On créer une nouvelle liste ou tous les nombres rencontrés sont classés par ordre croissant
print(liste_ep)

if liste_ep == []:
    print("Aucun fichier à ranger")
    exit()

if max(liste_ep)>10000:
    liste_ep_alt = list(range(len(liste_ep))) 
    print(liste_ep_alt)
    fill_0 = len(str(liste_ep_alt[-1]))
    k=len(liste_ep_alt) 
    for j in p.parent.glob("*."+extension):    
        for h in j.stem:    
            if h.isdigit():
                if j != j.parent / f"{nom_fichier}_{str(liste_ep_alt[k-1]).zfill(fill_0)}.{extension}" :  
                    j.rename(j.parent / f"{nom_fichier}_{str(liste_ep_alt[k-1]).zfill(fill_0)}.{extension}") 
                    k-=1 
            break 

else : 
    fill_0 = len(str(liste_ep[-1])) # On regarde la taille du plus grand nombre rencontré pour faire énumération de nos fichiers remplie de 0 (ex: 019 si le max est d'ordre 100)


    for j in p.parent.glob("*."+extension):    # On refait une boucle sur tous les fichiers avec l'extension .txt contenus dans le fichier parent du chemin p
        for h in j.stem:    #   On reparcours chaque lettre de chaque fichier
            if h.isdigit(): # Si le i-ème caractère est un entier
                pre_val_digit = True
                k=len(liste_ep) # On défini un k équivalent à la taille de notre liste_ep pour pouvoir faire des itérations négative dessus
                while k !=0 : # Tant que k différent de 0
                    if str(liste_ep[k-1])+cond_aj in j.stem :   # Si le charactère équivalent à l'entier k-1 dans list_ep est présent dans le nom du fichier
                        if j != j.parent / f"{nom_fichier}_{str(liste_ep[k-1]).zfill(fill_0)}.{extension}" :  # Si le nom du fichier n'est pas déjà sous la forme qu'on veut lui donner
                            j.rename(j.parent / f"{nom_fichier}_{str(liste_ep[k-1]).zfill(fill_0)}.{extension}") # Alors on le renomme grâce à un fstring et en remplissant notre str de 0 avec .zfill
                            k=0 # Dans ce cas on sort de la boucle car on ne peut pas travailler sur un fichier déjà renommé
                    else:
                        k-=1 # Sinon on chercher l'entier plus petit de la liste_ep présent dans le nom du fichier
                break # Si il y a un chiffre et qu'on a trouvé lequel on passe au nom de fichier suivant 