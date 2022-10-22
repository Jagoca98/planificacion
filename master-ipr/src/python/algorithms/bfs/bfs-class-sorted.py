#! usr/bin/python3

import pygame
import time
import numpy as np
import math
import threading
from random import randint as r

# FREE = (random.randint(0.255), 255, 255)
# OBSTACLE = (255, 179, 15)
# VISITED = (141, 181, 128)
# GOAL = (255, 255, 0)
# START = (0, 0, 255)
# PATH = (75, 74, 103)
FREE = (r(0,255), r(0,255), r(0,255))
OBSTACLE = (r(0,255), r(0,179), r(0,15))
VISITED = (r(0,141), r(0,181), r(0,128))
GOAL = (r(0,255), r(0,255), r(0,0))
START = (r(0,0), r(0,0), r(0,255))
PATH = (r(0,75), r(0,74), r(0,103))

class Node:
    def __init__(self, x, y, myId, parentId, distance):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.distance = distance
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

class Bfs:

    def __init__(self, MAP=1):
        """!@brief Creates a new BFS object.

        This Bfs object is being used to setup environment.

        @param MAP The map number in which set the search.
        """
        self.MAP = MAP
        if (self.MAP < 1 or self.MAP > 11):
            self.MAP = 1
        self.FILE_NAME = "../../../../map"+str(self.MAP)+"/map"+str(self.MAP)+".csv"
        self.mutex = threading.Lock()  # is equal to threading.Semaphore(1)
        self.mutex.acquire()
        self.ok = False
        self.done = False
        self.mutex.release()

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
        distance = max(abs(self.end_x - self.start_x), abs(self.end_y - self.start_y)) 
        self.init = Node(self.start_x, self.start_y, 0, self.map2index(self.start_x, self.start_y), distance)

        pygame.init()

        pygame.display.set_caption('Mapa ' + str(self.MAP))
        self.window_surface = pygame.display.set_mode((1000, 1000))

        self.background = pygame.Surface((600, 600))
        self.background.fill(pygame.Color('#000000'))
        self.draw_board()

        self.quit = threading.Thread(target=self.quit)
        self.quit.start()
    
    def draw_square(self, x , y, value):
        """!@brief Draw a simple square.

        This function draw a simple square in the position (x,y) with the value using pygame.

        @param x The x coordinate of the cell.
        @param y The y coordinate of the cell.
        @param value The value of the cell.
        """
        # R if value=1, G if value=2, W if value=0, Y if value=3, B if value=4
        if value == '0':
            self.color = FREE
        elif value == '1':
            self.color = OBSTACLE
        elif value == '2':
            self.color = VISITED
        elif value == '3':
            self.color = GOAL
        elif value == '5': # camino
            self.color = PATH
        else:
            self.color = START
        self.rec_ext = pygame.draw.rect( self.window_surface,
                                    self.color, 
                                    pygame.Rect(x*self.window_surface.get_width()/(self.SIZE_X),
                                                y*self.window_surface.get_height()/(self.SIZE_Y),
                                                self.window_surface.get_width()/(self.SIZE_X),
                                                self.window_surface.get_height()/(self.SIZE_Y)),
                                    2,
                                    border_radius=12)
        self.rec_int = pygame.draw.rect( self.window_surface,
                                    self.color, 
                                    pygame.Rect(x*self.window_surface.get_width()/(self.SIZE_X),
                                                y*self.window_surface.get_height()/(self.SIZE_Y),
                                                self.window_surface.get_width()/(self.SIZE_X)-10,
                                                self.window_surface.get_height()/(self.SIZE_Y)-10),
                                    border_radius=12)
        self.rec_int.center = self.rec_ext.center
        pygame.display.update(self.rec_ext)

    def draw_board (self):
        """!@brief Draw the board.

        This function draw the complete board.
        """
        for i in range(len(self.charMap)):
            self.map_x, self.map_y = self.index2map(i)
            self.draw_square(self.map_x, self.map_y, self.charMap[i])

    def index2map(self, index):
        """!@brief Convert from index to map coordinates.

        This function converts the index position of the charMap cell to the (x,y) coordinates of the map cell.

        @param index The index of the charMap cell.
        @return (x, y) The coordinates (x, y) of the map cell. 
        """
        return(index%(self.SIZE_X), math.trunc(index/(self.SIZE_X)))

    def map2index(self, x, y):
        """!@brief Convert from map coordinates to index.

        This function converts the (x,y) coordinates of the map to the index position of the charMap.

        @param x The x coordinate of a map cell.
        @param y The y coordinate of a map cell.
        @return index The index of the charMap cell.
        """
        return(self.SIZE_X * y + x)

    def update_value(self, index, value):
        """!@brief Update the value of a cell.

        This function updates the index cell of a charMap with the value value.

        @param index The index of the charMap cell.
        @param value The value of the map cell.
        """
        self.charMap[index] = value;

    def setup(self, MAP):
        """!@brief Setup Start and Goal position

        This function setup the Start and Goal position depending on the MAP input.

        @param MAP The MAP number in which set the search.
        @return (x_start, y_start, x_end, y_end) The coordinates of the Start and Goal position.
        """
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
        """!@brief Search 4 neighbourgs

        Determine 4-connected neighbourhood of an input cell, checking for map edges

        @param index Input cell index
        @return 4-neighbour cell indexes
        """
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
        """!@brief Search 8 neighbourgs

        Determine 8-connected neighbourhood of an input cell, checking for map edges

        @param index Input cell index
        @return 8-neighbour cell indexes
        """
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
        """!@brief Bfs-sorted algorithm

        Starts the Bfs search with an sorted-by-distance heuristic. The distance is calculated as Chebyseb distance.

        @return nodes Visited nodes during the exploration.
        """
        self.goalParentId = - 1
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
                        distance = max(abs(self.end_x - self.x_tmp), abs(self.end_y - self.y_tmp))  
                        self.node_tmp = Node(self.x_tmp, self.y_tmp, n, self.index, distance)
                        self.bfs.append(self.node_tmp)
                        self.nodes.append(self.node_tmp)
                        self.update_value(n, 2)
                        self.draw_square(self.x_tmp, self.y_tmp, self.charMap[n])
                        time.sleep(0.05)
                    elif (self.charMap[n] == '4'):
                        self.mutex.acquire()
                        self.done = True
                        self.mutex.release()
                        self.x_tmp, self.y_tmp = self.index2map(n)
                        distance = max(abs(self.end_x - self.x_tmp), abs(self.end_y - self.y_tmp))  
                        self.node_tmp = Node(self.x_tmp, self.y_tmp, self.goalParentId, self.index, distance)
                        self.bfs.append(self.node_tmp)
                        self.nodes.append(self.node_tmp)
                        print("Golaso mi nino oleoleole")
            self.bfs = sorted(self.bfs, key=lambda x: x.distance) ## Sort bfs nodes by distance to the goal
        return self.nodes

    def path_search(self):
        """!@brief path search function

        This function looks for the path from the goal to the start.

        """
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
                        self.mutex.acquire()
                        self.ok = True
                        self.mutex.release()
                        input("Press Enter to close")
                        pygame.quit()

    def quit(self):
        """!@brief Quit the game.

        This function let to close pygame whenever.
        """        
        while not self.ok:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mutex.acquire()
                    self.ok = True
                    self.done = True
                    self.mutex.release()
            time.sleep(0.5)

if __name__ == "__main__":
    MAP = int(input('Mapa (1 - 11): '))
    bfs = Bfs(MAP)
    bfs.bfs_search()
    bfs.path_search()