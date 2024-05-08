# 🐍 Python Tetris

<p>
<!--   <a aria-label="Python Version" href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/pypi/pyversions/pygame?style=for-the-badge&logo=python&logoColor=yellow&color=yellow">
  </a> -->
  <a aria-label="GitHub commit activity" href="https://github.com/RedDotz20/python-tetris/commits/main/" title="GitHub commit activity">
    <img src="https://img.shields.io/github/commit-activity/w/RedDotz20/python-tetris?style=for-the-badge">
  </a>
    <a aria-label="LICENSE" href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge">
  </a>
  <a aria-label="GitHub contributors" href="https://github.com/RedDotz20/python-tetris/graphs/contributors" title="GitHub contributors">
    <img src="https://img.shields.io/github/contributors/RedDotz20/python-tetris?color=orange&style=for-the-badge">
  </a>
</p>

A Tetris game built with Python programming language alongside with `PyGame` library.

## 🚀 Features

- [x] `Blocks (Tetrominoes)`: Tetris is built around tetrominoes, geometric shapes consisting of four square blocks each. These shapes fall from the top of the game area and can be rotated and moved horizontally as they descend.
- [x] `Gameplay Mechanics`: Players must manipulate the falling tetrominoes to create complete horizontal lines without any gaps. When a line is completed, it disappears, and any blocks above it will fall to fill the space. The game ends if the stack of tetrominoes reaches the top of the game area.
- [x] `Scoring System`: Points are typically awarded for each line cleared, with more points given for clearing multiple lines simultaneously (known as a "Tetris"). The scoring system may also reward players for the speed at which they clear lines or for achieving certain milestones.
- [x] `Speed Increase`: As players progress through the game, the falling speed of the tetrominoes typically increases, making the game more challenging over time.
- [x] `Level Progression`: Tetris often features a level system where players advance to higher levels as they clear more lines. Advancing levels may bring increased speed or other changes to the gameplay.
- [x] `Hold Piece`: Some versions of Tetris allow players to temporarily hold a tetromino, to be used strategically later.
- [x] `Next Piece Preview`: Many Tetris games offer a preview of the next tetromino that will appear, allowing players to plan their moves in advance.

## 💡 Prerequisites

Before running the application, make sure you have the following installed:

- Python `v3.6` or later
- pip `v10.0.1` or later

## 🛠️ Installation

1. Clone the repository

  ```bash
  git https://github.com/RedDotz20/python-tetris.git
  ```

2. Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

3. Run the `main.py` application

  ```bash
  python main.py
  # or
  python3 main.py
  ```

>**NOTE:** As of the moment for temporary storage of scores, create a `scores.txt` file in the root of the directory.

Execute the following to create a new `scores.txt` file and set it to `0`

```bash
touch scores.txt
```

## 🤝 Contributing

If you're open to contributions from others, outline guidelines for contributing to your project. This might include information on how to report bugs, submit feature requests, or contribute code.

## 👨‍💻 Authors

- [@carlos-tabangay | reddotz20](https://github.com/RedDotz20)
- [@andre-santelices | andresntics](https://github.com/andresntlcs)
- [@paul-rogayan | popoyisded](https://github.com/popoyisded)
- [@sam-velasco | zestomilk2002](https://github.com/ZestoMilk2002)

## 📃 License

This project is [MIT licensed](./LICENSE)
