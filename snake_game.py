import pygame
import sys
import random
pygame.init()

size = [440, 440]

back_color = (30,30,30)
blue_blocks = (255,255,255)
white_blocks = (205,205,205)
snake_color = (48,221,39)
red = (224, 0, 0)
margin = 1
size_block = 20
count_blocks = 20
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()

class SnakeBlock:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def is_inside(self):
    return 0 <= self.x < count_blocks and 0 <= self.y < count_blocks

  def __eq__(self, other):
    return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

def get_random_empty_block():
  x = random.randint(0, count_blocks - 1)
  y = random.randint(0, count_blocks - 1)
  empty_block = SnakeBlock(x, y)

  while empty_block in snake_blocks:
    empty_block.x = random.randint(0, count_blocks - 1)
    empty_block.y = random.randint(0, count_blocks - 1)
  return empty_block

def draw_block(color, i, j):
  pygame.draw.rect(screen, color,
                   [10 + j * count_blocks + margin * (j + 1),
                    10 + i * count_blocks + margin * (i + 1), 
                    size_block,
                    size_block])

snake_blocks = [SnakeBlock(9, 9)]
apple = get_random_empty_block()
d_row = 0
d_col = 1
total = 0
speed = 1

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP and d_col != 0:
        d_row = -1
        d_col = 0
      elif event.key == pygame.K_DOWN and d_col != 0:
        d_row = 1
        d_col = 0
      elif event.key == pygame.K_LEFT and d_row != 0:
        d_row = 0
        d_col = -1
      elif event.key == pygame.K_RIGHT and d_row != 0:
        d_row = 0
        d_col = 1

  screen.fill(back_color)

  for i in range(count_blocks):
    for j in range(count_blocks):
      if (i + j) % 2 == 0:
        color = blue_blocks
      else:
        color = white_blocks
      draw_block(color, i, j)

  head = snake_blocks[-1]
  if not head.is_inside():
    print('Встреча со стеной!')
    pygame.quit()
    sys.exit()

  draw_block(red, apple.x, apple.y)
  for block in snake_blocks:
    draw_block(snake_color, block.x, block.y)

  if apple == head:
    total += 1
    speed = total//5 + 1
    snake_blocks.append(apple)
    apple = get_random_empty_block()
    print("Счет: ", total)

  new_head = SnakeBlock((head.x + d_row + 20) % 20, (head.y + d_col + 20) % 20)

  if new_head in snake_blocks:
    print('Вы столкнулись с собой')
    pygame.quit()
    sys.exit()

  snake_blocks.append(new_head)
  snake_blocks.pop(0)

  pygame.display.flip()

  timer.tick(3 + speed)#3
