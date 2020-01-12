# coding=UTF-8
import io
import sys
import random
import base64
import pygame

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (213, 213, 213)
RED = (233, 76, 61)
ORANGE = (255, 97, 0)
YELLOW = (241, 196, 15)
GREEN = (28, 143, 26)
BLUE = (52, 161, 218)
PURPLE = (160, 32, 240)
DARKGREY = (45, 62, 80)
DICEGREY = (171, 171, 171)

# define constants
WIDTH = 700
HEIGHT = 900
FPS = 70
FONTFAMILY = 'consolas'
INTERVAL = pygame.USEREVENT
CENTER = 0
LEFTCENTER = 1

pygame.init()

pygame.display.set_caption('Jusdice')
pygame.display.set_icon(pygame.image.load('res/icon.png'))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# time variables
stage_start_time = 0
current_time = 0

game_speed = 1

running = True
# basic data, icons, and sounds
skill_data = [{'color': RED, 'name': 'fire', 'speed': 1},
              {'color': YELLOW, 'name': 'thunder', 'speed': 1},
              {'color': BLUE, 'name': 'snowflake', 'speed': 1},
              {'color': GREEN, 'name': 'poison', 'speed': 0.5},
              {'color': DARKGREY, 'name': 'death', 'speed': 1},
              {'color': DICEGREY, 'name': 'speed', 'speed': 1}]
icon = {'coin': pygame.image.load('res/coin.png'),
        'play': pygame.image.load('res/play.png'),
        'fire': pygame.image.load('res/fire.png'),
        'thunder': pygame.image.load('res/thunder.png'),
        'poison': pygame.image.load('res/poison.png'),
        'snowflake': pygame.image.load('res/snowflake.png'),
        'death': pygame.image.load('res/death.png'),
        'speed': pygame.image.load('res/speed.png'),
        'sword': pygame.image.load('res/sword.png'),
        'add': pygame.image.load('res/add.png')}
sound = {'attack': [pygame.mixer.Sound('res/attack1.wav'),
                    pygame.mixer.Sound('res/attack2.wav'),
                    pygame.mixer.Sound('res/attack3.wav')]}
game_data = {'playing': False,
             'skill': [{'level': 1, 'value': 100, 'money': 100}, {'level': 1, 'value': 2, 'money': 100},
                       {'level': 1, 'value': 2, 'money': 100}, {
                           'level': 1, 'value': 1, 'money': 100},
                       {'level': 1, 'value': 1, 'money': 100}, {'level': 1, 'value': 2, 'money': 100}],
             'coins': 0,
             'adddice': {'time': 0, 'money': 10}, 'dice': [], 'nodice': [], 'wave': 1, 'gameover': False}

tip_texts = pygame.sprite.Group()
fires = pygame.sprite.Group()
lightning = pygame.sprite.Group()
bullets = pygame.sprite.Group()
cubes = pygame.sprite.Group()
cube_to_add = []

all_cubes = 0
dead_cubes = 0


def init():
    for i in range(5):
        game_data['dice'].append([])
        for j in range(5):
            game_data['dice'][i].append({'point': 0, 'skill': -1})
            game_data['nodice'].append([i, j])
            dices.add(Dice(i, j))
    d = random.choice(game_data['nodice'])
    i, j = d
    game_data['nodice'].remove(d)
    game_data['dice'][i][j]['point'] = 1
    game_data['dice'][i][j]['skill'] = random.randint(0, 5)
    pygame.time.set_timer(INTERVAL, 1000)


def interval():
    if game_data['playing'] and len(cube_to_add):
        cubes.add(Cube(*cube_to_add[len(cube_to_add) - 1]))
        del cube_to_add[len(cube_to_add) - 1]
    for cb in cubes.sprites():
        if cb.poison > 0:
            cb.point -= cb.poison


def probable(prob):
    x = random.uniform(0, 1)
    if x < prob:
        return True
    else:
        return False


