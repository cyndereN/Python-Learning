from tkinter.messagebox import *
from pygame.locals import *
from random import *
import tkinter as tk
import pygame
base = tk.Tk()
base.geometry('0x0')
base.resizable(False,False)
pygame.init()
def gen_sudoku():
    def list_roll(ls,n):
        new = list(ls)
        for i in range(n):
            new.append(new.pop(0))
        return new
    s = [i for i in range(1,10)]
    n = [0,3,6,1,4,7,2,5,8]
    shuffle(s)
    sudoku = []
    for i in range(9):
        row = list_roll(s,n[i])
        sudoku.append(row)
    return sudoku
def gen_question(sudoku):
    res = [[j for j in i] for i in sudoku]
    n = randint(21,56)
    for i in range(n):
        x = randint(0,8)
        y = randint(0,8)
        while(res[x][y] == None):
            x = randint(0, 8)
            y = randint(0, 8)
        res[x][y] = None
    return res
def show_sudoku(surf,sudoku,s,e):
    font = pygame.font.Font('songti SC.TTF',100)
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if((j,i) == s):
                color = ((255,255,255),(65,105,225))
            elif((j,i) in e):
                color = ((227,23,13),(0,0,0))
            else:
                color = ((255,255,255),(0,0,0))
            if(sudoku[i][j] == None):
                t = font.render(' ', True, color[0],color[1])
            else:
                t = font.render(str(sudoku[i][j]),True,color[0],color[1])
            t = pygame.transform.scale(t,(64,64))
            surf.blit(t,(64 * j,64 * i))
            pygame.draw.rect(surf,(255,255,255),Rect((64 * j,64 * i),(64,64)),1)
def main():
    scr = pygame.display.set_mode((576,576),DOUBLEBUF)
    ans = gen_sudoku()
    ques = gen_question(ans)
    selected = None
    errors = []
    while(1):
        pygame.display.update()
        show_sudoku(scr,ques,selected,errors)
        if(ques == ans):
            pygame.display.update()
            return
        for ev in pygame.event.get():
            if(ev.type == QUIT):
                exit()
            elif(ev.type == MOUSEBUTTONDOWN):
                x,y = ev.pos[0] // 64,ev.pos[1] // 64
                if(ques[y][x] == None or (x,y) in errors):
                    selected = (x,y)
            elif(ev.type == KEYDOWN):
                if(ev.unicode not in '123456789' or (not ev.unicode) or (not selected)):continue
                ques[selected[1]][selected[0]] = int(ev.unicode)
                if(ans[selected[1]][selected[0]] != ques[selected[1]][selected[0]]):
                    errors.append(selected)
                if(ans[selected[1]][selected[0]] == ques[selected[1]][selected[0]] and selected in errors):
                    errors.remove(selected)
if(__name__ == '__main__'):
    main()
    showinfo('Congratulations!','Congratulations!You\'done it!')
