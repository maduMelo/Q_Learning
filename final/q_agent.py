import numpy as np

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
