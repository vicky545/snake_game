import pygame
import random
import os
from enum import Enum
from collections import namedtuple

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_GREEN = (0, 200, 0)

# Define directions
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Define Point
Point = namedtuple('Point', 'x, y')

# Game settings
BLOCK_SIZE = 20
SPEED = 8

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        # Initialize display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Load scores from file
        self.best_score = 0
        self.last_score = 0
        self._load_scores()
        
        # Initialize game state
        self.reset()
    
    def _load_scores(self):
        """Load best score and last score from scores.txt file"""
        if os.path.exists('scores.txt'):
            try:
                with open('scores.txt', 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.best_score = int(lines[0].strip())
                        self.last_score = int(lines[1].strip())
            except (ValueError, IOError):
                # If file is corrupted or can't be read, start with default values
                self.best_score = 0
                self.last_score = 0
    
    def _save_scores(self):
        """Save best score and last score to scores.txt file"""
        try:
            with open('scores.txt', 'w') as f:
                f.write(f"{self.best_score}\n")
                f.write(f"{self.last_score}\n")
        except IOError:
            # If we can't write to file, just continue without saving
            pass
    
    def reset(self):
        """Reset the game to initial state"""
        self.direction = Direction.RIGHT
        
        # Start snake in the middle
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        """Place food at random location not occupied by snake"""
        while True:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = Point(x, y)
            if self.food not in self.snake:
                break
    
    def play_step(self):
        """Execute one game step"""
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        
        # 2. Move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        return game_over, self.score
    
    def _is_collision(self, point=None):
        """Check if snake collides with walls or itself"""
        if point is None:
            point = self.head
        
        # Check boundary collision
        if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
            return True
        
        # Check self collision
        if point in self.snake[1:]:
            return True
        
        return False
    
    def _move(self, direction):
        """Move snake head in given direction"""
        x = self.head.x
        y = self.head.y
        
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)
    
    def _update_ui(self):
        """Update game display"""
        self.display.fill(BLACK)
        
        # Draw snake
        for i, point in enumerate(self.snake):
            if i == 0:  # Head
                pygame.draw.rect(self.display, DARK_GREEN, 
                               pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            else:  # Body
                pygame.draw.rect(self.display, GREEN, 
                               pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw food
        pygame.draw.rect(self.display, RED, 
                        pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw scores
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(score_text, [10, 10])
        
        last_score_text = self.font.render(f"Last: {self.last_score}", True, WHITE)
        self.display.blit(last_score_text, [10, 45])
        
        best_score_text = self.font.render(f"Best: {self.best_score}", True, WHITE)
        self.display.blit(best_score_text, [10, 80])
        
        pygame.display.flip()
    
    def game_over_screen(self):
        """Display game over screen"""
        game_over_text = self.font.render('Game Over!', True, RED)
        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press Q-Quit or C-Play Again', True, WHITE)
        
        text_rect1 = game_over_text.get_rect(center=(self.width/2, self.height/2 - 50))
        text_rect2 = score_text.get_rect(center=(self.width/2, self.height/2))
        text_rect3 = restart_text.get_rect(center=(self.width/2, self.height/2 + 50))
        
        self.display.blit(game_over_text, text_rect1)
        self.display.blit(score_text, text_rect2)
        self.display.blit(restart_text, text_rect3)
        pygame.display.flip()
        
        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False
                    if event.key == pygame.K_c:
                        return True
    
    def start_screen(self):
        """Display start screen with a button to start the game"""
        # Button dimensions and position
        button_width = 200
        button_height = 60
        button_x = (self.width - button_width) // 2
        button_y = (self.height - button_height) // 2
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        while True:
            self.display.fill(BLACK)
            
            # Draw title
            title_text = self.font.render('Snake Game', True, GREEN)
            title_rect = title_text.get_rect(center=(self.width/2, self.height/2 - 100))
            self.display.blit(title_text, title_rect)
            
            # Get mouse position to check hover
            mouse_pos = pygame.mouse.get_pos()
            mouse_over_button = button_rect.collidepoint(mouse_pos)
            
            # Draw button with hover effect
            button_color = BLUE if mouse_over_button else DARK_GREEN
            pygame.draw.rect(self.display, button_color, button_rect)
            pygame.draw.rect(self.display, WHITE, button_rect, 3)  # Button border
            
            # Draw button text
            button_text = self.font.render('Start Game', True, WHITE)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.display.blit(button_text, button_text_rect)
            
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if button_rect.collidepoint(event.pos):
                            return True
            
            self.clock.tick(30)  # Limit frame rate for start screen

def main():
    """Main game loop"""
    game = SnakeGame()
    
    # Show start screen
    start_game = game.start_screen()
    if not start_game:
        pygame.quit()
        return
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            # Update scores
            game.last_score = score
            if score > game.best_score:
                game.best_score = score
            
            # Save scores to file
            game._save_scores()
            
            play_again = game.game_over_screen()
            if play_again:
                game.reset()
            else:
                break
    
    pygame.quit()

if __name__ == '__main__':
    main()
