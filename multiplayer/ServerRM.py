from socket import *
import threading
import json
import math as m
import random as r
import time
import copy


cols = {0:(255, 0, 0),      #P1 - red
        1:(0, 255, 0),      #P2 - green
        2:(0, 0, 255),      #P3 - blue
        3:(255, 255, 0),    #P4 - yellow
        4:(255, 0, 255),    #P5 - magenta
        5:(0, 255, 255),    #P6 - cyan
        6:(255, 255, 255),  #P7 - white
        7:(0, 0, 0)}        #P8 - black

chance = 180



def attemptZombieSpawn(playerNum):
    global chance
    chance -= (0.001/playerNum)
    n = r.randint(0, int(chance*(playerNum**2)))

    if n == 0:
        side = r.randint(1, 4)
        if side == 1:
            game.zombies.append(Zombie([r.randint(0, 1600), r.randint(0, 25)], (50, 120, 50), r.randint(1, 4)))
        if side == 2:
            game.zombies.append(Zombie([r.randint(1575, 1600), r.randint(0, 1000)], (50, 120, 50), r.randint(1, 4)))
        if side == 3:
            game.zombies.append(Zombie([r.randint(0, 1600), r.randint(975, 1000)], (50, 120, 50), r.randint(1, 4)))
        if side == 4:
            game.zombies.append(Zombie([r.randint(0, 25), r.randint(0, 1000)], (50, 120, 50), r.randint(1, 4)))
            
    


class Game():

    def __init__(self):
        self.players = []
        self.zombies = []
        self.projectiles = []

    def moveZombies(self):
        dire = 270
        for z in self.zombies:
            highest = 10000
            for p in self.players:
                if z.pos[0] < p.pos[0]:
                    xDif = p.pos[0] - z.pos[0]
                else:
                    xDif = z.pos[0] - p.pos[0]

                if z.pos[1] < p.pos[1]:
                    yDif = p.pos[1] - z.pos[1]
                else:
                    yDif = z.pos[1] - p.pos[1]

                dist = m.sqrt((xDif**2)+(yDif**2))
                if dist < highest:
                    highest = dist

                    try:
                        if z.pos[0] > p.pos[0]:
                            if z.pos[1] > p.pos[1]:
                                dire = m.degrees(m.atan((z.pos[0]-p.pos[0]) / (z.pos[1]-p.pos[1])))
                                dire = 90 + dire
                            else:
                                dire = m.degrees(m.atan((z.pos[0]-p.pos[0]) / (p.pos[1]-z.pos[1])))
                                dire = 270 - dire
                        else:
                            if z.pos[1] > p.pos[1]:
                                dire = m.degrees(m.atan((p.pos[0]-z.pos[0]) / (z.pos[1]-p.pos[1])))
                                dire = 90 - dire
                            else:
                                dire = m.degrees(m.atan((p.pos[0]-z.pos[0]) / (p.pos[1]-z.pos[1])))
                                dire = 270 + dire
                    except ZeroDivisionError:
                        if z.pos[0] > i.pos[0]:
                            dire = 0
                        else:
                            dire = 180
            
            z.pos[0] += m.cos(m.radians(dire)) * z.speed
            z.pos[1] -= m.sin(m.radians(dire)) * z.speed

            clear = False
            while not clear:
                for i in self.zombies:
                    if i != z:
                        if z.pos[0] > i.pos[0] - 50 and z.pos[0] < i.pos[0] + 50 and z.pos[1] > i.pos[1] - 50 and z.pos[1] < i.pos[1] + 50:
                            try:
                                if z.pos[0] > i.pos[0]:
                                    if z.pos[1] > i.pos[1]:
                                        dire = m.degrees(m.atan((z.pos[0]-i.pos[0]) / (z.pos[1]-i.pos[1])))
                                        dire = 90 + dire
                                    else:
                                        dire = m.degrees(m.atan((z.pos[0]-i.pos[0]) / (i.pos[1]-z.pos[1])))
                                        dire = 270 - dire
                                else:
                                    if z.pos[1] > i.pos[1]:
                                        dire = m.degrees(m.atan((i.pos[0]-z.pos[0]) / (z.pos[1]-i.pos[1])))
                                        dire = 90 - dire
                                    else:
                                        dire = m.degrees(m.atan((i.pos[0]-z.pos[0]) / (i.pos[1]-z.pos[1])))
                                        dire = 270 + dire
                            except ZeroDivisionError:
                                if z.pos[0] > i.pos[0]:
                                    dire = 0
                                else:
                                    dire = 180

                            z.pos[0] -= m.cos(m.radians(dire)) * 1
                            z.pos[1] += m.sin(m.radians(dire)) * 1
                            break
                else:
                    clear = True
                            
                            
                    

    def update(self, clientsocket, playerID):
        keyInfo = json.loads(clientsocket.recv(4096))
        brk = False

        if keyInfo[2][2]:
            brk = True

        if not brk:
            for i in self.players:
                if i.playerID == playerID:
                    own = i
                    break

            for i in self.players:
                if self.players.index(i) == 0:
                    self.moveZombies()

            attemptZombieSpawn(self.players.index(own)+1)

            mousePos = keyInfo[0]
            keys = keyInfo[1]
            mouseEvents = keyInfo[2]

            mouseXDif = mousePos[0] - 400
            mouseYDif = mousePos[1] - 250

            try:
                if mouseXDif >= 0 and mouseYDif >= 0:
                    own.dir = m.degrees(m.atan(-mouseYDif/mouseXDif))
                if mouseXDif < 0 and mouseYDif >= 0:
                    own.dir = m.degrees(m.atan(mouseXDif/mouseYDif)) + 270
                if mouseXDif < 0 and mouseYDif < 0:
                    own.dir = m.degrees(m.atan(mouseYDif/-mouseXDif)) + 180
                if mouseXDif >= 0 and mouseYDif < 0:
                    own.dir = m.degrees(m.atan(mouseXDif/mouseYDif)) + 90
            except ZeroDivisionError:
                pass

            if mouseEvents[0]:
                if not own.holdingMouse:
                    self.projectiles.append(Bullet(mousePos, [own.pos[0] + int(m.sin(m.radians(own.dir + 71.56)) * 31.6), own.pos[1] + int(m.cos(m.radians(own.dir + 71.56)) * 31.6)], 1, own))
                    
                own.holdingMouse = True
            else:
                own.holdingMouse = False
                
            if keys[0]:
                own.pos[1] -= 5
            elif keys[1]:
                own.pos[1] += 5

            if keys[2]:
                own.pos[0] -= 5
            elif keys[3]:
                own.pos[0] += 5

            for i in self.projectiles:
                if i.player.playerID == own.playerID:
                    i.move()
                    if i.checkCollision(self.zombies):
                        if i in self.projectiles:
                            self.projectiles.remove(i)

                    if i.checkOffScreen():
                        if i in self.projectiles:
                            self.projectiles.remove(i)

            for i in self.zombies:
                if i.health < 0:
                    for x in self.players:
                        if x.playerID == i.lastHit:
                            x.kills += 1
                            
                    if i in self.zombies:
                        self.zombies.remove(i)

                for y in self.players:
                    if y.playerID == playerID:
                        i.checkCollision(y)

            playerInfo = []
            for i in self.players:
                playerInfo.append([i.playerID, i.pos, i.col, i.dir, i.kills])

            zombieInfo = []
            for i in self.zombies:
                zombieInfo.append([i.pos, i.col])

            projectileInfo = []
            for i in self.projectiles:
                projectileInfo.append([i.pos])
                
            gameInfo = json.dumps([playerInfo, zombieInfo, projectileInfo]).encode()
            clientsocket.sendall(gameInfo)
            return None
        
        else:
            return "a summoner has disconnected"


