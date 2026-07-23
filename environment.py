import random

GRID_SIZE = 15

EMPTY = "."
DRONE = "D"
SURVIVOR = "S"
OBSTACLE = "X"

ROAD = "R"
TREE = "T"
HOSPITAL = "H"
CHARGING = "C"
FIRE = "F"
SMOKE = "M"
FLOOD = "W"


class DisasterEnvironment:

    def __init__(self):

        self.grid = [
            [EMPTY for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

        self.fire_locations = []
        self.flood_locations = []
        self.survivor_locations = []

        self.hospital = None
        self.charging_station = None

    def place_objects(self):

        self.grid = [
            [EMPTY for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

        self.fire_locations.clear()
        self.flood_locations.clear()
        self.survivor_locations.clear()

        # ===========================
        # Trees
        # ===========================

        for i in range(GRID_SIZE):
            self.grid[0][i] = TREE
            self.grid[14][i] = TREE
            self.grid[i][0] = TREE
            self.grid[i][14] = TREE

        # ===========================
        # Roads
        # ===========================

        for j in range(1, 14):
            self.grid[6][j] = ROAD

        for i in range(1, 14):
            self.grid[i][7] = ROAD

        # ===========================
        # Buildings
        # ===========================

        buildings = [
            (3,3),(3,4),(4,3),(4,4),
            (8,9),(8,10),(9,9),(9,10)
        ]

        for x,y in buildings:
            self.grid[x][y] = OBSTACLE

        # ===========================
        # Fire
        # ===========================

        fires = [
            (3,5),
            (4,5),
            (9,3)
        ]

        for x,y in fires:
            self.grid[x][y] = FIRE
            self.fire_locations.append((x,y))

        # ===========================
        # Smoke
        # ===========================

        smokes = [
            (3,6),
            (4,6),
            (8,3)
        ]

        for x,y in smokes:
            self.grid[x][y] = SMOKE

        # ===========================
        # Flood
        # ===========================

        floods = [
            (8,4),
            (8,5),
            (9,4),
            (9,5)
        ]

        for x,y in floods:
            self.grid[x][y] = FLOOD
            self.flood_locations.append((x,y))

        # ===========================
        # Hospital
        # ===========================

        self.grid[3][11] = HOSPITAL
        self.hospital = (3,11)

        # ===========================
        # Charging Station
        # ===========================

        self.grid[5][11] = CHARGING
        self.charging_station = (5,11)

        # ===========================
        # Survivors
        # ===========================

        survivors = [
            (4,2),
            (9,6),
            (11,11),
            (2,10),
            (12,5)
        ]

        for x,y in survivors:
            self.grid[x][y] = SURVIVOR
            self.survivor_locations.append((x,y))

        # ===========================
        # Drone Positions
        # ===========================

        drones = [
            (13,1),
            (13,13),
            (1,1),
            (1,13),
            (7,7)
        ]

        for x,y in drones:
            self.grid[x][y] = DRONE

    # =====================================
    # Dynamic Fire Spread
    # =====================================

    def spread_fire(self):

        new_fire = []

        for x,y in self.fire_locations:

            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:

                    if self.grid[nx][ny] == EMPTY:

                        self.grid[nx][ny] = FIRE
                        new_fire.append((nx,ny))

        self.fire_locations.extend(new_fire)

    # =====================================
    # Dynamic Flood Spread
    # =====================================

    def spread_flood(self):

        new_flood = []

        for x,y in self.flood_locations:

            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:

                    if self.grid[nx][ny] == EMPTY:

                        self.grid[nx][ny] = FLOOD
                        new_flood.append((nx,ny))

        self.flood_locations.extend(new_flood)

    # =====================================

    def get_survivor_count(self):
        return len(self.survivor_locations)

    def get_drone_positions(self):

        positions=[]

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                if self.grid[i][j]==DRONE:
                    positions.append((i,j))

        return positions

    def display(self):

        print("\n====== DISASTER MAP ======\n")

        for row in self.grid:
            print(" ".join(row))