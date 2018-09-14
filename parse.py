#!/usr/bin/env python

import pygame
import sys
from random import choice
import pprint
pp = pprint.PrettyPrinter(depth=3, indent=2)

pygame.init()
asurf = pygame.image.load('original.png')
asurf_rect = asurf.get_rect()
black = 0, 0, 0
red = 255, 0, 0

screen = pygame.display.set_mode([48 * 20, 48 * 20])

iarea = pygame.Rect(0, 0, 48, 48)
cells = []

for x in range(0, 20):
    for y in range(0, 20):
        subsurf = asurf.subsurface(pygame.Rect(
            x * 49 + x + 1, y * 49 + y + 1, 48, 48))
        topleft = subsurf.get_at([3, 3])
        bottomleft = subsurf.get_at([3, 45])
        topright = subsurf.get_at([45, 3])
        bottomright = subsurf.get_at([45, 45])
        if topleft == (0, 0, 0, 255) or topleft == (255, 255, 255, 255):
            topleft = 'border'
        if topright == (0, 0, 0, 255) or topright == (255, 255, 255, 255):
            topright = 'border'
        if bottomleft == (0, 0, 0, 255) or bottomleft == (255, 255, 255, 255):
            bottomleft = 'border'
        if bottomright == (0, 0, 0, 255) or bottomright == (255, 255, 255, 255):
            bottomright = 'border'
        cells.append({'id': [x, y], 'surf': subsurf, 'bottom': [], 'top': [], 'left': [], 'right': [], 'moved': False, 'locked': False,
                      'topleft': topleft, 'bottomleft': bottomleft, 'topright': topright, 'bottomright': bottomright})

for cell in cells:
    for target_cell in cells:
        if cell == target_cell:
            next
        if (cell['topleft'] != 'border' or cell['bottomleft'] != 'border') and cell['topleft'] == target_cell['topright'] and cell['bottomleft'] == target_cell['bottomright']:
            if not target_cell in cell['left']:
                cell['left'].append(target_cell)
            if not cell in target_cell['right']:
                target_cell['right'].append(cell)
        if (cell['topleft'] != 'border' or cell['topright'] != 'border') and cell['topleft'] == target_cell['bottomleft'] and cell['topright'] == target_cell['bottomright']:
            if not target_cell in cell['top']:
                cell['top'].append(target_cell)
            if not cell in target_cell['bottom']:
                target_cell['bottom'].append(cell)
        if (cell['topright'] != 'border' or cell['bottomright'] != 'border') and cell['topright'] == target_cell['topleft'] and cell['bottomright'] == target_cell['bottomleft']:
            if not target_cell in cell['right']:
                cell['right'].append(target_cell)
            if not cell in target_cell['left']:
                target_cell['left'].append(cell)
        if (cell['bottomleft'] != 'border' or cell['bottomright'] != 'border') and cell['bottomleft'] == target_cell['topleft'] and cell['bottomright'] == target_cell['topright']:
            if not target_cell in cell['bottom']:
                cell['bottom'].append(target_cell)
            if not cell in target_cell['top']:
                target_cell['top'].append(cell)

root = None
for cell in cells:
    if (cell['topleft'] == 'border') and (cell['topright'] == 'border') and (cell['bottomleft'] == 'border'):
        root = cell
        root['locked'] = True
        index = cells.index(root)
        cells[index] = cells[0]
        cells[0] = root
        break

pp.pprint(root)

for cell in cells:
    if (cell['topleft'] == 'border') and (cell['topright'] == 'border') and (cell['bottomright'] == 'border'):
        cell['locked'] = True
        index = cells.index(cell)
        cells[index] = cells[0 * 20 + 19]
        cells[0 * 20 + 19] = cell
        break

for cell in cells:
    if (cell['topleft'] == 'border') and (cell['bottomleft'] == 'border') and (cell['bottomright'] == 'border'):
        cell['locked'] = True
        index = cells.index(cell)
        cells[index] = cells[19 * 20 + 0]
        cells[19 * 20 + 0] = cell
        break

