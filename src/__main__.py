import arcade
import itertools
import random
import time

SQR_LEN = 35
SCREEN_LEN = 512
WINDOW_LEN = int(SCREEN_LEN * 1.25)
LIST_LEN = SCREEN_LEN // SQR_LEN
EDGE = SQR_LEN // 16


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_LEN, WINDOW_LEN, "Minesweeper")
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.grid = [[0 for _ in range(LIST_LEN)] for _ in range(LIST_LEN)]
        mines = random.sample(
            [(x, y) for x in range(LIST_LEN) for y in range(LIST_LEN)],
            int(LIST_LEN**2 / 8),
        )
        for x, y in mines:
            self.grid[x][y] = -1

        for i in range(LIST_LEN):
            for j in range(LIST_LEN):
                if self.grid[i][j] != -1:
                    self.grid[i][j] = len([x for x in self.get_neighbors(i, j) if self.grid[x[0]][x[1]] == -1])

        self.known = set()
        self.flags = set()

    def get_neighbors(self, i, j):
        neighboring_mines = []
        for x, y in list(itertools.product((0, -1, 1), repeat=2)):
            if i + x in range(LIST_LEN) and j + y in range(LIST_LEN):
                neighboring_mines.append((i + x, j + y))
        return neighboring_mines

    def on_draw(self):
        arcade.start_render()
        self.draw_squares()

    def on_mouse_press(self, x, y, _button, _modifiers):
        i = map_to_index(x)
        j = map_to_index(y)
        if _button == arcade.MOUSE_BUTTON_RIGHT:
            self.flags.add((i, j))
        elif _button == arcade.MOUSE_BUTTON_LEFT:
            if not self.known:
                for neighbor in self.get_neighbors(i, j):
                    self.known.add(neighbor)
            self.known.add((i, j))

    def draw_squares(self):
        for j in range(LIST_LEN):
            y = map_to_coordinate(j)
            for i in range(LIST_LEN):
                x = map_to_coordinate(i)
                if (i, j) in self.known:
                    arcade.draw_lrtb_rectangle_outline(
                        x + EDGE,
                        x + SQR_LEN - EDGE,
                        y + SQR_LEN - EDGE,
                        y + EDGE, 
                        arcade.color.BLACK,
                    )
                    if self.grid[i][j] != 0:
                        arcade.draw_text(
                            self.grid[i][j],
                            x + SQR_LEN // 4,
                            y + SQR_LEN // 6,
                            arcade.color.BLACK,
                            23,
                        )

                elif (i, j) in self.flags:
                    flag = arcade.Sprite(
                        "src/images/flag.jpeg",
                        scale = 0.12,
                        center_x = x + SQR_LEN // 2,
                        center_y = y + SQR_LEN // 2,
                    )
                    flag.draw()

                else:
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
