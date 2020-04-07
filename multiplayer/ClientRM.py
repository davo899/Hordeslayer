from socket import *
from pygame import *
import json
import math

init()
offset = [0, 0]

black = (0, 0, 0)

win = display.set_mode((800, 500))
bg = image.load("images/bg.jpg")
clock = time.Clock()

s = socket(AF_INET, SOCK_STREAM)
s.bind((gethostbyname(gethostname()), 1025))
s.connect(("192.168.0.7", 1026))

def bgOffset(pos):
    return [(-pos[0])+400, (-pos[1])+250]


def selfDraw(pos, col, dire):
    points = [[400 + int(math.sin(math.radians(dire + 33.69)) * 18.02776), 250 + int(math.cos(math.radians(dire + 33.69)) * 18.02776)],
                [400 + int(math.sin(math.radians(dire + 63.43)) * 33.541), 250 + int(math.cos(math.radians(dire + 63.43)) * 33.541)],
                [400 + int(math.sin(math.radians(dire + 80.53)) * 30.4138), 250 + int(math.cos(math.radians(dire + 80.53)) * 30.4138)],
                [400 + int(math.sin(math.radians(dire + 63.43)) * 11.18034), 250 + int(math.cos(math.radians(dire + 63.43)) * 11.18034)]]

    draw.ellipse(win, col, (376, 226, 48, 48))
    draw.ellipse(win, black, (375, 225, 50, 50), 3)
    draw.polygon(win, black, points)


def playerDraw(pos, col, dire):
    playerOffset = []
    playerOffset.append(offset[0] + pos[0])
    playerOffset.append(offset[1] + pos[1])

    points = [[playerOffset[0] + int(math.sin(math.radians(dire + 33.69)) * 18.02776), playerOffset[1] + int(math.cos(math.radians(dire + 33.69)) * 18.02776)],
                [playerOffset[0] + int(math.sin(math.radians(dire + 63.43)) * 33.541), playerOffset[1] + int(math.cos(math.radians(dire + 63.43)) * 33.541)],
                [playerOffset[0] + int(math.sin(math.radians(dire + 80.53)) * 30.4138), playerOffset[1] + int(math.cos(math.radians(dire + 80.53)) * 30.4138)],
                [playerOffset[0] + int(math.sin(math.radians(dire + 63.43)) * 11.18034), playerOffset[1] + int(math.cos(math.radians(dire + 63.43)) * 11.18034)]]

    draw.ellipse(win, col, (playerOffset[0] - 24, playerOffset[1] - 24, 48, 48))
    draw.ellipse(win, black, (playerOffset[0] - 25, playerOffset[1] - 25, 50, 50), 3)
    draw.polygon(win, black, points)


def zombieDraw(pos, col):
    zombieOffset = []
    zombieOffset.append(offset[0] + pos[0])
    zombieOffset.append(offset[1] + pos[1])

    draw.ellipse(win, col, (zombieOffset[0] - 24, zombieOffset[1] - 24, 48, 48))
    draw.ellipse(win, black, (zombieOffset[0] - 25, zombieOffset[1] - 25, 50, 50), 3)


def bulletDraw(pos):
    pos[0] += offset[0]
    pos[1] += offset[1]

    draw.ellipse(win, (255, 255, 100), (pos[0] - 3, pos[1] - 3, 6, 6))
    

def update(gameInfo):
    global offset
    win.fill(black)
    for i in gameInfo[0]:
        if i[0] == ownID:
            offset = bgOffset(i[1])
            win.blit(bg, (offset[0], offset[1], 1600, 1600))
            
    for i in gameInfo[0]:
        if i[0] == ownID:
            selfDraw(i[1], i[2], i[3])
        else:
            playerDraw(i[1], i[2], i[3])

    for i in gameInfo[1]:
        zombieDraw(i[0], i[1])

    for i in gameInfo[2]:
        bulletDraw(i[0])

    display.update()

            
ownID = int(s.recv(4096).decode())
while True:
    keys = key.get_pressed()
    mouseDown = False
    mouseUp = False
    qt = False
    for even in event.get():
        if even.type == MOUSEBUTTONDOWN:
            mouseDown = True
        if even.type == MOUSEBUTTONUP:
            mouseUp = True
        if even.type == QUIT:
            qt = True
    
    s.sendall(json.dumps([mouse.get_pos(), [keys[K_w], keys[K_s], keys[K_a], keys[K_d], keys[K_ESCAPE]], [mouseDown, mouseUp, qt]]).encode())
    #game.update() run by server

    if qt:
        break

    gameInfo = json.loads(s.recv(4096))
    update(gameInfo)
    clock.tick(60)

quit()

    
    
