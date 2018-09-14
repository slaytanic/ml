#!/usr/bin/env python

import pygame
import sys
from random import choice

pygame.init()
asurf = pygame.image.load('original.png')
asurf_rect = asurf.get_rect()
black = 0, 0, 0

screen = pygame.display.set_mode([48 * 20, 48 * 20])

iarea = pygame.Rect(0, 0, 48, 48)
cells = []

for x in range(0, 20):
  for y in range(0, 20):
    subsurf = asurf.subsurface(pygame.Rect(x * 49 + x + 1, y * 49 + y + 1, 48, 48))
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
    cells.append({ 'id': [x, y], 'surf': subsurf, 'bottom': [], 'top': [], 'left': [], 'right': [],
                   'topleft': topleft, 'bottomleft': bottomleft, 'topright': topright, 'bottomright': bottomright })

root = None
for cell in cells:
  if (cell['topleft'] == 'border') and (cell['topright'] == 'border') and (cell['bottomleft'] == 'border'):
    root = cell
    break

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

paths = []
curr_node = root
grid = cells.copy()
# index = grid.index(root)
# grid[index] = grid[0]
# grid[0] = root
# col = 0
# row = 0

print('grid len', len(grid))

iternum = 0
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)
  posx = 0
  posy = 0
  count = 0
  for cell in grid:
    if cell:
      screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
    posx += 48
    count += 1
    if count >= 20:
      count = 0
      posx = 0
      posy += 48

  pygame.display.flip()

  iternum += 1
  # print('Gen', iternum)
  for col in range(0, 20):
    for row in range(0, 20):
      # print(row, col)
      cell = grid[row * 20 + col]
      if row == 0 and col == 0:
        if cell['topleft'] != 'border' or cell['topright'] != 'border' or cell['bottomleft'] != 'border':
          choices = []
          for gcell in grid:
            # print(gcell['topleft'], gcell['topright'], gcell['bottomleft'])
            if (gcell['topleft'] == 'border') and (gcell['topright'] == 'border') and (gcell['bottomleft'] == 'border'):
              index = grid.index(gcell)
              grid[index] = cell
              grid[row * 20 + col] = gcell
      elif row == 0:
        if not (cell['topleft'] == 'border' and cell['topright'] == 'border'):
          choices = []
          for gcell in reversed(grid):
            if gcell['topleft'] == 'border' and gcell['topright'] == 'border':
              choices.append(gcell)

          choice_cell = choice(choices)
          index = grid.index(choice_cell)
          grid[index] = cell
          grid[row * 20 + col] = choice_cell
      elif col == 0:
        if not (cell['topleft'] == 'border' and cell['bottomleft'] == 'border'):
          choices = []
          for gcell in reversed(grid):
            if gcell['topleft'] == 'border' and gcell['bottomleft'] == 'border':
              choices.append(gcell)

          choice_cell = choice(choices)
          index = grid.index(choice_cell)
          grid[index] = cell
          grid[row * 20 + col] = choice_cell
      elif col == 19:
        if not (cell['topright'] == 'border' and cell['bottomright'] == 'border'):
          choices = []
          for gcell in grid:
            if gcell['topright'] == 'border' and gcell['bottomright'] == 'border':
              choices.append(gcell)

          choice_cell = choice(choices)
          index = grid.index(choice_cell)
          grid[index] = cell
          grid[row * 20 + col] = choice_cell
      elif row == 19:
        if not (cell['bottomleft'] == 'border' and cell['bottomright'] == 'border'):
          choices = []
          for gcell in grid:
            if gcell['bottomleft'] == 'border' and gcell['bottomright'] == 'border':
              choices.append(gcell)

          choice_cell = choice(choices)
          index = grid.index(choice_cell)
          grid[index] = cell
          grid[row * 20 + col] = choice_cell

  for col in range(1, 19):
    for row in range(1, 19):
      # print(row, col)
      cell = grid[row * 20 + col]

      if len(cell['right']) > 0:
        next_cell_right = grid[row * 20 + col + 1]

        if not next_cell_right in cell['right']:
          right_cell = choice(cell['right'])
          index = grid.index(right_cell)
          grid[index] = next_cell_right
          grid[row * 20 + col + 1] = right_cell

  for col in range(1, 19):
    for row in range(1, 19):
      cell = grid[row * 20 + col]

      if len(cell['bottom']) > 0:
        next_cell_bottom = grid[row * 20 + col + 1]

        if not next_cell_bottom in cell['bottom']:
          bottom_cell = choice(cell['bottom'])
          index = grid.index(bottom_cell)
          grid[index] = next_cell_bottom
          grid[row * 20 + col + 1] = bottom_cell

      # if row < 19 and len(cell['bottom']) > 0:
      #   next_cell_bottom = grid[(row + 1) * 20 + col]

      #   if not next_cell_bottom in cell['bottom']:
      #     bottom_cell = choice(cell['bottom'])
      #     index = grid.index(bottom_cell)
      #     grid[index] = next_cell_bottom
      #     grid[row * 20 + col + 1] = bottom_cell

      # if len(cell['right']) > 0 and len(cell['bottom']) > 0:
      #   if not next_cell_right in cell['right'] and not next_cell_bottom in cell['bottom']:
      #     if len(cell['right']) > 0:
      #       right_cell = choice(cell['right'])
      #       index = grid.index(right_cell)
      #       grid[index] = next_cell_right
      #       grid[row * 20 + col + 1] = right_cell

      #     # if len(cell['bottom']) > 0:
      #     #   bottom_cell = choice(cell['bottom'])
      #     #   index = grid.index(bottom_cell)
      #     #   grid[index] = next_cell_bottom
      #     #   grid[(row + 1) * 20 + col] = bottom_cell




