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

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

grid = []

for row in range(MAX_ROW_LENGTH):
    grid.append([])
    for column in range(MAX_COLUMN_LENGTH):
        grid[row].append(0)

clock = pg.time.Clock()


class Seed(object):
    def __init__(self, color_matrix, adjacent_range, tick_framerate, initiative):
        self.color_matrix = color_matrix
        self.adjacent_range = adjacent_range
        self.tick_framerate = tick_framerate
        self.initiative = initiative

        self.seed_tick = tick_framerate

        self.seed_heart = []
        self.seed_grid = []
        self.active_cells = []


green_seed = Seed({"heart": [(5, 160, 30), 1], "grow": [
                  (10, 200, 40), 2], "old": [(0, 100, 20), 3]}, 1, 4, 1)

blue_seed = Seed({"heart": [(5, 30, 160), 4], "grow": [
                 (10, 40, 200), 5], "old": [(0, 20, 100), 6]}, 3, 9, 2)

red_seed = Seed({"heart": [(160, 30, 5), 7], "grow": [
                 (200, 40, 10), 8], "old": [(100, 20, 0), 9]}, 2, 7, 3)

yellow_seed = Seed({"heart": [(160, 160, 40), 10], "grow": [
    (200, 200, 80), 11], "old": [(100, 100, 10), 12]}, 1, 2, 4)

active_colors = []


def main():

    pg.init()

    BLACK = (0, 0, 0)

    SCREEN.fill(BLACK)

    active_seeds = [green_seed, blue_seed, red_seed, yellow_seed]

    for seed in active_seeds:
        rand_x = rand.randint(0, MAX_ROW_LENGTH - 1)
        rand_y = rand.randint(0, MAX_COLUMN_LENGTH - 1)
        grid[rand_x][rand_y] = seed.color_matrix["heart"][1]
        seed.seed_heart.extend([rand_x, rand_y])

        active_colors.append(seed.color_matrix)

        for prelim in neighbors(seed.seed_heart, adjacent_range=seed.adjacent_range):
            seed.active_cells.append(prelim)

        for indi_cells in seed.active_cells:
            grid[indi_cells[0]][indi_cells[1]] = seed.color_matrix["grow"][1]

    update_grid()

    ignit = True

    while ignit:
        clock.tick(120)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ignit = False

        for seed_grow in active_seeds:
            seed_grow.seed_tick -= 1
            if seed_grow.seed_tick == 0:

                new_cells = []

                for old_cells in seed_grow.active_cells:
                    seed_grow.seed_grid.append(old_cells)
                    grid[old_cells[0]][old_cells[1]] = seed_grow.color_matrix["old"][1]

                    for grow_cells in neighbors(old_cells, new_cells, adjacent_range=seed_grow.adjacent_range):
                        new_cells.append(grow_cells)

                seed_grow.active_cells = new_cells

                # print(f'\nCurrent growing cells for {seed_grow}:\n{seed_grow.active_cells}')
                # print(f'Current grow color: {seed_grow.color_matrix["grow"][1]}')

                for indi_cells in seed_grow.active_cells:
                    grid[indi_cells[0]][indi_cells[1]] = seed_grow.color_matrix["grow"][1]
                    # print(f'Loop grow color: {seed_grow.color_matrix["grow"][1]}')
                    # print(
                    # f"Cell value of ({indi_cells[0]}, {indi_cells[1]}): {grid[indi_cells[0]][indi_cells[1]]}")

                seed_grow.seed_tick = seed_grow.tick_framerate

        update_grid()

    pg.quit()


def update_grid(seed_colors=active_colors, base_grid=grid):

    WHITE = (160, 160, 160)

    def grid_create(color=WHITE):

        pg.draw.rect(SCREEN, color, [(BOX_SIZE + MARGIN) * column + MARGIN,
                                     (BOX_SIZE + MARGIN) * row + MARGIN, BOX_SIZE, BOX_SIZE])

    for row in range(MAX_ROW_LENGTH):
        for column in range(MAX_COLUMN_LENGTH):
            if grid[row][column] == 0:
                grid_create()
            else:
                for colors in seed_colors:
                    for values in colors.values():
                        if grid[row][column] == values[1]:
                            # print(
                                # f'Non 0 detected. Assigning cell with value {values[1]} with color {values[0]}')
                            grid_create(values[0])


def neighbors(cell, new=[], adjacent_range=1, min_grid_y=0, min_grid_x=0, max_grid_x=MAX_COLUMN_LENGTH, max_grid_y=MAX_ROW_LENGTH):
    cell_y = cell[0]
    cell_x = cell[1]

    neighbor_list = []

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
