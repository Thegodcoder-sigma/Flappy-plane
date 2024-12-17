import pygame
import sys
import os

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Plane beta/")

logo_path = r"C:\Users\Asus\Downloads\logo.png"
plane_path = r"C:\Users\Asus\Downloads\plane.png"

if os.path.exists(logo_path):
    logo = pygame.image.load(logo_path)
    pygame.display.set_icon(logo)
else:
    print("Logo file not found")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (135, 206, 250)
red = (255, 0, 0)
gray = (200, 200, 200)
green = (34, 139, 34)

button_color = (100, 149, 237)
button_hover = (70, 130, 180)
button_text_color = white

ground_height = 50

about_text = "This game was created for fun. Fly the plane and avoid obstacles!"
instructions_text = "Instructions: Use SPACE to jump. Don't hit the obstacles!"

def draw_text(text, x, y, color, font):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, x + 10, y + 10, button_text_color, font)

def about_screen():
    running = True
    while running:
        screen.fill(white)
        draw_text("About", 300, 50, black, font)
        draw_text(about_text, 50, 150, black, font)
        draw_button("Back", 350, 700, 100, 50, button_color, button_hover, main_menu)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def instructions_screen():
    running = True
    while running:
        screen.fill(white)
        draw_text("Instructions", 250, 50, black, font)
        draw_text(instructions_text, 50, 150, black, font)
        draw_button("Back", 350, 700, 100, 50, button_color, button_hover, main_menu)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_menu():
    running = True
    while running:
        screen.fill(blue)
        draw_text("Flappy Plane", 300, 50, white, font)
        draw_button("Play", 350, 300, 100, 50, button_color, button_hover, game_loop)
        draw_button("About", 350, 400, 100, 50, button_color, button_hover, about_screen)
        draw_button("Instructions", 350, 500, 190, 50, button_color, button_hover, instructions_screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_loop():
    plane_x = 100
    plane_y = 300
    plane_speed = 0
    gravity = 0.5
    jump_strength = -10
    obstacle_x = 800
    obstacle_width = 50
    obstacle_gap = 250
    obstacle_speed = 4
    plane = None
    score = 0  # Initialize score
    passed_obstacle = False  # To track if the plane passed an obstacle

    if os.path.exists(plane_path):
        plane = pygame.image.load(plane_path).convert_alpha()
        plane = pygame.transform.scale(plane, (50, 40))  # Resize plane to 50x40
    else:
        print("Plane image not found")

    running = True
    while running:
        screen.fill(blue)
        pygame.draw.rect(screen, green, (0, screen_height - ground_height, screen_width, ground_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    plane_speed = jump_strength

        plane_speed += gravity
        plane_y += plane_speed

        obstacle_x -= obstacle_speed
        if obstacle_x + obstacle_width < plane_x and not passed_obstacle:
            score += 1
            passed_obstacle = True

        if obstacle_x < -obstacle_width:
            obstacle_x = screen_width
            obstacle_gap = 250
            passed_obstacle = False

        if plane:
            screen.blit(plane, (plane_x, plane_y))
        else:
            pygame.draw.rect(screen, red, (plane_x, plane_y, 30, 30))

        pygame.draw.rect(screen, black, (obstacle_x, 0, obstacle_width, 300))
        pygame.draw.rect(screen, black, (obstacle_x, 300 + obstacle_gap, obstacle_width, screen_height - 300 - obstacle_gap - ground_height))

        draw_text(f"Score: {score}", 10, 10, white, font)

        if plane_y > screen_height - ground_height or plane_y < 0 or (
            plane_x + 50 > obstacle_x and plane_x < obstacle_x + obstacle_width and (
                plane_y < 300 or plane_y + 40 > 300 + obstacle_gap)):
            draw_text("Game Over", 300, 400, white, font)
            pygame.display.update()
            pygame.time.wait(2000)
            main_menu()

        pygame.display.update()
        clock.tick(60)

main_menu()
