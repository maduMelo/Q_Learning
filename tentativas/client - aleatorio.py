#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import numpy as np
import pyautogui
import time

import q_table as qt

class Q_LearningAgent:
    def __init__(self, n_states, n_actions, alpha, gamma, epsilon):
        self.alpha_0 = alpha
        self.gamma = gamma
        self.epsilon_0 = epsilon

        self.n_states = n_states
        self.n_actions = n_actions
        self.q_table = np.zeros([n_states, n_actions])
    
    def get_alpha(self, epoch):
        return max(.2, self.alpha_0 / (1 + .0005 * epoch))

    def get_epsilon(self, epoch, epochs):
        return max(.1, self.epsilon_0 - (epoch / epochs))

    def choose_action(self, state, epoch, epochs):
        epsilon = self.get_epsilon(epoch, epochs)

        if np.random.rand() < epsilon:
            print('Exploring')
            return np.random.randint(self.n_actions)  # Explore
        else:
            print('Exploiting')
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_table(self, state, action, reward, next_state, epoch):
        alpha = self.get_alpha(epoch)
        self.q_table[state, action] += alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - self.q_table[state, action])

paths = {
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

def random_start():
    return np.random.choice(list(paths.keys()))

def position_self():
    platform = random_start()
    for step in paths[platform]:
        pyautogui.press(step)
        time.sleep(1)
    
    return format_state(platform)

def format_state(state):
    return (int(state[:-2], 2) * 4) + int(state[-2:], 2)


# Conectando ao servidor
socket = cn.connect(2037)

# Definição do ambiente
N_STATES, N_ACTIONS = 96, 3
MOVES = ['left', 'jump', 'right']

# Denifindo parâmetros de aprendizado
ALPHA_0, GAMMA, EPSILON_0 = .4, .7, .5 # learning_rate, discount_factor, exploration_rate
EPOCHS = 350 # Número de episódios # 1000 epochs

# Instanciando Agente
agent = Q_LearningAgent(N_STATES, N_ACTIONS, ALPHA_0, GAMMA, EPSILON_0)
agent.q_table = np.array(qt.Q_table)

for epoch in range(EPOCHS):
    if epoch != 0:
        current_state = position_self()
    else:
        current_state = 0

    print('\n----------------')
    print(f'Epoch {epoch}')
    print(f'Learning rate: {agent.get_alpha(epoch)}')
    print(f'Tendency to explore: {agent.get_epsilon(epoch, EPOCHS)}')
    print('----------------\n')

    terminal_state = False
    while not terminal_state:
        
        # Ecolher a ação que o agente irá tomar
        action = agent.choose_action(current_state, epoch, EPOCHS)

        # Executar a ação
        next_state, reward = cn.get_state_reward(socket, MOVES[action])
        next_state = format_state(next_state)
        terminal_state = reward == -100 or reward == 300

        # Atualizar Q_table
        agent.update_q_table(current_state, action, reward, next_state, epoch)

        # Atualizar estado atual
        current_state = next_state

print()
print(agent.q_table)

np.savetxt('./desperate_mesures/resultado5.txt', agent.q_table, fmt='%.6f', delimiter=', ')