from pygame import *
from Main import *

init()

win = display.set_mode((800, 500), FULLSCREEN)

class Menu():

    def __init__(self, win):
        self.win = win
        self.ssLock = True
        self.menu = True
        self.end = False
        self.startGame = False
        self.fon1 = font.SysFont('Verdana', 15)
        self.fon2 = font.SysFont('Verdana', 18)
        self.fon3 = font.SysFont('Verdana', 29)
        self.fon4 = font.SysFont('Verdana', 10)
        self.highlight = (100, 100, 100)
        self.clock = time.Clock()
        self.mode = 0
        self.titleMusic = mixer.Sound("sounds/titleMusic.ogg")
        self.start = mixer.Sound("sounds/start.ogg")
        self.start.set_volume(0.2)
        self.channel1 = mixer.Channel(0)
        self.lock = image.load("images/lock.png")
        self.lock = transform.scale(self.lock, (30, 40))
        self.title = image.load("images/title.png")

        self.channel1.play(self.titleMusic)

        try:
            with open("scores.txt") as file:
                top = file.readline()

                if int(top) >= 1000:
                    self.ssLock = False
        except FileNotFoundError:
            pass

    def update(self):
        for even in event.get():
            if even.type == QUIT:
                self.end = True
            if even.type == MOUSEBUTTONUP:
                clickPos = mouse.get_pos()
                if clickPos[0] > 80 and clickPos[0] < 220 and clickPos[1] > 300 and clickPos[1] < 350:
                    self.channel1.stop()
                    self.channel1.play(self.start)
                    
                    for i in range(600):
                        self.win.blit(self.title, (101, 120))

                        draw.rect(self.win, (255, 255, 255), (80, 300, 140, 50), 5)
                        draw.rect(self.win, (255, 255, 255), (240, 300, 140, 50), 5)
                        draw.rect(self.win, (255, 255, 255), (400, 300, 140, 50), 5)
                        draw.rect(self.win, (255, 255, 255), (560, 300, 140, 50), 5)

                        normal = self.fon3.render("NORMAL", False, (255, 255, 255))
                        if not self.ssLock:
                            sharpshooter = self.fon1.render("SHARPSHOOTER", False, (255, 255, 255))
                        else:
                            sharpshooter = self.fon4.render("SHARPSHOOTER", False, (255, 255, 255))
                        highscores = self.fon2.render("HIGHSCORES", False, (255, 255, 255))
                        ext = self.fon3.render("EXIT", False, (255, 255, 255))

                        self.win.blit(normal, (86, 305))
                        if self.ssLock:
                            self.win.blit(sharpshooter, (247, 318))
                        else:
                            self.win.blit(sharpshooter, (247, 315))
                        self.win.blit(highscores, (406, 314))
                        self.win.blit(ext, (592, 307))

                        if self.ssLock:
                            self.win.blit(self.lock, (345, 305))
                        
                        s = Surface((800, 500))
                        s.set_alpha(i)                
                        s.fill((0, 0, 0))           
                        self.win.blit(s, (0, 0))
                        display.update()

                    self.mode = 0
                    self.startGame = True
                    
                elif clickPos[0] > 240 and clickPos[0] < 380 and clickPos[1] > 300 and clickPos[1] < 350:
                    if not self.ssLock:
                        self.channel1.stop()
                        self.channel1.play(self.start)
                        
                        for i in range(600):
                            self.win.blit(self.title, (101, 120))

                            draw.rect(self.win, (255, 255, 255), (80, 300, 140, 50), 5)
                            draw.rect(self.win, (255, 255, 255), (240, 300, 140, 50), 5)
                            draw.rect(self.win, (255, 255, 255), (400, 300, 140, 50), 5)
                            draw.rect(self.win, (255, 255, 255), (560, 300, 140, 50), 5)

                            normal = self.fon3.render("NORMAL", False, (255, 255, 255))
                            sharpshooter = self.fon1.render("SHARPSHOOTER", False, (255, 255, 255))
                            highscores = self.fon2.render("HIGHSCORES", False, (255, 255, 255))
                            ext = self.fon3.render("EXIT", False, (255, 255, 255))

                            self.win.blit(normal, (86, 305))
                            self.win.blit(sharpshooter, (247, 315))
                            self.win.blit(highscores, (406, 314))
                            self.win.blit(ext, (592, 307))
                            
                            s = Surface((800, 500))
                            s.set_alpha(i)                
                            s.fill((0, 0, 0))           
                            self.win.blit(s, (0, 0))
                            display.update()

                        
                        self.mode = 1
                        self.startGame = True
                
                elif clickPos[0] > 400 and clickPos[0] < 540 and clickPos[1] > 300 and clickPos[1] < 350:
                    self.menu = False
                
                elif clickPos[0] > 560 and clickPos[0] < 700 and clickPos[1] > 300 and clickPos[1] < 350:
                    self.end = True

        if not self.startGame:
            mousePos = mouse.get_pos()
            
            self.win.fill((0, 0, 0))

            self.win.blit(self.title, (101, 120))

            if mousePos[0] > 80 and mousePos[0] < 220 and mousePos[1] > 300 and mousePos[1] < 350:
                draw.rect(self.win, self.highlight, (82, 302, 136, 46))
            if mousePos[0] > 240 and mousePos[0] < 380 and mousePos[1] > 300 and mousePos[1] < 350 and not self.ssLock:
                draw.rect(self.win, self.highlight, (242, 302, 136, 46))
            if mousePos[0] > 400 and mousePos[0] < 540 and mousePos[1] > 300 and mousePos[1] < 350:
                draw.rect(self.win, self.highlight, (402, 302, 136, 46))
            if mousePos[0] > 560 and mousePos[0] < 700 and mousePos[1] > 300 and mousePos[1] < 350:
                draw.rect(self.win, self.highlight, (562, 302, 136, 46))

            draw.rect(self.win, (255, 255, 255), (80, 300, 140, 50), 5)
            draw.rect(self.win, (255, 255, 255), (240, 300, 140, 50), 5)
            draw.rect(self.win, (255, 255, 255), (400, 300, 140, 50), 5)
            draw.rect(self.win, (255, 255, 255), (560, 300, 140, 50), 5)

            normal = self.fon3.render("NORMAL", False, (255, 255, 255))
            if not self.ssLock:
                sharpshooter = self.fon1.render("SHARPSHOOTER", False, (255, 255, 255))
            else:
                sharpshooter = self.fon4.render("SHARPSHOOTER", False, (255, 255, 255))
            highscores = self.fon2.render("HIGHSCORES", False, (255, 255, 255))
            ext = self.fon3.render("EXIT", False, (255, 255, 255))

            self.win.blit(normal, (86, 305))
            if self.ssLock:
                self.win.blit(sharpshooter, (247, 318))
            else:
                self.win.blit(sharpshooter, (247, 315))
            self.win.blit(highscores, (406, 314))
            self.win.blit(ext, (592, 307))

            if self.ssLock:
                self.win.blit(self.lock, (345, 305))

            display.update()


