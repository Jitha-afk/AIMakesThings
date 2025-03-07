import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

# Initialize game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def move(self):
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'

        head = list(self.body[0])
        if self.direction == 'RIGHT':
            head[0] += BLOCK_SIZE
        elif self.direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif self.direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            head[1] += BLOCK_SIZE

        self.body.insert(0, tuple(head))

    def grow(self):
        self.score += 1

    def check_collision(self):
        head = self.body[0]
        return (
            head[0] < 0 or
            head[0] >= WINDOW_WIDTH or
            head[1] < 0 or
            head[1] >= WINDOW_HEIGHT or
            head in self.body[1:]
        )

class Food:
    def __init__(self):
        self.position = self.get_random_position()

    def get_random_position(self):
        x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
        y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
        return (x, y)

    def respawn(self):
        self.position = self.get_random_position()

def main():
    snake = Snake()
    food = Food()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_to = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    snake.change_to = 'LEFT'
                elif event.key == pygame.K_UP:
                    snake.change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    snake.change_to = 'DOWN'

        snake.move()

        # Check if snake ate food
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()
        else:
            snake.body.pop()

        # Check collision
        if snake.check_collision():
            game_over = True

        # Draw everything
        window.fill(BLACK)
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(window, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw food
        pygame.draw.rect(window, RED, (food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        window.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)  # Control game speed

    pygame.quit()

if __name__ == '__main__':
    main()