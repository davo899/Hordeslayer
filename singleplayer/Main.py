from pygame import *
import math
import copy
import time as t
import random as r

init()

black = (0, 0, 0)

legit = False

def writeHighscore(kills, mode):
    if mode == 0:
        fileName = "scores.txt"
    else:
        fileName = "sharpshooterScores.txt"
        
    try:
        with open(fileName, "r") as file:
            scoreList = file.readlines()
            for i in range(len(scoreList)):
                scoreList[i] = scoreList[i].strip("\n")

    except FileNotFoundError:
        with open(fileName, "w") as file:
            for i in range(10):
                file.write("0\n")

        scoreList = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

    for i in range(len(scoreList)):
        scoreList[i] = int(scoreList[i])

    scoreList.append(kills)
    scoreList.sort()
    scoreList.reverse()

    scoreList.pop(10)

    with open(fileName, "w") as file:
        for i in range(10):
            file.write(str(scoreList[i])+"\n")
            
            

class Game():

    def __init__(self, win, mode, run = True):
        self.win = win
        self.mode = mode
        self.end = False
        self.run = run
        self.bgPos = [0, 0]
        self.clock = time.Clock()
        self.player = Player()
        self.projectiles = []
        self.deathFon = font.SysFont('Verdana', 80)
        self.killsFon = font.SysFont('Verdana', 20)
        self.zombies = [Zombie([0, 20], 2, 50, 3)]
        self.counter = 0
        self.chance = 60
        self.bg = image.load("images/bg.jpg")
        self.dead = False
        self.kills = 0
        self.weaponList = [["SMG", 20, 3, 20, 10], ["Shotgun", 100, 30, 30, 10], ["Assault Rifle", 250, 5, 30, 6], ["LMG", 500, 8, 40, 10], ["Minigun", 1000, 1, 50, 12]]
        self.weaponIndex = -1
        self.weapon = "Pistol"
        self.shooting = 0
        self.holding = False
        self.paused = False
        self.pausing = False
        self.pause = Pause()
        self.health = 3
        self.speedMod = 1
        self.hitShots = 0
        self.missedShots = 0
        
        self.pistol = mixer.Sound("sounds/pistol.ogg")
        self.smg = mixer.Sound("sounds/smg.ogg")
        self.shotgun = mixer.Sound("sounds/shotgun.ogg")
        self.ar = mixer.Sound("sounds/ar.ogg")
        self.lmg = mixer.Sound("sounds/lmg.ogg")
        self.minigun = mixer.Sound("sounds/minigun.ogg")
        self.zSound1 = mixer.Sound("sounds/zombie1.ogg")
        self.zSound2 = mixer.Sound("sounds/zombie2.ogg")
        self.zSound3 = mixer.Sound("sounds/zombie3.ogg")
        self.zSound4 = mixer.Sound("sounds/zombie4.ogg")
        self.zSound5 = mixer.Sound("sounds/zombie5.ogg")
        self.zDeath = mixer.Sound("sounds/zombieDeath.ogg")
        self.zDeath1 = mixer.Sound("sounds/zombieDeath1.ogg")
        self.zDeath2 = mixer.Sound("sounds/zombieDeath2.ogg")
        self.zDeath3 = mixer.Sound("sounds/zombieDeath3.ogg")
        self.zDeath4 = mixer.Sound("sounds/zombieDeath4.ogg")
        self.zDeath5 = mixer.Sound("sounds/zombieDeath5.ogg")
        self.zDeath6 = mixer.Sound("sounds/zombieDeath6.ogg")
        self.zDeath7 = mixer.Sound("sounds/zombieDeath7.ogg")
        self.zDeath8 = mixer.Sound("sounds/zombieDeath8.ogg")
        self.zDeath9 = mixer.Sound("sounds/zombieDeath9.ogg")
        self.zDeath10 = mixer.Sound("sounds/zombieDeath10.ogg")

        self.pistol.set_volume(0.05)
        self.smg.set_volume(0.05)
        self.shotgun.set_volume(0.05)
        self.ar.set_volume(0.04)
        self.lmg.set_volume(0.05)
        self.minigun.set_volume(0.03)
        
        self.gunChannel1 = mixer.Channel(0)
        self.gunChannel2 = mixer.Channel(1)
        self.gunChannel3 = mixer.Channel(2)
        self.zChannel1 = mixer.Channel(3)
        self.zChannel2 = mixer.Channel(4)
        self.zChannel3 = mixer.Channel(5)

        mixer.set_reserved(3)

        if self.mode == 1:
            self.ammo = 999
            self.weapon = "Minigun"
            self.weaponIndex = 0
            self.weaponList = [["Minigun", 1000, 1, 50, 12]]

        if legit:
            self.weaponList.append(["NANI", 1337, 1, 50, 12])

    def playSound(self, sound):
        if self.gunChannel1.get_busy():
            if self.gunChannel2.get_busy():
                self.gunChannel3.play(sound)
            else:
                self.gunChannel2.play(sound)
        else:
            self.gunChannel1.play(sound)

    def playZSound(self, dist, death = False):
        offset = 0
        if not death:
            offset = 0.1
            n = r.randint(0, 4)
            if n == 0:
                sound = self.zSound1
            if n == 1:
                sound = self.zSound2
            if n == 2:
                sound = self.zSound3
            if n == 3:
                sound = self.zSound4
            if n == 4:
                sound = self.zSound5
        else:
            n = r.randint(0, 10)
            if n == 0:
                sound = self.zDeath1
            if n == 1:
                sound = self.zDeath2
            if n == 2:
                sound = self.zDeath3
            if n == 3:
                sound = self.zDeath4
            if n == 4:
                sound = self.zDeath5
            if n == 5:
                sound = self.zDeath6
            if n == 6:
                sound = self.zDeath7
            if n == 7:
                sound = self.zDeath8
            if n == 8:
                sound = self.zDeath9
            if n == 9:
                sound = self.zDeath10
            if n == 10:
                sound = self.zDeath
                
        sound.set_volume((8/dist) + offset)
            
        mixer.find_channel(True).play(sound)

    def update(self):
        self.bgMoveX = 0
        self.bgMoveY = 0

        clickPos = None
        for even in event.get():
            if even.type == QUIT:
                self.end = True
            if even.type == MOUSEBUTTONDOWN:
                if self.weapon != "Pistol":
                    self.holding = True
                else:
                    if not self.paused:
                        self.playSound(self.pistol)
                        dispClickPos = mouse.get_pos()
                        clickPos = [self.bgPos[0] - dispClickPos[0], self.bgPos[1] - dispClickPos[1]]
            if even.type == MOUSEBUTTONUP:
                self.holding = False
                if self.paused:
                    clickPos = mouse.get_pos()

        keys = key.get_pressed()

        if keys[K_ESCAPE]:
            if not self.pausing:
                self.paused = not self.paused
            self.pausing = True
        else:
            self.pausing = False
        
        if not self.paused:
            if self.mode == 0:
                self.counter += 1
                if self.health < 100:
                    self.health += (0.00016*self.health)
                if self.chance > 40:
                    self.chance -= (0.00005*self.chance)
                if self.chance > 20 and self.counter < 18000:
                    self.chance -= (0.00001*self.chance)
                if self.chance > 18 and self.counter > 18000:
                    self.chance -= (0.00001*self.chance)
                if self.speedMod < 2:
                    self.speedMod += (0.00009*self.speedMod)
            else:
                self.chance = 15
                self.health = 50
                self.speedMod = 1
                    
            spawn = r.randint(0, int(self.chance))

            if spawn == 0:
                side = r.randint(1, 4)
                if side == 1:
                    self.zombies.append(Zombie([r.randint(self.bgPos[0], self.bgPos[0] + 1600), r.randint(self.bgPos[1], self.bgPos[1] + 25)], r.randint(0 + int(self.speedMod), 2 + int(self.speedMod)), 50, self.health))
                if side == 2:
                    self.zombies.append(Zombie([r.randint(self.bgPos[0] + 1575, self.bgPos[0] + 1600), r.randint(self.bgPos[1], self.bgPos[1] + 1000)], r.randint(0 + int(self.speedMod), 2 + int(self.speedMod)), 50, self.health))
                if side == 3:
                    self.zombies.append(Zombie([r.randint(self.bgPos[0], self.bgPos[0] + 1600), r.randint(self.bgPos[1] + 975, self.bgPos[1] + 1000)], r.randint(0 + int(self.speedMod), 2 + int(self.speedMod)), 50, self.health))
                if side == 4:
                    self.zombies.append(Zombie([r.randint(self.bgPos[0], self.bgPos[0] + 25), r.randint(self.bgPos[1], self.bgPos[1] + 1000)], r.randint(0 + int(self.speedMod), 2 + int(self.speedMod)), 50, self.health))

            if self.mode == 1:
                if self.ammo == 0:
                    self.dead = True

            if self.holding:
                if self.shooting == 0:
                    self.shooting = self.weaponList[self.weaponIndex][2]
                    
            if self.weapon == "Pistol":
                if clickPos != None:
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + 71.56)) * 31.6), 250 + int(math.cos(math.radians(self.player.dir + 71.56)) * 31.6)], 1))
            else:
                dispClickPos = mouse.get_pos()
                clickPos = [self.bgPos[0] - dispClickPos[0], self.bgPos[1] - dispClickPos[1]]
                
            if self.shooting == self.weaponList[self.weaponIndex][2]:
                weaponL = self.weaponList[self.weaponIndex][3]
                weaponW = self.weaponList[self.weaponIndex][4]
                if self.weapon == "SMG":
                    self.playSound(self.smg)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 0.8))
                if self.weapon == "Shotgun":
                    self.playSound(self.shotgun)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 8))
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir - 15 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir - 15 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 8))
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + 15 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + 15 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 8))
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir - 30 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir - 30 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 8))
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + 30 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + 30 + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 8))
                if self.weapon == "Assault Rifle":
                    self.playSound(self.ar)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 16))
                if self.weapon == "LMG":
                    self.playSound(self.lmg)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 50))
                if self.weapon == "Minigun":
                    self.playSound(self.minigun)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 50))
                    if self.mode == 1:
                        self.ammo -= 1
                if self.weapon == "NANI":
                    self.playSound(self.minigun)
                    self.projectiles.append(Bullet(clickPos, self.bgPos, [400 + int(math.sin(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2))), 250 + int(math.cos(math.radians(self.player.dir + math.degrees(math.atan((10 + weaponL)/(5 + (weaponW/2)))))) * math.sqrt(((10 + weaponL)**2) + ((5 + (weaponW/2))**2)))], 101))

            if self.shooting > 0:
                self.shooting -= 1
                
            keys = key.get_pressed()

            if keys[K_w]:
                if self.bgPos[1] < 225:
                    self.bgPos[1] += 5
                    self.bgMoveY = 5
            elif keys[K_s]:
                if self.bgPos[1] > -725:
                    self.bgPos[1] -= 5
                    self.bgMoveY = -5

            if keys[K_a]:
                if self.bgPos[0] < 375:
                    self.bgPos[0] += 5
                    self.bgMoveX = 5
            elif keys[K_d]:
                if self.bgPos[0] > -1175:
                    self.bgPos[0] -= 5
                    self.bgMoveX = -5

            if self.paused:
                self.bgMoveX = 0
                self.bgMoveY = 0

            mousePos = mouse.get_pos()

            mouseXDif = mousePos[0] - 400
            mouseYDif = mousePos[1] - 250

            try:
                if mouseXDif >= 0 and mouseYDif >= 0:
                    self.player.dir = math.degrees(math.atan(-mouseYDif/mouseXDif))
                if mouseXDif < 0 and mouseYDif >= 0:
                    self.player.dir = math.degrees(math.atan(mouseXDif/mouseYDif)) + 270
                if mouseXDif < 0 and mouseYDif < 0:
                    self.player.dir = math.degrees(math.atan(mouseYDif/-mouseXDif)) + 180
                if mouseXDif >= 0 and mouseYDif < 0:
                    self.player.dir = math.degrees(math.atan(mouseXDif/mouseYDif)) + 90
            except ZeroDivisionError:
                pass
                
        self.win.fill((0, 0, 0))

        if not self.dead:
            self.win.blit(self.bg, (self.bgPos[0], self.bgPos[1], 1600, 1000))

            if self.weapon == "Pistol":
                self.player.draw(self.win, 10, 20, "Pistol")
            else:
                self.player.draw(self.win, self.weaponList[self.weaponIndex][4], self.weaponList[self.weaponIndex][3], self.weapon)

            
            for k in self.projectiles:
                if k.pos[0] < -500 or k.pos[0] > 2100 or k.pos[1] < -500 or k.pos[1] > 1500:
                    self.projectiles.remove(k)
                    self.missedShots += 1
                k.drawCalc(self.paused)
                k.offsetX += self.bgMoveX
                k.offsetY += self.bgMoveY
                k.draw(self.win, self.paused)
                if k.checkCollision(self.zombies):
                    if k in self.projectiles:
                        self.projectiles.remove(k)
                        self.hitShots += 1
                if not self.paused:
                    k.rad += 20

            for i in self.zombies:
                xDif = 400 - i.pos[0]
                yDif = 250 - i.pos[1]
                dist = math.sqrt((xDif**2) + (yDif**2))
                if dist < 300:
                    n = r.randint(0, 40)
                    if n == 0 and not self.paused:
                        self.playZSound(dist)
                if i.health <= 0:
                    self.kills += 1
                    self.zombies.remove(i)
                    
                    xDif = 400 - i.pos[0]
                    yDif = 250 - i.pos[1]
                    dist = math.sqrt((xDif**2) + (yDif**2))
                    if dist < 300 and not self.paused:
                        self.playZSound(dist, True)
                        
                i.drawCalc()
                i.checkPlayerCollision(self.player, self.paused)
                i.offsetX += self.bgMoveX
                i.offsetY += self.bgMoveY
                i.draw(self.win, self.zombies, self.paused)

            for i in self.weaponList:
                if self.kills == i[1]:
                    self.weaponIndex = self.weaponList.index(i)
                    self.weapon = i[0]

            draw.rect(self.win, (0, 0, 0), (8, 478, 104, 16))
            draw.rect(self.win, (255, 0, 0), (10, 480, self.player.health * 10, 12))

            if self.mode == 1:
                ammo = self.killsFon.render("Ammo: "+str(self.ammo), False, (100, 100, 255), (0, 0, 0))
                self.win.blit(ammo, (650, 450))

            kills = self.killsFon.render("KILLS: "+str(self.kills), False, (255, 255, 0), (0, 0, 0))
            self.win.blit(kills, (20, 20))

            try:
                nxt = self.killsFon.render(self.weaponList[self.weaponIndex + 1][0]+" at "+str(self.weaponList[self.weaponIndex + 1][1])+" kills", False, (255, 255, 0), (0, 0, 0))
                self.win.blit(nxt, (20, 50))

                try:
                    acc = self.killsFon.render("Accuracy: "+str(int(round(self.hitShots/(self.hitShots+self.missedShots), 2) * 100))+"%", False, (255, 255, 0), (0, 0, 0))
                except ZeroDivisionError:
                    acc = self.killsFon.render("Accuracy: 0%", False, (255, 255, 0), (0, 0, 0))
                self.win.blit(acc, (20, 80))
            except IndexError:
                try:
                    acc = self.killsFon.render("Accuracy: "+str(int(round(self.hitShots/(self.hitShots+self.missedShots), 2) * 100))+"%", False, (255, 255, 0), (0, 0, 0))
                except ZeroDivisionError:
                    acc = self.killsFon.render("Accuracy: 0%", False, (255, 255, 0), (0, 0, 0))
                self.win.blit(acc, (20, 50))
                    
            if self.player.health < 0:
                self.dead = True

            if not self.paused:
                if self.player.health > 10:
                    self.player.health = 10
                elif self.player.health == 10:
                    pass
                else:
                    self.player.health += 0.01
                
        else:
            writeHighscore(self.kills, self.mode)
                
            death = self.deathFon.render("GAME OVER", False, (255, 255, 255))
            self.win.blit(death, (153, 180))

            kills = self.killsFon.render("You got "+str(self.kills)+" kills", False, (100, 100, 255), (0, 0, 0))
            self.win.blit(kills, (323, 300))

            display.update()
            
            t.sleep(3)
            
            self.run = False

        if self.paused:
            mousePos = mouse.get_pos()
            if clickPos == None:
                oof = self.pause.update(self.win, mousePos)
            else:
                if self.pause.update(self.win, mousePos, clickPos) == "unPause":
                    if not self.pausing:
                        self.paused = not self.paused
                        self.pausing = True
                    else:
                        self.pausing = False
                if self.pause.update(self.win, mousePos, clickPos) == "endGame":
                    if not self.pausing:
                        self.paused = not self.paused
                        self.dead = True
                        self.pausing = True
                    else:
                        self.pausing = False
        else:
            display.update()



