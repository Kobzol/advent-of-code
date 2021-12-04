import dataclasses
from typing import List

import numpy as np


@dataclasses.dataclass
class Board:
    numbers: np.ndarray
    marked: np.ndarray

    def mark(self, number: int):
        n = self.numbers
        indices = np.where(n == number)
        self.marked[indices] = True

    def get_unmarked(self) -> List[int]:
        return list(self.numbers[np.where(self.marked == False)])

    def is_winning(self) -> bool:
        by_row = np.any(np.all(self.marked == True, axis=1))
        by_col = np.any(np.all(self.marked == True, axis=0))
        return by_row or by_col


boards = []
board = []


def make_board(board) -> Board:
    return Board(np.array(board, dtype=np.int32).reshape((5, 5)),
                                    np.zeros((5, 5), dtype=bool))


with open("input.txt") as f:
    draws = [int(v) for v in f.readline().strip().split(",")]
    for line in f:
        line = line.strip()
        if line == "":
            if board:
                boards.append(make_board(board))
            board = []
        else:
            board += [int(v) for v in line.split()]
boards.append(make_board(board))

already_winned = set()
for draw in draws:
    for (board_index, board) in enumerate(boards):
        if board_index in already_winned:
            continue
        board.mark(draw)
        if board.is_winning():
            if len(already_winned) == len(boards) - 1:
                score = sum(board.get_unmarked())
                print(score * draw)
                exit()
            already_winned.add(board_index)
