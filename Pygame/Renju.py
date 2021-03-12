import pygame

EMPTY = ""
BLACK = (0,0,0)
WHITE = (255,255,255)
class Chess(object):
    """棋子类"""
    def __init__(self, x, y, is_black):
        self._is_black = is_black
        self._row = x
        self._col = y

    @property
    def is_black(self):
        return self._is_black

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

class RenjuBoard(object):
    """棋盘类"""
    def __init__(self):
        self._board = [[]] * 15
        self.reset()

    def reset(self):
        """重置棋盘"""
        for row in range(len(self._board)):
            self._board[row] = [EMPTY] * 15

    def move(self, row, col, is_black):
        """判断是否有棋子"""
        if self._board[row][col] == EMPTY:
            self._board[row][col] = BLACK if is_black else WHITE
            return True
        return False

    def draw(self, screen):
        """画棋盘"""
        for i in range(1, 16):  # 画格子：窗口，颜色，起始位置，结束位置，粗细
            pygame.draw.line(screen, BLACK, [40, 40 * i], [600, 40 * i], 1)
            pygame.draw.line(screen, BLACK, [40 * i, 40], [40 * i, 600], 1)
        pygame.draw.rect(screen, BLACK, [36, 36, 568, 568], 4)  # 画边框
        # 画圆 窗口，颜色，位置，半径，0实心
        pygame.draw.circle(screen, BLACK, [320, 320], 4, 0)
        pygame.draw.circle(screen, BLACK, [160, 160], 3, 0)
        pygame.draw.circle(screen, BLACK, [160, 480], 3, 0)
        pygame.draw.circle(screen, BLACK, [480, 480], 3, 0)
        pygame.draw.circle(screen, BLACK, [480, 160], 3, 0)
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] != EMPTY:
                    ccolor = BLACK if self._board[row][col] == BLACK else WHITE
                    pos = [40 * (col + 1), 40 * (row + 1)]
                    pygame.draw.circle(screen, ccolor, pos, 20, 0)

    def who_wins(self, x, y, chess):
        """判断输赢"""
        # 三维数组记录横向，纵向，左斜，右斜
        dir = [[[-1, 0], [1, 0]], [[0, -1], [0, 1]], [[-1, -1], [1, 1]], [[1, -1], [-1, 1]]]
        tempx = x
        tempy = y
        # 循环四个大方向
        for i in range(4):
            count = 1
            # 循环两边方向
            for j in range(2):
                flag = True  # 一直向一个方向遍历，有相同的，count+1，否则置flag为False
                while flag:
                    tempx += dir[i][j][0]
                    tempy += dir[i][j][1]
                    if chess[x][y] == chess[tempx][tempy]:
                        count += 1
                    else:
                        flag = False
                tempx = x
                tempy = y
                if count >= 5:
                    return True
        return False

def main():
    board = RenjuBoard()  # 创建棋盘对象
    chess = [[EMPTY] * 16 for _ in range(16)]  # 棋子位置
    is_black = True  # 黑白棋分辨变量
    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode([640, 640])  # 初始化用于显示的窗口并设置窗口尺寸
    pygame.display.set_caption('五子棋')  # 设置当前窗口的标题
    screen.fill([218, 165, 105])  # 填充背景色 红绿蓝三原色
    board.draw(screen)  # 画棋盘
    pygame.display.flip()  # 刷新窗口
    runing = True  # 是否退出游戏变量
    gameover = True  # 游戏是否结束变量
    while runing:  # 开启一个事件循环处理发生的事件
        for event in pygame.event.get():  # 从消息队列中获取事件并对事件进行处理
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    board.reset()
                    gameover = True
                    is_black = True
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gameover:  # 鼠标点击事件
                x, y = event.pos
                if 20 < x <= 600 and 20 < y < 600:
                    row = round((y - 40) / 40)
                    col = round((x - 40) / 40)
                    if board.move(row, col, is_black):
                        screen.fill([218, 165, 105])
                        board.draw(screen)
                        chess[col][row] = 1 if is_black else 2
                        pygame.display.flip()
                        if board.who_wins(col, row, chess):
                            my_font = pygame.font.SysFont("宋体", 60)  # 字体，大小
                            if is_black:
                                position = my_font.render('game over, black win', True,
                                                          (255, 0, 0))  # 内容，抗锯齿，颜色，背景色（可选）
                            else:
                                position = my_font.render('game over, white win', True, (255, 0, 0))
                            screen.blit(position, (120, 310))
                            pygame.display.flip()
                            gameover = False
                            chess = [[EMPTY] * 16 for _ in range(16)]
                        is_black = not is_black
    pygame.quit()

if __name__ == '__main__':
    main()