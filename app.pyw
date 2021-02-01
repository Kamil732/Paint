import pygame as pg
from math import hypot

class RectBtn(object):
    def __init__(self, width, height, color, text_color, font, font_size, text='', x=0, y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size

    def draw(self, surface, game_width, game_height):
        if not(self.x):
            pg.draw.rect(surface, (self.color), (game_width//2 - self.width//2, game_height//2 - self.height//2, self.width, self.height))
        else:
            pg.draw.rect(surface, (self.color), (self.x, self.y, self.width, self.height))

        if self.text:
            font1 = pg.font.Font(self.font, self.font_size)
            text1 = font1.render(self.text, 1, (self.text_color))
            surface.blit(text1, (self.x + self.width//2 - text1.get_width()//2, self.y + self.height//2 - text1.get_height()//2))

    def isHover(self, pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height:
            return True
        return False

class CircleBtn(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface, outline=False, outline_color=(0,0,0), outline_size=0):
        if outline:
            pg.draw.circle(surface, (outline_color), (self.x, self.y), self.radius + outline_size)
        pg.draw.circle(surface, (self.color), (self.x, self.y), self.radius)

    def isHover(self, pos):
        distance = hypot(self.x - pos[0], self.y - pos[1])
        if distance <= self.radius:
            return True
        return False

class Brush:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.isDraw = False
        self.drawList = []

    def update(self, pos):
        if self.isDraw:
            self.drawList.append(pos)

class Game:
    def __init__(self, width, height):
        pg.init()
        self.width = width
        self.height = height
        self.win = pg.display.set_mode((width, height))
        self.brush = Brush(7, (0,0,0))
        self.colorBtns = [(CircleBtn(30, self.height//2 + self.height//3 + self.height//15 + 36, 23, (255,0,0)), (255,0,0)), (CircleBtn(30*3, self.height//2 + self.height//3 + self.height//15 + 36, 23, (0,255,0)), (0,255,0)),(CircleBtn(30*5, self.height//2 + self.height//3 + self.height//15 + 36, 23, (0,0,255)), (0,0,255)), (CircleBtn(30*7, self.height//2 + self.height//3 + self.height//15 + 36, 23, (0,0,0)), (0,0,0)),]
        self.rectBtns = [(RectBtn(90, 35, (50,70,100), (211,211,211), 'font.ttf', 26, 'SIZE +', 30*9, self.height//2 + self.height//3 + self.height//15 + 20), 1), (RectBtn(90, 35, (50,70,100), (211,211,211), 'font.ttf', 26, 'SIZE -', 30*13 - 20, self.height//2 + self.height//3 + self.height//15 + 20), -1), (RectBtn(155, 35, (50,70,100), (211,211,211), 'font.ttf', 26, 'CLEAR ALL', 30*16, self.height//2 + self.height//3 + self.height//15 + 20), 20)]
        self.pos = pg.mouse.get_pos()

    def redrawWindow(self):
        self.win.fill((233,233,233))
        for pos in self.brush.drawList:
            pg.draw.circle(self.win, (self.brush.color), (pos), self.brush.radius)
        self.brush.update(self.pos)
        pg.draw.rect(self.win, (100,100,50), (0, self.height//2 + self.height//3 + self.height//15, self.width, self.height - self.height//2 + self.height//3 + self.height//15))
        for i in range(len(self.colorBtns)):
            self.colorBtns[i][0].draw(self.win)
        for i in range(len(self.rectBtns)):
            self.rectBtns[i][0].draw(self.win, self.width, self.height)
        pg.display.update()

    def run(self):
        while True:
            self.pos = pg.mouse.get_pos()

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    quit()

                if ev.type == pg.MOUSEBUTTONDOWN:
                    if self.pos[1] < self.height//2 + self.height//3 + self.height//15:
                        self.brush.isDraw = True
                    
                    elif self.pos[1] > self.height//2 + self.height//3 + self.height//15:
                        for i in range(len(self.colorBtns)):
                            if self.colorBtns[i][0].isHover(self.pos):
                                self.brush.color = self.colorBtns[i][1]
                        for i in range(len(self.rectBtns) - 1):
                            if self.rectBtns[i][0].isHover(self.pos):
                                if self.brush.radius > 1 and self.brush.radius <= 50:
                                    self.brush.radius += self.rectBtns[i][1]
                                else:
                                    self.brush.radius = 7
                        if self.rectBtns[2][0].isHover(self.pos):
                            self.brush.drawList = []
                
                if ev.type == pg.MOUSEBUTTONUP:
                    self.brush.isDraw = False

            self.redrawWindow()

if __name__ == "__main__":
    g = Game(850,720)
    pg.display.set_caption('Paint')
    g.run()