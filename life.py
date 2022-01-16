import random
import pygame
import sys

BG = (20, 20, 20)  # Фон
LIFECOLOR = (31, 97, 189)  # Цвет клетки
LINECOLOR = (52, 53, 46)  # Цвет сетки
LINE_WIDTH = 3  # Ширина линии
EDGE_WIDTH = 20   # Ширина сетки от края рамки
START_POSX = 20
START_POSY = 20

class Cell:
    """
    Тип ячейки, одиночная ячейка
    """
    def __init__(self, ix, iy, is_live):
        self.ix = ix
        self.iy = iy
        self.is_live = is_live
        self.neighbour_count = 0

    
    def calc_neighbour_count(self):
        count = 0
        pre_x = self.ix - 1 if self.ix > 0 else 0  
        for i in range(pre_x, self.ix+1+1):     
            pre_y = self.iy - 1 if self.iy > 0 else 0 
            for j in range(pre_y, self.iy+1+1): 
                
                if i == self.ix and j == self.iy:
                    continue
                
                if self.invalidate(i, j):
                    continue
                
                
                count += int(CellGrid.cells[i][j].is_live)
        self.neighbour_count = count
        return count

    def invalidate(self, x, y):
        if x >= CellGrid.cx or y >= CellGrid.cy:  
            return True
        if x < 0 or y < 0:
            return True
        return False

    def rule(self):
        if self.neighbour_count > 3 or self.neighbour_count < 2:
            self.is_live = False
        elif self.neighbour_count == 3:
            self.is_live = True
        elif self.neighbour_count == 2:
            pass


class CellGrid:
    """
         Тип сетки ячеек, все ячейки находятся в сетке длиной cx и шириной cy
    """
    cells = []
    cx = 0
    cy = 0

    def __init__(self, cx, cy):
        CellGrid.cx = cx
        CellGrid.cy = cy
        for i in range(cx):
            cell_list = []
            for j in range(cy):

                cell = Cell(i, j, random.random() > 0.5)
                cell_list.append(cell)
            CellGrid.cells.append(cell_list)
    def circulate_rule(self):
        for cell_list in CellGrid.cells:
            for item in cell_list:
                item.rule()

    def circulate_nbcount(self):
        for cell_list in CellGrid.cells:
            for item in cell_list:
                item.calc_neighbour_count()


class Game:
    screen = None

    def __init__(self, width, height, cx, cy):
        self.width = width
        self.height = height
        self.cx_rate = int((width - 2*EDGE_WIDTH) / cx)
        self.cy_rate = int((height - 2*EDGE_WIDTH) / cy)
        self.screen = pygame.display.set_mode([width, height])
        self.cells = CellGrid(cx, cy)

    def show_life(self):
        for i in range(self.cells.cx + 1):
            pygame.draw.line(self.screen, LINECOLOR, (START_POSX, START_POSY + i * self.cy_rate),
                             (START_POSX + self.cells.cx * self.cx_rate, START_POSY + i * self.cy_rate), LINE_WIDTH)
            pygame.draw.line(self.screen, LINECOLOR, (START_POSX + i * self.cx_rate, START_POSY),
                             (START_POSX + i * self.cx_rate, START_POSY + self.cells.cx * self.cy_rate), LINE_WIDTH)

        for cell_list in self.cells.cells:
            for item in cell_list:
                x = item.ix
                y = item.iy
                if item.is_live:
                    pygame.draw.rect(self.screen, LIFECOLOR,
                                     [START_POSX+x * self.cx_rate+ (LINE_WIDTH - 1),
                                      START_POSY+y * self.cy_rate+ (LINE_WIDTH - 1),
                                      self.cx_rate- LINE_WIDTH, self.cy_rate- LINE_WIDTH])


def main():
    pygame.init()
    pygame.display.set_caption("Game of Life")
    game = Game(440, 440, 20, 20)

    clock = pygame.time.Clock()
    while True:
        game.screen.fill(BG)
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        game.cells.circulate_nbcount()
        game.cells.circulate_rule()

        game.show_life()
        pygame.display.flip()


if __name__ == "__main__":
    main()
