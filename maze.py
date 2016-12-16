#!/usr/bin/python

import pygame
import random

WIDTH = 600
HEIGHT = 600
CELLWIDTH = 20
COLS = WIDTH/CELLWIDTH
ROWS = HEIGHT/CELLWIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

 
class Maze:
    def __init__(self, w, h):
        pygame.init()
        random.seed()
        self.screen = pygame.display.set_mode([w, h])
        pygame.display.set_caption("Maze Generator")
        self.clock = pygame.time.Clock()
        self.grid = [[Cell(j * CELLWIDTH, i * CELLWIDTH, i, j) for i in range(COLS)] for j in range(ROWS)]
        self.current = self.grid[0][0]
        self.current.visited = True
        self.stack = []

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
            self.current.updateNeighbors(self.grid)
            if self.unvisitedNeighbors(self.current):
                self.next = self.chooseNext()
                self.next.visited = True
                self.stack.append(self.current)
                self.removeLines()
                self.current = self.next
            elif self.stack:
                self.current = self.stack.pop(-1)

            self.screen.fill(BLACK)

            self.drawFill()
            self.drawLines()
            pygame.draw.rect(self.screen, WHITE, self.current.square)


            pygame.display.update()
            self.clock.tick(60)


    def drawLines(self):
        for i in range(COLS):
            for j in range(ROWS):
                if self.grid[j][i].lines[0]:
                    pygame.draw.line(self.screen, WHITE, self.grid[j][i].topLeft, self.grid[j][i].topRight)
                if self.grid[j][i].lines[1]:
                    pygame.draw.line(self.screen, WHITE, self.grid[j][i].topRight, self.grid[j][i].botRight)
                if self.grid[j][i].lines[2]:
                    pygame.draw.line(self.screen, WHITE, self.grid[j][i].botRight, self.grid[j][i].botLeft)
                if self.grid[j][i].lines[3]:
                    pygame.draw.line(self.screen, WHITE, self.grid[j][i].botLeft, self.grid[j][i].topLeft)


    def drawFill(self):
        for i in range(COLS):
            for j in range(ROWS):
                if self.grid[j][i].visited:
                    pygame.draw.rect(self.screen, (100, 0, 200), self.grid[j][i].square)


    def chooseNext(self):
        r = random.randrange(len(self.current.neighbors))
        return self.current.neighbors[r]
 

    def removeLines(self):
        if self.current.j - 1 == self.next.j:
            self.current.lines[3] = False
            self.next.lines[1] = False
        elif self.current.j + 1 == self.next.j:
            self.current.lines[1] = False
            self.next.lines[3] = False
        elif self.current.i - 1 == self.next.i:
            self.current.lines[0] = False
            self.next.lines[2] = False
        elif self.current.i + 1 == self.next.i:
            self.current.lines[2] = False
            self.next.lines[0] = False

    def unvisitedNeighbors(self, cur):
        for i in range(len(cur.neighbors)):
            if not cur.neighbors[i].visited:
                return True

        return False

class Cell:
    def __init__(self, x, y, i, j):
        self.visited = False
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.lines = [True, True, True, True]
        self.topLeft = (x, y)
        self.topRight = (x + CELLWIDTH, y)
        self.botRight = (x + CELLWIDTH, y + CELLWIDTH)
        self.botLeft = (x, y + CELLWIDTH)
        self.neighbors = []
        self.square = pygame.Rect(self.x, self.y, CELLWIDTH, CELLWIDTH)


    def updateNeighbors(self, g):
        if 0 <= self.j - 1 < ROWS and not g[self.j - 1][self.i].visited:
            self.neighbors.append(g[self.j - 1][self.i])
        if 0 <= self.j + 1 < ROWS and not g[self.j + 1][self.i].visited:
            self.neighbors.append(g[self.j + 1][self.i])
        if 0 <= self.i - 1 < ROWS and not g[self.j][self.i - 1].visited:
            self.neighbors.append(g[self.j][self.i - 1])
        if 0 <= self.i + 1 < ROWS and not g[self.j][self.i + 1].visited:
            self.neighbors.append(g[self.j][self.i + 1])


def main():
    Maze(WIDTH, HEIGHT).run()

if __name__ == "__main__":
    main()