class Player():

    def __init__(self):
        self.col = (150, 10, 10)
        self.dir = 0
        self.health = 10

    def draw(self, win, weaponW, weaponL, weapon):
        if weapon == "Pistol":
            self.points = [[400 + int(math.sin(math.radians(self.dir + 33.69)) * 18.02776), 250 + int(math.cos(math.radians(self.dir + 33.69)) * 18.02776)],\
                           [400 + int(math.sin(math.radians(self.dir + 63.43)) * 33.541), 250 + int(math.cos(math.radians(self.dir + 63.43)) * 33.541)],\
                           [400 + int(math.sin(math.radians(self.dir + 80.53)) * 30.4138), 250 + int(math.cos(math.radians(self.dir + 80.53)) * 30.4138)],\
                           [400 + int(math.sin(math.radians(self.dir + 63.43)) * 11.18034), 250 + int(math.cos(math.radians(self.dir + 63.43)) * 11.18034)]]
        else:
            self.points = [[400 + int(math.sin(math.radians(self.dir + math.degrees(math.atan(10/(5 + weaponW))))) * math.sqrt((10**2) + ((5 + weaponW)**2))), 250 + int(math.cos(math.radians(self.dir + math.degrees(math.atan(10/(5 + weaponW))))) * math.sqrt((10**2) + ((5 + weaponW)**2)))],\
                           [400 + int(math.sin(math.radians(self.dir + math.degrees(math.atan((10 + weaponL)/(5 + weaponW))))) * math.sqrt(((10 + weaponL)**2) + ((5 + weaponW)**2))), 250 + int(math.cos(math.radians(self.dir + math.degrees(math.atan((10 + weaponL)/(5 + weaponW))))) * math.sqrt(((10 + weaponL)**2) + ((5 + weaponW)**2)))],\
                           [400 + int(math.sin(math.radians(self.dir + math.degrees(math.atan((10 + weaponL)/5)))) * math.sqrt(((10 + weaponL)**2) + (5**2))), 250 + int(math.cos(math.radians(self.dir + math.degrees(math.atan((10 + weaponL)/5)))) * math.sqrt(((10 + weaponL)**2) + (5**2)))],\
                           [400 + int(math.sin(math.radians(self.dir + math.degrees(math.atan(10/5)))) * math.sqrt((10**2) + (5**2))), 250 + int(math.cos(math.radians(self.dir + math.degrees(math.atan(10/5)))) * math.sqrt((10**2) + (5**2)))]]
            
        draw.ellipse(win, self.col, (376, 226, 48, 48))
        draw.ellipse(win, black, (375, 225, 50, 50), 3)
        draw.polygon(win, black, self.points)
        


