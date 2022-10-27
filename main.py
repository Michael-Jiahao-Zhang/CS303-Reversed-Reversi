import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
enemy_color = 1
self_color = 1
random.seed(0)


# don't change the class name
class AI(object):

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        global enemy_color
        global self_color
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        enemy_color = -color
        self_color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list.
        # The system will get the end of your candidate_list as your decision.
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()
        for y, x in np.ndindex(chessboard.shape):
            if self.is_legal(chessboard, y, x):
                self.candidate_list.append((y, x))

    # check whether it has opponent neighbour, and return a direction
    def check_neighbour(self, y, x, board):
        neighbour_enemy_direction = []
        if self.not_out_of_bound(y - 1, x):
            if board[y - 1, x] == enemy_color:
                neighbour_enemy_direction.append((-1, 0))
        if self.not_out_of_bound(y + 1, x):
            if board[y + 1, x] == enemy_color:
                neighbour_enemy_direction.append((1, 0))
        if self.not_out_of_bound(y, x - 1):
            if board[y, x - 1] == enemy_color:
                neighbour_enemy_direction.append((0, -1))
        if self.not_out_of_bound(y, x + 1):
            if board[y, x + 1] == enemy_color:
                neighbour_enemy_direction.append((0, 1))
        if self.not_out_of_bound(y - 1, x - 1):
            if board[y - 1, x - 1] == enemy_color:
                neighbour_enemy_direction.append((-1, -1))
        if self.not_out_of_bound(y - 1, x + 1):
            if board[y - 1, x + 1] == enemy_color:
                neighbour_enemy_direction.append((-1, 1))
        if self.not_out_of_bound(y + 1, x - 1):
            if board[y + 1, x - 1] == enemy_color:
                neighbour_enemy_direction.append((1, -1))
        if self.not_out_of_bound(y + 1, x + 1):
            if board[y + 1, x + 1] == enemy_color:
                neighbour_enemy_direction.append((1, 1))

        return neighbour_enemy_direction

    # check whether(x, y) is out of bound
    def not_out_of_bound(self, y, x):
        if (0 <= y <= self.chessboard_size - 1) and (0 <= x <= self.chessboard_size - 1):
            return True
        return False

    def update_board(self, chessboard, y, x):   #(y, x) is a solution, but not sure what direction
        updated_chessboard = chessboard.copy()
        neighbour_enemy = self.check_neighbour(y, x, updated_chessboard)
        for direction in neighbour_enemy:
            flag = False
            yi = direction[0]
            xi = direction[1]
            y_cur = y + yi
            x_cur = x + xi
            while self.not_out_of_bound(y_cur, x_cur):
                y_cur += yi
                x_cur += xi
                if self.not_out_of_bound(y_cur, x_cur):
                    if updated_chessboard[y_cur][x_cur] == self_color:     #不可能紧挨着，因为是enemy direction
                        flag = True
                        break
                    elif updated_chessboard[y_cur][x_cur] == 0:
                        break
            if flag:
                    y_temp, x_temp = y, x
                    while(y_temp != y_cur):
                        y_temp = y + yi
                        x_temp = x + xi
                        updated_chessboard[y_temp][x_temp] = self_color
        return updated_chessboard
    
    # judge whether (y,x) is legal
    def is_legal(self, chessboard, y, x):
        flag = False
        if chessboard[y][x] == 0:
            neighbour_enemy = self.check_neighbour(y, x, chessboard)
            for direction in neighbour_enemy:
                yi = direction[0]
                xi = direction[1]
                y_cur = y + yi
                x_cur = x + xi
                while self.not_out_of_bound(y_cur, x_cur):
                    y_cur += yi
                    x_cur += xi
                    if self.not_out_of_bound(y_cur, x_cur):
                        if chessboard[y_cur][x_cur] == self_color:
                            flag = True
                        elif chessboard[y_cur][x_cur] == 0:
                            break
        return flag