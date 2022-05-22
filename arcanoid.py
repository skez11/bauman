import pygame
import time
pygame.init()
back = (200, 255, 255)
clock = pygame.time.Clock()

mw = pygame.display.set_mode((500,500))


class Area():
    def __init__(self, x=0, y=0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width = 10, height = 10):
        Area.__init__(self, x=x, y=y, width = width, height = height, color = None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, fsize = 12, text_color = (0,0,0)):
        self.image = pygame.font.SysFont('Verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x = 0, shift_y = 0):
        self.fill()
        mw.blit(self.image, (self.rect.x + start_x, self.rect.y + shift_y))

platform_x = 200
platform_y = 330
start_x = 5
start_y = 5


ball = Picture('ball.png', 160, 200, 50, 50)
platform = Picture('platform.png', platform_x, platform_y, 100, 30)

n = 9
monsters = []
for j in range(3):
    y = start_y + (55*j)
    x = start_x + (27.5*j)
    for i in range(n):
        monster = Picture('enemy.png', x, y, 50, 50)
        monsters.append(monster)
        x+=55
    n -= 1

game_over = False

dx, dy = 3, 3


move_right = False
move_left = False

while not game_over:
    mw.fill(back)
    ball.fill()
    platform.fill()
    
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy*= -1

    ball.draw()
    platform.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.colliderect(platform.rect):
        dy *= -1


    if ball.rect.y > 350:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10,10)
        game_over = True

    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (255, 0, 0))
        time_text.draw(10,10)
        game_over = True


    pygame.display.update()
    clock.tick(40)