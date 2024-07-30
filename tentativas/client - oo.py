#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import numpy as np

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
        return max(.0, self.alpha_0 / (1 + .0005 * epoch))

    def get_epsilon(self, epoch, epochs):
        return max(.0, self.epsilon_0 - (epoch / epochs))

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


def format_state(state):
    return (int(state[:-2], 2) * 4) + int(state[-2:], 2)


# Conectando ao servidor
socket = cn.connect(2037)

# Definição do ambiente
N_STATES, N_ACTIONS = 96, 3
MOVES = ['left', 'jump', 'right']

# Denifindo parâmetros de aprendizado
ALPHA_0, GAMMA, EPSILON_0 = .1, .9, .0 # learning_rate, discount_factor, exploration_rate
EPOCHS = 2000 # Número de episódios # 13000 epochs ## 3000

# Instanciando Agente
agent = Q_LearningAgent(N_STATES, N_ACTIONS, ALPHA_0, GAMMA, EPSILON_0)
agent.q_table = np.array(qt.Q_table)

for epoch in range(EPOCHS):
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

np.savetxt('./oo/resultado111.txt', agent.q_table, fmt='%.6f', delimiter=', ')