import pygame
import random

# Initialize PyGame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Pet class
class DesktopPet:
    def __init__(self):
        self.image = pygame.image.load('pet_image.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)  # Start position
        self.speed = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        # Move pet randomly
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.rect.y -= self.speed
        elif direction == 'down':
            self.rect.y += self.speed
        elif direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed

        # Keep pet within screen bounds
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def handle_events(self, event):
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.rect.center = event.pos  # Move pet to clicked position

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Desktop Pet')

# Create pet instance
pet = DesktopPet()

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pet.handle_events(event)

    pet.update()

    # Draw everything
    screen.fill(WHITE)
    pet.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit PyGame
pygame.quit()
