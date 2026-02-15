"""
Snake Game - A classic arcade game built with Pygame
Author: Roba SH
Date: 2026
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    """Snake class to manage snake behavior"""
    
    def __init__(self):
        """Initialize the snake with 3 blocks in the middle of the screen"""
        self.reset()
    
    def reset(self):
        """Reset the snake to starting position"""
        self.body = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        """Move the snake in the current direction"""
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def check_collision(self):
        """Check if snake hits walls or itself"""
        head = self.body[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Check self collision (ignore head)
        if head in self.body[1:]:
            return True
        
        return False
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent going back on itself)"""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def eat_food(self, food_pos):
        """Check if snake eats food and grow"""
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

def generate_food(snake_body):
    """Generate food at random position not occupied by snake"""
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake_body:
            return food_pos

def draw_snake(screen, snake_body):
    """Draw the snake on the screen"""
    for i, segment in enumerate(snake_body):
        x = segment[0] * GRID_SIZE
        y = segment[1] * GRID_SIZE
        
        # Make head slightly different shade
        color = DARK_GREEN if i == 0 else GREEN
        
        # Draw segment with a small border effect
        pygame.draw.rect(screen, color, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
        pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

def display_score(screen, score):
    """Display current score on screen"""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(screen, score):
    """Display game over screen with play again options"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    game_over_text = font_large.render('GAME OVER', True, RED)
    score_text = font_small.render(f'Final Score: {score}', True, WHITE)
    continue_text = font_small.render('Press C to Play Again or Q to Quit', True, WHITE)
    
    # Center text
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True  # Play again
                if event.key == pygame.K_q:
                    return False  # Quit

def game_loop():
    """Main game loop"""
    # Set up the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    # Game variables
    snake = Snake()
    food_pos = generate_food(snake.body)
    score = 0
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
        
        # Game logic
        snake.move()
        
        # Check collision
        if snake.check_collision():
            # Show game over screen and get player choice
            play_again = game_over_screen(screen, score)
            if play_again:
                return True  # Restart game
            else:
                return False  # Quit game
        
        # Check food collision
        if snake.eat_food(food_pos):
            score += 1
            food_pos = generate_food(snake.body)
        
        # Drawing
        screen.fill(BLACK)  # Clear screen with black background
        
        # Draw grid lines (optional, for better visibility)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))
        
        # Draw food
        food_rect = pygame.Rect(food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, 
                                GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        pygame.draw.rect(screen, BLACK, food_rect, 1)  # Border
        
        # Draw snake
        draw_snake(screen, snake.body)
        
        # Display score
        display_score(screen, score)
        
        # Update display
        pygame.display.flip()
        
        # Control game speed
        clock.tick(FPS)
    
    return False  # Quit game

def main():
    """Main function to run the game"""
    print("=" * 50)
    print("Welcome to Snake Game!")
    print("=" * 50)
    print("\nInstructions:")
    print("- Use arrow keys to control the snake")
    print("- Eat red food to grow and increase score")
    print("- Avoid hitting walls or yourself")
    print("\nStarting game...\n")
    
    # Keep playing until player quits
    playing = True
    while playing:
        playing = game_loop()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()