class Highscores():

    def __init__(self, win):
        self.win = win
        self.end = False
        self.ext = False
        self.highlight = (100, 100, 100)
        self.fon = font.SysFont('Verdana', 21)
        self.titleFon = font.SysFont('Verdana', 28)

        try:
            with open("scores.txt", "r") as file:
                self.scoreList = file.readlines()
                for i in range(len(self.scoreList)):
                    self.scoreList[i] = self.scoreList[i].strip("\n")

        except FileNotFoundError:
            with open("scores.txt", "w") as file:
                for i in range(10):
                    file.write("0\n")

            self.scoreList = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

        try:
            with open("sharpshooterScores.txt", "r") as file:
                self.ssScoreList = file.readlines()
                for i in range(len(self.ssScoreList)):
                    self.ssScoreList[i] = self.ssScoreList[i].strip("\n")

        except FileNotFoundError:
            with open("sharpshooterScores.txt", "w") as file:
                for i in range(10):
                    file.write("0\n")

            self.ssScoreList = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

        

    def update(self):
        for even in event.get():
            if even.type == QUIT:
                self.end = True
            if even.type == MOUSEBUTTONUP:
                clickPos = mouse.get_pos()
                if clickPos[0] > 600 and clickPos[0] < 740 and clickPos[1] > 400 and clickPos[1] < 450:
                    self.ext = True

        mousePos = mouse.get_pos()
            
        self.win.fill((0, 0, 0))

        if mousePos[0] > 600 and mousePos[0] < 740 and mousePos[1] > 400 and mousePos[1] < 450:
            draw.rect(self.win, self.highlight, (602, 402, 136, 46))
                    
        draw.rect(self.win, (255, 255, 255), (600, 400, 140, 50), 5)

        mainmenu = self.fon.render("MAIN MENU", False, (255, 255, 255))
        self.win.blit(mainmenu, (607, 410))

        normal = self.titleFon.render("Normal", False, (255, 255, 255))
        self.win.blit(normal, (200, 80))

        sharpshooter = self.titleFon.render("Sharpshooter", False, (255, 255, 255))
        self.win.blit(sharpshooter, (375, 80))

        val1 = self.fon.render("1: "+self.scoreList[0], False, (255, 255, 255))
        val2 = self.fon.render("2: "+self.scoreList[1], False, (255, 255, 255))
        val3 = self.fon.render("3: "+self.scoreList[2], False, (255, 255, 255))
        val4 = self.fon.render("4: "+self.scoreList[3], False, (255, 255, 255))
        val5 = self.fon.render("5: "+self.scoreList[4], False, (255, 255, 255))
        val6 = self.fon.render("6: "+self.scoreList[5], False, (255, 255, 255))
        val7 = self.fon.render("7: "+self.scoreList[6], False, (255, 255, 255))
        val8 = self.fon.render("8: "+self.scoreList[7], False, (255, 255, 255))
        val9 = self.fon.render("9: "+self.scoreList[8], False, (255, 255, 255))
        val10 = self.fon.render("10: "+self.scoreList[9], False, (255, 255, 255))

        val11 = self.fon.render("1: "+self.ssScoreList[0], False, (255, 255, 255))
        val12 = self.fon.render("2: "+self.ssScoreList[1], False, (255, 255, 255))
        val13 = self.fon.render("3: "+self.ssScoreList[2], False, (255, 255, 255))
        val14 = self.fon.render("4: "+self.ssScoreList[3], False, (255, 255, 255))
        val15 = self.fon.render("5: "+self.ssScoreList[4], False, (255, 255, 255))
        val16 = self.fon.render("6: "+self.ssScoreList[5], False, (255, 255, 255))
        val17 = self.fon.render("7: "+self.ssScoreList[6], False, (255, 255, 255))
        val18 = self.fon.render("8: "+self.ssScoreList[7], False, (255, 255, 255))
        val19 = self.fon.render("9: "+self.ssScoreList[8], False, (255, 255, 255))
        val20 = self.fon.render("10: "+self.ssScoreList[9], False, (255, 255, 255))

        self.win.blit(val1, (220, 120))
        self.win.blit(val2, (220, 145))
        self.win.blit(val3, (220, 170))
        self.win.blit(val4, (220, 195))
        self.win.blit(val5, (220, 220))
        self.win.blit(val6, (220, 245))
        self.win.blit(val7, (220, 270))
        self.win.blit(val8, (220, 295))
        self.win.blit(val9, (220, 320))
        self.win.blit(val10, (207, 345))

        self.win.blit(val11, (440, 120))
        self.win.blit(val12, (440, 145))
        self.win.blit(val13, (440, 170))
        self.win.blit(val14, (440, 195))
        self.win.blit(val15, (440, 220))
        self.win.blit(val16, (440, 245))
        self.win.blit(val17, (440, 270))
        self.win.blit(val18, (440, 295))
        self.win.blit(val19, (440, 320))
        self.win.blit(val20, (427, 345))

        display.update()
        
    
menu = Menu(win)
game = Game(win, 0, False)
highscore = Highscores(win)

while True:
    if menu.end or game.end or highscore.end:
        break

    if game.run:
        game.clock.tick(60)
        game.update()
        if not game.run:
           menu.channel1.play(menu.titleMusic, -1)
           menu.menu = True
    elif menu.menu:
        menu.clock.tick(60)
        menu.update()
        if menu.startGame:
            game = Game(win, menu.mode)
            menu.startGame = False
        if not menu.menu:
            highscore = Highscores(win)
    else:
        highscore.update()
        if highscore.ext:
            menu.menu = True
            highscore.ext = False
        
quit()
