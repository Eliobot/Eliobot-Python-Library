# Documentation Python-Library

## Fonction set_pixel_power 
La fonction set_pixel_power est utilisée pour activer ou désactiver l'alimentation de la LED intégrée. Elle prend en paramètre un état (state) et la fonction utilise une variable globale pixel_power pour pouvoir l'utiliser dans différentes fonctions.



## Fonction get_battery_voltage
La fonction get_battery_voltage permet de récupérer approximativement la tension de la batterie 



## Fonction get_vbus_present
Le code utilise une variable globale vbus_sense et retourne la valeur de cette variable. La variable vbus_sense est utilisée pour détecter si une tension VBUS (5V) est présente. Si la valeur retournée est True, cela indique que la source d'alimentation VBUS est présente. Sinon, si la valeur retournée est False, cela signifie que la source d'alimentation VBUS n'est pas détectée.



## Fonction rgb_color_wheel
La fonction rgb_color_wheel permet de créer une séquence de couleurs RVB en utilisant la "roue des couleurs". Cette roue représente les différentes couleurs de l'arc-en-ciel (rouge, orange, jaune, vert, bleu, violet) et permet de les parcourir progressivement.

Le code de la fonction prend en compte une position dans cette roue des couleurs, représentée par la valeur wheel_pos. Pour s'assurer que cette valeur reste dans la plage valide, le code utilise l'opération "modulo" en la divisant par 255. Cela signifie que lorsque wheel_pos atteint 255, il revient à 0 et continue à augmenter progressivement.

En fonction de la position dans la roue des couleurs, la fonction détermine quelle couleur RVB retourner. Le code utilise trois plages de valeurs : de 0 à 84, de 85 à 169, et de 170 à 254.

Dans la première plage (0 à 84), la fonction retourne des valeurs RVB où le rouge diminue progressivement de 255 à 0, le vert est nul, et le bleu augmente progressivement de 0 à 255. Cela représente les couleurs allant du rouge à l'orange.

Dans la deuxième plage (85 à 169), le rouge est nul, le vert augmente progressivement de 0 à 255, et le bleu diminue progressivement de 255 à 0. Cela représente les couleurs allant du jaune au bleu.

Dans la troisième plage (170 à 254), le rouge augmente progressivement de 0 à 255, le vert diminue progressivement de 255 à 0, et le bleu est nul. Cela représente les couleurs allant du vert au violet.



## Fonction get_obstacle
La fonction get_obstacle permet de détecter s’il y a un obstacle devant ou derrière le robot grâce à des capteurs infrarouge qui sont référencés dans un tableau obstacleInput. En passant un nombre compris dans la taille du tableau 0 à 3 en paramètre la fonction renvoie True ou False selon la valeur récupérer par le capteur. 

Les capteurs infrarouges sont assignés à des broches et ces broches sont elles-mêmes assignées à un nombre allant de 0 à 3. Si Obstacle_pos = 0 on regarde s’il y a un obstacle à gauche du robot. Le capteur envoie et réceptionne un rayon infrarouge et selon la valeur qui est retournée on peut savoir s’il y a un obstacle proche. Si la valeur retournée est inférieur à 10000 alors la réponse sera True et si la valeur est supérieur à 10000 alors la réponse sera False. 

C'est exactement la même chose pour les 3 autres capteurs 
    Si l'obstacle_pos = 1 on regarde s’il y a un obstacle au milieu.
    Si l'obstacle_pos = 2 on regarde s’il y a un obstacle à gauche.
    Si l'obstacle_pos = 3 on regarde s’il y a un obstacle derrière.
 
 
    
    
## Fonction set_speed 
Cette fonction prend en paramètre un int compris entre 0 et 100 qui correspond au pourcentage de la vitesse du robot. 100 % vitesse max et 0% vitesse minimale cependant si speed est entre 0 et 10 le robot n'avance pas, d'où la vérification qui permet de rajouter 10 pour que le robot puisse quand même avancer. Puis nous convertissons la valeur des pourcentages en valeur réelle qui permet de donner une vitesse au robot. La plage de fonctionnement du robot est de 0 à 65535, 65535 correspondants à 100 % de la vitesse du robot et 0 à 0%.



## Fonction advance
Cette fonction permet de faire avancer le robot. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour avancer. 
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant
        