for cell in cells:
    if (cell['topright'] == 'border') and (cell['bottomright'] == 'border') and (cell['bottomleft'] == 'border'):
        cell['locked'] = True
        index = cells.index(cell)
        cells[index] = cells[19 * 20 + 19]
        cells[19 * 20 + 19] = cell
        break

font = pygame.font.Font(None, 12)
lock = font.render("LOCK", True, red)

iternum = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    posx = 0
    posy = 0
    count = 0
    for cell in cells:
        if cell:
            screen.blit(cell['surf'], [posx, posy])
            # if cell['locked']:
                # screen.blit(lock, [posx + 10, posy + 10])
        posx += 48
        count += 1
        if count >= 20:
            count = 0
            posx = 0
            posy += 48

    pygame.display.flip()

    # if iternum > 2:
    #     continue

    iternum += 1
    print('Gen', iternum)

    for cell in cells:
        cell['moved'] = False

    # col = 0
    # row = 0
    # curr_node = None
    for col in range(0, 20):
      for row in range(0, 20):
        cell = cells[row * 20 + col]

        if len(cell['top']) > 0 and row > 0:
            next_node_top = cells[(row - 1) * 20 + col]
            if not next_node_top in cell['top']:
                new_node = choice(cell['top'])
                if not (new_node['locked'] or next_node_top['locked']):
                    new_node['moved'] = True
                    next_node_top['moved'] = True
                    if (cell['locked'] and len(cell['top']) == 1):
                        new_node['locked'] = True
                    index = cells.index(new_node)
                    cells[index] = next_node_top
                    cells[(row - 1) * 20 + col] = new_node

        if len(cell['left']) > 0 and col > 0:
            next_node_left = cells[row * 20 + col - 1]
            if not next_node_left in cell['left']:
                new_node = choice(cell['left'])
                if not (new_node['locked'] or next_node_left['locked']):
                    new_node['moved'] = True
                    next_node_left['moved'] = True
                    if (cell['locked'] and len(cell['left']) == 1):
                        new_node['locked'] = True
                    index = cells.index(new_node)
                    cells[index] = next_node_left
                    cells[row * 20 + col - 1] = new_node

        if len(cell['right']) > 0 and col < 19:
            next_node_right = cells[row * 20 + col + 1]
            if not next_node_right in cell['right']:
                new_node = choice(cell['right'])
                lock_it = False
                if row == 0:
                    rcells = []
                    for rcell in cell['right']:
                        if rcell['topleft'] == 'border' and rcell['topright'] == 'border':
                            rcells.append(rcell)
                    if len(rcells) > 1:
                        new_node = choice(rcells)
                    if len(rcells) == 1 and cell['locked']:
                        lock_it = True
                if not (new_node['moved'] or next_node_right['moved'] or new_node['locked'] or next_node_right['locked']):
                    new_node['moved'] = True
                    next_node_right['moved'] = True
                    if (cell['locked'] and len(cell['right']) == 1) or lock_it:
                        new_node['locked'] = True
                    index = cells.index(new_node)
                    cells[index] = next_node_right
                    cells[row * 20 + col + 1] = new_node

        if len(cell['bottom']) > 0 and row < 19:
            next_node_bottom = cells[(row + 1) * 20 + col]
            if not next_node_bottom in cell['bottom']:
                new_node = choice(cell['bottom'])
                lock_it = False
                if col == 0:
                    bcells = []
                    for bcell in cell['bottom']:
                        if bcell['topleft'] == 'border' and bcell['bottomleft'] == 'border':
                            bcells.append(bcell)
                    if len(bcells) > 1:
                        new_node = choice(bcells)
                    if len(bcells) == 1 and cell['locked']:
                        lock_it = True
                if not (new_node['moved'] or next_node_bottom['moved'] or new_node['locked'] or next_node_bottom['locked']):
                    new_node['moved'] = True
                    next_node_bottom['moved'] = True
                    if cell['locked'] and len(cell['bottom']) == 1:
                        new_node['locked'] = True
                    index = cells.index(new_node)
                    cells[index] = next_node_bottom
                    cells[(row + 1) * 20 + col] = new_node

        # col += 1
        # if row > 20:
        #     row += 1
        #     col = 0


    # for col in range(0, 20):
    #   for row in range(0, 20):
    #     # print(row, col)
    #     cell = grid[row * 20 + col]
    #     if row == 0 and col == 0:
    #       if cell['topleft'] != 'border' or cell['topright'] != 'border' or cell['bottomleft'] != 'border':
    #         choices = []
    #         for gcell in grid:
    #           if (gcell['topleft'] == 'border') and (gcell['topright'] == 'border') and (gcell['bottomleft'] == 'border'):
    #             index = grid.index(gcell)
    #             grid[index] = cell
    #             grid[row * 20 + col] = gcell
    #             gcell['moved'] = True
    #     elif row == 0:
    #       if not (cell['topleft'] == 'border' and cell['topright'] == 'border'):
    #         choices = []
    #         for gcell in reversed(grid):
    #           if gcell['topleft'] == 'border' and gcell['topright'] == 'border' and not gcell['moved']:
    #             choices.append(gcell)

    #         choice_cell = choice(choices)
    #         index = grid.index(choice_cell)
    #         grid[index] = cell
    #         grid[row * 20 + col] = choice_cell
    #     elif col == 0:
    #       if not (cell['topleft'] == 'border' and cell['bottomleft'] == 'border'):
    #         choices = []
    #         for gcell in reversed(grid):
    #           if gcell['topleft'] == 'border' and gcell['bottomleft'] == 'border' and not gcell['moved']:
    #             choices.append(gcell)

    #         choice_cell = choice(choices)
    #         index = grid.index(choice_cell)
    #         grid[index] = cell
    #         grid[row * 20 + col] = choice_cell
    #     elif col == 19:
    #       if not (cell['topright'] == 'border' and cell['bottomright'] == 'border'):
    #         choices = []
    #         for gcell in grid:
    #           if gcell['topright'] == 'border' and gcell['bottomright'] == 'border' and not gcell['moved']:
    #             choices.append(gcell)

    #         choice_cell = choice(choices)
    #         index = grid.index(choice_cell)
    #         grid[index] = cell
    #         grid[row * 20 + col] = choice_cell
    #     elif row == 19:
    #       if not (cell['bottomleft'] == 'border' and cell['bottomright'] == 'border'):
    #         choices = []
    #         for gcell in grid:
    #           if gcell['bottomleft'] == 'border' and gcell['bottomright'] == 'border' and not gcell['moved']:
    #             choices.append(gcell)

    #         choice_cell = choice(choices)
    #         index = grid.index(choice_cell)
    #         grid[index] = cell
    #         grid[row * 20 + col] = choice_cell

    # for col in range(1, 19):
    #   for row in range(1, 19):
    #     # print(row, col)
    #     cell = grid[row * 20 + col]

    #     if len(cell['right']) > 0:
    #       next_cell_right = grid[row * 20 + col + 1]

    #       if not next_cell_right in cell['right']:
    #         right_cell = choice(cell['right'])
    #         index = grid.index(right_cell)
    #         grid[index] = next_cell_right
    #         grid[row * 20 + col + 1] = right_cell

    # for col in range(1, 19):
    #   for row in range(1, 19):
    #     cell = grid[row * 20 + col]

    #     if len(cell['bottom']) > 0:
    #       next_cell_bottom = grid[row * 20 + col + 1]

    #       if not next_cell_bottom in cell['bottom']:
    #         bottom_cell = choice(cell['bottom'])
    #         index = grid.index(bottom_cell)
    #         grid[index] = next_cell_bottom
    #         grid[row * 20 + col + 1] = bottom_cell