class Player():

    def __init__(self, playerID, pos, dire):
        self.playerID = playerID
        self.dir = dire
        self.pos = pos
        self.health = 10
        self.kills = 0
        self.col = cols[playerID]
        self.holdingMouse = False


class Bullet():

    def __init__(self, clickPos, centre, damage, player):
        self.centre = centre
        self.damage = damage
        self.player = player
        self.lastHit = -1
        self.pos = centre
        self.rad = 10
        self.dir = 270

        try:
            self.dir = m.degrees(m.atan((clickPos[1]-250) / (clickPos[0]-400)))
        except ZeroDivisionError:
            pass

        if clickPos[0] < 400:
            self.dir += 180

    def move(self):
        self.rad += 1

        self.pos[0] = self.centre[0] + int(m.cos(m.radians(self.dir)) * self.rad)
        self.pos[1] = self.centre[1] + int(m.sin(m.radians(self.dir)) * self.rad)

    def checkCollision(self, zombies):
        for i in zombies:
            if self.pos[0] < i.pos[0] + 25 and self.pos[0] > i.pos[0] - 25 and self.pos[1] < i.pos[1] + 25 and self.pos[1] > i.pos[1] - 25:
                i.lastHit = self.player.playerID
                i.health -= self.damage
                return True

        return False

    def checkOffScreen(self):
        if self.pos[0] < -400 or self.pos[1] < -250 or self.pos[0] > 2000 or self.pos[1] > 1250:
            return True
        return False


class Zombie():

    def __init__(self, pos, col, speed):
        self.health = 2
        self.pos = pos
        self.col = col
        self.speed = speed

    def checkCollision(self, player):
        if self.pos[0] > player.pos[0] - 25 and self.pos[0] < player.pos[0] + 25 and self.pos[1] > player.pos[1] - 25 and self.pos[1] < player.pos[1] + 25:
            try:
                if self.pos[0] > player.pos[0]:
                    if self.pos[1] > player.pos[1]:
                        dire = m.degrees(m.atan((self.pos[0]-player.pos[0]) / (self.pos[1]-player.pos[1])))
                        dire = 90 + dire
                    else:
                        dire = m.degrees(m.atan((self.pos[0]-player.pos[0]) / (player.pos[1]-self.pos[1])))
                        dire = 270 - dire
                else:
                    if self.pos[1] > player.pos[1]:
                        dire = m.degrees(m.atan((player.pos[0]-self.pos[0]) / (self.pos[1]-player.pos[1])))
                        dire = 90 - dire
                    else:
                        dire = m.degrees(m.atan((player.pos[0]-self.pos[0]) / (player.pos[1]-self.pos[1])))
                        dire = 270 + dire
            except ZeroDivisionError:
                if self.pos[0] > i.pos[0]:
                    dire = 0
                else:
                    dire = 180
                    
            self.pos[0] -= m.cos(m.radians(dire)) * 20
            self.pos[1] += m.sin(m.radians(dire)) * 20
            player.health -= 1

                
def newPlayer(clientsocket):
    try:
        pID = str(len(game.players))
        clientsocket.send(pID.encode())
        game.players.append(Player(int(pID), [200, 200], 0))

        while True:
            a = game.update(clientsocket, int(pID))
            if a != None:
                print(a)
                game.players.remove(game.players[int(pID)])
                break
            
    except ConnectionResetError:
        game.players.remove(game.players[int(pID)])



def startServer():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((gethostbyname(gethostname()), 1026))
    s.listen(5)

    while True:
        (clientsocket, address) = s.accept()
        print(clientsocket)

        x = threading.Thread(target=newPlayer, args=(clientsocket, ))
        x.start()

game = Game()
startServer()
