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
        mines = random.sample([(x, y) for x in range(LIST_LEN) for y in range(LIST_LEN)], int(LIST_LEN ** 2 / 8))
        for x, y in mines:
            self.grid[x][y] = -1
        
        for i in range(LIST_LEN):
            for j in range(LIST_LEN):
                if self.grid[i][j] != -1:
                    self.grid[i][j] = self.get_neighbors(i, j)
        
        self.known = set()
    
    def get_neighbors(self, i, j):
        neighboring_mines = 0
        for x, y in list(itertools.product((0, -1, 1), repeat=2)):
            if i + x in range(LIST_LEN) and j + y in range(LIST_LEN):
                neighboring_mines += self.grid[i + x][j + y] == -1
        return neighboring_mines

    def on_draw(self):
        arcade.start_render()
        self.draw_squares()
        time.sleep(0.1)

    def on_mouse_press(self, x, y, _button, _modifiers):
        i = map_to_index(x)
        j = map_to_index(y)
        if i in range(LIST_LEN) and j in range(LIST_LEN):
            if not self.known:
                pass
            self.known.add((i, j))

    def draw_squares(self):
        for j in range(LIST_LEN):
            y = map_to_coordinate(j)
            for i in range(LIST_LEN):
                x = map_to_coordinate(i)
                if (i, j) in self.known:
                    f = arcade.draw_lrtb_rectangle_outline
                    arcade.draw_text(
                        self.grid[i][j],
                        x + SQR_LEN // 6,
                        y + SQR_LEN // 6,
                        arcade.color.BLACK,
                        25,
                    )
                else:
                    f = arcade.draw_lrtb_rectangle_filled
                f(
                    x + EDGE,
                    x + SQR_LEN - EDGE,
                    y + SQR_LEN - EDGE,
                    y + EDGE,
                    arcade.color.BLACK
                )

def map_to_coordinate(n: int) -> int:
    return (n - LIST_LEN // 2) * SQR_LEN + int((WINDOW_LEN - SCREEN_LEN) * 2.5)

def map_to_index(n: int) -> int:
    return (n - int((WINDOW_LEN - SCREEN_LEN) * 2.5)) // SQR_LEN + LIST_LEN // 2


game = Game()
game.run()
