import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 15
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sand Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (0, 0, 0)
YELLOW = (255, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SAND1 = (210, 180, 140)
SAND2 = (169, 142, 107)
GRAY = (100, 100, 100)

COLOR = (255, 200, 0)  # current drawing color
sand_choice = [SAND1, SAND2]
# Grid size
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# 2D grid: 0 = empty, 1 = sand
grid = [[0 for i in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]

# List of sand particles: [x, y, color]
particles = []

# how to use: display_text("text", text_font, (R, G, B), x, y)
text_font = pygame.font.SysFont('Arial', 30)
large_font = pygame.font.SysFont('Arial', 60)

def display_text(text, font, text_col, x, y):
    dr_text = font.render(text, True, text_col)
    screen.blit(dr_text, (x, y))

mode = "main"
# bools
st = False
rand = False
sand = True

# Variables for custom color input
custom_color_text = ""
custom_error = ""

# Main loop
while True:
    if mode == "main":
        screen.fill(GRAY)

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
                for x, y, col in old_particles:
                    if x < GRID_WIDTH and y < GRID_HEIGHT:
                        grid[x][y] = 1
                        particles.append([x, y, col])

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
                if rand == True:
                    rand = False
                sand = not sand
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                if sand == True or rand == True:
                    sand = False
                    rand = False
                COLOR = (255, 200, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                if sand == True or rand == True:
                    sand = False
                    rand = False
                COLOR = (255, 0, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                if sand == True or rand == True:
                    sand = False
                    rand = False
                COLOR = (0, 0, 255)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                if sand == True or rand == True:
                    sand = False
                    rand = False
                COLOR = (0, 255, 0)
            
            # rgb randomizer
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                if sand == True:
                    sand = False
                    rand = False
                rand = not rand
            # custom color
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                if sand == True or rand == True:
                    sand = False
                    rand = False   
                mode = "cust"

        if st:
            display_text("1=SAND 2=YELLOW 3=RED 4=BLUE 5=GREEN 6=RANDOM 7=CUSTOM", text_font, (GREEN), 0, 0)

        # Add new sand with mouse
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            cell_x = mx // CELL_SIZE
            cell_y = my // CELL_SIZE
            if cell_x < GRID_WIDTH and cell_y < GRID_HEIGHT:
                if grid[cell_x][cell_y] == 0:
                    grid[cell_x][cell_y] = 1
                    particles.append([cell_x, cell_y, COLOR])  # store color!

        # Update particles
        for particle in particles:
            x, y, col = particle

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
        for x, y, col in particles:
            pygame.draw.rect(screen, col, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Randomize drawing color if active
        if rand:
            COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # sand color
        if sand:
            COLOR = random.choice(sand_choice)

        pygame.display.flip()
        clock.tick(60)

    elif mode == "cust":
        # Custom color input screen
        screen.fill(GRAY)

        display_text("Enter RGB values as R,G,B", text_font, WHITE, 50, 40)
        display_text("Example: 255,200,0", text_font, WHITE, 50, 80)

        display_text(custom_color_text, large_font, WHITE, 50, 150)

        if custom_error != "":
            display_text(custom_error, text_font, RED, 50, 220)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ESC = return to main mode
                if event.key == pygame.K_ESCAPE:
                    custom_color_text = ""
                    custom_error = ""
                    mode = "main"

                # Backspace
                elif event.key == pygame.K_BACKSPACE:
                    custom_color_text = custom_color_text[:-1]

                # Enter = try to set new color
                elif event.key == pygame.K_RETURN:
                    try:
                        r, g, b = map(int, custom_color_text.split(","))
                        COLOR = (r, g, b)
                        custom_color_text = ""
                        custom_error = ""
                        mode = "main"
                    except:
                        custom_error = "Invalid format! Use: R,G,B"
                        custom_color_text = ""

                else:
                    custom_color_text += event.unicode

        pygame.display.flip()
        clock.tick(60)
