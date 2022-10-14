#! usr/bin/python3

import pygame
import time
import numpy as np
import math
import threading
from sys import exit



class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

class Bfs:

    def __init__(self, MAP=1):
        self.MAP = MAP
        if (self.MAP < 1 or self.MAP > 11):
            self.MAP = 1
        self.FILE_NAME = "../../../../map"+str(self.MAP)+"/map"+str(self.MAP)+".csv"
        self.ok = False

        self.charMap = []
        with open(self.FILE_NAME) as self.f:
            self.line = self.f.readline()
            while self.line:
                self.charLine = self.line.strip().split(',')
                self.charMap.append(self.charLine)
                self.line = self.f.readline() 

        self.SIZE_X = len(self.charLine)
        self.SIZE_Y = len(self.charMap)

        self.charMap = np.concatenate(self.charMap)

        self.start_x, self.start_y, self.end_x, self.end_y = self.setup(self.MAP)
        self.init = Node(self.start_x, self.start_y, 0, self.map2index(self.start_x, self.start_y))

        pygame.init()

        pygame.display.set_caption('Mapa ' + str(self.MAP))
        self.window_surface = pygame.display.set_mode((1000, 1000))

        self.background = pygame.Surface((600, 600))
        self.background.fill(pygame.Color('#000000'))
        self.draw_board()
        quit = threading.Thread(target=self.quit)
        quit.start()

    def draw_square(self, x , y, value):
        # R if value=1, G if value=2, W if value=0, Y if value=3, B if value=4
        if value == '0':
            self.color = (255, 255, 255)
            self.colorint = (255, 255, 255, 100)
        elif value == '1':
            self.color = (255, 0, 0)
            self.colorint = (255, 0, 0, 100)
        elif value == '2':
            self.color = (0, 255, 0)
            self.colorint = (0, 255, 0, 100)
        elif value == '3':
            self.color = (255, 255, 0)
            self.colorint = (255, 255, 0, 100)
        elif value == '5': # camino
            self.color = (128, 64, 0)
            self.colorint = (128, 64, 0, 100)
        else:
            self.color = (0, 0, 255)
            self.colorint = (0, 0, 255, 100)
        self.rec_ext = pygame.draw.rect( self.window_surface,
                                    self.color, 
                                    pygame.Rect(x*self.window_surface.get_width()/(self.SIZE_X),
                                                y*self.window_surface.get_height()/(self.SIZE_Y),
                                                self.window_surface.get_width()/(self.SIZE_X),
                                                self.window_surface.get_height()/(self.SIZE_Y)),
                                    2,
                                    border_radius=12)
        self.rec_int = pygame.draw.rect( self.window_surface,
                                    self.colorint, 
                                    pygame.Rect(x*self.window_surface.get_width()/(self.SIZE_X),
                                                y*self.window_surface.get_height()/(self.SIZE_Y),
                                                self.window_surface.get_width()/(self.SIZE_X)-10,
                                                self.window_surface.get_height()/(self.SIZE_Y)-10),
                                    border_radius=12)
        self.rec_int.center = self.rec_ext.center
        pygame.display.update(self.rec_ext)

    def draw_board (self):
        for i in range(len(self.charMap)):
            self.map_x, self.map_y = self.index2map(i)
            self.draw_square(self.map_x, self.map_y, self.charMap[i])

    def index2map(self, index):
        return(index%(self.SIZE_X), math.trunc(index/(self.SIZE_X)))

    def map2index(self, x, y):
        return(self.SIZE_X * y + x)

    def update_value(self, index, value):
        self.charMap[index] = value;

    def setup(self, MAP):
        if MAP == 1:
            start_x = 3
            start_y = 3
            end_x = 3
            end_y = 8
        elif MAP == 2:
            start_x = 3
            start_y = 3
            end_x = 8
            end_y = 11
        elif MAP == 3:
            start_x = 11
            start_y = 5
            end_x = 15
            end_y = 5
        elif MAP == 4:
            start_x = 15
            start_y = 5
            end_x = 11
            end_y = 5
        elif MAP == 5:
            start_x = 16
            start_y = 4
            end_x = 10
            end_y = 4
        elif MAP == 6:
            start_x = 3
            start_y = 3
            end_x = 18
            end_y = 11
        elif MAP == 7:
            start_x = 10
            start_y = 4
            end_x = 16
            end_y = 4
        elif MAP == 8:
            start_x = 3
            start_y = 3
            end_x = 18
            end_y = 11
        elif MAP == 9:
            start_x = 10
            start_y = 4
            end_x = 16
            end_y = 4
        elif MAP == 10:
            start_x = 10
            start_y = 4
            end_x = 16
            end_y = 4
        elif MAP == 11:
            start_x = 16
            start_y = 4
            end_x = 10
            end_y = 4
        i_start = self.map2index(start_x-1, start_y-1)
        self.update_value (i_start, 3)
        i_goal = self.map2index(end_x-1, end_y-1)
        self.update_value (i_goal, 4)
        return start_x-1, start_y-1, end_x-1, end_y-1

    def nhood4(self, index):
        out = []
        if(index > self.SIZE_X * self.SIZE_Y -1):
            print("Evaluating nhood out of the map")
            return out
        if(index % self.SIZE_X > 0):
            out.append(index - 1)
        if(index % self.SIZE_X < self.SIZE_X - 1):
            out.append(index + 1)
        if(index>= self.SIZE_X):
            out.append(index - self.SIZE_X)
        if(index < self.SIZE_X * (self.SIZE_Y - 1)):
            out.append(index + self.SIZE_X)
        return out

    def nhood8(self, index):
        out = self.nhood4(index)
        if(index > self.SIZE_X * self.SIZE_Y - 1):
            return out
        if(index % self.SIZE_X > 0 and index >= self.SIZE_X):
            out.append(index - 1 - self.SIZE_X)
        if(index % self.SIZE_X > 0 and index < self.SIZE_X * (self.SIZE_Y - 1)):
            out.append(index - 1 + self.SIZE_X)
        if(index % self.SIZE_X < self.SIZE_X -1 and index >= self.SIZE_X):
            out.append(index + 1 - self.SIZE_X)
        if(index % self.SIZE_X < self.SIZE_X - 1 and index < self.SIZE_X * (self.SIZE_Y - 1)):
            out.append(index + 1 + self.SIZE_X)
        return out

    def bfs_search(self):
        self.goalParentId = - 1
        self.done = False
        self.visited_flag = np.zeros(self.SIZE_X * self.SIZE_Y)
        self.bfs = []
        self.nodes = []
        self.bfs.append(self.init)
        self.nodes.append(self.init)

        while not self.done:
            self.idx = self.bfs[0]
            self.index = self.map2index(self.idx.x, self.idx.y)
            self.bfs.pop(0)

            for n in self.nhood8(self.index):
                if (not self.visited_flag[n]):
                    self.visited_flag[n] = True
                    if(self.charMap[n] == '0'):
                        self.x_tmp, self.y_tmp = self.index2map(n)
                        self.node_tmp = Node(self.x_tmp, self.y_tmp, n, self.index)
                        self.bfs.append(self.node_tmp)
                        self.nodes.append(self.node_tmp)
                        self.update_value(n, 2)
                        self.draw_square(self.x_tmp, self.y_tmp, self.charMap[n])
                        time.sleep(0.05)
                    elif (self.charMap[n] == '4'):
                        self.done = True
                        self.x_tmp, self.y_tmp = self.index2map(n)
                        self.node_tmp = Node(self.x_tmp, self.y_tmp, self.goalParentId, self.index)
                        self.bfs.append(self.node_tmp)
                        self.nodes.append(self.node_tmp)
                        print("Golaso mi nino oleoleole")
        return self.nodes

    def path_search(self):
        print("%%%%%%%%%%%%%%%%%%%")
        while not self.ok:
            for self.node in self.nodes:
                if( self.node.myId == self.goalParentId):
                    if (self.charMap[self.map2index(self.node.x, self.node.y)] == '2'):
                        self.update_value(self.map2index(self.node.x, self.node.y), 5)
                        self.draw_square(self.node.x, self.node.y, self.charMap[self.map2index(self.node.x, self.node.y)])
                    time.sleep(0.05)
                    self.node.dump()
                    self.goalParentId = self.node.parentId
                    if( self.goalParentId == self.map2index(self.start_x, self.start_y)):
                        print("%%%%%%%%%%%%%%%%%")
                        self.ok = True

    def quit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.ok = True
                    self.done = True
                    break      
            time.sleep(0.5)



if __name__ == "__main__":
    MAP = int(input('Mapa (1 - 11): '))
    bfs = Bfs(MAP)
    bfs.bfs_search()
    bfs.path_search()
    input("Press Enter to close")