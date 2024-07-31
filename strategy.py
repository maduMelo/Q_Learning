import numpy as np
import time
import pyautogui

class Strategy:
    def __init__(self):
        # Ordem das setas do teclado que devem ser pressionadas para posicionar o agente em determinada plataforma
        self.paths = {
            '0b0000000': [],
            '0b0000100': ['up'],
            '0b1000111': ['up', 'left', 'up'],
            '0b1001011': ['up', 'left', 'up', 'up'],
            '0b1001111': ['up', 'left', 'up', 'up', 'up'],
            '0b1010011': ['up', 'left', 'up', 'up', 'up', 'up'],
            '0b1010111': ['up', 'left', 'up', 'up', 'up', 'up', 'up'],
            '0b1011000': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up'],
            '0b1011100': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up', 'up'],
            '0b0001000': ['up', 'up'],
            '0b0001100': ['up', 'up', 'up'],
            '0b0010000': ['up', 'up', 'up', 'up'],
            '0b0111011': ['up', 'up', 'up', 'left', 'up'],
            '0b0010100': ['up', 'up', 'up', 'left', 'up', 'right', 'up'],
            '0b0011000': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'up'],
            '0b0111111': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'left', 'up'],
            '0b0011100': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up'],
            '0b0100000': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up', 'up'],
            '0b1000011': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up', 'left', 'up'],
            '0b0100100': ['up', 'up', 'up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up', 'left', 'up', 'right', 'up'],
            '0b0110100': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up', 'up', 'up'],
            '0b0110000': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up', 'up', 'up', 'up'],
            '0b0101100': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up', 'up', 'up', 'up', 'up'],
            '0b0101001': ['up', 'left', 'up', 'up', 'up', 'up', 'up', 'right', 'up', 'up', 'up', 'up', 'up', 'right', 'up']
        }

    # Sorteia uma plataforma aleatória por onde começar a percorrer o ambiente
    def random_start(self):
        return np.random.choice(list(self.paths.keys()))

    # Move, determinísticamente, o agente para a plataforma sorteada
    def position_self(self):
        platform = self.random_start()
        for step in self.paths[platform]:
            pyautogui.press(step)
            time.sleep(1)
        return self.format_state(platform)

    # Traduz o estado atual do agente para seu índice na q_table
    def format_state(self, state):
        return (int(state[:-2], 2) * 4) + int(state[-2:], 2)