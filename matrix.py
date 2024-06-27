# Eliobot MATRIX LED
#
# 2023 ELIO SAS
#
# Project home:
#   https://eliobot.com
#

#------------- LIBRARIES IMPORT --------------#

import neopixel
import board
import time

#--------------- MATRIX CLASS ---------------#

class MatrixLED:
    def __init__(self, pin, brightness=0.2):
        """
        Initializes a new instance of the MatrixLED class.

        Args:
        pin (Pin): The pin object from the board module which the NeoPixel LED matrix is connected to.

        Attributes:
        matrix (NeoPixel): An instance of the NeoPixel class to control the LED matrix.
        logo (list of bools): A list representing the LED status (on/off) for displaying the logo.
        """

        self.matrix = neopixel.NeoPixel(pin, 25, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB)

        self.logoHeart = [
            False, True, False, True, False,
            True, False, True, False, True,
            True, False, False, False, True,
            False, True, False, True, False,
            False, False, True, False, False]

        self.logoSmiley = [
            False, False, False, False, False,
            False, True, False, True, False,
            False, False, False, False, False,
            True, False, False, False, True,
            False, True, True, True, False]

        self.logoSad = [
            False, False, False, False, False,
            False, True, False, True, False,
            False, False, False, False, False,
            False, True, True, True, False,
            True, False, False, False, True]

        self.logoArrowUp = [
            False, False, True, False, False,
            False, True, True, True, False,
            True, False, True, False, True,
            False, False, True, False, False,
            False, False, True, False, False]

        self.logoArrowDown = [
            False, False, True, False, False,
            False, False, True, False, False,
            True, False, True, False, True,
            False, True, True, True, False,
            False, False, True, False, False]

        self.logoArrowLeft = [
            False, False, True, False, False,
            False, True, False, False, False,
            True, True, True, True, True,
            False, True, False, False, False,
            False, False, True, False, False]

        self.logoArrowRight = [
            False, False, True, False, False,
            False, False, False, True, False,
            True, True, True, True, True,
            False, False, False, True, False,
            False, False, True, False, False]

        self.logoCross = [
            True, False, False, False, True,
            False, True, False, True, False,
            False, False, True, False, False,
            False, True, False, True, False,
            True, False, False, False, True]

        self.logoCheck = [
            False, False, False, False, True,
            False, False, False, True, False,
            True, False, True, False, False,
            False, True, False, False, False,
            False, False, False, False, False]

    def set_matrix_colors(self, led_colors):
        """
       Sets the colors of all LEDs in the matrix.

       Args:
       led_colors (list of tuples): A list of RGB tuples where each tuple represents the color for each LED.
       """

        for i, color in enumerate(led_colors):
            if 0 <= i < 25:
                self.matrix[i] = color
        self.matrix.show()

    def clear_matrix(self):
        """
        Turns off all LEDs in the matrix by setting their color to black (0, 0, 0).
        """

        for i in range(25):
            self.matrix[i] = (0, 0, 0)
        self.matrix.show()

    def set_matrix_logo(self, logo, color):
        """
       Displays a logo on the LED matrix.

       Args:
       color (tuple): An RGB tuple specifying the color of the logo.
       logo (list of bools): A list representing the LED status (on/off) for displaying the logo.
       """

        for i, led in enumerate(logo):
            self.matrix[i] = color if led else (0, 0, 0)
        self.matrix.show()

    def scroll_matrix_text(self, text, color, speed=0.1):
        """
        Scrolls text across the LED matrix from right to left.

        Args:
        text (str): The text to scroll.
        color (tuple): An RGB tuple specifying the color of the text.
        speed (float): The delay in seconds between shifts, controlling the scroll speed.

        Details:
        Each character in the text is represented by a 5x5 matrix pattern. The function handles smooth
        scrolling of text across the LED matrix, including managing character spacing and ensuring characters
        exit the display one column at a time.
        """

        width = 5  # Assume each character is 5 columns wide
        space = 1  # Space between characters

        # Create an extended matrix to handle scrolling out
        extended_matrix = [0] * (len(text) * (width + space) + width)

        # Build the matrix for the entire string first
        for i, char in enumerate(text):
            if char in self.character:
                for x in range(5):
                    for y in range(5):
                        if self.character[char][x][y] == 1:
                            extended_matrix[(i * (width + space)) + y + width] |= (1 << (4 - x))

        # Scroll through the extended matrix
        for offset in range(len(extended_matrix) - width):
            for x in range(5):
                for y in range(5):
                    idx = self.m_matrix[x][y]
                    # Check if we're within the visible area of the matrix
                    char_col = y + offset
                    if char_col < len(extended_matrix) and (extended_matrix[char_col] & (1 << (4 - x))):
                        self.matrix[idx] = color
                    else:
                        self.matrix[idx] = (0, 0, 0)
            self.matrix.show()
            time.sleep(speed)

    # 5x5 matrix index mapping
    m_matrix = [
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24]
    ]

    # Character mapping
    character = {
        'A': [
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0]
        ],
        'a': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1]
        ],
        'B': [
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ],
        'b': [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ],
        'C': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0]
        ],
        'c': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0]
        ],
        'D': [
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ],
        'd': [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0]
        ],
        'E': [
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0]
        ],
        'e': [
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0]
        ],
        'F': [
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ],
        'f': [
            [0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0]
        ],
        'G': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0]
        ],
        'g': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ],
        'H': [
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0]
        ],
        'h': [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0]
        ],
        'I': [
            [1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0]
        ],
        'i': [
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0]
        ],
        'J': [
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 1, 0, 0]
        ],
        'j': [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ],
        'K': [
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0]
        ],
        'k': [
            [1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0]
        ],
        'L': [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0]
        ],
        'l': [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0]
        ],
        'M': [
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1]
        ],
        'm': [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1]
        ],
        'N': [
            [1, 0, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1]
        ],
        'n': [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0]
        ],
        'O': [
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ],
        'o': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ],
        'P': [
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ],
        'p': [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0]
        ],
        'Q': [
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0]
        ],
        'q': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0]
        ],
        'R': [
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0]
        ],
        'r': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ],
        'S': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ],
        's': [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 0]
        ],
        'T': [
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ],
        't': [
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1]
        ],
        'U': [
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ],
        'u': [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0]
        ],
        'V': [
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ],
        'v': [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ],
        'W': [
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1]
        ],
        'w': [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 0, 0, 1]
        ],
        'X': [
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1]
        ],
        'x': [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0]
        ],
        'Y': [
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ],
        'y': [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 0]
        ],
        'Z': [
            [1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0]
        ],
        'z': [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0]
        ],
        ' ': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]],
        '?': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0]],
        '!': [[0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0]],
        ',': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 0, 0, 0, 0]],
        '.': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0]],
        '0': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [1, 0, 0, 1, 1],
              [1, 0, 1, 0, 1],
              [0, 1, 1, 1, 0]],
        '1': [[0, 0, 1, 0, 0],
              [0, 1, 1, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 1, 0, 0],
              [1, 1, 1, 1, 1]],
        '2': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 1, 1, 1, 1]],
        '3': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 0, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 1, 1, 1, 0]],
        '4': [[0, 0, 0, 1, 0],
              [0, 0, 1, 1, 0],
              [0, 1, 0, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 1, 0]],
        '5': [[1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0],
              [0, 0, 0, 0, 1],
              [1, 1, 1, 1, 0]],
        '6': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 1, 1, 1, 0]],
        '7': [[1, 1, 1, 1, 1],
              [0, 0, 0, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0]],
        '8': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 1, 1, 1, 0]],
        '9': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 1, 1, 1, 1],
              [0, 0, 0, 0, 1],
              [0, 1, 1, 1, 0]],
        '-': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]],
        '_': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0]],
        '/': [[0, 0, 0, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 0, 0, 0, 0]],
        '\\': [[1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1]],
        '(': [[0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0]],
        ')': [[0, 0, 1, 0, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0]],
        '[': [[0, 1, 1, 1, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 1, 1, 0]],
        ']': [[0, 1, 1, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 1, 1, 1, 0]],
        '@': [[0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1],
              [1, 0, 1, 0, 1],
              [0, 1, 1, 1, 0]],
        '#': [[0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 1, 0, 1, 0],
              [1, 1, 1, 1, 1]],
        '$': [[0, 1, 1, 1, 1],
              [1, 0, 1, 0, 0],
              [0, 1, 1, 1, 0],
              [0, 0, 1, 0, 1],
              [1, 1, 1, 1, 0]],
        '\<': [[0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 1, 0]],
        '\>': [[0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0],
               [0, 1, 0, 0, 0]],
        '=': [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1]],
        '+': [[0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 1, 1, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0]],
        '*': [[0, 0, 0, 0, 0],
              [0, 1, 0, 1, 0],
              [1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0],
              [0, 0, 0, 0, 0]],
        '^': [[0, 0, 1, 0, 0],
              [0, 1, 0, 1, 0],
              [1, 0, 0, 0, 1],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]],
        '&': [[0, 0, 1, 1, 0],
              [0, 1, 0, 0, 1],
              [0, 0, 1, 1, 0],
              [1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0]],
        '%': [[1, 0, 0, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 0, 0, 0, 1]],
        '|': [[0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0]],
        ':': [[0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0]],
        ';': [[0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [1, 0, 0, 0, 0]],
        '\'': [[0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
    }
