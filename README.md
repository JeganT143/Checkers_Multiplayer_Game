# Multiplayer Checkers Game

## Overview
This project is a **multiplayer checkers game** implemented in Python. It utilizes network programming concepts to allow two players to compete against each other over a network connection. The game follows the traditional rules of checkers and provides a user-friendly graphical interface for an engaging experience.

## Features
- **Multiplayer Support:** Connect two players over a network.
- **Graphical User Interface (GUI):** Built using `pygame` for an interactive experience.
- **Turn-based System:** Ensures structured gameplay.
- **Game Logic Implementation:** Supports legal moves, capturing, and king promotions.
- **Real-time Communication:** Uses socket programming for smooth data exchange.
- **Match Status Handling:** The game ensures fair turns and handles disconnected players.

## Technologies Used
- **Python**: Core programming language.
- **Pygame**: For rendering the board and pieces.
- **Sockets**: For establishing client-server communication.
- **Pickle**: For serializing and deserializing game data.

## Project Structure
```
📂 multiplayer-checkers
│-- 📂 checkers
│   │-- __init__.py
│   │-- board.py
│   │-- constants.py
│   │-- piece.py
│-- 📂 network
│   │-- network.py
│-- server.py
│-- client.py
│-- manageGame.py
│-- README.md
```

## Installation and Setup
### Prerequisites
Ensure you have **Python 3.x** installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/multiplayer-checkers.git
cd multiplayer-checkers
```

### Step 2: Install Dependencies
```bash
pip install pygame
```

### Step 3: Running the Game
- **Start the server**
  ```bash
  python server.py
  ```
- **Start a client** (run this on both players' machines)
  ```bash
  python client.py
  ```
- Enter the **server IP address** when prompted.
- Enjoy the game!

## How It Works
1. The **server** script initializes a TCP socket and listens for incoming connections.
2. Two players connect to the **server** using the **client** script.
3. The **game state** is synchronized between both clients using socket communication.
4. The GUI updates after every move, ensuring real-time gameplay.

## Rules of the Game
- Players take turns moving their pieces diagonally.
- Capturing opponent pieces is mandatory when possible.
- Pieces reaching the last row are promoted to kings, which can move both forward and backward.
- The game ends when a player has no valid moves left.

## File Descriptions
- **`server.py`** - Manages game sessions, player connections, and network communication.
- **`client.py`** - Handles the graphical interface and player interactions.
- **`manageGame.py`** - Implements game logic and turn handling.
- **`network.py`** - Manages the client's connection to the server.
- **`checkers/board.py`** - Represents the game board and its logic.
- **`checkers/piece.py`** - Represents individual checkers pieces and their behavior.
- **`checkers/constants.py`** - Stores game-wide constants, such as colors and board size.


## Contributors
- **Your Name** - Developer
- **Your Team Members**

---
Happy Gaming! 🎮

