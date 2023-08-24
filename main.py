import pygame
import sys
import time
from pygame.math import Vector2

game_width = 1000.0
game_height = 1000.0
key_pressed = False
clock = pygame.time.Clock()
deltaTime = clock.tick(60) / 1000.0


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
        print(next_pos_x)
        print(next_pos_y)
        if next_pos_x >= game_width or next_pos_x <= 20:
            print("check1")
            self.direction.x *= -1
        if next_pos_y >= game_height or next_pos_y <= 5:
            print("check2")
            self.direction.y *= -1
        else:
            self.position = Vector2(next_pos_x, next_pos_y)


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
        self.position  = new_position


class BAR:
    def __init__(self, height, width):
        self.direction = Vector2(0, 0)
        self.width = width
        self.height = height
        self.speed = 1000 * deltaTime
        self.position = Vector2(game_width - 2/50 * game_width, game_height / 2 - 100 )
        self.collider = self.set_collision()

    def draw_bar(self):
        bar = pygame.Rect(self.position[0], self.position[1], self.height, self.width )
        pygame.draw.rect(screen, (255, 255, 0), bar)

    def move_bar(self):
        self.position = self.position + self.direction * self.speed
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

class MAIN:
    def __init__(self):
        self.bar = BAR(1.5/100*game_height, 2/10*game_width)
        self.score = Vector2(0, 0)
        self.ball = BALL()

    def set_screen(self):
        self.bar.draw_bar()
        self.ball.draw_ball()

    def update(self):
        screen.fill((0, 0, 0))
        self.bar.move_bar()
        self.ball.move_ball()
        collision = self.check_ball_collision()
        self.change_ball_direction(collision)

    def check_ball_collision(self):
        if self.ball.collider.check_collision(self.bar.collider[0]): #top
            return "top"
        elif self.ball.collider.check_collision(self.bar.collider[1]): #middle
            return "middle"
        elif self.ball.collider.check_collision(self.bar.collider[2]): #bottom
            return "bottom"
        return "False"

    def change_ball_direction(self, collision):
        if collision == "top":
            if self.ball.direction.y == 0:
                self.ball.direction.y = -1
            else:
                self.ball.direction.y = self.ball.direction.y * -1
        elif collision == "bottom":
            if self.ball.direction.y == 0:
                self.ball.direction.y = 1
            else:
                self.ball.direction.y = self.ball.direction.y * -1

        if collision != "False":
            self.ball.direction.x = self.ball.direction.x * -1  #hit ball -> turn back always

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
            print("KEYDOWN")
            start_time_press = time.time()
            key_pressed = True
            if event.key == pygame.K_UP:
                main_game.bar.direction[1] = -1
            if event.key == pygame.K_DOWN:
                main_game.bar.direction[1] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and main_game.bar.direction[1] == -1:
                continue
            if event.key == pygame.K_UP and main_game.bar.direction[1] == 1:
                key_pressed = True
                continue
            key_pressed = False
    pygame.display.update()
