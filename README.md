# Snake Game

A classic Snake game implementation in Python using Pygame.

## Description

This is a simple implementation of the classic Snake game. Control the snake to eat food, grow longer, and avoid hitting the walls or your own tail. The game gets progressively harder as your snake grows longer!

## Features

- Classic snake gameplay
- Score tracking
- Collision detection (walls and self)
- Colorful graphics
- Game over screen with restart option
- Smooth controls

## Installation

1. Make sure you have Python 3.6 or higher installed on your system.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install pygame directly:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python snake_game.py
   ```

2. Use the arrow keys to control the snake:
   - **↑ (UP)** - Move up
   - **↓ (DOWN)** - Move down
   - **← (LEFT)** - Move left
   - **→ (RIGHT)** - Move right

3. Eat the red food blocks to grow your snake and increase your score.

4. Avoid hitting the walls or your own tail!

5. When the game is over:
   - Press **C** to play again
   - Press **Q** to quit

## Game Rules

- The snake starts with a length of 3 blocks
- Each food item increases your score by 1 and makes the snake grow by 1 block
- You cannot move in the opposite direction (e.g., if moving right, you can't immediately move left)
- The game ends when the snake hits a wall or collides with itself

## Technical Details

- **Display Size**: 640x480 pixels
- **Block Size**: 20x20 pixels
- **Game Speed**: 15 FPS
- **Colors**: 
  - Background: Black
  - Snake Head: Dark Green
  - Snake Body: Green
  - Food: Red
  - Score Text: White

## Requirements

- Python 3.6+
- Pygame 2.0.0+

## License

This is a simple educational project. Feel free to use and modify it as you wish!

Enjoy playing! 🐍
