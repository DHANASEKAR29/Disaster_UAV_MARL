import random
import pickle
import os


class QLearning:

    def __init__(self):
        self.q_table = {}

        self.learning_rate = 0.1
        self.discount_factor = 0.9

        self.epsilon = 0.2
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995

        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def get_state(self, drone):
        battery_level = drone.battery // 20
        return (drone.x, drone.y, battery_level, drone.zone)

    def initialize_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = {}
            for action in self.actions:
                self.q_table[state][action] = 0.0

    def choose_action(self, state):
        self.initialize_state(state)

        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state, action, reward, next_state):
        self.initialize_state(state)
        self.initialize_state(next_state)

        old_value = self.q_table[state][action]
        future_reward = max(self.q_table[next_state].values())

        new_value = old_value + self.learning_rate * (
            reward +
            self.discount_factor * future_reward -
            old_value
        )

        self.q_table[state][action] = new_value

    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

            if self.epsilon < self.min_epsilon:
                self.epsilon = self.min_epsilon

    def show_qtable(self):
        print("\n========== Q TABLE ==========")

        if len(self.q_table) == 0:
            print("Q-Table Empty")
            return

        for state in self.q_table:
            print(f"State : {state}")
            for action in self.actions:
                print(f"   {action:6} -> {round(self.q_table[state][action],2)}")
            print()

    def total_states(self):
        return len(self.q_table)

    def save_qtable(self, filename="qtable.pkl"):
        data = {
            "q_table": self.q_table,
            "epsilon": self.epsilon
        }

        with open(filename, "wb") as file:
            pickle.dump(data, file)

        print(f"\nQ-Table saved -> {filename}")

    def load_qtable(self, filename="qtable.pkl"):
        if not os.path.exists(filename):
            print("\nNo previous Q-Table found.")
            return

        with open(filename, "rb") as file:
            data = pickle.load(file)

        self.q_table = data["q_table"]
        self.epsilon = data["epsilon"]

        print(f"\nQ-Table loaded -> {filename}")
        print(f"Learned States : {len(self.q_table)}")
