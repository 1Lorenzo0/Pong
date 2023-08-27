import pygame
import sys
import time
from pygame.math import Vector2
game_width = 1000.0
game_height = 1000.0
key_pressed = False
clock = pygame.time.Clock()
deltaTime = clock.tick(60) / 1000.0


class AI:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

    def move(self):
        y_diff = self.ball.position.y - self.paddle.position.y

        max_speed = 1

        if abs(y_diff) < max_speed:
            self.paddle.direction.y = y_diff
        else:
            self.paddle.direction.y = max_speed if y_diff > 0 else -max_speed
        self.paddle.move_bar()

class BALL:
    def __init__(self):
        self.position = Vector2(game_width/2, game_height/2 - 100 )
        self.direction = Vector2(1, 0)
        self.radius = 8
        self.speed = 500 * deltaTime
        self.collider = COLLIDER(self.position, self.radius, self.radius)

    def draw_ball(self):
        pygame.draw.circle(screen, (255,255,255), self.position, self.radius)

    def move_ball(self):
        self.check_ball_on_screen()
        self.collider.set_collider_position(self.position)
        pygame.draw.circle(screen, (255,255,255), self.position, self.radius)

    def check_ball_on_screen(self):
        next_pos_x = self.position.x + self.direction.x * self.speed
        next_pos_y = self.position.y + self.direction.y * self.speed
        if next_pos_y >= game_height or next_pos_y <= 5:
            self.direction.y *= -1
        else:
            self.position = Vector2(next_pos_x, next_pos_y)

    def check_goal(self, score):
        next_pos_x = self.position.x + self.direction.x * self.speed
        if next_pos_x >= game_width:
            score[0] += 1
            self.direction.x = -1
            self.position.x, self.position.y = game_width / 2, game_height / 2 - 100
        elif next_pos_x <= 0:
            score[1] += 1
            self.direction.x = 1
            self.position.x, self.position.y = game_width/2, game_height/2 - 100

class COLLIDER:
    def __init__(self, position, radius_x, radius_y):
        self.position = position  # Posizione del collider
        self.radius_x = radius_x      # Raggio del collider
        self.radius_y = radius_y  # Raggio del collider

    def check_collision(self, other_collider):
        distance_x = self.position[0] - other_collider.position[0]
        distance_y = self.position[1] - other_collider.position[1]
        if (abs(distance_x) <= self.radius_x + other_collider.radius_x and
                abs(distance_y) <= self.radius_y + other_collider.radius_y):
            return True
        else:
            return False

    def set_collider_position(self, new_position):
        self.position = new_position


class BAR:
    def __init__(self, height, width, position=None):
        if position is None:
            print("Error, position not mentioned")
        self.direction = Vector2(0, 0)
        self.width = width
        self.height = height
        self.speed = 1000 * deltaTime
        self.position = position
        self.collider = self.set_collision()

    def draw_bar(self):
        bar = pygame.Rect(self.position[0], self.position[1], self.height, self.width )
        pygame.draw.rect(screen, (255, 255, 0), bar)

    def move_bar(self):
        self.change_position()
        self.collider = self.set_collision()
        self.draw_bar()
        if not key_pressed:
            self.direction = Vector2(0, 0)

    def collision_area(self):
        bar = pygame.Rect(self.position[0], self.position[1], self.height, self.width)
        top_third = pygame.Rect(self.position[0], bar.top, self.height, self.width/3)
        middle_third = pygame.Rect(self.position[0], top_third.bottom, self.height, self.width/3)
        bottom_third = pygame.Rect(self.position[0],  middle_third.bottom , self.height, self.width/3)

        return [top_third, middle_third, bottom_third]

    def set_collision(self):
        bar_position = self.collision_area()
        collider = [None, None, None]
        collider[0] = COLLIDER(bar_position[0], self.height / 2, self.width / 3)
        collider[1] = COLLIDER(bar_position[1], self.height / 2, self.width / 3)
        collider[2] = COLLIDER(bar_position[2], self.height / 2, self.width / 3)
        return collider

    def change_position(self):
        new_pos = self.position + self.direction * self.speed
        if new_pos.y + self.width - 10 > game_height or new_pos.y < 0:
            return
        else:
            self.position = new_pos


class MAIN:
    def __init__(self):
        self.bars = self.set_bars()
        self.score = Vector2(0, 0)
        self.ball = BALL()
        self.ai_bar = AI(self.bars[1], self.ball)

    def set_screen(self):
        self.bars[0].draw_bar()
        self.bars[1].draw_bar()
        self.ball.draw_ball()

    def update(self):
        screen.fill((0, 0, 0))
        self.update_bars()
        self.ball.move_ball()
        self.ball.check_goal(self.score)
        collision = self.check_ball_collision()
        self.change_ball_direction(collision)

    def check_ball_collision(self) -> str:
        if (self.ball.collider.check_collision(self.bars[0].collider[0]) or
                self.ball.collider.check_collision(self.bars[1].collider[0])):
            return "top"
        elif (self.ball.collider.check_collision(self.bars[0].collider[1]) or
              self.ball.collider.check_collision(self.bars[1].collider[1])):
            return "middle"
        elif (self.ball.collider.check_collision(self.bars[0].collider[2]) or
              self.ball.collider.check_collision(self.bars[1].collider[2])):
            return "bottom"
        return "False"


    def change_ball_direction(self, collision):
        if collision == "top":
            print("top")
            if self.ball.direction.y == 0:
                self.ball.direction.y = -1
        elif collision == "bottom":
            print("bottom")
            if self.ball.direction.y == 0:
                self.ball.direction.y = 1
        elif collision == "middle":
            print("middle")
            self.ball.direction.y = 0

        if collision != "False":
            self.ball.direction.x = self.ball.direction.x * -1  #hit ball -> turn back always
            self.ball.speed += 1

    def set_bars(self) -> list[BAR]:
        right_bar = Vector2(game_width - 2 / 50 * game_width, game_height / 2 - 100)
        left_bar = Vector2(2 / 50 * game_width - 15, game_height / 2 - 100)
        bar_left = BAR(1.5 / 100 * game_height, 2 / 10 * game_width, left_bar)
        bar_right = BAR(1.5 / 100 * game_height, 2 / 10 * game_width, right_bar)
        return [bar_left, bar_right]

    def update_bars(self):
        self.bars[0].move_bar()
        self.ai_bar.move()


pygame.init()
screen = pygame.display.set_mode((game_width, game_height))
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)
screen.fill((0, 0, 0))

main_game.set_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            key_pressed = True
            if event.key == pygame.K_UP:
                main_game.bars[0].direction[1] = -1
            if event.key == pygame.K_DOWN:
                main_game.bars[0].direction[1] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and main_game.bars[0].direction[1] == -1:
                continue
            if event.key == pygame.K_UP and main_game.bars[0].direction[1] == 1:
                key_pressed = True
                continue
            key_pressed = False
    pygame.display.update()