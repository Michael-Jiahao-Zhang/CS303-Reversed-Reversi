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

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        self.candidate_list.clear()
        for y, x in np.ndindex(chessboard.shape):
            if chessboard[y][x] == 0:
                flag = False
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
                if flag:
                    self.candidate_list.append((y, x))

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

    def not_out_of_bound(self, y, x):
        if (0 <= y <= self.chessboard_size - 1) and (0 <= x <= self.chessboard_size - 1):
            return True
        return False
