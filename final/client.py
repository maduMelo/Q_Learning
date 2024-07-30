#Aqui vocês irão colocar seu algoritmo de aprendizado
import numpy as np

import connection as cn
import q_table as qt
import q_agent
import strategy

# Conectando ao servidor
socket = cn.connect(2037)

# Definição do ambiente
N_STATES, N_ACTIONS = 96, 3
MOVES = ['left', 'jump', 'right']

# Denifindo parâmetros de aprendizado
ALPHA_0, GAMMA, EPSILON_0 = .0, .7, .0 # learning_rate, discount_factor, exploration_rate
EPOCHS = 350 # Número de episódios # 1000 epochs

# Instanciando Agente
agent = q_agent.Q_LearningAgent(N_STATES, N_ACTIONS, ALPHA_0, GAMMA, EPSILON_0)
my_strategy = strategy.Strategy()
agent.q_table = np.array(qt.Q_table)

for epoch in range(EPOCHS):
    """
    if epoch != 0:
        current_state = my_strategy.position_self()
    else:
    """
    
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
        next_state = my_strategy.format_state(next_state)
        terminal_state = reward == -100 or reward == 300

        # Atualizar Q_table
        agent.update_q_table(current_state, action, reward, next_state, epoch)

        # Atualizar estado atual
        current_state = next_state

print()
print(agent.q_table)

np.savetxt('./desperate_mesures/resultado5.txt', agent.q_table, fmt='%.6f', delimiter=', ')