# while row < 20:
# while len(curr_node['right']) > 0:
#   print(row, col)
#   print(curr_node['id'])
#   for cell in curr_node['right']:
#     index = grid.index(cell)
#     oldcell = grid[row * 20 + col]
#     grid[index] = oldcell
#     grid[row * 20 + col] = cell
#     curr_node = cell
#     col += 1
#     break

# curr_path = []
# while len(curr_path) < 20:
#   col = 0
#   row = 1
#   curr_node = root
#   while len(curr_node['bottom']) > 0:
#     for cell in curr_node['bottom']:
#       if not cell in grid:
#         grid[row * 20 + col] = cell
#         curr_node = cell
#         row += 1
#         break

# col = 1
# row = 2
# print(row, col)
# curr_node = grid[1]
# while len(curr_node['bottom']) > 0:
#   print(curr_node['id'])
#   for cell in curr_node['bottom']:
#     if not cell in grid:
#       grid[row * 20 + col] = cell
#       # grid.append(cell)
#       curr_node = cell
#       row += 1
#       print(row)
#       break


# col = 1
# row = 16
# print(row, col)
# curr_node = grid[row * 20]
# # while len(curr_node['right']) > 0:
#   # print(curr_node['id'])
# print(curr_node['id'])
# for cell in curr_node['right']:
#   if not cell in grid: # and grid[row * 20 + col] in cell['top']:
#     grid[row * 20 + col] = cell
#     # grid.append(cell)
#     curr_node = cell
#     col += 1
#     break


  # row += 1
  # col = 0

  # row += 1
  # col = 0
  # print(row * 20 - 20)
  # try:
  #   print('bottom', len(grid[row * 20 - 20]['bottom']))
  #   for cell in grid[row * 20 - 20]['bottom']:
  #     if not cell in grid:
  #       # grid.append(cell)
  #       grid[row * 20 + col] = cell
  #       curr_node = cell
  #       col += 1
  #       break
  #     else:
  #       print('cell already in grid')
  # except:
  #   print('except')
  #   break

print(len(grid))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)
  posx = 0
  posy = 0
  count = 0
  # for cell in cells:
  #   if cell['id'] == [16, 19]:
  #     screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
  for cell in grid:
    if cell:
      screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
    posx += 48
    count += 1
    if count >= 20:
      count = 0
      posx = 0
      posy += 48

  pygame.display.flip()

sys.exit()

possible_cells = []
row = 0
col = 0

cells_in_pos = []

