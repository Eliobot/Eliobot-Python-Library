## Librairie Python pour Eliobot

### Introduction
La librairie Python fournit des fonctionnalités pour contrôler un robot. Elle utilise les bibliothèques `time`, `board`, `digitalio`, `analogio`, `pwmio` et `busio` pour interagir avec les différents composants matériels du robot, tels que les capteurs, les moteurs, les LED, etc.

### Installation
Pour utiliser cette librairie, vous devez importer le fichier `code.py` dans le dossier `lib` de votre Eliobot.


### Importation des librairies annexes
La libriaire se base sur les librairies suivantes, déjà intégrées :

```python
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import pwmio
import busio
```

### Déclaration des broches
Avant d'utiliser les différents composants du robot, vous devez déclarer les broches utilisées pour chaque composant. Voici les déclarations des broches pour les différents composants :

```python
# Déclaration de la broche de mesure de tension de la batterie (vbat_voltage)
vbat_voltage = AnalogIn(board.BATTERY)

# Déclaration de la broche de détection VBUS
vbus_sense = DigitalInOut(board.VBUS_SENSE)
vbus_sense.direction = Direction.INPUT

# Déclaration des broches d'entrée des capteurs d'obstacles
obstacleCmd = DigitalInOut(board.IO33)
obstacleCmd.direction = Direction.OUTPUT
obstacleInput = [AnalogIn(board.IO4), AnalogIn(board.IO5), AnalogIn(board.IO6), AnalogIn(board.IO7)]

# Déclaration des broches d'entrée des capteurs de ligne
lineInput = [AnalogIn(board.IO10), AnalogIn(board.IO11), AnalogIn(board.IO12), AnalogIn(board.IO13), AnalogIn(board.IO14)]
threshold = 45000

# Déclaration des broches du moteur
AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)
```

### Fonctionnalités

#### Mesure de la tension de la batterie

```python
def get_battery_voltage():
    """Récupère la tension approximative de la batterie."""
    global vbat_voltage
    return (vbat_voltage.value / 5371)
```

Cette fonction renvoie la tension de la batterie en volts.

#### Détection de la présence de l'alimentation VBUS

```python
def get_vbus_present():
    """Détecte si une source d'alimentation VBUS (5V) est présente."""
    global vbus_sense
    return vbus_sense.value
```

Cette fonction renvoie `True` si une source d'alimentation VBUS est détectée, sinon elle renvoie `False`.

#### Roue des couleurs RVB

```python
def rgb_color_wheel(wheel_pos):
    """Roue des couleurs pour parcourir les couleurs RVB de l'arc-en-ciel."""
    wheel_pos = wheel_pos % 255

    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0
```

Cette fonction prend une position de roue en entrée (0-254) et renvoie la couleur correspondante en RVB. Elle permet de parcourir les couleurs de l'arc-en-ciel.

#### Capteurs d'obstacles

```python
def getObstacle(obstacle_pos):
    """Récupère les valeurs des capteurs d'obstacles de gauche (position 0) à droite (position 3) et retour (position 4)."""
    obstacle_pos = obstacle_pos
    
    value = 0

    value = obstacleInput[obstacle_pos].value

    if value < 10000:
        return True
    else:
        return False
```

Cette fonction prend la position d'un capteur d'obstacle en entrée (0-4) et renvoie `True` s'il détecte un obstacle, sinon elle renvoie `False`.

#### Contrôle des moteurs

```python
def setSpeed(speedValue):
    """Convertit la vitesse de 0-100% en 0-65535 pour une utilisation avec pwmio."""
    if speedValue > 100:
        speedValue = 100
    elif speedValue < 15:
        speedValue += 15
        
    pwmValue = int((speedValue / 100) * 65535)

    return pwmValue


def moveForward(speed):
    """Fait avancer le robot à une vitesse donnée (0-100%)."""
    pwm_value = setSpeed(speed)
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = pwm_value
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = pwm_value
```

Les autres fonctions de contrôle des moteurs `moveBackward`, `turnLeft`, `turnRight`, `motorStop`, `motorSlow`, `spinLeftWheelForward`, `spinLeftWheelBackward`, `spinRightWheelForward`, `spinRightWheelBackward`,
`moveOneStep` suivent une structure similaire.

