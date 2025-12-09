
import unittest
from unittest.mock import Mock, patch
from enum import Enum
from collections import namedtuple
import sys

# Mock pygame before importing snake_game
mock_pygame = Mock()
sys.modules['pygame'] = mock_pygame

# Setup mock constants and classes
mock_pygame.init = Mock()
mock_pygame.display.set_mode = Mock()
mock_pygame.display.set_caption = Mock()
mock_pygame.time.Clock = Mock()
mock_pygame.font.Font = Mock()
mock_pygame.event.get = Mock(return_value=[])
mock_pygame.QUIT = 1
mock_pygame.KEYDOWN = 2
mock_pygame.K_LEFT = 3
mock_pygame.K_RIGHT = 4
mock_pygame.K_UP = 5
mock_pygame.K_DOWN = 6
mock_pygame.K_q = 7
mock_pygame.K_c = 8
mock_pygame.Rect = Mock()
mock_pygame.draw.rect = Mock()

# Import the game module after mocking
import snake_game
from snake_game import SnakeGame, Direction, Point, BLOCK_SIZE

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_pygame.reset_mock()
        self.game = SnakeGame()

    def test_initialization(self):
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(self.game.head, self.game.snake[0])
        # Check snake is horizontal
        self.assertEqual(self.game.snake[1].x, self.game.head.x - BLOCK_SIZE)
        self.assertEqual(self.game.snake[2].x, self.game.head.x - 2 * BLOCK_SIZE)

    def test_move_right(self):
        start_x = self.game.head.x
        start_y = self.game.head.y
        self.game._move(Direction.RIGHT)
        self.assertEqual(self.game.head.x, start_x + BLOCK_SIZE)
        self.assertEqual(self.game.head.y, start_y)

    def test_move_left(self):
        start_x = self.game.head.x
        start_y = self.game.head.y
        self.game._move(Direction.LEFT)
        self.assertEqual(self.game.head.x, start_x - BLOCK_SIZE)
        self.assertEqual(self.game.head.y, start_y)

    def test_move_up(self):
        start_x = self.game.head.x
        start_y = self.game.head.y
        self.game._move(Direction.UP)
        self.assertEqual(self.game.head.x, start_x)
        self.assertEqual(self.game.head.y, start_y - BLOCK_SIZE)

    def test_move_down(self):
        start_x = self.game.head.x
        start_y = self.game.head.y
        self.game._move(Direction.DOWN)
        self.assertEqual(self.game.head.x, start_x)
        self.assertEqual(self.game.head.y, start_y + BLOCK_SIZE)

    def test_collision_wall(self):
        # Right wall
        self.game.head = Point(self.game.width, 100)
        self.assertTrue(self.game._is_collision())
        
        # Left wall
        self.game.head = Point(-BLOCK_SIZE, 100)
        self.assertTrue(self.game._is_collision())
        
        # Top wall
        self.game.head = Point(100, -BLOCK_SIZE)
        self.assertTrue(self.game._is_collision())
        
        # Bottom wall
        self.game.head = Point(100, self.game.height)
        self.assertTrue(self.game._is_collision())

    def test_collision_self(self):
        self.game.score = 3
        self.game.snake = [
            Point(100, 100),
            Point(120, 100),
            Point(120, 120),
            Point(100, 120),
            Point(100, 100)  # Loop back to head
        ]
        self.game.head = self.game.snake[0]
        # We need to test if collision checks against body (snake[1:])
        # Set head to be same as snake[4]
        self.game.head = Point(100, 100) 
        # But _is_collision checks self.head against snake[1:]
        # Let's set the list manually to simulate the loop
        # snake = [Head(100,100), Body(100,120), Body(120,120), Body(120,100), Body(100,100)]
        # This represents the state AFTER move but BEFORE popping tail? 
        # Or simply: if head is in body list.
        self.game.snake = [Point(100, 100), Point(100, 120), Point(100, 100)]
        self.game.head = self.game.snake[0]
        self.assertTrue(self.game._is_collision())

    def test_play_step_eat_food(self):
        # Place food right in front of snake
        next_x = self.game.head.x + BLOCK_SIZE
        next_y = self.game.head.y
        self.game.food = Point(next_x, next_y)
        
        initial_score = self.game.score
        initial_len = len(self.game.snake)
        
        # Mock event (empty)
        mock_pygame.event.get.return_value = []
        
        game_over, score = self.game.play_step()
        
        self.assertFalse(game_over)
        self.assertEqual(score, initial_score + 1)
        self.assertEqual(len(self.game.snake), initial_len + 1)
        self.assertEqual(self.game.head, Point(next_x, next_y))

    def test_play_step_move_no_eat(self):
        # Ensure food is NOT in front
        next_x = self.game.head.x + BLOCK_SIZE
        next_y = self.game.head.y
        self.game.food = Point(next_x + 100, next_y) # Far away
        
        initial_score = self.game.score
        initial_len = len(self.game.snake)
        
        mock_pygame.event.get.return_value = []
        
        game_over, score = self.game.play_step()
        
        self.assertFalse(game_over)
        self.assertEqual(score, initial_score)
        self.assertEqual(len(self.game.snake), initial_len) # Should pop tail, so length constant
        self.assertEqual(self.game.head, Point(next_x, next_y))

    def test_game_over_collision(self):
        # Move right into wall
        self.game.head = Point(self.game.width - BLOCK_SIZE, 100)
        self.game.direction = Direction.RIGHT
        
        mock_pygame.event.get.return_value = []
        
        game_over, score = self.game.play_step()
        
        self.assertTrue(game_over)

    # ==================== NEW TEST CASES ====================

    def test_cannot_reverse_direction_right_to_left(self):
        """Snake cannot reverse direction from RIGHT to LEFT"""
        self.game.direction = Direction.RIGHT
        mock_event = Mock()
        mock_event.type = mock_pygame.KEYDOWN
        mock_event.key = mock_pygame.K_LEFT
        mock_pygame.event.get.return_value = [mock_event]
        
        self.game.food = Point(9999, 9999)  # Far away to avoid eating
        self.game.play_step()
        
        # Direction should remain RIGHT, not change to LEFT
        self.assertEqual(self.game.direction, Direction.RIGHT)

    def test_cannot_reverse_direction_left_to_right(self):
        """Snake cannot reverse direction from LEFT to RIGHT"""
        self.game.direction = Direction.LEFT
        mock_event = Mock()
        mock_event.type = mock_pygame.KEYDOWN
        mock_event.key = mock_pygame.K_RIGHT
        mock_pygame.event.get.return_value = [mock_event]
        
        self.game.food = Point(9999, 9999)
        self.game.head = Point(200, 200)  # Safe position
        self.game.play_step()
        
        self.assertEqual(self.game.direction, Direction.LEFT)

    def test_cannot_reverse_direction_up_to_down(self):
        """Snake cannot reverse direction from UP to DOWN"""
        self.game.direction = Direction.UP
        mock_event = Mock()
        mock_event.type = mock_pygame.KEYDOWN
        mock_event.key = mock_pygame.K_DOWN
        mock_pygame.event.get.return_value = [mock_event]
        
        self.game.food = Point(9999, 9999)
        self.game.head = Point(200, 200)
        self.game.play_step()
        
        self.assertEqual(self.game.direction, Direction.UP)

    def test_cannot_reverse_direction_down_to_up(self):
        """Snake cannot reverse direction from DOWN to UP"""
        self.game.direction = Direction.DOWN
        mock_event = Mock()
        mock_event.type = mock_pygame.KEYDOWN
        mock_event.key = mock_pygame.K_UP
        mock_pygame.event.get.return_value = [mock_event]
        
        self.game.food = Point(9999, 9999)
        self.game.head = Point(200, 200)
        self.game.play_step()
        
        self.assertEqual(self.game.direction, Direction.DOWN)

    def test_valid_direction_change(self):
        """Snake CAN change to perpendicular direction"""
        self.game.direction = Direction.RIGHT
        mock_event = Mock()
        mock_event.type = mock_pygame.KEYDOWN
        mock_event.key = mock_pygame.K_UP
        mock_pygame.event.get.return_value = [mock_event]
        
        self.game.food = Point(9999, 9999)
        self.game.play_step()
        
        self.assertEqual(self.game.direction, Direction.UP)

    def test_food_not_on_snake(self):
        """Food should never spawn on the snake's body"""
        # Make a longer snake
        self.game.snake = [Point(x * BLOCK_SIZE, 100) for x in range(10)]
        self.game.head = self.game.snake[0]
        
        for _ in range(50):  # Run multiple times due to randomness
            self.game._place_food()
            self.assertNotIn(self.game.food, self.game.snake)

    def test_food_within_bounds(self):
        """Food should always spawn within game boundaries"""
        for _ in range(50):
            self.game._place_food()
            self.assertGreaterEqual(self.game.food.x, 0)
            self.assertLess(self.game.food.x, self.game.width)
            self.assertGreaterEqual(self.game.food.y, 0)
            self.assertLess(self.game.food.y, self.game.height)

    def test_reset_restores_initial_state(self):
        """Reset should restore game to initial state"""
        # Modify game state
        self.game.score = 50
        self.game.direction = Direction.UP
        self.game.snake = [Point(0, 0)]
        self.game.head = Point(0, 0)
        
        self.game.reset()
        
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(len(self.game.snake), 3)
        self.assertEqual(self.game.head, self.game.snake[0])
        self.assertIsNotNone(self.game.food)

    def test_reset_preserves_scores(self):
        """Reset should not affect best_score and last_score"""
        self.game.best_score = 100
        self.game.last_score = 50
        
        self.game.reset()
        
        self.assertEqual(self.game.best_score, 100)
        self.assertEqual(self.game.last_score, 50)

    def test_no_collision_valid_position(self):
        """No collision when snake is in valid position"""
        self.game.head = Point(100, 100)
        self.game.snake = [self.game.head, Point(80, 100), Point(60, 100)]
        self.assertFalse(self.game._is_collision())

    def test_collision_at_exact_boundary_top_left(self):
        """No collision at top-left corner (valid position)"""
        self.game.head = Point(0, 0)
        self.game.snake = [self.game.head]
        self.assertFalse(self.game._is_collision())

    def test_collision_at_exact_boundary_bottom_right(self):
        """No collision at bottom-right valid position"""
        self.game.head = Point(self.game.width - BLOCK_SIZE, self.game.height - BLOCK_SIZE)
        self.game.snake = [self.game.head]
        self.assertFalse(self.game._is_collision())

    def test_snake_body_follows_head(self):
        """Snake body correctly follows head after movement"""
        initial_head = self.game.head
        mock_pygame.event.get.return_value = []
        self.game.food = Point(9999, 9999)  # Far away
        
        self.game.play_step()
        
        # Previous head should now be second element in snake
        self.assertEqual(self.game.snake[1], initial_head)

    def test_is_collision_with_custom_point(self):
        """_is_collision works with custom point argument"""
        # Valid position
        self.assertFalse(self.game._is_collision(Point(100, 100)))
        
        # Out of bounds positions
        self.assertTrue(self.game._is_collision(Point(-10, 100)))
        self.assertTrue(self.game._is_collision(Point(100, -10)))
        self.assertTrue(self.game._is_collision(Point(self.game.width + 10, 100)))
        self.assertTrue(self.game._is_collision(Point(100, self.game.height + 10)))

    def test_is_collision_custom_point_with_snake_body(self):
        """_is_collision detects collision with snake body for custom point"""
        self.game.snake = [Point(100, 100), Point(120, 100), Point(140, 100)]
        self.game.head = self.game.snake[0]
        
        # Point colliding with snake body (not head)
        self.assertTrue(self.game._is_collision(Point(120, 100)))
        self.assertTrue(self.game._is_collision(Point(140, 100)))

    def test_best_score_updated_on_new_high(self):
        """Best score updates when current score exceeds it"""
        self.game.best_score = 5
        self.game.score = 10
        
        # Simulate what happens in main() after game over
        self.game.last_score = self.game.score
        if self.game.score > self.game.best_score:
            self.game.best_score = self.game.score
        
        self.assertEqual(self.game.best_score, 10)
        self.assertEqual(self.game.last_score, 10)

    def test_best_score_not_updated_on_lower_score(self):
        """Best score stays same when current score is lower"""
        self.game.best_score = 20
        self.game.score = 5
        
        self.game.last_score = self.game.score
        if self.game.score > self.game.best_score:
            self.game.best_score = self.game.score
        
        self.assertEqual(self.game.best_score, 20)
        self.assertEqual(self.game.last_score, 5)

    def test_snake_grows_when_eating_food(self):
        """Snake length increases by 1 when eating food"""
        initial_length = len(self.game.snake)
        next_pos = Point(self.game.head.x + BLOCK_SIZE, self.game.head.y)
        self.game.food = next_pos
        
        mock_pygame.event.get.return_value = []
        self.game.play_step()
        
        self.assertEqual(len(self.game.snake), initial_length + 1)

    def test_snake_length_unchanged_when_not_eating(self):
        """Snake length stays same when not eating food"""
        initial_length = len(self.game.snake)
        self.game.food = Point(9999, 9999)  # Far away
        
        mock_pygame.event.get.return_value = []
        self.game.play_step()
        
        self.assertEqual(len(self.game.snake), initial_length)


