import math
import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
search_depth = 4
stable_factor = 10

# 想办法让自己分最大
weight = np.array([[-500, 20, -100, -50, -50, -100, 20, -500],
                   [20, 150, -4, -2, -2, -4, 150, 20],
                   [-100, -4, -8, -1, -1, -8, -4, -10],
                   [-5, -2, -1, 0, 0, -1, -2, -5],
                   [-5, -2, -1, 0, 0, -1, -2, -5],
                   [-100, -4, -8, -1, -1, -8, -4, -10],
                   [20, 150, -4, -2, -2, -4, 150, 20],
                   [-500, 20, -100, -50, -50, -100, 20, -500]
                   ])

weight_end = np.array([[-5, -1, -1, -1, -1, -1, -1, -5],
                       [-1, 1, -1, -1, -1, -1, 1, -1],
                       [-1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, 1, -1, -1, -1, -1, 1, -1],
                       [-5, -1, -1, -1, -1, -1, -1, -5]])


# don't change the class name


class AI(object):

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        self.enemy_color = -color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list.
        # The system will get the end of your candidate_list as your decision.
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()
        print(chessboard)
        possible_pos = self.get_possible_pos_list(chessboard, self.color)
        top_val = -math.inf
        self.calculate_edge_stable(chessboard)
        for pos in possible_pos:
            updated_chessboard = self.update_board(chessboard, self.color, pos[0], pos[1])
            pos_value = self.min_value(
                updated_chessboard, -math.inf, math.inf, search_depth)
            if pos_value > top_val:
                top_val = pos_value
                self.candidate_list.append(pos)
            else:
                self.candidate_list.insert(0, pos)
        return self.candidate_list

    def evaluate(self, chessboard):
        point = 0
        remaining_steps = len(np.where(chessboard == 0)[0])
        if remaining_steps > 8:
            point += np.sum(chessboard * weight)
        else:
            point += np.sum(chessboard * weight_end)
        point *= self.color
        point += self.calculate_edge_stable(chessboard)

        if len(self.get_possible_pos_list(chessboard, self.enemy_color)) == 0:
            point -= 20
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
            direction_flag = False
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
                        direction_flag = True
                        break
                    elif updated_chessboard[y_cur][x_cur] == 0:
                        break
            if direction_flag:
                y_temp, x_temp = y, x
                while y_temp != y_cur or x_temp != x_cur:
                    updated_chessboard[y_temp][x_temp] = cur_color
                    y_temp += yi
                    x_temp += xi
        return updated_chessboard

    def max_value(self, chessboard, alpha, beta, depth):
        cur_color = self.color
        if depth == 0:
            return self.evaluate(chessboard)
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
        cur_color = self.enemy_color
        if depth == 0:
            return self.evaluate(chessboard)
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

    def calculate_edge_stable(self, chessboard):
        cnt_self, cnt_enemy = 0, 0
        dup_self_cnt, dup_enemy_cnt = 0, 0
        if chessboard[0][0] == self.color:
            cnt_self += 1
            i, j = 1, 1
            while chessboard[i][0] == self.color and i < 7:
                cnt_self += 1
                i += 1
            while chessboard[0][j] == self.color and j < 7:
                cnt_self += 1
                j += 1
            if i == 7 and chessboard[7][0] == self.color:
                dup_self_cnt += 1
            if j == 7 and chessboard[0][7] == self.color:
                dup_self_cnt += 1

        if chessboard[0][0] == self.enemy_color:
            cnt_enemy += 1
            i, j = 1, 1
            while chessboard[i][0] == self.enemy_color and i < 7:
                cnt_enemy += 1
                i += 1
            while chessboard[0][j] == self.enemy_color and j < 7:
                cnt_enemy += 1
                j += 1
            if i == 7 and chessboard[7][0] == self.enemy_color:
                dup_enemy_cnt += 1
            if j == 7 and chessboard[0][7] == self.enemy_color:
                dup_enemy_cnt += 1

        if chessboard[0][7] == self.color:
            cnt_self += 1
            i, j = 1, 1
            while chessboard[i][7] == self.color and i < 7:
                cnt_self += 1
                i += 1
            while chessboard[0][7 - j] == self.color and j < 7:
                cnt_self += 1
                j += 1
            if i == 7 and chessboard[7][7] == self.color:
                dup_self_cnt += 1
            if j == 7 and chessboard[0][0] == self.color:
                dup_self_cnt += 1

        if chessboard[0][7] == self.enemy_color:
            cnt_enemy += 1
            i, j = 1, 1
            while chessboard[i][7] == self.enemy_color and i < 7:
                cnt_enemy += 1
                i += 1
            while chessboard[0][7 - j] == self.enemy_color and j < 7:
                cnt_enemy += 1
                j += 1
            if i == 7 and chessboard[7][7] == self.enemy_color:
                dup_enemy_cnt += 1
            if j == 7 and chessboard[0][0] == self.enemy_color:
                dup_enemy_cnt += 1

        if chessboard[7][0] == self.color:
            cnt_self += 1
            i, j = 1, 1
            while chessboard[7 - i][0] == self.color and i < 7:
                cnt_self += 1
                i += 1
            while chessboard[7][j] == self.color and j < 7:
                cnt_self += 1
                j += 1

            if i == 7 and chessboard[0][0] == self.color:
                dup_self_cnt += 1
            if j == 7 and chessboard[7][7] == self.color:
                dup_self_cnt += 1

        if chessboard[7][0] == self.enemy_color:
            cnt_enemy += 1
            i, j = 1, 1
            while chessboard[7 - i][0] == self.enemy_color and i < 7:
                cnt_enemy += 1
                i += 1
            while chessboard[7][j] == self.enemy_color and j < 7:
                cnt_enemy += 1
                j += 1

            if i == 7 and chessboard[0][0] == self.enemy_color:
                dup_enemy_cnt += 1
            if j == 7 and chessboard[7][7] == self.enemy_color:
                dup_enemy_cnt += 1

        if chessboard[7][7] == self.color:
            cnt_self += 1
            i, j = 1, 1
            while chessboard[7 - i][7] == self.color and i < 7:
                cnt_self += 1
                i += 1
            while chessboard[7][7 - j] == self.color and j < 7:
                cnt_self += 1
                j += 1

            if i == 7 and chessboard[0][7] == self.color:
                dup_self_cnt += 1
            if j == 7 and chessboard[7][0] == self.color:
                dup_self_cnt += 1

        if chessboard[7][7] == self.enemy_color:
            cnt_enemy += 1
            i, j = 1, 1
            while chessboard[7 - i][7] == self.enemy_color and i < 7:
                cnt_enemy += 1
                i += 1
            while chessboard[7][7 - j] == self.enemy_color and j < 7:
                cnt_enemy += 1
                j += 1

            if i == 7 and chessboard[0][7] == self.enemy_color:
                dup_enemy_cnt += 1
            if j == 7 and chessboard[7][0] == self.enemy_color:
                dup_enemy_cnt += 1

        dup_self_cnt /= 2
        dup_enemy_cnt /= 2
        cnt_self -= int(6 * dup_self_cnt)
        cnt_enemy -= int(6 * dup_enemy_cnt)
        print(cnt_self)
        print(cnt_enemy)

        return stable_factor * (cnt_enemy - cnt_self)