#! usr/bin/python3

import pygame
import time
import numpy as np
import math

MAP = 1
MAP = int(input('Mapa (1 - 11): '))
if (MAP < 1 or MAP > 11):
    MAP = 1
FILE_NAME = "../../../../map"+str(MAP)+"/map"+str(MAP)+".csv"


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

def draw_square(x , y, value):
    # R if value=1, G if value=2, W if value=0, Y if value=3, B if value=4
    if value == '0':
        color = (255, 255, 255)
        colorint = (255, 255, 255, 100)
    elif value == '1':
        color = (255, 0, 0)
        colorint = (255, 0, 0, 100)
    elif value == '2':
        color = (0, 255, 0)
        colorint = (0, 255, 0, 100)
    elif value == '3':
        color = (255, 255, 0)
        colorint = (255, 255, 0, 100)
    elif value == '5': # camino
        color = (128, 64, 0)
        colorint = (128, 64, 0, 100)
    else:
        color = (0, 0, 255)
        colorint = (0, 0, 255, 100)
    rec_ext = pygame.draw.rect( window_surface,
                                color, 
                                pygame.Rect(x*window_surface.get_width()/(SIZE_X),
                                            y*window_surface.get_height()/(SIZE_Y),
                                            window_surface.get_width()/(SIZE_X),
                                            window_surface.get_height()/(SIZE_Y)),
                                2,
                                border_radius=12)
    rec_int = pygame.draw.rect( window_surface,
                                colorint, 
                                pygame.Rect(  x*window_surface.get_width()/(SIZE_X),
                                                        y*window_surface.get_height()/(SIZE_Y),
                                                        window_surface.get_width()/(SIZE_X)-10,
                                                        window_surface.get_height()/(SIZE_Y)-10),
                                border_radius=12)
    rec_int.center = rec_ext.center
    pygame.display.update(rec_ext)

def draw_board (charmap):
    for i in range(len(charMap)):
        map_x, map_y = index2map(i)
        draw_square(map_x, map_y, charmap[i])

def index2map(index):
    return(index%(SIZE_X), math.trunc(index/(SIZE_X)))

def map2index(x, y):
    return(SIZE_X * y + x)

def update_value(index, value):
    charMap[index] = value;

def setup(MAP):
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
    i_start = map2index(start_x-1, start_y-1)
    update_value (i_start, 3)
    i_goal = map2index(end_x-1, end_y-1)
    update_value (i_goal, 4)
    return start_x-1, start_y-1, end_x-1, end_y-1

def nhood4(index):
    out = []
    if(index > SIZE_X * SIZE_Y -1):
        print("Evaluating nhood out of the map")
        return out
    if(index % SIZE_X > 0):
        out.append(index - 1)
    if(index % SIZE_X < SIZE_X - 1):
        out.append(index + 1)
    if(index>= SIZE_X):
        out.append(index -SIZE_X)
    if(index < SIZE_X * (SIZE_Y - 1)):
        out.append(index + SIZE_X)
    return out

def nhood8(index):
    out = nhood4(index)
    if(index > SIZE_X * SIZE_Y - 1):
        return out
    if(index % SIZE_X > 0 and index >= SIZE_X):
        out.append(index - 1 -SIZE_X)
    if(index % SIZE_X > 0 and index < SIZE_X * (SIZE_Y - 1)):
        out.append(index - 1 + SIZE_X)
    if(index % SIZE_X < SIZE_X -1 and index >= SIZE_X):
        out.append(index + 1 -SIZE_X)
    if(index % SIZE_X < SIZE_X - 1 and index < SIZE_X * (SIZE_Y - 1)):
        out.append(index + 1 + SIZE_X)
    return out

def bfs_search(init):
    goalParentId = - 1
    done = False
    visited_flag = np.zeros(SIZE_X * SIZE_Y)
    bfs = []
    nodes = []
    bfs.append(init)
    nodes.append(init)

    while not done:
        idx = bfs[0]
        index = map2index(idx.x, idx.y)
        bfs.pop(0)

        for n in nhood8(index):
            if (not visited_flag[n]):
                visited_flag[n] = True
                if(charMap[n] == '0'):
                    x_tmp, y_tmp = index2map(n)
                    node_tmp = Node(x_tmp, y_tmp, n, index)
                    bfs.append(node_tmp)
                    nodes.append(node_tmp)
                    update_value(n, 2)
                    draw_square(x_tmp, y_tmp, charMap[n])
                    time.sleep(0.05)
                elif (charMap[n] == '4'):
                    done = True
                    x_tmp, y_tmp = index2map(n)
                    node_tmp = Node(x_tmp, y_tmp, goalParentId, index)
                    bfs.append(node_tmp)
                    nodes.append(node_tmp)
                    print("Golaso mi nino oleoleole")
    return nodes

def path_search(nodes):
    goalParentId = -1
    ok = False
    print("%%%%%%%%%%%%%%%%%%%")
    while not ok:
        for node in nodes:
            if( node.myId == goalParentId):
                if (charMap[map2index(node.x, node.y)] == '2'):
                    update_value(map2index(node.x, node.y), 5)
                    draw_square(node.x, node.y, charMap[map2index(node.x, node.y)])
                time.sleep(0.05)
                node.dump()
                goalParentId = node.parentId
                if( goalParentId == map2index(start_x, start_y)):
                    print("%%%%%%%%%%%%%%%%%")
                    ok = True

## creamos el mapa
charMap = []

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

## calculamos el tamaño del mapa  

SIZE_X = len(charLine)
SIZE_Y = len (charMap)

## Lo convertimos en una lista de elementos 

charMap = np.concatenate(charMap)

start_x, start_y, end_x, end_y = setup(MAP)

## creamos primer nodo

init = Node(start_x, start_y, 0, map2index(start_x, start_y))

pygame.init()

pygame.display.set_caption('Mapa ' + str(MAP))
window_surface = pygame.display.set_mode((1000, 1000))

background = pygame.Surface((600, 600))
background.fill(pygame.Color('#000000'))

draw_board(charMap)

# Ejecutamos el bfs

nodes = bfs_search(init)

# Buscamos el camino

path_search(nodes)

input("Press Enter to close")
    


