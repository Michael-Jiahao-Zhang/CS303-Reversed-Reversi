import numpy as np
import random
import math

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
math.inf = math.inf
chess_piece_points = -10
search_depth = 3

weight = np.array([
    [500, -25, 10, 5, 5, 10, -25, 500],
    [-25, -45, 1, 1, 1, 1, -45, -25],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [10, 1, 3, 2, 2, 3, 1, 10],
    [-25, -45, 1, 1, 1, 1, -45, -25],
    [500, -25, 10, 5, 5, 10, -25, 500]
    # [-150, 20, -8, -6, -6, -8, 20, -150],
    # [20, 50, 4, 4, 4, 4, 50, 20],
    # [-8, 4, -6, -4, -4, -6, -4, -8],
    # [-6, 4, -4, 0, 0, 4, -4, -6],
    # [-6, 4, -4, 0, 0, 4, -4, -6],
    # [-8, 4, -6, -4, -4, -6, -4, -8],
    # [20, 50, 4, 4, 4, 4, 50, 20],
    # [-150, 20, -8, -6, -6, -8, 20, -150]
])


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.other_color = -color
        self.time_out = time_out
        self.candidate_list = []
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # def go(self, chessboard):
    #     self.candidate_list.clear()
    #     next_positions = self.get_possible_pos_list(chessboard, self.color)
    #     highest_value = -math.inf
    #     for position in next_positions:
    #         next_chessboard = self.update_board(chessboard, self.color, position[0], position[1])
    #         value = self.min_value(next_chessboard, -math.inf, math.inf, search_depth)
    #         if value > highest_value:
    #             highest_value = value
    #             self.candidate_list.append(position)
    #         else:
    #             self.candidate_list.insert(0, position)
    #     return self.candidate_list
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

    # Decide the possible positions for placing a chess piece
    def get_possible_pos_list(self, chessboard, self_color) -> list:
        positions = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i][j] == COLOR_NONE and self.is_legal(chessboard, self_color, i, j):
                    positions.append((i, j))
        return positions

    # Decide whether the current position is legal to place a chess piece
    def is_legal(self, chessboard, self_color, x, y) -> bool:
        for direction in self.directions:
            possible_x = x + direction[0]
            possible_y = y + direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] != -self_color:
                continue
            while 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] == -self_color:
                possible_x += direction[0]
                possible_y += direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    chessboard[possible_x][possible_y] == self_color:
                return True
        return False

    # 在指定位置下棋并翻转棋子，返回新的chessboard
    def update_board(self, chessboard, self_color, x, y):
        # 因为这个chessboard是传引用的，所以要弄个新的
        new_chessboard = chessboard.copy()
        # 在指定位置下棋
        new_chessboard[x][y] = self_color
        # 检查所有方向，翻转棋子
        for direction in self.directions:
            possible_x = x + direction[0]
            possible_y = y + direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] != -self_color:
                continue
            while 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] == -self_color:
                possible_x += direction[0]
                possible_y += direction[1]
            if 0 <= possible_x < self.chessboard_size and 0 <= possible_y < self.chessboard_size and \
                    new_chessboard[possible_x][possible_y] == self_color:
                while possible_x != x:
                    possible_x -= direction[0]
                    possible_y -= direction[1]
                    new_chessboard[possible_x][possible_y] = self_color
        return new_chessboard

    # 评估函数
    # def evaluate(self, chessboard, self_color) -> int:
    #     count = 0
    #     points = 0
    #     for i in range(self.chessboard_size):
    #         for j in range(self.chessboard_size):
    #             if chessboard[i][j] == self_color:
    #                 count += 1
    #                 points += -point_weight[i][j]
    #     points += count * chess_piece_points
    #     return points
    def evaluate(self, chessboard, cur_color):
        cnt, point = 0, 0
        for y, x in np.ndindex(chessboard.shape):
            if chessboard[y][x] == cur_color:
                cnt += 1
                point += weight[y][x]
        return point

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

    # def max_value(self, chessboard, alpha, beta, depth):
    #     current_color = self.color
    #     if depth == 0:
    #         return self.evaluate(chessboard, current_color)
    #     next_positions = self.get_possible_pos_list(chessboard, current_color)
    #     if len(next_positions) == 0:
    #         return self.min_value(chessboard, alpha, beta, depth - 1)
    #     value = -math.inf
    #     for position in next_positions:
    #         next_chessboard = self.update_board(chessboard, current_color, position[0], position[1])
    #         value = max(value, self.min_value(next_chessboard, alpha, beta, depth - 1))
    #         if value >= beta:
    #             return value
    #         alpha = max(alpha, value)
    #     return value
    #
    # def min_value(self, chessboard, alpha, beta, depth):
    #     current_color = self.other_color
    #     if depth == 0:
    #         return self.evaluate(chessboard, current_color)
    #     next_positions = self.get_possible_pos_list(chessboard, current_color)
    #     if len(next_positions) == 0:
    #         return self.max_value(chessboard, alpha, beta, depth - 1)
    #     value = math.inf
    #     for position in next_positions:
    #         next_chessboard = self.update_board(chessboard, current_color, position[0], position[1])
    #         value = min(value, self.max_value(next_chessboard, alpha, beta, depth - 1))
    #         if value <= alpha:
    #             return value
    #         beta = min(beta, value)
    #     return value
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