class Bullet():

    def __init__(self, clickPos, scenePos, centre, damage):
        self.pos = [0, 0]
        self.offsetX = 0
        self.offsetY = 0
        self.damage = damage
        #self.nani = image.load("images/nani.png")

        try:
            self.dir = math.degrees(math.atan((clickPos[1] - (copy.copy(scenePos[1]) - 250)) / (clickPos[0] - (copy.copy(scenePos[0]) - 400))))
        except ZeroDivisionError:
            self.dir = 0
            
        if scenePos[0] - 400 < clickPos[0] and scenePos[1] - 250 > clickPos[1]:
            self.dir = 180 + self.dir
        if scenePos[0] - 400 == clickPos[0] and scenePos[1] - 250 > clickPos[1]:
            self.dir = 90
                
        if scenePos[0] - 400 < clickPos[0] and scenePos[1] - 250 < clickPos[1]:
            self.dir = 180 + self.dir
        if scenePos[0] - 400 < clickPos[0] and scenePos[1] - 250 == clickPos[1]:
            self.dir = 180
            
        if scenePos[0] - 400 > clickPos[0] and scenePos[1] - 250 < clickPos[1]:
            self.dir = 360 + self.dir
        if scenePos[0] - 400 == clickPos[0] and scenePos[1] - 250 < clickPos[1]:
            self.dir = 270

        while self.dir > 360:
            self.dir -= 360

        self.centre = centre
        self.rad = 10

    def drawCalc(self, paused):
        if not paused:
            self.pos[0] = self.centre[0] + int(math.cos(math.radians(self.dir)) * self.rad)
            self.pos[1] = self.centre[1] + int(math.sin(math.radians(self.dir)) * self.rad)

    def draw(self, win, paused):
        if not paused:
            self.pos[0] += self.offsetX
            self.pos[1] += self.offsetY
        if legit and self.damage == 101:
            win.blit(self.nani, (self.pos[0] - 14, self.pos[1] - 14))
        else: 
            draw.ellipse(win, (255, 255, 100), (self.pos[0] - 3, self.pos[1] - 3, 6, 6))

    def checkCollision(self, zombies):
        for i in zombies:
            if self.pos[0] > i.pos[0] - 25 and self.pos[0] < i.pos[0] - 25 + i.size and self.pos[1] > i.pos[1] - 25 and self.pos[1] < i.pos[1] - 25 + i.size:
                i.health -= self.damage
                return True

        return False


