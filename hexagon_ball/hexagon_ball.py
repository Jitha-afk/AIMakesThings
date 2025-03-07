import pygame
import pymunk
import sys
import math

# Initialize Pygame and Pymunk
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Rolling in Hexagon")

# Setup Pymunk space
space = pymunk.Space()
space.gravity = (0, 981)  # Gravity in pixels/s^2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create hexagon vertices
hex_size = 200
center_x = WIDTH // 2
center_y = HEIGHT // 2
vertices = []
for i in range(6):
    angle = i * math.pi / 3
    x = center_x + hex_size * math.cos(angle)
    y = center_y + hex_size * math.sin(angle)
    vertices.append((x, y))

# Create hexagon segments in Pymunk
segments = []
for i in range(6):
    start = vertices[i]
    end = vertices[(i + 1) % 6]
    segment = pymunk.Segment(space.static_body, start, end, 5)
    segment.elasticity = 0.95
    segment.friction = 0.5
    segments.append(segment)
    space.add(segment)

# Create ball
ball_mass = 1
ball_radius = 20
ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
ball_body = pymunk.Body(ball_mass, ball_moment)
ball_body.position = center_x, center_y
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = 0.95
ball_shape.friction = 0.5
space.add(ball_body, ball_shape)

# Add initial impulse to the ball
impulse = (5000, 0)
ball_body.apply_impulse_at_local_point(impulse)

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Apply random impulse on spacebar press
                impulse = (5000 * (2 * math.random() - 1), 5000 * (2 * math.random() - 1))
                ball_body.apply_impulse_at_local_point(impulse)

    # Update physics
    space.step(1/60.0)

    # Clear screen
    screen.fill(WHITE)

    # Draw hexagon
    for segment in segments:
        pygame.draw.line(screen, BLACK, segment.a, segment.b, 5)

    # Draw ball
    ball_pos = ball_body.position
    pygame.draw.circle(screen, RED, (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)