def make_icon():
    app_icon = pygame.Surface([48, 48])
    app_icon.fill(WHITE)
    pygame.draw.line(app_icon, DICEGREY, (0, 3), (48, 3), 7)
    pygame.draw.line(app_icon, DICEGREY, (3, 0), (3, 48), 7)
    pygame.draw.line(app_icon, DICEGREY, (44, 0), (44, 48), 7)
    pygame.draw.line(app_icon, DICEGREY, (0, 44), (48, 44), 7)
    pygame.draw.circle(app_icon, DICEGREY, (24, 24), 8, 0)
    pygame.image.save(app_icon, 'icon.png')


def show_font(surface, text, color, size, pos, style):
    font_surface = pygame.font.SysFont(
        FONTFAMILY, size).render(str(text), 1, color)
    rect = font_surface.get_rect()
    if style == CENTER:
        rect.center = pos
    elif style == LEFTCENTER:
        rect.left, rect.centery = pos
    surface.blit(font_surface, rect.topleft)


def get_skill_text(skill):
    if skill == 0 or skill == 1 or skill == 3:
        return str(game_data['skill'][skill]['value'])
    if skill == 2:
        return '-' + str(game_data['skill'][skill]['value']) + '%'
    if skill == 4:
        return str(game_data['skill'][skill]['value']) + '%'
    if skill == 5:
        return 'x' + str(game_data['skill'][skill]['value'])


def draw_dice_point(surface, point, color):
    radius = 6
    rect = surface.get_rect()
    if point == 1:
        pygame.draw.circle(surface, color, rect.center, radius, 0)
    elif point == 2:
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery * 3 / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery / 2)], radius, 0)
    elif point == 3:
        pygame.draw.circle(surface, color, rect.center, radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery * 3 / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery / 2)], radius, 0)
    elif point == 4:
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery * 3 / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery * 3 / 2)], radius, 0)
    elif point == 5:
        pygame.draw.circle(surface, color, rect.center, radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx / 2), int(rect.centery * 3 / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 3 / 2), int(rect.centery * 3 / 2)], radius, 0)
    else:
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 2 / 3), rect.centery], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 4 / 3), rect.centery], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 2 / 3), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 4 / 3), int(rect.centery / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 2 / 3), int(rect.centery * 3 / 2)], radius, 0)
        pygame.draw.circle(surface, color, [int(
            rect.centerx * 4 / 3), int(rect.centery * 3 / 2)], radius, 0)


