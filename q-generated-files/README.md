# Burger Stacker

A color-matching memory game where players recreate color patterns from bottom to top within a time limit.

## Game Description

In Burger Stacker, you'll be presented with a colorful burger stack on the left side of the screen. Your goal is to recreate this pattern by pressing the corresponding color keys in the correct order, building your burger from bottom to top. Each correctly matched stack earns you points equal to the number of layers in the stack. The game lasts for 60 seconds, and your objective is to match as many stacks as possible to achieve the highest score!

## Installation

1. Make sure you have Python 3.6+ installed on your system
2. Clone or download this repository
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Run

Run the game using Python:

```bash
python burger_stacker.py
```

Or if you're on Unix/Linux/Mac:

```bash
chmod +x burger_stacker.py
./burger_stacker.py
```

## Game Controls

- **Q**: Add a red layer
- **W**: Add a yellow layer
- **E**: Add a blue layer
- **R**: Add a green layer
- **BACKSPACE**: Remove the topmost layer from your stack
- **ENTER**: Submit your stack for matching
- **SPACE**: Restart the game (after game over)

## Game Rules

1. Match the target burger pattern shown on the left side of the screen
2. Build your burger from bottom to top using the color keys
3. Each correctly matched stack earns points equal to the number of layers
4. You must match the pattern exactly - no partial points
5. The game lasts for 60 seconds
6. Your high score is saved between sessions

## System Requirements

- Python 3.6+
- PyGame library
- Minimum screen resolution: 800x600
- Keyboard input

## Game Features

- Visual representation of target and player burger stacks
- Arcade-style color buttons with key labels
- Score tracking and high score persistence
- 60-second time limit with countdown
- Simple and intuitive controls