while row < 20:
  print(row, col)
  prevcells = cells_in_pos
  cells_in_pos = []

  if row == 0 and col == 0:
    for cell in cells:
      if (cell['topleft'] == 'border') and (cell['topright'] == 'border') and (cell['bottomleft'] == 'border'):
        cells_in_pos.append(cell)
        # prevcells = [cell]
        root = cell
        break
  elif row == 0 and col > 0:
    print('here', prevcells)
    for prevcell in prevcells:
      for cell in cells:
        if cell['topleft'] == prevcell['topright'] and cell['bottomleft'] == prevcell['bottomright'] and cell['topright'] == 'border':
          cells_in_pos.append(cell)
          prevcell['right'] = cell
          cell['left'] = prevcell
    # print('here2', len(cells_in_pos))
    # sys.exit(1)
          # prevcells.push(cell)
  # elif col == 0 and row > 0:
  #   # print('here')
  #   prevpos = 20 * row - 20 + col
  #   for cell in cell_list:
  #     if cell['topleft'] == newcells[prevpos]['bottomleft'] and cell['topright'] == newcells[prevpos]['bottomright']:
  #       # newcells.append(cell)
  #       cells_in_pos.append(cell)
  #       newcells[prevpos]['bottom'] = cell
  #       cell['top'] = newcells[prevpos]['bottom']
  #       prevcell = cell
  #       # cell_list.remove(cell)
  #       # found_match = True
  #       # break
  # elif col > 0 and row > 0:
  #   prevpos = 20 * row - 20 + col
  #   for cell in cell_list:
  #     if cell['topleft'] == newcells[prevpos]['bottomleft'] and cell['topright'] == newcells[prevpos]['bottomright'] and prevcell['bottomright'] == cell['bottomleft']:
  #       # newcells.append(cell)
  #       cells_in_pos.append(cell)
  #       prevcell['right'] = cell
  #       cell['left'] = prevcell
  #       newcells[prevpos]['bottom'] = cell
  #       cell['top'] = newcells[prevpos]['bottom']
  #       prevcell = cell
  #       # cell_list.remove(cell)
  #       # found_match = True
  #       # break

  possible_cells.append(cells_in_pos)
  # if len(cells_in_pos) == 1:
  for cell in cells_in_pos:
    cells.remove(cell)

  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)
  posx = 0
  posy = 0
  count = 0
  for cells_in_pos in possible_cells:
    try:
      cell = cells_in_pos[0]
      screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
      posx += 48
      count += 1
      if count >= 20:
        count = 0
        posx = 0
        posy += 48
    except:
      pass

  pygame.display.flip()

  # print(cells_in_pos)
  col += 1
  if col >= 20:
    col = 0
    row += 1

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  screen.fill(black)
  posx = 0
  posy = 0
  count = 0
  for cells_in_pos in possible_cells:
    try:
      cell = cells_in_pos[0]
      screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
      posx += 48
      count += 1
      if count >= 20:
        count = 0
        posx = 0
        posy += 48
    except:
      pass

  pygame.display.flip()

  # if found_match != True:
  #   print('reset state had', len(newcells), 'cells')
  #   # break
  #   # print('reset state had', len(newcells), 'cells')
  #   newcells = []
  #   found_match = True
  #   row = 0
  #   col = 0
  #   # cells = original_cells.copy()
  #   # shuffle(cells)
  #   # break
  #   next
  # else:
  #   break


# prevcell = newcells[0]
# found_match = True
# while len(newcells) < 20:
#   found_match = False
#   for cell in cells:
#     if cell['topleft'] == prevcell['topright'] and cell['bottomleft'] == prevcell['bottomright'] and cell['topright'] == 'border':
#       newcells.append(cell)
#       prevcell = cell
#       cells.remove(cell)
#       found_match = True
#       break


# row = 1
# col = 0
# found_match = True
# while len(newcells) < 22 and found_match == True:
#   prevpos = 20 * row - 20 + col
#   print(prevpos)
#   print(newcells[prevpos])
#   found_match = False
#   for cell in cells:
#     if cell['topleft'] == newcells[prevpos]['bottomleft'] and cell['topright'] == newcells[prevpos]['bottomright']:
#       print('possible match', prevcell['bottomright'] == cell['bottomleft'], prevcell, cell)
#       # sys.exit()
#       # if (col > 0 and prevcell['bottomright'] == cell['bottomleft']) or col == 0:
#       if col == 0 or (prevcell['bottomright'] == cell['bottomleft'] and col > 0):
#       # if True:
#         newcells.append(cell)
#         prevcell = cell
#         print(cell)
#         cells.remove(cell)
#         # col += 1
#         if col >= 20:
#           col = 0
#           row += 1
#         found_match = True
#         break

#   screen.fill(black)
#   # screen.blit(asurf, asurf_rect)
#   posx = 0
#   posy = 0
#   count = 0
#   for cell in newcells:
#     screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
#     posx += 48
#     count += 1
#     if count >= 20:
#       count = 0
#       posx = 0
#       posy += 48

#   pygame.display.flip()


# while 1:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT: sys.exit()

#   screen.fill(black)
#   posx = 0
#   posy = 0
#   count = 0
#   for cell in newcells:
#     screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
#     posx += 48
#     count += 1
#     if count >= 20:
#       count = 0
#       posx = 0
#       posy += 48

#   pygame.display.flip()

  # pygame.display.flip()

#     screen.fill(black)
#     # screen.blit(asurf, asurf_rect)
#     posx = 0
#     posy = 0
#     count = 0
#     for cell in newcells:
#       screen.blit(cell['surf'], [posx, posy]) #pygame.Rect(posx, posy, 48, 48))
#       posx += 48
#       count += 1
#       if count >= 20:
#         count = 0
#         posx = 0
#         posy += 48

#     pygame.display.flip()
