import pygame
import time


class Dashboard:

    def __init__(self, screen):

        self.screen = screen

        pygame.font.init()

        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.font = pygame.font.SysFont("Arial", 20)
        self.small = pygame.font.SysFont("Arial", 18)

        self.start_time = time.time()

    def battery_color(self, battery):

        if battery >= 70:
            return (0, 180, 0)      # Green

        elif battery >= 30:
            return (255, 165, 0)    # Orange

        else:
            return (220, 0, 0)      # Red

    def draw(self, drones, coverage):

        panel_x = 670
        panel_y = 10
        panel_w = 510
        panel_h = 680

        # Background Panel
        pygame.draw.rect(
            self.screen,
            (245, 245, 245),
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            (panel_x, panel_y, panel_w, panel_h),
            2,
            border_radius=10
        )

        # ======================
        # TITLE
        # ======================

        title = self.title_font.render(
            "Mission Dashboard",
            True,
            (20, 20, 120)
        )

        self.screen.blit(title, (panel_x + 90, 20))

        y = 80

        # ======================
        # Mission Time
        # ======================

        elapsed = int(time.time() - self.start_time)

        mins = elapsed // 60
        secs = elapsed % 60

        timer = self.font.render(
            f"Mission Time : {mins:02}:{secs:02}",
            True,
            (0, 0, 0)
        )

        self.screen.blit(timer, (panel_x + 20, y))

        y += 40

        # ======================
        # Coverage
        # ======================

        cov = self.font.render(
            f"Coverage : {coverage:.2f} %",
            True,
            (0, 140, 0)
        )

        self.screen.blit(cov, (panel_x + 20, y))

        y += 40

        # ======================
        # Active Drones
        # ======================

        active = sum(1 for d in drones if d.active)

        txt = self.font.render(
            f"Active Drones : {active}",
            True,
            (0, 0, 0)
        )

        self.screen.blit(txt, (panel_x + 20, y))

        y += 50

        pygame.draw.line(
            self.screen,
            (180, 180, 180),
            (panel_x + 10, y),
            (panel_x + panel_w - 10, y),
            2
        )

        y += 20

        subtitle = self.font.render(
            "Drone Status",
            True,
            (0, 0, 150)
        )

        self.screen.blit(subtitle, (panel_x + 20, y))

        y += 35

        # ======================
        # Drone Details
        # ======================

        for drone in drones:

            color = self.battery_color(drone.battery)

            pygame.draw.circle(
                self.screen,
                color,
                (panel_x + 18, y + 10),
                6
            )

            text = self.small.render(
                f"{drone.drone_id}   Battery: {drone.battery:3}%   Score: {drone.score}",
                True,
                (0, 0, 0)
            )

            self.screen.blit(text, (panel_x + 30, y))

            y += 28

            status = self.small.render(
                f"Status : {drone.status}",
                True,
                (80, 80, 80)
            )

            self.screen.blit(status, (panel_x + 45, y))

            y += 30