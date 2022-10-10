import arcade
import itertools
import random
from collections import deque
from enum import Enum

SQR_LEN = 35
SCREEN_LEN = 512
WINDOW_LEN = int(SCREEN_LEN * 1.25)
LIST_LEN = SCREEN_LEN // SQR_LEN
EDGE = SQR_LEN // 16


class GameState(Enum):
    PLAYING = 0
    LOST = 1
    WON = 2


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_LEN, WINDOW_LEN, "Minesweeper")
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.grid = [[0 for _ in range(LIST_LEN)] for _ in range(LIST_LEN)]
        self.known = set()
        self.flags = set()
        self.mines = set()
        self.state = GameState.PLAYING

    def get_neighbors(self, i, j):
        neighboring_mines = []
        for x, y in list(itertools.product((0, -1, 1), repeat=2)):
            if i + x in range(LIST_LEN) and j + y in range(LIST_LEN):
                neighboring_mines.append((i + x, j + y))
        return neighboring_mines

    def on_draw(self):
        arcade.start_render()
        if self.state is GameState.LOST:
            arcade.draw_text(
                "You Lose D:",
                WINDOW_LEN // 2,
                WINDOW_LEN // 2,
                (255, 0, 0),
                anchor_x="center",
                bold=True,
                font_size=50,
            )
        elif self.state is GameState.WON:
            arcade.draw_text(
                "You won!!!",
                WINDOW_LEN // 2,
                WINDOW_LEN // 2,
                (0, 255, 0),
                anchor_x="center",
                bold=True,
                font_size=50,
            )
        else:
            self.draw_squares()

            self.remaining_mines = int(LIST_LEN**2 / 8) - len(self.flags)

            flag = arcade.Sprite(
                "src/images/flag.jpeg",
                center_x=WINDOW_LEN - 100 - SQR_LEN * 1.5,
                center_y=int(WINDOW_LEN * (15 / 16)),
                scale=0.20,
            )
            flag.draw()

            arcade.draw_text(
                    self.remaining_mines,
                    WINDOW_LEN - 100,
                    int(WINDOW_LEN * (15 / 16)),
                    anchor_x="center",
                    anchor_y="center",
                    font_size=20,
            )


    def on_mouse_press(self, x, y, _button, _):
        if self.state is GameState.PLAYING:
            i = map_to_index(x)
            j = map_to_index(y)
            if _button == arcade.MOUSE_BUTTON_RIGHT:
                if (i, j) in self.flags:
                    self.flags.remove((i, j))
                else:
                    self.flags.add((i, j))
            elif _button == arcade.MOUSE_BUTTON_LEFT:
                if not self.known:
                    self.start(i, j)
                value = self.grid[i][j]
                if value == 0:
                    self.bfs_expand(i, j)
                elif value == -1:
                    # Lost D:
                    self.state = GameState.LOST
                    self.known.add((i, j))
                else:
                    self.known.add((i, j))

        # In order for the player to win, they must uncover all non-mine squares
        if len(self.known) == LIST_LEN**2 - len(self.mines):
            self.state = GameState.WON

    def start(self, i, j):
        self.mines = random.sample(
            [
                (x, y)
                for x in range(LIST_LEN)
                for y in range(LIST_LEN)
                if (x, y) not in self.get_neighbors(i, j)
            ],
            int(LIST_LEN**2 / 8),
        )
        for x, y in self.mines:
            self.grid[x][y] = -1

        for x in range(LIST_LEN):
            for y in range(LIST_LEN):
                if self.grid[x][y] != -1:
                    self.grid[x][y] = len(
                        [
                            coord
                            for coord in self.get_neighbors(x, y)
                            if self.grid[coord[0]][coord[1]] == -1
                        ]
                    )

        self.bfs_expand(i, j)

    def bfs_expand(self, i, j):
        neighbors = deque(self.get_neighbors(i, j))
        visited = set()
        while neighbors:
            i, j = neighbors.popleft()
            visited.add((i, j))
            if self.grid[i][j] == 0:
                neighbors += [x for x in self.get_neighbors(i, j) if x not in visited]
            self.known.add((i, j))

    def draw_squares(self):
        for j in range(LIST_LEN):
            y = map_to_coordinate(j)
            for i in range(LIST_LEN):
                x = map_to_coordinate(i)

                arcade.draw_lrtb_rectangle_outline(
                    x + EDGE,
                    x + SQR_LEN - EDGE,
                    y + SQR_LEN - EDGE,
                    y + EDGE,
                    arcade.color.BLACK,
                )

                if (i, j) in self.known:
                    arcade.draw_lrtb_rectangle_filled(
                        x + EDGE,
                        x + SQR_LEN - EDGE,
                        y + SQR_LEN - EDGE,
                        y + EDGE,
                        arcade.color.ANTIQUE_WHITE,
                    )

                if (i, j) in self.flags:
                    flag = arcade.Sprite(
                        "src/images/flag.jpeg",
                        scale=0.12,
                        center_x=x + SQR_LEN // 2,
                        center_y=y + SQR_LEN // 2,
                    )
                    flag.draw()

                elif (i, j) in self.known and self.grid[i][j] == -1:
                    mine = arcade.Sprite(
                        "src/images/mine.png",
                        scale=0.08,
                        center_x=x + SQR_LEN // 2,
                        center_y=y + SQR_LEN // 2,
                    )
                    mine.draw()


                elif (i, j) in self.known and self.grid[i][j] != 0:
                    arcade.draw_text(
                        self.grid[i][j],
                        x + SQR_LEN // 4,
                        y + SQR_LEN // 6,
                        arcade.color.BLACK,
                        23,
                    )

                elif (i, j) not in self.known:
                    arcade.draw_lrtb_rectangle_filled(
                        x + EDGE,
                        x + SQR_LEN - EDGE,
                        y + SQR_LEN - EDGE,
                        y + EDGE,
                        arcade.color.BLACK,
                    )


def map_to_coordinate(n: int) -> int:
    return (n - LIST_LEN // 2) * SQR_LEN + int((WINDOW_LEN - SCREEN_LEN) * 2.5)


def map_to_index(n: int) -> int:
    return (n - int((WINDOW_LEN - SCREEN_LEN) * 2.5)) // SQR_LEN + LIST_LEN // 2


game = Game()
game.run()
