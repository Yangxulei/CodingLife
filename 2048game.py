import curses
from random import randrange,choice
from collections import defaultdict

#用户行为
actions = ['up','Left','Down','Right','Restart','Exit']
#有效输入键最常用的 W A S D R Q，获得有效键值列表
letter_code = [ord(ch) for ch in 'WASDRQwasdrq']
#将输入与行为绑定
actions_dict = dict(zip(letter_code, actions * 2))



#用户输入处理
    #循环+阻塞，直到获取用户有效输入才返回对应行为
def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return  actions_dict[char]

#矩阵转置
def transpose(field):
    return [list(row) for row in  zip(*field)]

#矩阵逆转
def invert(field):
    return [row[::-1] for row in field]

#创建棋盘
class GameField(object):
    def __init__(self,height = 4, width = 4, win = 2048):
        self.heigth = height  #高
        self.width = width     #宽
        self.win_value = 2048  #过关分数
        self.score = 0    #当前分数
        self.hightscore = 0 #最高分数
        self.reset()     #棋盘重置

    #重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.score = 0
            self.field = [[0 for i in range(self.width)] for j in range(self.height)]
            self.spawn()
            self.spawn()

     # 通过对矩阵进行转置与逆转可以直接从左移得到其余三个方向的移动操作
    def move(self, direction):
        def move_row_left(row):
            def tighten(row): #把零散单元推到一块
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):  #对邻近元素进行合并
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
        return tighten(merge(tighten(row)))

     moves = {}
     moves['Left'] = lambda field: \
           [move_row_left(row) for row in field]
     moves['Right'] = lambda field: \
            invert(moves['Left'](invert(field)))
    moves['Up'] = lambda field: \
            transpose(moves['Left'](transpose(field)))
    moves['Down'] = lambda field: \
            transpose(moves['Right'](transpose(field)))

    if direction in moves:
        if self.move_is_possible(direction):
           self.field = moves[direction](self.field)
           self.spawn()
           return True
        else:
            return False

    # 判断输赢
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        # 绘制游戏界面
        # 绘制水平分割线
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    # 棋盘操作随机生成一个2或者4
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    # 判断是否移动
    def move_is_possibele(self, direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:  # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:  # Merge
                    return True
                return False
            return any(choice(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: \
            any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field: \
            check['Left'](invert(field))

        check['Up'] = lambda field: \
            check['Left'](transpose(field))

        check['Down'] = lambda field: \
            check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False


#状态机
def main(stdscr):

    def init():
       #重置键盘棋盘
       game_field_reset()
       return 'Game'

    def not_game():
        #画出GameOver 或者win
        game_field.draw(stdscr)
        #读取用户输入的acitons，判断是否重启游戏或者结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda :state)#默认当前状态，没有行为就一直在当前界面循环
        responses['Restart'],responses['Exit'] = 'Init','Exit'  #对应不同的行为转换到不同的状态
        return  responses[action]

    def game():
        #画出当前棋盘
        game_field.draw(stdscr)
        #读取当前棋盘状态
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
     }
    curses.use_default_colors()
    game_field = GameField(win=32)

    state = 'Init'

    #状态机开始循环

    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)






