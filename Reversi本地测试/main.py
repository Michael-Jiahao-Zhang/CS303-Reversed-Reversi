import math
import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
search_depth = 5

weight = np.array([
    [-1000, 25, -10, 5, 5, -10, 25, -1000],
    [25, 100, -1, -1, -1, -1, 100, 25],
    [-10, -1, -1, -1, -1, -1, -1, -10],
    [-5, -1, -1, -1, -1, -1, -1, -5],
    [-5, -1, -1, -1, -1, -1, -1, -5],
    [-10, -1, -1, -1, -1, -1, -1, -10],
    [25, 100, -1, -1, -1, -1, 100, 25],
    [-1000, 25, -10, 5, 5, -10, 25, -1000],
])


# don't change the class name


class AI(object):

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        self.other_color = -color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list.
        # The system will get the end of your candidate_list as your decision.
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()
        possible_pos = self.get_possible_pos_list(chessboard, self.color)
        top_val = -math.inf
        for pos in possible_pos:
            updated_chessboard = self.update_board(
                chessboard, self.color, pos[0], pos[1])
            cur_val = self.min_value(
                updated_chessboard, -math.inf, math.inf, search_depth)
            if cur_val > top_val:
                top_val = cur_val
                self.candidate_list.append(pos)
            else:
                self.candidate_list.insert(0, pos)
        return self.candidate_list

    def evaluate(self, chessboard, cur_color):
        cnt, point = 0, 0
        for y, x in np.ndindex(chessboard.shape):
            if chessboard[y][x] == cur_color:
                cnt += 1
                point += weight[y][x]
        return point

    # check whether it has opponent neighbour, and return a direction
    def check_neighbour(self, board, cur_color, y, x):
        neighbour_enemy_direction = []
        if self.not_out_of_bound(y - 1, x):
            if board[y - 1, x] == -cur_color:
                neighbour_enemy_direction.append((-1, 0))
        if self.not_out_of_bound(y + 1, x):
            if board[y + 1, x] == -cur_color:
                neighbour_enemy_direction.append((1, 0))
        if self.not_out_of_bound(y, x - 1):
            if board[y, x - 1] == -cur_color:
                neighbour_enemy_direction.append((0, -1))
        if self.not_out_of_bound(y, x + 1):
            if board[y, x + 1] == -cur_color:
                neighbour_enemy_direction.append((0, 1))
        if self.not_out_of_bound(y - 1, x - 1):
            if board[y - 1, x - 1] == -cur_color:
                neighbour_enemy_direction.append((-1, -1))
        if self.not_out_of_bound(y - 1, x + 1):
            if board[y - 1, x + 1] == -cur_color:
                neighbour_enemy_direction.append((-1, 1))
        if self.not_out_of_bound(y + 1, x - 1):
            if board[y + 1, x - 1] == -cur_color:
                neighbour_enemy_direction.append((1, -1))
        if self.not_out_of_bound(y + 1, x + 1):
            if board[y + 1, x + 1] == -cur_color:
                neighbour_enemy_direction.append((1, 1))
        return neighbour_enemy_direction

    # check whether(x, y) is out of bound
    def not_out_of_bound(self, y, x):
        if (0 <= y <= self.chessboard_size - 1) and (0 <= x <= self.chessboard_size - 1):
            return True
        return False

    def get_possible_pos_list(self, chessboard, cur_color):
        possible_pos = []
        for y, x in np.ndindex(chessboard.shape):
            if self.is_legal(chessboard, cur_color, y, x):
                possible_pos.append((y, x))
        return possible_pos

    # judge whether (y,x) is legal
    def is_legal(self, chessboard, cur_color, y, x):
        flag = False
        if chessboard[y][x] == 0:
            neighbour_enemy = self.check_neighbour(chessboard, cur_color, y, x)
            for direction in neighbour_enemy:
                yi = direction[0]
                xi = direction[1]
                y_cur = y + yi
                x_cur = x + xi
                while self.not_out_of_bound(y_cur, x_cur):
                    y_cur += yi
                    x_cur += xi
                    if self.not_out_of_bound(y_cur, x_cur):
                        if chessboard[y_cur][x_cur] == cur_color:
                            flag = True
                        elif chessboard[y_cur][x_cur] == 0:
                            break
        return flag

    # (y, x) is a solution, but not sure what direction
    def update_board(self, chessboard, cur_color, y, x):
        updated_chessboard = chessboard.copy()
        neighbour_enemy = self.check_neighbour(
            updated_chessboard, cur_color, y, x)
        for direction in neighbour_enemy:
            flag = False
            yi = direction[0]
            xi = direction[1]
            y_cur = y + yi
            x_cur = x + xi
            # now (y_cur, x_cur) is enemy position
            while self.not_out_of_bound(y_cur, x_cur):
                y_cur += yi
                x_cur += xi
                if self.not_out_of_bound(y_cur, x_cur):
                    # 不可能紧挨着，因为是enemy direction
                    if updated_chessboard[y_cur][x_cur] == cur_color:
                        flag = True
                        break
                    elif updated_chessboard[y_cur][x_cur] == 0:
                        break
            if flag:
                y_temp, x_temp = y, x
                while y_temp != y_cur and x_temp != x_cur:
                    y_temp += yi
                    x_temp += xi
                    updated_chessboard[y_temp][x_temp] = cur_color
        return updated_chessboard

    def max_value(self, chessboard, alpha, beta, depth):
        cur_color = self.color
        if depth == 0:
            return self.evaluate(chessboard, cur_color)
        possible_pos = self.get_possible_pos_list(chessboard, cur_color)
        if not possible_pos:
            return self.min_value(chessboard, alpha, beta, depth - 1)
        value = -math.inf
        for pos in possible_pos:
            new_chessboard = self.update_board(chessboard, cur_color, pos[0], pos[1])
            value = max(value, self.min_value(new_chessboard, alpha, beta, depth - 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, chessboard, alpha, beta, depth):
        cur_color = self.other_color
        if depth == 0:
            return self.evaluate(chessboard, cur_color)
        possible_pos = self.get_possible_pos_list(chessboard, cur_color)
        if not possible_pos:
            return self.max_value(chessboard, alpha, beta, depth - 1)
        value = math.inf
        for pos in possible_pos:
            new_chessboard = self.update_board(chessboard, cur_color, pos[0], pos[1])
            value = min(value, self.max_value(new_chessboard, alpha, beta, depth - 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value