Ces fonctions permettent de contrôler les moteurs du robot pour effectuer différentes actions telles que avancer, reculer, tourner, arrêter, etc.

#### Buzzer

```python
def buzzerInit():
    """Initialise le buzzer."""
    buzzerPin = pwmio.PWMOut(board.IO17, variable_frequency=True)
    return buzzerPin
    

def playFrequency(frequency, waitTime, volume):
    """Joue une fréquence (en Hertz) pendant une durée donnée (en secondes) avec un volume spécifié."""
    buzzer = buzzerInit()
    buzzer.frequency = round(frequency)
    buzzer.duty_cycle = int(2 ** (0.06 * volume + 9))  # La valeur 32768 correspond à un cycle de service de 50 % pour obtenir une onde carrée.
    time.sleep(waitTime)
    buzzer.deinit()


def playNote(note, duration, NOTES_FREQUENCIES, volume):
    """Joue une note (C, D, E, F, G, A ou B) pendant une durée donnée (en secondes)."""
    if note in NOTES_FREQUENCIES:
        frequency = NOTES_FREQUENCIES[note]
        if frequency != 0.1:
            playFrequency(frequency, duration, volume)
        else:
            time.sleep(duration)
```

Ces fonctions permettent de contrôler le buzzer pour jouer des fréquences spécifiques et des notes de musique avec une durée et un volume donnés.

#### Suivi de ligne

```python
def getLine(line_pos):
    """Récupère les valeurs des capteurs de ligne de gauche (position 0) à droite (position 4)."""
    ambient = 0
    lit = 0
    value = 0

    # Mesure de la lumière réfléchie par le capteur IR
    obstacleCmd.value = True
    time.sleep(0.02)
    lit = lineInput[line_pos].value

    # Mesure de la lumière ambiante
    obstacleCmd.value = False
    time.sleep(0.02)
    ambient = lineInput[line_pos].value

    # Lumière ambiante - Lumière réfléchie
    value = ambient - lit

    return value


def followLine():
    """Fonction d'exemple pour suivre une ligne noire sur du papier blanc."""
    sensor1_value = getLine(0)
    sensor2_value = getLine(2)
    sensor3_value = getLine(4)

    # Affichage des valeurs des capteurs
    print(sensor1_value, sensor2_value, sensor3_value)

    # Logique de suivi de ligne
    if sensor2_value < threshold + 1500:
        # Ligne détectée par le capteur central, avancer
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 65535
        BIN1.duty_cycle = 0
        BIN2.duty_cycle = 65535

    elif sensor1_value < threshold - 9500:
        # Ligne détectée par le capteur gauche, tourner à gauche
        AIN1.duty_cycle = 0
        AIN2.duty_cycle = 8000
        BIN1.duty_cycle = 8000
        BIN2.duty_cycle = 0

    elif sensor3_value < threshold - 9500:
        # Ligne détectée par le capteur droit, tourner à droite
        AIN1.duty_cycle = 8000
        AIN2.duty_cycle = 0
        BIN1.duty_cycle = 0
        BIN2.duty_cycle = 8000

    else:
        # Aucune ligne détectée, reculer à une vitesse plus lente
        AIN1.duty_cycle = 8000
        AIN2.duty_cycle = 0
        BIN1.duty_cycle = 8000
        BIN2.duty_cycle = 0

    time.sleep(0.1)
```

Ces fonctions permettent de détecter et de suivre une ligne noire sur une surface blanche à l'aide de capteurs de ligne. La fonction `getLine` récupère les valeurs des capteurs de ligne de gauche à droite et calcule la différence entre la lumière ambiante et la lumière réfléchie pour déterminer la position de la ligne. La fonction `followLine` utilise ces valeurs pour prendre des décisions sur la direction à suivre. Si la ligne est détectée par le capteur central, le robot avance, s'il est détecté par le capteur gauche, le robot tourne à gauche, s'il est détecté par le capteur droit, le robot tourne à droite, sinon le robot recule à une vitesse plus lente.


