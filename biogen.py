import pygame as pg
import random as rand
import string
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
    def __init__(self, color_matrix, adjacent_range, tick_framerate, initiative, seed_id):
        self.color_matrix = color_matrix
        self.adjacent_range = adjacent_range
        self.tick_framerate = tick_framerate
        self.initiative = initiative
        self.seed_id = seed_id

        self.seed_tick = tick_framerate

        self.seed_heart = []
        self.seed_grid = []
        self.active_cells = []

    def _name(self):
        return self.__class__.__name__


class GreenSeed(Seed):
    def __init__(self, unique_id="0"):
        super().__init__({"heart": [(5, 160, 30), 1], "grow": [
            (10, 200, 40), 2], "old": [(0, 100, 20), 3]}, 1, 3, 1, "Grn")

        self.unique_id = unique_id
        self.unique_name = self.seed_id + str(self.initiative) + unique_id


class BlueSeed(Seed):
    def __init__(self, unique_id="0"):
        super().__init__({"heart": [(5, 30, 160), 4], "grow": [
                         (10, 40, 200), 5], "old": [(0, 20, 100), 6]}, 3, 9, 2, "Blu")

        self.unique_id = unique_id
        self.unique_name = self.seed_id + str(self.initiative) + unique_id


class RedSeed(Seed):
    def __init__(self, unique_id="0"):
        super().__init__({"heart": [(160, 30, 5), 7], "grow": [
                         (200, 40, 10), 8], "old": [(100, 20, 0), 9]}, 2, 7, 3, "Red")

        self.unique_id = unique_id
        self.unique_name = self.seed_id + str(self.initiative) + unique_id


class YellowSeed(Seed):
    def __init__(self, unique_id="0"):
        super().__init__({"heart": [(160, 160, 40), 10], "grow": [
            (200, 200, 80), 11], "old": [(100, 100, 10), 12]}, 1, 1, 4, "Ylw")

        self.unique_id = unique_id
        self.unique_name = self.seed_id + str(self.initiative) + unique_id


seed_types = [cls()._name() for cls in Seed.__subclasses__()]
# print(seed_types)

seed_number = 7

unique_seeds = []
random_taken = []

for unique in range(seed_number):
    pick = rand.choice(seed_types)
    while True:
        random_id = ''.join(rand.choice(string.digits)
                            for length in range(2))
        if random_id not in random_taken:
            break
    random_taken.append(random_id)
    unique_seeds.append((pick, random_id))

# print(unique_seeds)

active_seeds = []

for activate, id in unique_seeds:
    activate_seed = locals()[activate](id)
    seed_name = activate_seed.seed_id + id
    active_seeds.append((seed_name, activate_seed))

unique_hearts = []

for heart in active_seeds:
    while True:
        rand_x = rand.randint(0, MAX_ROW_LENGTH - 1)
        rand_y = rand.randint(0, MAX_COLUMN_LENGTH - 1)
        if [rand_x, rand_y] not in unique_hearts:
            break
    grid[rand_x][rand_y] = (heart[1].unique_name, heart[1].color_matrix["heart"][1])
    heart[1].seed_heart.extend([rand_x, rand_y])
    # print(f"{grid[rand_x][rand_y]} at {heart[1].seed_heart}")
    heart[1].active_cells.append([rand_x, rand_y])
    unique_hearts.append([rand_x, rand_y])


def main():

    pg.init()

    BLACK = (0, 0, 0)

    SCREEN.fill(BLACK)

    ignit = True

    update_grid()

    while ignit:
        clock.tick(120)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ignit = False

        new_cells = []

        for seed_grow in active_seeds:
            current_seed = seed_grow[1]
            current_seed.seed_tick -= 1
            if current_seed.seed_tick == 0:

                for old_cells in current_seed.active_cells:
                    current_seed.seed_grid.append(old_cells)
                    grid[old_cells[0]][old_cells[1]] = (
                        seed_grow[0], current_seed.color_matrix["old"][1])

                    for grow_cells in neighbors(old_cells, new_cells, adjacent_range=current_seed.adjacent_range):
                        add_cell = (seed_grow[0], grow_cells, seed_grow[1].color_matrix["grow"][1])
                        for replace_cell in new_cells:
                            if add_cell[1] == replace_cell[1]:
                                new_cells.remove(replace_cell)
                        new_cells.append(add_cell)

                current_seed.seed_tick = current_seed.tick_framerate

        for assign_cells in new_cells:
            for seed_assign in active_seeds:
                if assign_cells[0] == seed_assign[0]:
                    seed_assign[1].active_cells.append(assign_cells[1])

        # print(new_cells)

        update_grid(new_cells)

    pg.quit()


def update_grid(list_grid=grid):

    def grid_create(color=(160, 160, 160)):

        pg.draw.rect(SCREEN, color, [(BOX_SIZE + MARGIN) * column + MARGIN,
                                     (BOX_SIZE + MARGIN) * row + MARGIN, BOX_SIZE, BOX_SIZE])

    if list_grid == grid:
        for row in range(MAX_ROW_LENGTH):
            for column in range(MAX_COLUMN_LENGTH):
                grid_create()
    else:
        for grid_cell in list_grid:
            row = grid_cell[1][0]
            column = grid_cell[1][1]
            for color_check in active_seeds:
                if grid_cell[0] == color_check[0]:
                    grid_create(color_check[1].color_matrix["grow"][0])


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
