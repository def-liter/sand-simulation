import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sand Simulation")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COLOR = (255, 200, 0)
# Grid size
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# 2D grid: 0 = empty, 1 = sand
grid = [[0 for i in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]

# List of sand particles
particles = []
# how to use: display_text("text", text_font, (R, G, B), x, y)
text_font = pygame.font.SysFont('Arial', 30)
large_font = pygame.font.SysFont('Arial', 60)
def display_text(text, font, text_col, x, y):
    dr_text = font.render(text, True, text_col)
    screen.blit(dr_text, (x, y))
# bools
st = False
rand = False
# Main loop
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():

        # resize case
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            old_particles = particles
            GRID_WIDTH = WIDTH // CELL_SIZE
            GRID_HEIGHT = HEIGHT // CELL_SIZE

            grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
            particles = []
            for x, y in old_particles:
                if x < GRID_WIDTH and y < GRID_HEIGHT:
                    grid[x][y] = 1
                    particles.append([x, y])

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            st = not st
        # clear screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            particles.clear()
            grid = [[0 for i in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]
        # change colors
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            COLOR = (255, 200, 0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            COLOR = (255, 0, 0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            COLOR = (0, 0, 255)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            COLOR = (0, 255, 0)
        # rgb randomizer
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            rand = not rand



    if st:
        display_text("1=YELLOW 2=RED 3=BLUE 4=GREEN 5=SWITCH", text_font, (GREEN), 0, 0)
    # Add new sand with mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        cell_x = mx // CELL_SIZE
        cell_y = my // CELL_SIZE
        if cell_x < GRID_WIDTH and cell_y < GRID_HEIGHT:
            if grid[cell_x][cell_y] == 0:
                grid[cell_x][cell_y] = 1
                particles.append([cell_x, cell_y])

    # Update particles
    for particle in particles:
        x, y = particle

        # Check if can move down
        if y + 1 < GRID_HEIGHT and grid[x][y + 1] == 0:
            grid[x][y] = 0
            grid[x][y + 1] = 1
            particle[1] += 1
        # Try down-left
        elif x > 0 and y + 1 < GRID_HEIGHT and grid[x - 1][y + 1] == 0:
            grid[x][y] = 0
            grid[x - 1][y + 1] = 1
            particle[0] -= 1
            particle[1] += 1
        # Try down-right
        elif x + 1 < GRID_WIDTH and y + 1 < GRID_HEIGHT and grid[x + 1][y + 1] == 0:
            grid[x][y] = 0
            grid[x + 1][y + 1] = 1
            particle[0] += 1
            particle[1] += 1

    # Draw particles
    for x, y in particles:
        if COLOR != (0, 0, 0) or (255, 255, 255):
            pygame.draw.rect(screen, COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if rand == True:
        COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        pass
    pygame.display.flip()
    clock.tick(60)

