import pygame as pg
import random as rand
import cProfile as cP

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 320

BOX_SIZE = 9
MARGIN = 1

MAX_ROW_LENGTH = SCREEN_HEIGHT // (BOX_SIZE + MARGIN)
MAX_COLUMN_LENGTH = SCREEN_WIDTH // (BOX_SIZE + MARGIN)

BLACK = (0, 0, 0)
WHITE = (160, 160, 160)
GREEN = (10, 200, 40)
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


# print(grid)


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

        global grid_active
        grid_active = []

        row_index = 0
        for row in grid:
            column_index = 0
            for column in row:
                if column != 0:
                    grid_active.append([row_index, column_index])
                column_index += 1
            row_index += 1

        global new_cells
        new_cells = []

        for cell in grid_active:
            new_cells = neighbors(cell)
            grid[cell[0]][cell[1]] = 2
            for new_cell in new_cells:
                if grid[new_cell[0]][new_cell[1]] == 0:
                    grid[new_cell[0]][new_cell[1]] = 1

    pg.quit()
    # print(grid_active)


def grid_create():

    for row in range(MAX_ROW_LENGTH):
        for column in range(MAX_COLUMN_LENGTH):
            if grid[row][column] == 0:
                color = WHITE
            elif grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = DARK_GREEN
            pg.draw.rect(SCREEN, color, [(BOX_SIZE + MARGIN) * column + MARGIN,
                                         (BOX_SIZE + MARGIN) * row + MARGIN, BOX_SIZE, BOX_SIZE])


def neighbors(cell, min_grid_y=0, min_grid_x=0, max_grid_y=MAX_COLUMN_LENGTH, max_grid_x=MAX_ROW_LENGTH):
    # print(cell)
    cell_y = cell[0]
    cell_x = cell[1]

    neighbor_list = []

    adjacent = 1
    min_cell_y = cell_y - adjacent
    min_cell_x = cell_x - adjacent
    max_cell_y = min_cell_y + (adjacent * 2 + 1)
    max_cell_x = min_cell_x + (adjacent * 2 + 1)

    for y in range(min_cell_y, max_cell_y):
        for x in range(min_cell_x, max_cell_x):
            neighbor_list.append([y, x])

    # print(f"Starting list: {neighbor_list}")
    for trim in neighbor_list[:]:
        # print(trim)
        if trim in grid_active:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by already existing!")
        elif trim in new_cells:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by already being counted!")
        elif trim[0] < min_grid_x:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by trim[0] < min!")
        elif trim[1] < min_grid_y:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by trim[1] < min!")
        elif trim[0] >= max_grid_x:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by trim[0] >= max!")
        elif trim[1] >= max_grid_y:
            neighbor_list.remove(trim)
            # print(f"Removed {trim} by trim[1] >= max!")
    # print(f"Ending list: {neighbor_list} \n")

    return neighbor_list


cP.run('main()')