On donne donc une vitesse aux 2 variables qui font avancer le robot soit AIN2 et BIN2.

## Fonction back
Cette fonction permet de faire reculer le robot. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour reculer  
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse aux 2 variables qui font reculer le robot soit AIN1 et BIN1.



## Fonction left
Cette fonction permet de faire tourner le robot vers la gauche. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner à gauche. Pour que le robot tourne à gauche il faut que la roue droite avance et que la roue gauche recule.
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse aux 2 variables qui font tourner le robot à gauche soit AIN2 et BIN1.




## Fonction right
Cette fonction permet de faire tourner le robot vers la droite. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner à droite. Pour que le robot tourne à droite il faut que la roue droite recule et que la roue gauche avance.        AIN1 permet de faire reculer la roue droite vers l'arrière        AIN2 permet de faire avancer la roue droite vers l'avant        BIN1 permet de faire reculer la roue gauche vers l'arrière        BIN2 permet de faire avancer la roue gauche vers l'avantOn donne donc une vitesse aux 2 variables qui font tourner le robot à droite soit AIN1 et BIN2.



## Fonction stop
Cette fonction permet d'arrêter le robot elle met tous les moteurs à la vitesse 0.


## Fonction left_wheel_back
Cette fonction permet de faire tourner la roue gauche du robot vers l'arrière. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner, pour faire tourner la roue gauche vers l'arrière il faut : 
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse à la variable qui fait tourner la roue gauche du robot vers l'arrière soit BIN1.



## Fonction left_wheel_advance
Cette fonction permet de faire tourner la roue gauche du robot vers l'avant. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner, pour faire tourner la roue gauche vers l'avant il faut: 
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse à la variable qui fait tourner la roue gauche du robot vers l'avant soit BIN2.



## Fonction right_wheel_back
Cette fonction permet de faire tourner la roue droite du robot vers l'arrière. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner, pour faire tourner la roue droite vers l'arrière il faut: 
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse à la variable qui fait tourner la roue droite du robot vers l'arrière soit AIN1.


## Fonction right_wheel_advance
Cette fonction permet de faire tourner la roue droite du robot vers l'avant. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une variable. Le robot à 2 moteurs pour le faire tourner, pour faire tourner la roue droite vers l'avant il faut: 
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant

On donne donc une vitesse à la variable qui fait tourner la roue droite du robot vers l'avant soit AIN2.


##Fonction oneCase
Cette fonction permet de faire avancer le robot d'une case sachant qu'une case fait 15 cm. Elle prend en paramètre une vitesse comprise entre 0 et 100% qui sera directement convertie en vitesse pour le robot grâce à la fonction set_speed puis elle est stockée dans une varible. Le robot à 2 moteurs pour le faire avancer.
        AIN1 permet de faire reculer la roue droite vers l'arrière
        AIN2 permet de faire avancer la roue droite vers l'avant
        BIN1 permet de faire reculer la roue gauche vers l'arrière
        BIN2 permet de faire avancer la roue gauche vers l'avant
    
On donne donc une vitesse aux variables qui font avancer le robot soit AIN2 et BIN2 puis on attend un certain temps le temps que le robot avance de 15cm puis on l'arrête. 


## Fonction buzzerInit
Cette fonction permet de configurer le buzzer pour pouvoir l'utiliser pour jouer des sons 



## Fonction playFrequency
La fonction playFrequency est utilisée pour jouer une fréquence sonore pendant une durée spécifiée.

Elle initialise le buzzer en appelant une fonction buzzerInit() 
Elle arrondit la valeur de frequency à l'entier le plus proche et la configure comme la fréquence du buzzer.
Elle définit le cycle de service (duty_cycle) du buzzer à 2>>15e qui correspond à un rapport cyclique de 50% pour obtenir une onde carrée.
Elle attend pendant la durée spécifiée en utilisant la fonction time.sleep(waitTime).
Elle désactive le buzzer en appelant la méthode deinit().
La fonction playFrequency est utilisée pour jouer une note spécifique sur un buzzer pendant un certain laps de temps donné par waitTime. La fréquence de la note est définie par le paramètre frequency.



## Fonction get_line
La fonction get_line permet de détecter s’il y a une ligne à l'avant du robot grâce à des capteurs de couleur qui sont référencés dans un tableau lineInput. En passant un nombre compris dans la taille du tableau 0 à 4 en paramètre la fonction renvoie la valeur récupérer par le capteur correspondant au chiffre. 

