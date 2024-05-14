import pygame
import random
import sys

pygame.init()

# game settings
window_width = 800
window_height = 600
rec_color_r = (255, 0, 0)
rec_color_b = (0, 0, 255)
bullet_color = (255, 255, 255)
player_size = 50
bullet_size = 5

# number of bullets
bullet_list = []
color_yellow = (255, 255, 0)
item_color = (248, 24, 148)
enemy_speed = 6

background_color = (0, 0, 0)
my_font = pygame.font.SysFont("arial", 30)
clock = pygame.time.Clock()
game_fps = 30

#  GUI
screen = pygame.display.set_mode((window_width, window_height))
game_over = False
score = 0

# control
pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
pressed_z = False  # fire
pressed_x = False  # ability


# bullet settings
class bullet:
    def __init__(self, size = [bullet_size, bullet_size], speed = 10, pos = [0, 0], color = bullet_color):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.color = color


def spawn_bullets(bullet_list, xpos, ypos):
    if len(bullet_list) < 5:
        bullet_list.append(bullet(pos=[xpos + (player_size-bullet_size)/2, ypos]))
# (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2, bullet.size, bullet.size)
# spawn bullets at designated postion


def draw_bullets(bullet_list):
    for bullet in bullet_list:
        pygame.draw.rect(screen, bullet.color, (bullet.pos[0], bullet.pos[1], bullet.size[0], bullet.size[1]))


def update_bullet_positions():
    for idx, bullet in enumerate(bullet_list):
        if bullet.pos[1] <= window_height and bullet.pos[1] > 0:
            bullet.pos[1] -= bullet.speed
        else:
            bullet_list.pop(idx)


# player settings
class player:
    def fire(self):
        spawn_bullets(bullet_list, self.pos[0], self.pos[1])
        pass

    def __init__(self, size=[player_size, player_size], speed=[10, 10], pos=[window_width / 2, window_height - 2 * 50], color=rec_color_r):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.color = color
#         self.bullet_list = []


player_main = player()


# enemy settings
class square:
    def __init__(self, size=[50, 50], speed=10, pos=[0, 0], color=rec_color_b):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.color = color


square_list = [square([30, 30], enemy_speed, [random.randint(0, window_width - 10), 0])]


# items
class speedup:
    def __init__(self, size=[10, 10], speed=12, pos=[0, 0], color=item_color):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.color = color


speedup_list = []


def set_level(score):
    speed = score * 0.2 + 1
    return speed


def draw_speedup_items(score, speedup_list):
    pass


def drop_items():
    pass


def drop_enemies(square_list):
    delay = random.random()
    if len(square_list) < 10 and delay < 0.2:
        x_pos = random.randint(0, window_width - 50)
        y_pos = 0
        square_list.append(square([30,30], enemy_speed, [x_pos, y_pos], rec_color_b))


def draw_enemies(square_list):
    for square in square_list:
        pygame.draw.rect(screen, rec_color_b, (square.pos[0], square.pos[1], square.size[0], square.size[1]))


def update_enemy_positions(square_list, score):
    for idx, square in enumerate(square_list):
        if square.pos[1] >= 0 and square.pos[1] < window_height:
            square.pos[1] += square.speed
        else:
            square_list.pop(idx)
            score += 1
    return score


def collision_check(square_list, player):
    for square in square_list:
        if detect_collision(player, square):
            return True
    return False


def killbox_check(square_list, bullet_list):
    for idx, square in enumerate(square_list):
        for bullet in bullet_list:
            if detect_collision(square, bullet):
                square_list.pop(idx)
                return True
    return False


def detect_collision(player, enemy):
    p_x = player.pos[0]
    p_y = player.pos[1]

    e_x = enemy.pos[0]
    e_y = enemy.pos[1]

    if (e_x >= p_x and e_x < (p_x + player.size[0])) or (p_x >= e_x and p_x < (e_x + enemy.size[0])):
        if (e_y >= p_y and e_y < (p_y + player.size[1])) or (p_y >= e_y and p_y < (e_y + enemy.size[1])):
            return True


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressed_left = True
            elif event.key == pygame.K_RIGHT:
                pressed_right = True
            elif event.key == pygame.K_UP:
                pressed_up = True
            elif event.key == pygame.K_DOWN:
                pressed_down = True
            elif event.key == pygame.K_z:
                pressed_z = True
            elif event.key == pygame.K_x:
                pressed_x = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressed_left = False
            elif event.key == pygame.K_RIGHT:
                pressed_right = False
            elif event.key == pygame.K_UP:
                pressed_up = False
            elif event.key == pygame.K_DOWN:
                pressed_down = False
            elif event.key == pygame.K_z:
                pressed_z = False
            elif event.key == pygame.K_x:
                pressed_x = False
    screen.fill(background_color)
    x = player_main.pos[0]
    y = player_main.pos[1]
    if pressed_left and x > 0:
        x -= player_main.speed[0]
    if pressed_right and x < window_width - player_size:
        x += player_main.speed[0]
    if pressed_up and y > 0:
        y -= player_main.speed[1]
    if pressed_down and y < window_height - player_size:
        y += player_main.speed[1]
    if pressed_x:
        pass
    if pressed_z:
        player_main.fire()

    player_main.pos = [x, y]
    if collision_check(square_list, player_main):
        game_over = True
        print("Your score is: %d"%score)
        break

    drop_enemies(square_list)
    update_bullet_positions()
    if killbox_check(square_list, bullet_list):
        score += 1
    score = update_enemy_positions(square_list, score)
    enemy_speed = set_level(score)
    text = "Score: " + str(score)
    label = my_font.render(text, 1, color_yellow)
    screen.blit(label, (window_width - 200, window_height - 40))

    draw_bullets(bullet_list)
    draw_enemies(square_list)
    pygame.draw.rect(screen, rec_color_r, (player_main.pos[0], player_main.pos[1], player_main.size[0],player_main.size[1]))

    clock.tick(game_fps)
    pygame.display.update()
