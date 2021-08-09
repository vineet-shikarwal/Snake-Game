# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 18:33:39 2021

@author: ACER
"""

import pygame as py
from pygame.locals import *
import time
import random

size = 40

class Apple:
    def __init__(self, surface):
        self.parent_screen= surface
        self.image= py.image.load('apple.jpg').convert()
        self.x= 120
        self.y= 120
        
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x,self.y))
        py.display.flip()
       
    def move(self):
        self.x= random.randint(1, 23)*size
        self.y= random.randint(1, 15)*size
        

class Snake:
    def __init__(self, surface):
        self.parent_screen= surface
        self.block= py.image.load('block.jpg').convert()
        
        self.length = 1
        self.x= [40]
        self.y= [40]
        self.direction= ''
        
    def move_up(self):
        self.direction= 'up'
        
    def move_down(self):
        self.direction= 'down'
        
    def move_left(self):
        self.direction= 'left'
        
    def move_right(self):
        self.direction= 'right'
        
    def walk(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i]= self.x[i-1]
            self.y[i]= self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= size 
        if self.direction == 'down':
            self.y[0] += size 
        if self.direction == 'left':
            self.x[0] -= size 
        if self.direction == 'right':
            self.x[0] += size 
            
        self.draw()
            
        
    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
        py.display.flip()
            
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        
class Game:
    def __init__(self):
        py.init()
        py.mixer.init()
        
        self.play_background_music()
        self.surface= py.display.set_mode((1000,650))
        self.snake= Snake(self.surface)
        self.snake.draw()
        self.apple= Apple(self.surface)
        self.apple.draw()
        
        # self.screen = py.display.get_surface()
        # w,h = self.screen.get_width() , self.screen.get_height()
        # print(w)
        # print(h)
        
       
        
    def reset(self):
        self.snake= Snake(self.surface)
        self.apple= Apple(self.surface)
        
    def is_collision(self, x1, y1, x2, y2):
        if (x1 >= x2) and (x1 < x2+size):
            if (y1 >= y2) and (y1 < y2+size):
                return True
        return False
        
    
    def display_score(self):
        font= py.font.SysFont('arial', 40)
        score= font.render(f'score: {self.snake.length}', True, 'white')  
        self.surface.blit(score, (850,10))
        
    def play_background_music(self):
        py.mixer.music.load("bg_music_1.mp3")
        py.mixer.music.play(-1, 0)
        
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = py.mixer.Sound("crash.mp3")
        if sound_name == "ding":
            sound = py.mixer.Sound("ding.mp3")
        
        py.mixer.Sound.play(sound)
        
    def render_background(self):
        bg = py.image.load("background.jpg")
        self.surface.blit(bg, (0, 0))
        
        
    def play(self):
        
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        py.display.flip()
        
        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()
        
        # snake colliding itself
        for i in range( 3 , self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise 'collision occured'
                
        
        if (self.snake.x[0]< 0 or self.snake.x[0]>1000 or self.snake.y[0]< 0 or self.snake.y[0]>650):
            self.play_sound("crash")
            raise 'collision occured'
            
            
     
    def show_gameover(self):
        self.render_background()
        font= py.font.SysFont('arial', 40)
        
        line1= font.render(f'Game Over! Your score is : {self.snake.length}', True, 'white')  
        self.surface.blit(line1, (200,300))
        
        line2= font.render('Play Again press Enter. For exit press Escape! ', True, 'white')  
        self.surface.blit(line2, (200,350))
        
        py.mixer.music.pause()
        py.display.flip()
        
    def run(self):
        running= True
        pause= False
        
        while running:
            for event in py.event.get():
                if event.type == KEYDOWN:
                    
                    if event.key == K_ESCAPE:
                        running= False
                        py.quit()
                    
                    if event.key == K_RETURN:
                        py.mixer.music.unpause()
                        pause= False
                        
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                    
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        
                        if event.key == K_RIGHT:
                           self.snake.move_right()
                    
                    
                elif event.type == QUIT:
                    running= False
                    py.quit()
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pause= True
                self.reset()
            
            time.sleep(0.2)


if __name__ == '__main__':
    game= Game()
    game.run()
    
    