class Zombie():

    def __init__(self, pos, speed, size, health):
        self.health = health
        self.speed = speed
        self.size = size
        self.ogPos = copy.copy(pos)
        self.pos = copy.copy(self.ogPos)
        self.movedX = 0
        self.movedY = 0
        self.offsetX = 0
        self.offsetY = 0
        self.dir = 0

    def checkPlayerCollision(self, player, paused):
        if not paused:
            if self.pos[0] > 350 and self.pos[0] < 450 and self.pos[1] > 200 and self.pos[1] < 300:
                self.movedX -= math.cos(math.radians(self.dir)) * 20
                self.movedY += math.sin(math.radians(self.dir)) * 20
                player.health -= 1
            

    def drawCalc(self):
        xDif = self.pos[0] - 400
        yDif = self.pos[1] - 250 
        
        try:
            if xDif >= 0 and yDif >= 0:
                self.dir = math.degrees(math.atan(-yDif/xDif))
            if xDif < 0 and yDif >= 0:
                self.dir = math.degrees(math.atan(xDif/yDif)) + 270
            if xDif < 0 and yDif < 0:
                self.dir = math.degrees(math.atan(yDif/-xDif)) + 180
            if xDif >= 0 and yDif < 0:
                self.dir = math.degrees(math.atan(xDif/yDif)) + 90
        except ZeroDivisionError:
            pass

        self.dir -= 180

    def draw(self, win, zombies, paused):
        if not paused:
            if math.cos(math.radians(self.dir)) * self.speed < 0:
                for i in zombies:
                    if i.pos[0] < self.pos[0] and self.pos[0] - i.pos[0] < 50 and self.pos[1] - i.pos[1] > -50 and self.pos[1] - i.pos[1] < 50:
                        break
                else:
                    self.movedX += math.cos(math.radians(self.dir)) * self.speed
            else:
                for i in zombies:
                    if i.pos[0] > self.pos[0] and i.pos[0] - self.pos[0] < 50 and self.pos[1] - i.pos[1] > -50 and self.pos[1] - i.pos[1] < 50:
                        break
                else:
                    self.movedX += math.cos(math.radians(self.dir)) * self.speed

            if math.sin(math.radians(self.dir)) * self.speed > 0:
                
                for i in zombies:
                    if i.pos[1] < self.pos[1] and self.pos[1] - i.pos[1] < 50 and self.pos[0] - i.pos[0] > -50 and self.pos[0] - i.pos[0] < 50:
                        break
                else:
                    self.movedY -= math.sin(math.radians(self.dir)) * self.speed
            else:
                for i in zombies:
                    if i.pos[1] > self.pos[1] and i.pos[1] - self.pos[1] < 50 and self.pos[0] - i.pos[0] > -50 and self.pos[0] - i.pos[0] < 50:
                        break
                else:
                    self.movedY -= math.sin(math.radians(self.dir)) * self.speed
            
            self.pos = copy.copy(self.ogPos)
            self.pos[0] += self.movedX
            self.pos[1] += self.movedY
            self.pos[0] += self.offsetX
            self.pos[1] += self.offsetY
            
        draw.ellipse(win, (50, 120, 50), (self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.size, self.size))
        draw.ellipse(win, black, (self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.size, self.size), 3)

