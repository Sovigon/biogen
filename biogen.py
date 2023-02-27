import pygame as pg
import random as rand
import cProfile as cP

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1800

BOX_SIZE = 4
MARGIN = 1

MAX_ROW_LENGTH = SCREEN_HEIGHT // (BOX_SIZE + MARGIN)
MAX_COLUMN_LENGTH = SCREEN_WIDTH // (BOX_SIZE + MARGIN)
print(f'Max x: {MAX_ROW_LENGTH}\nMax y: {MAX_COLUMN_LENGTH}')

BLACK = (0, 0, 0)
WHITE = (160, 160, 160)
LIGHT_GREEN = (10, 200, 40)
GREEN = (5, 160, 30)
DARK_GREEN = (0, 100, 20)

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

grid = []

for row in range(MAX_ROW_LENGTH):
    grid.append([])
    for column in range(MAX_COLUMN_LENGTH):
        grid[row].append(0)

clock = pg.time.Clock()

for start_cell in range(rand.randint(3, 5)):
    rand_x = rand.randint(0, MAX_ROW_LENGTH - 1)
    rand_y = rand.randint(0, MAX_COLUMN_LENGTH - 1)
    grid[rand_x][rand_y] = 1

grid_active = []
new_cells = []


def main():

    pg.init()

    SCREEN.fill(BLACK)

    ignit = True

    while ignit:
        grid_create()
        clock.tick(120)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ignit = False

        grid_active = []

        row_index = 0
        for row in grid:
            column_index = 0
            for column in row:
                if column == 1:
                    grid_active.append([row_index, column_index])
                column_index += 1
            row_index += 1

        new_cells = []

        for cell in grid_active:
            new_cells = neighbors(cell)
            grid[cell[0]][cell[1]] = 3
            for new_cell in new_cells:
                if grid[new_cell[0]][new_cell[1]] == 0:
                    grid[new_cell[0]][new_cell[1]] = 1

    pg.quit()


def grid_create():

    grid_key = {0: WHITE, 1: LIGHT_GREEN, 2: GREEN, 3: DARK_GREEN}

    for row in range(MAX_ROW_LENGTH):
        for column in range(MAX_COLUMN_LENGTH):
            if grid[row][column] in grid_key:
                color = grid_key[grid[row][column]]
            else:
                color = BLACK
            pg.draw.rect(SCREEN, color, [(BOX_SIZE + MARGIN) * column + MARGIN,
                                         (BOX_SIZE + MARGIN) * row + MARGIN, BOX_SIZE, BOX_SIZE])


def neighbors(cell, min_grid_y=0, min_grid_x=0, max_grid_x=MAX_COLUMN_LENGTH, max_grid_y=MAX_ROW_LENGTH, new=new_cells):
    cell_y = cell[0]
    cell_x = cell[1]

    neighbor_list = []

    adjacent_range = 1
    min_cell_y = cell_y - adjacent_range
    min_cell_x = cell_x - adjacent_range
    max_cell_y = min_cell_y + (adjacent_range * 2 + 1)
    max_cell_x = min_cell_x + (adjacent_range * 2 + 1)

    for y in range(min_cell_y, max_cell_y):
        for x in range(min_cell_x, max_cell_x):
            if min_grid_x <= x < max_grid_x and min_grid_y <= y < max_grid_y:
                if grid[y][x] == 0 and [y, x] not in new:
                    neighbor_list.append([y, x])

    return neighbor_list


cP.run('main()')
