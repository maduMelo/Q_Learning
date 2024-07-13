#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import numpy as np

def format_state(state):
    return (int(state[:-2], 2) * 4) + int(state[-2:], 2)


# Conectando ao servidor
socket = cn.connect(2037)

# Definição do ambiente
N_STATES, N_ACTIONS = 96, 3
MOVES = ['left', 'jump', 'right']
Q_table = np.zeros([N_STATES, N_ACTIONS])


# Denifindo parâmetros de aprendizado
alpha, gamma, epilson = .2, .7, .1 # learning_rate, discount_factor, exploration_rate
epochs = 2 # Número de episódios # 1600 epochs

for epoch in range(epochs):
    current_state = 0

    print(f'Epoch {epoch}')

    terminal_state = False
    while not terminal_state:
        
        # Ecolher a ação que o agente irá tomar
        if np.random.rand() < epilson:
            print('Exploring')
            action = np.random.randint(N_ACTIONS) # Explore
        else:
            print('Exploiting')
            action = np.argmax(Q_table[current_state])  # Exploit

        # Executar a ação
        next_state, reward = cn.get_state_reward(socket, MOVES[action])
        next_state = format_state(next_state)
        terminal_state = reward == -100 or reward == 300

        # Atualizar Q_table
        Q_table[current_state, action] += alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[current_state, action])

        # Atualizar estado atual
        current_state = next_state

np.savetxt('resultado.txt', Q_table, fmt='%.6f', delimiter=' ')