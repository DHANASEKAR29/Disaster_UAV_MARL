import random

GRID_SIZE = 15

EMPTY = "."
DRONE = "D"
SURVIVOR = "S"
OBSTACLE = "X"


class Drone:

    def __init__(self, drone_id, x, y):

        self.drone_id = drone_id
        self.x = x
        self.y = y

        self.battery = 100
        self.score = 0

        self.status = "Searching"

        self.visited = {(x, y)}

        self.low_battery_alert_sent = False

        self.active = True
        self.busy = False

        self.zone = "Unknown"

    def display_status(self):

        print("------------------------------")
        print(f"Drone    : {self.drone_id}")
        print(f"Zone     : {self.zone}")
        print(f"Position : ({self.x}, {self.y})")
        print(f"Battery  : {self.battery}%")
        print(f"Score    : {self.score}")
        print(f"Status   : {self.status}")
        print("------------------------------")

    def in_zone(self, x, y):

        if self.zone == "Zone-1":
            return x <= 4 and y <= 4

        elif self.zone == "Zone-2":
            return x <= 4 and y >= 5

        elif self.zone == "Zone-3":
            return x >= 5 and y <= 4

        elif self.zone == "Zone-4":
            return x >= 5 and y >= 5

        elif self.zone == "Support Zone":
            return True

        return True

    def move(self, grid, communication, qlearning=None, mode="qlearning"):

        if not self.active:
            return

        state = qlearning.get_state(self) if qlearning else None

        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        possible = list(directions.items())
        random.shuffle(possible)

        action = None
        new_x = self.x
        new_y = self.y

        # Prefer unexplored cells
        for act, (dx, dy) in possible:

            tx = self.x + dx
            ty = self.y + dy

            if not (0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE):
                continue

            if not self.in_zone(tx, ty):
                continue

            if grid[tx][ty] == OBSTACLE:
                continue

            if (tx, ty) not in self.visited:
                action = act
                new_x = tx
                new_y = ty
                break

        # RL / Random fallback
        if action is None:

            if mode == "qlearning" and qlearning:
                action = qlearning.choose_action(state)
            else:
                action = random.choice(list(directions.keys()))

            dx, dy = directions[action]

            new_x = self.x + dx
            new_y = self.y + dy
        print(f"{self.drone_id} trying ({self.x},{self.y}) -> ({new_x},{new_y})")

        # Boundary
        if not (0 <= new_x < GRID_SIZE and
                0 <= new_y < GRID_SIZE):
                print(f"{self.drone_id} -> Boundary Block")
                return

        # Zone
        if not self.in_zone(new_x, new_y):
            print(f"{self.drone_id} -> Zone Block")
            return

        # Obstacle
        if grid[new_x][new_y] == OBSTACLE:
            print(f"{self.drone_id} -> Obstacle Block")
            self.score -= 5
            return

        reward = 5

        if (new_x, new_y) not in self.visited:
            reward += 10
        else:
            reward -= 2

        # Clear old position
        grid[self.x][self.y] = EMPTY

        self.x = new_x
        self.y = new_y

        # Survivor
        if grid[self.x][self.y] == SURVIVOR:

            reward += 200
            self.status = "Rescued Survivor"

        else:
            self.status = "Searching"

        # Mark drone
        grid[self.x][self.y] = DRONE

        self.visited.add((self.x, self.y))

        self.score += reward

        # Battery drain (slow)
        self.battery -= 1

        if self.battery < 0:
            self.battery = 0

        # Exploration bonus
        if len(self.visited) % 10 == 0:
            self.score += 25

        # Low battery alert
        if self.battery <= 20 and not self.low_battery_alert_sent:

            communication.send(
                self.drone_id,
                f"LOW BATTERY ({self.battery}%)"
            )

            self.low_battery_alert_sent = True
            self.status = "Low Battery"

        # Auto recharge for continuous simulation
        if self.battery == 0:

            communication.send(
                self.drone_id,
                "RECHARGING..."
            )

            self.status = "Recharging"

            self.battery = 100

            self.low_battery_alert_sent = False

            communication.send(
                self.drone_id,
                "FULLY RECHARGED"
            )

            self.status = "Searching"

        print(f"{self.drone_id} moved {action}")

        if mode == "qlearning" and qlearning:

            next_state = qlearning.get_state(self)

            qlearning.update(
                state,
                action,
                reward,
                next_state
            )

    def accept_mission(self, failed_drone, communication):

        if self.busy:
            return

        self.busy = True
        self.status = "Mission Accepted"

        communication.receive(
            self.drone_id,
            failed_drone.drone_id,
            "LOW BATTERY ALERT"
        )

        communication.mission_accepted(self.drone_id)

    def complete_mission(self):

        self.busy = False
        self.status = "Searching"

    def deactivate(self):

        self.active = False
        self.busy = False
        self.status = "Mission Transferred"