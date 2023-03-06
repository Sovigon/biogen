import pygame as pg
import random as rand

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1800

BOX_SIZE = 18
MARGIN = 2

MAX_ROW_LENGTH = SCREEN_HEIGHT // (BOX_SIZE + MARGIN)
MAX_COLUMN_LENGTH = SCREEN_WIDTH // (BOX_SIZE + MARGIN)
print(f'Max x: {MAX_ROW_LENGTH}\nMax y: {MAX_COLUMN_LENGTH}')

BLACK = (0, 0, 0)
WHITE = (160, 160, 160)

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

        self.seed_heart = []
        self.seed_grid = []
        self.active_cells = []


green_seed = Seed({"heart": [(5, 160, 30), 1], "grow": [
                  (10, 200, 40), 2], "old": [(0, 100, 20), 3]}, 1, 4, 1)

blue_seed = Seed({"heart": [(5, 30, 160), 4], "grow": [
                 (10, 40, 200), 5], "old": [(0, 20, 100), 6]}, 3, 8, 2)


# def green_seed():
#
#     LIGHT_GREEN = (10, 200, 40)
#     GREEN = (5, 160, 30)
#     DARK_GREEN = (0, 100, 20)
#
#     color_matrix = {"heart": [GREEN, 1], "grow": [LIGHT_GREEN, 2], "old": [DARK_GREEN, 3]}
#
#     adjacent_range = 1
#
#     tick_framerate = 4
#
#     initiative = 1
#
#     seed_grid = []
#
#
# def blue_seed():
#
#     LIGHT_BLUE = (10, 40, 200)
#     BLUE = (5, 30, 160)
#     DARK_BLUE = (0, 20, 100)
#
#     color_matrix = {"heart": [BLUE, 4], "grow": [LIGHT_BLUE, 5], "old": [DARK_BLUE, 6]}
#
#     adjacent_range = 3
#
#     tick_framerate = 8
#
#     initiative = 2
#
#     seed_grid = []


def main():

    pg.init()

    SCREEN.fill(BLACK)

    active_seeds = [green_seed, blue_seed]

    active_seed_colors = []

    for seed in active_seeds:
        print(
            f'\n -- Seed Properties -- \nSeed color matrix: {seed.color_matrix}\nSeed Heart Color: {seed.color_matrix["heart"][0]}\nSeed Heart Grid ID: {seed.color_matrix["heart"][1]}')
        rand_x = rand.randint(0, MAX_ROW_LENGTH - 1)
        rand_y = rand.randint(0, MAX_COLUMN_LENGTH - 1)
        print(f'Random coordinate: {rand_x}, {rand_y}')
        grid[rand_x][rand_y] = seed.color_matrix["heart"][1]
        seed.seed_heart.extend([rand_x, rand_y])
        print(f"Seed Heart: {seed.seed_heart}")

        for preliminary in neighbors(seed.seed_heart):
            seed.active_cells.append(preliminary)
        print(
            f"Preliminary growth cells created. For seed {seed} preliminary growth cells are: {seed.active_cells}")

        active_seed_colors.append(seed.color_matrix)
        print(f'Active seed colors: {active_seed_colors}')

    for row in range(MAX_ROW_LENGTH):
        for column in range(MAX_COLUMN_LENGTH):
            if grid[row][column] == 0:
                grid_create()
            else:
                print(
                    f"\nSeed cell detected. Cycling through colors. Current matrix value: {grid[row][column]}")
                for colors in active_seed_colors:
                    print(f"Current color check: {colors}")
                    for value in colors.values():
                        print(f"Checking value: {value}")
                        if grid[row][column] == value[1]:
                            grid_create(value[0])
                            print(f"Color assigned: {value[0]}")
                            break
                        else:
                            print("Value not assigned.")

    ignit = True

    while ignit:
        clock.tick(120)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ignit = False

        for seed_grow in active_seeds:
            print(f"\nCurrent seed: {seed_grow}")
            # growth_color = seed_grow.color_matrix["grow"][0]
            old_color = seed_grow.color_matrix["old"][0]
            new_cells = []
            for seed_cells in seed_grow.active_cells:
                print(f"Current seed cell list: {seed_cells}")
                for indi_cells in seed_cells:
                    # print(f"Current seed cell: {indi_cells}")
                    growing_cells = neighbors(indi_cells, new_cells)
                    new_cells.append(growing_cells)
                    seed_grow.seed_grid.append(seed_cells)
                    grid[indi_cells[0]][indi_cells[1]] == old_color[1]
                seed_grow.active_cells.remove(seed_cells)
                print("Removed calculated cells")
            print(f"List of new cells: {new_cells}")
            for add_cells_list in new_cells:
                for add_cells in add_cells_list:
                    seed_grow.active_cells.append(add_cells)
            print(f"Added next set of cells. New seed cells: {seed_grow.active_cells}")

        for row in range(MAX_ROW_LENGTH):
            for column in range(MAX_COLUMN_LENGTH):
                if grid[row][column] == 0:
                    grid_create()
                else:
                    for colors in active_seed_colors:
                        for values in colors:
                            if grid[row][column] == values[1]:
                                grid_create(values[0])
                                break

    pg.quit()


def grid_create(color=WHITE):

    pg.draw.rect(SCREEN, color, [(BOX_SIZE + MARGIN) * column + MARGIN,
                                 (BOX_SIZE + MARGIN) * row + MARGIN, BOX_SIZE, BOX_SIZE])


def neighbors(cell, new=[], min_grid_y=0, min_grid_x=0, max_grid_x=MAX_COLUMN_LENGTH, max_grid_y=MAX_ROW_LENGTH):
    cell_y = cell[0]
    cell_x = cell[1]
    # print(f"Current cell: {cell_y}, {cell_x}")

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

    # print(f'Current neighbors: {neighbor_list}\n')
    return neighbor_list


main()