class Pause():

    def __init__(self):
        self.fon1 = font.SysFont('Verdana', 15)
        self.fon2 = font.SysFont('Verdana', 18)
        self.fon3 = font.SysFont('Verdana', 29)
        self.fon4 = font.SysFont('Verdana', 10)
        self.highlight = (100, 100, 100)
        

    def update(self, win, mousePos, clickPos = [0, 0]):
        s = Surface((800, 500))
        s.set_alpha(128)                
        s.fill((0, 0, 0))           
        win.blit(s, (0, 0))

        draw.rect(win, (255, 255, 255), (330, 200, 140, 50), 5)
        draw.rect(win, (255, 255, 255), (330, 300, 140, 50), 5)

        resume = self.fon3.render("RESUME", False, (255, 255, 255))
        mainmenu = self.fon2.render("MAIN MENU", False, (255, 255, 255))

        if mousePos[0] > 330 and mousePos[0] < 470 and mousePos[1] > 200 and mousePos[1] < 250:
            draw.rect(win, self.highlight, (332, 202, 136, 46))
        if mousePos[0] > 330 and mousePos[0] < 470 and mousePos[1] > 300 and mousePos[1] < 350:
            draw.rect(win, self.highlight, (332, 302, 136, 46))

        win.blit(resume, (340, 205))
        win.blit(mainmenu, (345, 312))
        
        display.update()

        if clickPos[0] > 340 and clickPos[0] < 470 and clickPos[1] > 200 and clickPos[1] < 250:
            return "unPause"
        elif clickPos[0] > 340 and clickPos[0] < 470 and clickPos[1] > 300 and clickPos[1] < 350:
            return "endGame"

        return False

























        

