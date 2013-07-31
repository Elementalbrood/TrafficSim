__author__ = 'elemental'

from datetime import datetime
import time
from world import *
import pygame


DEBUG = True

black = (  0,   0,   0)
white = (255, 255, 255)
green = (  0, 255,   0)
red   = (255,   0,   0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
grey = (125, 125, 125)


class Universe:
    def __init__(self, world, target=60):
        self.fps_counter = 0
        self.last_frame = datetime.now()
        self.alpha = 0.15
        self.sleep_time = 1
        self.last_FPS = datetime.now()
        self.micro_in_second = 1000000
        self.running = True
        self.target_fps = target
        self.world = world
        self.paused = False
        self.stored_delta = 0
        self.size = [400, 400]
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("ZAH universe")

        self.clock = pygame.time.Clock()

    def start(self):
        pygame.init()

        self.getDelta()
        while self.running:
            self.game_loop()

    def game_loop(self):
        d = self.getDelta()
        self.GetnProcInput()
        self.updateAndRender(d)
        self.update_fps()
        time.sleep(self.sleep_time)
        if self.done:
            self.quit()

    def GetnProcInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def update_fps(self):

        if (datetime.now() - self.last_FPS).seconds >= 60:
            self.last_FPS = datetime.now()

            if DEBUG:
                print(self.fps_counter, self.sleep_time)

            if self.fps_counter < self.target_fps:
                self.sleep_time -= self.alpha * self.sleep_time
            elif self.fps_counter > self.target_fps:
                self.sleep_time += self.alpha * self.sleep_time

            recordedFPS = self.fps_counter
            self.fps_counter = 0

        self.fps_counter += 1

    def updateAndRender(self, delta):
        #update portion
        if not self.paused:
            self.stored_delta += delta
            #print(self.stored_delta, delta)
            if self.stored_delta >= 1:
                self.world.update(self.stored_delta)
                self.stored_delta = 0
        else:
            self.world.update(0)

        #render portion
        self.screen.fill(black)
        grid = self.world.canvas
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                color = black
                if grid[row][column] == World.PATH:
                    color = grey
                elif grid[row][column] == World.INTERSECTION:
                    color = white
                elif grid[row][column] == World.CAR:
                    color = blue
                elif grid[row][column] == World.TRAFFICLIGHT_RED:
                    color = red
                elif grid[row][column] == World.TRAFFICLIGHT_YELLOW:
                    color = yellow
                elif grid[row][column] == World.TRAFFICLIGHT_GREEN:
                    color = green

                pygame.draw.rect(self.screen, color,
                                 [20*column, 20*row, 20, 20])

        self.clock.tick(20)

        pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()

    def getDelta(self):
        t = datetime.now()
        d = t - self.last_frame
        #returns in milliseconds
        d = d.microseconds/1000 + d.seconds*1000
        self.last_frame = t
        return d