Les capteurs couleurs sont assignés à des broches et ces broches sont elles-mêmes assignées à un nombre allant de 0 à 4. Si Line_pos = 0 on regarde s’il y a une ligne tout à gauche du robot. Le capteur envoie et réceptionne un rayon infrarouge et selon la valeur qui est retournée on peut savoir s’il y a une ligne ou pas.

C'est exactement la même chose pour les 4 autres capteurs 
    Si le line_pos = 1 on regarde s’il y a une ligne au milieu gauche.
    Si le line_pos = 2 on regarde s’il y a une ligne au milieu.
    Si le line_pos = 3 on regarde s’il y a une ligne au milieu droit.
    Si le line_pos = 4 on regarde s’il y a une ligne tout à droite.
    
La fonction permet de faire abstraction de la luminosité ambiante ce qui permet de ne pas fausser les valeurs.


## Fonction followLine

La fonction followLine est utilisée pour suivre une ligne en utilisant des capteurs de ligne.

Elle obtient les valeurs des capteurs de ligne à travers les appels à la fonction get_line pour les capteurs 0, 2 et 4, et les assigne respectivement aux variables sensor1_value, sensor2_value et sensor3_value.

Elle met en oeuvre la logique de suivi de ligne en utilisant des conditions if-elif-else.
Si le capteur du milieu (get_line(2)) détecte une ligne (valeur inférieure à threshold + 1500), cela indique que le robot est centré sur la ligne. Dans ce cas, les moteurs sont configurés pour avancer en définissant les valeurs des broches AIN1 et BIN1 à 0 et les valeurs des broches AIN2 et BIN2 à 65535.
Si le capteur de gauche (get_line(0)) détecte une ligne (valeur inférieure à threshold - 9500), cela indique que le robot a dévié vers la gauche. Dans ce cas, les moteurs sont configurés pour tourner vers la gauche en définissant les valeurs des broches AIN1 et BIN2 à 0 et les valeurs des broches AIN2 et BIN1 à 8000.
Si le capteur de droite (get_line(4)) détecte une ligne (valeur inférieure à threshold - 9500), cela indique que le robot a dévié vers la droite. Dans ce cas, les moteurs sont configurés pour tourner vers la droite en définissant les valeurs des broches AIN1 et BIN2 à 8000 et les valeurs des broches AIN2 et BIN1 à 0.
Si aucun capteur ne détecte une ligne, cela indique que le robot est hors de la ligne. Dans ce cas, les moteurs sont configurés pour reculer à une vitesse plus lente en définissant les valeurs des broches AIN1 et BIN2 à 8000 et les valeurs des broches AIN2 et BIN1 à 0.
Elle attend pendant une courte durée de 0.1 seconde en utilisant la fonction time.sleep(0.1).
Fonction followLine est utilisée dans un contexte où un robot est équipé de capteurs de ligne pour suivre une ligne tracée au sol. Selon les valeurs des capteurs, le robot ajuste les vitesses des moteurs pour rester sur la ligne ou effectuer des corrections de trajectoire si nécessaire.



## Fonction play_note
La fonction play_note est utilisée pour jouer une note spécifiée pendant une durée donnée.

Elle vérifie si la note spécifiée (note) se trouve dans le dictionnaire NOTES_FREQUENCIES. Ce dictionnaire associe des notes à leurs fréquences correspondantes.
Si la note est présente dans le dictionnaire, la fonction récupère la fréquence associée à cette note.
Si la fréquence n'est pas égale à 0.1, cette  valeur est une valeur spéciale pour indiquer une pause, la fonction appelle la fonction playFrequency pour jouer la note à la fréquence spécifiée (frequency) et pendant la durée spécifiée (duration).
Sinon, si la fréquence est égale à 0.1, la fonction utilise la fonction time.sleep pour faire une pause pendant la durée spécifiée (duration).
La fonction play_note est utilisée pour jouer des notes musicales en utilisant des fréquences prédéfinies. La durée de lecture de chaque note est spécifiée, et si la fréquence de la note est différente de 0.1 (pour une pause), la fonction appelle une autre fonction playFrequency pour jouer la note à la fréquence correspondante. Sinon, la fonction fait une pause en utilisant time.sleep.