def start_stage():
    global stage_start_time, all_cubes, dead_cubes
    if game_data['wave'] % 10 == 0:
        cube_to_add.append([56, game_data['wave'] ** 2,
                            game_data['wave'] * 10, 110])
        all_cubes = 1
    else:
        for i in range(game_data['wave']):
            cube_to_add.append(
                [48, game_data['wave'] * (game_data['wave'] // 10 + 1), 10, 100])
        all_cubes = game_data['wave']
    dead_cubes = 0
    stage_start_time = pygame.time.get_ticks()
    game_data['playing'] = True


def game_over():
    game_data['playing'] = False
    game_data['gameover'] = True


def make_fire(pos):
    fires.add(Fire(pos, game_data['skill'][0]['value']))


def make_lightning(pos):
    lightning.add(Lightning(pos))


def make_tip_text(text, size, time, color, pos):
    tip_texts.add(TipText(text, size, time, color, pos))


def add_dice():
    if game_data['coins'] >= game_data['adddice']['money'] and len(game_data['nodice']) > 0:
        game_data['coins'] -= game_data['adddice']['money']
        game_data['adddice']['time'] += 1
        game_data['adddice']['money'] += 10
        d = random.choice(game_data['nodice'])
        i, j = d
        game_data['nodice'].remove(d)
        game_data['dice'][i][j]['point'] = 1
        game_data['dice'][i][j]['skill'] = random.randint(0, 5)


def attack(start_pos, skill, duration):
    if len(cubes.sprites()) == 0:
        return
    target = random.choice(cubes.sprites())
    bullets.add(Bullet(target, start_pos, skill, duration))


class Text(object):
    def __init__(self, surface, size, x, y):
        self.surface = surface
        self.image = []
        self.rect = []
        self.size = size
        self.x = x
        self.y = y

    def update(self, text):
        self.image = pygame.font.SysFont(
            FONTFAMILY, self.size).render(str(text), 1, BLACK, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.surface.blit(self.image, self.rect.topleft)


class TipText(pygame.sprite.Sprite):
    def __init__(self, text, size, time, color, pos):
        super().__init__()
        self.text = text
        self.size = size
        self.time = time
        self.start_time = current_time
        self.color = color
        self.image = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', self.size).render(str(self.text),
                                                                                                       1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if current_time - self.start_time >= self.time:
            tip_texts.remove(self)


class DiceContainer(object):
    def __init__(self):
        self.image = pygame.Surface([360, 360])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (350, 330)
        self.size = 360
        pygame.draw.line(self.image, BLACK, (0, 0), (359, 0))
        pygame.draw.line(self.image, BLACK, (0, 0), (0, 359))
        pygame.draw.line(self.image, BLACK, (359, 0), (359, 359))
        pygame.draw.line(self.image, BLACK, (0, 359), (359, 359))

    def update(self):
        screen.blit(self.image, self.rect.topleft)


class Dice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface([64, 64])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.center = [
            47 + (64 * self.x) + 5 * (self.x - 1), 47 + (64 * self.y) + 5 * (self.y - 1)]
        self.last_time = current_time
        self.dice = {}
        self.active = False

    def update(self):
        self.dice = game_data['dice'][self.x][self.y]
        if self.dice['point'] > 0:
            self.image.fill(skill_data[self.dice['skill']]['color'])
            draw_dice_point(self.image, self.dice['point'], WHITE)
            if current_time - stage_start_time < 1000:
                return
            gap = 1000 / game_speed / \
                  skill_data[self.dice['skill']]['speed'] / self.dice['point']
            if self.dice['skill'] == 5:
                gap /= game_data['skill'][self.dice['skill']]['value']
            if game_data['playing'] and current_time >= self.last_time + gap:
                self.last_time += gap * \
                                  ((current_time - self.last_time) // gap)
                attack([self.rect.centerx + dice_container.rect.x, self.rect.centery + dice_container.rect.y],
                       self.dice['skill'], 300)

        else:
            self.image.fill(GREY)


class Cube(pygame.sprite.Sprite):
    def __init__(self, size, point, value, speed):
        super().__init__()
        self.size = size
        self.point = point
        self.value = value
        self.frozen = 0
        self.poison = 0
        self.speed = speed
        self.x = dice_container.rect.left - 60
        self.y = -size
        self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        show_font(self.image, self.point, WHITE, 16,
                  (self.rect.width / 2, self.rect.height / 2), CENTER)

    def update(self):
        if self.point <= 0:
            global dead_cubes
            dead_cubes += 1
            game_data['coins'] += self.value
            cubes.remove(self)
            return
        self.image.fill(RED)
        if self.frozen > 0:
            pygame.draw.circle(self.image, BLUE, [10, 10], 5, 0)
        if self.poison > 0:
            pygame.draw.circle(self.image, GREEN, [
                self.rect.width - 10, 10], 5, 0)
        show_font(self.image, self.point, WHITE, 16,
                  (self.rect.width / 2, self.rect.height / 2), CENTER)
        if self.y >= dice_container.rect.bottom + 60 and self.x <= dice_container.rect.right + 60:
            self.x += self.speed * (100 - self.frozen) / 100 * game_speed / FPS
        elif self.x < dice_container.rect.x:
            self.y += self.speed * (100 - self.frozen) / 100 * game_speed / FPS
        else:
            self.y -= self.speed * (100 - self.frozen) / 100 \
                      * game_speed / FPS
            if self.y <= 0:
                game_over()
        self.rect.center = [self.x, self.y]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, target, start, skill, duration):
        super().__init__()
        self.target = target
        self.start = start
        self.skill = skill
        self.duration = duration
        self.start_time = current_time
        self.image = pygame.Surface([12, 12])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = start
        pygame.draw.circle(
            self.image, skill_data[self.skill]['color'], (6, 6), 6, 0)

    def update(self):
        if self.target.point <= 0:
            if len(cubes.sprites()) > 0:
                self.target = random.choice(cubes.sprites())
            else:
                bullets.remove(self)
                return
        x = self.start[0] + (self.target.rect.centerx - self.start[0]) * (
                current_time - self.start_time) / self.duration
        y = self.start[1] + (self.target.rect.centery - self.start[1]) * (
                current_time - self.start_time) / self.duration
        self.rect.center = [x, y]
        if current_time - self.start_time >= self.duration:
            random.choice(sound['attack']).play()
            self.target.point -= game_data['skill'][self.skill]['level']
            if self.skill == 0:
                make_fire(self.target.rect.center)
            elif self.skill == 1:
                make_lightning(self.target.rect.center)
            elif self.skill == 2:
                self.target.frozen = game_data['skill'][self.skill]['value']
            elif self.skill == 3:
                self.target.poison = game_data['skill'][self.skill]['value']
            elif self.skill == 4:
                if probable(game_data['skill'][self.skill]['value'] / 100) and game_data['wave'] % 10 != 0:
                    self.target.point = 0
                    make_tip_text('爆頭', 48, 200, DARKGREY,
                                  self.target.rect.center)
            bullets.remove(self)


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, area):
        super().__init__()
        self.image = pygame.Surface([area, area])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.image.set_alpha(125)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start_time = current_time
        pygame.draw.circle(
            self.image, RED, (area // 2, area // 2), area // 2, 0)
        for cb in cubes.sprites():
            if cb.rect.colliderect(self.rect):
                cb.point -= game_data['skill'][0]['level']

    def update(self):
        if current_time - self.start_time >= 150:
            fires.remove(self)


class Lightning(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        if 110 < pos[0] < 590:
            self.image = pygame.Surface([480, 3])
            self.rect = self.image.get_rect()
            self.rect.center = (350, 570)
        else:
            self.image = pygame.Surface([3, 570])
            self.rect = self.image.get_rect()
            if pos[0] <= 110:
                self.rect.center = (110, 285)
            else:
                self.rect.center = (590, 285)
        self.image.fill(YELLOW)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.start_time = current_time
        for cb in cubes.sprites():
            if cb.rect.colliderect(self.rect):
                cb.point -= game_data['skill'][1]['level']

    def update(self):
        if current_time - self.start_time >= 200:
            lightning.remove(self)


class CoinContainer:
    def __init__(self):
        self.image = pygame.Surface([250, 80])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.image.blit(icon['coin'], (0, 28))
        self.rect = self.image.get_rect()
        show_font(self.image, str(
            game_data['coins']), BLACK, 20, (28, 40), LEFTCENTER)

    def update(self):
        self.image.fill(WHITE)
        self.image.blit(icon['coin'], (0, 28))
        show_font(self.image, str(
            game_data['coins']), BLACK, 20, (28, 40), LEFTCENTER)
        screen.blit(self.image, (50, add_dice_btn.rect.y))


class ActionBtn(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([80, 80])
        self.image.fill(GREY)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH - 50, add_dice_btn.rect.y)
        self.image.blit(icon['play'], (8, 8))

    def update(self):
        screen.blit(self.image, self.rect.topleft)


class AddDiceBtn():
    def __init__(self):
        self.image = pygame.Surface([80, 80])
        self.image.fill(GREY)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, dice_container.rect.bottom + 120 + 40)
        self.image.blit(icon['add'], (24, 16))
        self.image.blit(icon['coin'], (5, 52))
        show_font(self.image, game_data['adddice']
        ['money'], BLACK, 18, (32, 64), LEFTCENTER)

    def update(self):
        self.image.fill(GREY)
        self.image.blit(icon['add'], (24, 16))
        self.image.blit(icon['coin'], (5, 52))
        show_font(self.image, game_data['adddice']
        ['money'], BLACK, 18, (32, 64), LEFTCENTER)
        screen.blit(self.image, self.rect.topleft)


class UpgradeBtn(pygame.sprite.Sprite):
    def __init__(self, skill, x, y):
        super().__init__()
        self.skill = skill
        self.image = pygame.Surface([64, 64])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.update()

    def update(self):
        self.image.fill(WHITE)
        pygame.draw.line(
            self.image, skill_data[self.skill]['color'], (0, 0), (64, 0), 5)
        pygame.draw.line(
            self.image, skill_data[self.skill]['color'], (0, 0), (0, 64), 5)
        pygame.draw.line(
            self.image, skill_data[self.skill]['color'], (63, 0), (63, 64), 5)
        pygame.draw.line(
            self.image, skill_data[self.skill]['color'], (0, 63), (64, 63), 5)
        self.image.blit(icon[skill_data[self.skill]['name']], (7, 24))
        self.image.blit(icon['sword'], (7, 42))
        show_font(self.image, 'Lv.' +
                  str(game_data['skill'][self.skill]['level']), BLACK, 18, (32, 12), CENTER)
        show_font(self.image, get_skill_text(self.skill),
                  BLACK, 16, (25, 32), LEFTCENTER)
        show_font(self.image, game_data['skill'][self.skill]
        ['level'], BLACK, 16, (25, 50), LEFTCENTER)

    def upgrade(self):
        if game_data['coins'] >= game_data['skill'][self.skill]['money']:
            if self.skill == 0:
                game_data['skill'][self.skill]['value'] += 50
            elif self.skill == 1 and game_data['skill'][self.skill]['level'] % 3 == 0:
                game_data['skill'][self.skill]['value'] += 1
            elif self.skill == 2 and game_data['skill'][self.skill]['level'] % 2 == 0:
                game_data['skill'][self.skill]['value'] += 1
            elif self.skill == 3 and game_data['skill'][self.skill]['level'] % 4 == 0:
                game_data['skill'][self.skill]['value'] += 1
            elif self.skill == 4 and game_data['skill'][self.skill]['level'] % 2 == 0:
                game_data['skill'][self.skill]['value'] += 1
            elif self.skill == 5 and game_data['skill'][self.skill]['level'] % 2 == 0:
                game_data['skill'][self.skill]['value'] += 1
            game_data['coins'] -= game_data['skill'][self.skill]['money']
            game_data['skill'][self.skill]['level'] += 1
            game_data['skill'][self.skill]['money'] += game_data['skill'][self.skill]['level'] * 100
            self.update()
            upgrade_bar.update()


class UpgradeBar:
    def __init__(self):
        self.image = pygame.Surface([WIDTH - 100, 120])
        self.image.fill(GREY)
        self.image.set_colorkey(WHITE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (
            WIDTH / 2, dice_container.rect.bottom + 120 + 80 + 50 + 20)
        self.dices = pygame.sprite.Group()
        self.update()
        for i in range(6):
            self.dices.add(UpgradeBtn(i, self.rect.x + 92 +
                                      64 * i + 30 * (i - 1), self.rect.y + 78))

    def update(self):
        self.image.fill(GREY)
        for i in range(6):
            self.image.blit(icon['coin'], (60 + 64 * i + 30 * (i - 1), 12))
            show_font(self.image, game_data['skill'][i]['money'], BLACK, 16, (84 + 64 * i + 30 * (i - 1), 25),
                      LEFTCENTER)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        self.dices.draw(surface)


class Dragger(object):
    def __init__(self):
        self.dice = None
        self.rect = None
        self.start = None
        self.end = None
        self.x = -1
        self.y = -1
        self.dragging = False

    def set_start(self, pos):
        self.start = pos
        dx = (pos[0] - dice_container.rect.x - 5)
        dy = (pos[1] - dice_container.rect.y - 5)
        self.x = dx // 69
        self.y = dy // 69
        if (dx % 69 < 5 and dy % 69 < 5) or self.x > 4 or self.y > 4 or game_data['dice'][self.x][self.y]['point'] <= 0:
            self.dragging = False
            return
        self.dragging = True
        for i in dices.sprites():
            if i.x == self.x and i.y == self.y:
                self.dice = i.image.copy()
                self.rect = self.dice.get_rect()
                self.rect.center = pos
                break
        if not self.dice:
            self.dragging = False
            return

    def set_end(self, pos):
        self.dragging = False
        if not dice_container.rect.collidepoint(pos):
            self.dice = None
            return
        dx = (pos[0] - dice_container.rect.x - 5)
        dy = (pos[1] - dice_container.rect.y - 5)
        x = dx // 69
        y = dy // 69
        if dx % 69 < 5 or dy % 69 < 5 or x > 4 or y > 4:
            return
        start_dice = game_data['dice'][self.x][self.y]
        end_dice = game_data['dice'][x][y]
        if (x != self.x or y != self.y) and end_dice['skill'] == start_dice['skill'] and \
                end_dice['point'] == start_dice['point']:
            # combine
            if game_data['dice'][x][y]['point'] < 6:
                game_data['dice'][x][y]['point'] += 1
                game_data['dice'][x][y]['skill'] = random.randint(0, 5)
                game_data['dice'][self.x][self.y]['point'] = 0
                game_data['nodice'].append([self.x, self.y])
        self.dice = None
        self.rect = None

    def moving(self, pos):
        self.rect.center = pos

    def draw(self, surface):
        if self.dragging:
            surface.blit(self.dice, self.rect.topleft)


dragger = Dragger()


def event_handle():
    mousepos = pygame.mouse.get_pos()
    if dragger.dragging:
        dragger.moving(mousepos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            return
        elif event.type == pygame.MOUSEBUTTONUP:
            if action_btn.rect.collidepoint(mousepos):
                if not game_data['playing']:
                    start_stage()
            elif add_dice_btn.rect.collidepoint(mousepos):
                add_dice()
            else:
                for btn in upgrade_bar.dices.sprites():
                    if btn.rect.collidepoint(mousepos):
                        btn.upgrade()
                        break
            if dragger.dragging:
                dragger.set_end(mousepos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dice_container.rect.collidepoint(mousepos):
                dragger.set_start(mousepos)
        elif event.type == INTERVAL:
            interval()


wave_font = Text(screen, 48, WIDTH / 2, 50)
dice_container = DiceContainer()
dices = pygame.sprite.Group()
add_dice_btn = AddDiceBtn()
upgrade_bar = UpgradeBar()
coin_container = CoinContainer()
action_btn = ActionBtn()

init()


def main():
    global current_time
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        event_handle()
        screen.fill(WHITE)
        if game_data['playing'] and dead_cubes == all_cubes:
            game_data['playing'] = False
            game_data['wave'] += 1
        if game_data['playing']:
            wave_font.update(str(dead_cubes) + ' / ' + str(all_cubes))
        else:
            wave_font.update('Wave ' + str(game_data['wave']))
        if game_data['gameover']:
            show_font(screen, 'Game Over', RED, 48, (WIDTH / 2, 100), CENTER)
        dice_container.update()
        dices.draw(dice_container.image)
        dices.update()
        pygame.draw.line(screen, BLACK, (110, 0), (110, 570))
        pygame.draw.line(screen, BLACK, (110, 570), (590, 570))
        pygame.draw.line(screen, BLACK, (590, 0), (590, 570))
        coin_container.update()
        action_btn.update()
        add_dice_btn.update()
        upgrade_bar.draw(screen)
        if game_data['playing']:
            cubes.update()
        cubes.draw(screen)
        bullets.update()
        bullets.draw(screen)
        dragger.draw(screen)
        tip_texts.update()
        tip_texts.draw(screen)
        fires.update()
        fires.draw(screen)
        lightning.update()
        lightning.draw(screen)
        # show_font(screen, 'FPS:' + str(round(clock.get_fps(), 1)), BLACK, 18, (10, 20), LEFTCENTER)
        pygame.display.flip()
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
