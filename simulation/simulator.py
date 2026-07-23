import pygame
from simulation.renderer import Renderer
from simulation.dashboard import Dashboard


class Simulator:

    def __init__(self, environment):

        pygame.init()

        self.environment = environment

        self.width = 1200
        self.height = 700

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("UAV Swarm Search & Rescue")

        self.clock = pygame.time.Clock()

        self.renderer = Renderer(self.screen)
        self.dashboard = Dashboard(self.screen)

    def update(self, drones, coverage):

        self.clock.tick(5)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.screen.fill((240, 240, 240))

        self.renderer.draw_environment(
            self.environment,
            drones
        )

        self.dashboard.draw(
            drones,
            coverage
        )

        pygame.display.flip()