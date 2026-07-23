import pygame

pygame.init()

pygame.display.set_mode((100,100))

try:
    pygame.image.load(r"C:\Users\vdhan\Downloads\grass.png")
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)

pygame.quit()