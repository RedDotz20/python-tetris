# 🐍 Python Tetris

A Tetris game built with Python programming language alongside with PyGame library.

## 🚀 Features 

- [x] Blocks (Tetrominoes): Tetris is built around tetrominoes, geometric shapes consisting of four square blocks each. These shapes fall from the top of the game area and can be rotated and moved horizontally as they descend.
- [x] Gameplay Mechanics: Players must manipulate the falling tetrominoes to create complete horizontal lines without any gaps. When a line is completed, it disappears, and any blocks above it will fall to fill the space. The game ends if the stack of tetrominoes reaches the top of the game area.
- [ ] Scoring System: Points are typically awarded for each line cleared, with more points given for clearing multiple lines simultaneously (known as a "Tetris"). The scoring system may also reward players for the speed at which they clear lines or for achieving certain milestones.
- [ ] Speed Increase: As players progress through the game, the falling speed of the tetrominoes typically increases, making the game more challenging over time.
- [ ] Level Progression: Tetris often features a level system where players advance to higher levels as they clear more lines. Advancing levels may bring increased speed or other changes to the gameplay.
- [ ] Hold Piece: Some versions of Tetris allow players to temporarily hold a tetromino, to be used strategically later.
- [x] Next Piece Preview: Many Tetris games offer a preview of the next tetromino that will appear, allowing players to plan their moves in advance.

## 💡 Prerequisites 

Before running the application, make sure you have the following installed:

- Python v3.6 or later
- pip v10.0.1 or later

## 🛠️ Installation 

1. Clone the repository

  ```bash
  git https://github.com/RedDotz20/python-tetris.git
  ```

2. Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

3. Run the main application

  ```bash
  python main.py # or python3 main.py
  ```

>**NOTE:** As of the moment for temporary storage of scores, create a `scores.txt` file in the root of the directory.

Execute the following to create a new `scores.txt` file and set it to `0`

```bash
touch scores.txt
```

## 🤝 Contributing 

If you're open to contributions from others, outline guidelines for contributing to your project. This might include information on how to report bugs, submit feature requests, or contribute code.

## 📃 License 

This project is [MIT licensed](./LICENSE)
