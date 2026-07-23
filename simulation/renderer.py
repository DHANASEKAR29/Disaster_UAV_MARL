import pygame
import os

CELL = 50
OFFSET = 20


class Renderer:

    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 14, bold=True)

        DOWNLOADS = r"C:\Users\vdhan\Downloads"

        def load(filename):

            path = os.path.join(DOWNLOADS, filename)

            print("=" * 60)
            print("Loading :", path)

            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found:\n{path}")

            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (CELL, CELL))

        # Terrain
        self.grass = load("grass.png")
        self.road = load("road.png")
        self.tree = load("tree.png")
        self.building = load("building.png")
        self.hospital = load("hospital.png")
        self.charging = load("charging_station.png")

        # Disaster Effects
        self.fire = load("fire.png")
        self.smoke = load("smoke.png")
        self.flood = load("flood.png")

        # Survivor
        self.survivor = load("survivor.png")

        # Drone
        self.drone = load("drone_blue.png")

    def draw_environment(self, env, drones):

        rows = len(env.grid)
        cols = len(env.grid[0])

        self.screen.fill((40, 40, 40))

        for i in range(rows):
            for j in range(cols):

                x = OFFSET + j * CELL
                y = OFFSET + i * CELL

                # Default Grass
                self.screen.blit(self.grass, (x, y))

                value = env.grid[i][j]

                if value == "R":
                    self.screen.blit(self.road, (x, y))

                elif value == "T":
                    self.screen.blit(self.tree, (x, y))

                elif value == "X":
                    self.screen.blit(self.building, (x, y))

                elif value == "H":
                    self.screen.blit(self.hospital, (x, y))

                elif value == "C":
                    self.screen.blit(self.charging, (x, y))

                elif value == "F":
                    self.screen.blit(self.fire, (x, y))

                elif value == "M":
                    self.screen.blit(self.smoke, (x, y))

                elif value == "W":
                    self.screen.blit(self.flood, (x, y))

                elif value == "S":
                    self.screen.blit(self.survivor, (x, y))

                pygame.draw.rect(
                    self.screen,
                    (80, 80, 80),
                    (x, y, CELL, CELL),
                    1
                )

        # Draw Drones
        for drone in drones:

            x = OFFSET + drone.y * CELL
            y = OFFSET + drone.x * CELL

            self.screen.blit(self.drone, (x, y))

            label = self.font.render(
                drone.drone_id,
                True,
                (255, 255, 255)
            )

            self.screen.blit(label, (x + 10, y + 15))