class TestScorePersistence(unittest.TestCase):
    """Tests for score loading and saving functionality"""

    def setUp(self):
        mock_pygame.reset_mock()

    @patch('os.path.exists', return_value=False)
    def test_load_scores_no_file(self, mock_exists):
        """Scores default to 0 when no file exists"""
        game = SnakeGame()
        self.assertEqual(game.best_score, 0)
        self.assertEqual(game.last_score, 0)

    @patch('builtins.open', side_effect=IOError("Cannot read file"))
    @patch('os.path.exists', return_value=True)
    def test_load_scores_io_error(self, mock_exists, mock_open):
        """Handles IOError gracefully when reading scores"""
        game = SnakeGame()
        self.assertEqual(game.best_score, 0)
        self.assertEqual(game.last_score, 0)

    @patch('builtins.open')
    @patch('os.path.exists', return_value=True)
    def test_load_scores_corrupted_data(self, mock_exists, mock_open):
        """Handles corrupted score data gracefully"""
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        mock_file.readlines.return_value = ['not_a_number\n', 'also_bad\n']
        mock_open.return_value = mock_file
        
        game = SnakeGame()
        self.assertEqual(game.best_score, 0)
        self.assertEqual(game.last_score, 0)

    @patch('builtins.open')
    @patch('os.path.exists', return_value=True)
    def test_load_scores_incomplete_file(self, mock_exists, mock_open):
        """Handles incomplete score file (less than 2 lines)"""
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        mock_file.readlines.return_value = ['10\n']  # Only one line
        mock_open.return_value = mock_file
        
        game = SnakeGame()
        # Should keep default values since file is incomplete
        self.assertEqual(game.best_score, 0)
        self.assertEqual(game.last_score, 0)


if __name__ == '__main__':
    unittest.main()
