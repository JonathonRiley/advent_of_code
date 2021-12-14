import os
import numpy as np
from collections import Counter
from typing import List, Tuple

DIRNAME = os.path.dirname(__file__)


class Board:
    def __init__(self, grid:List[List[int]]):
        self.size = len(grid)
        self.numbers = np.array(grid)
        self.crossed = np.array([[0 for _ in range(self.size)] for _ in range(self.size)])
    
    def check_for_number(self, number:int) -> bool:
        for i, row in enumerate(self.numbers):
            for ii, val in enumerate(row):
                if self.numbers[i][ii] == number:
                    self.crossed[i][ii] = 1
                    return True
        return False

    def check_if_winner(self) -> bool:
        rows = sum(self.crossed)
        cols = sum(np.array(list(zip(*self.crossed))))
        return any(rows==self.size) or any(cols==self.size)

    def calculate_score(self, number) -> int:
        unused = (self.crossed-1)*-1 * self.numbers
        return int(sum(sum(unused)) * number)

    def show_board(self) -> None:
        print(self.crossed * self.numbers)

class Game:
    def __init__(self, path:str):
        self.numbers, self.boards = self.read_file(path)
    
    def read_file(self, path:str) -> Tuple[List[int], List[List[int]]]:
        relative_path = os.path.join(DIRNAME, path)
        with open(relative_path) as file:
            numbers = [int(num) for num in file.readline().strip().split(',')]
            boards = []
            current_board = []
            for line in file.readlines():
                if line == '\n':
                    if current_board != []:
                        boards.append(Board(current_board))
                        current_board = []
                else:
                    current_board.append([int(char.strip()) for char in line.split(' ') if char!=''])
            boards.append(Board(current_board))
            return numbers, boards

    def find_winning_score(self, find_loser:bool=False) -> int:
        boards_in_play = list(range(len(self.boards)))
        for number in self.numbers:
            for board_num, board in enumerate(self.boards):
                found = board.check_for_number(number)
                if found:
                    winner = board.check_if_winner()
                    if winner:
                        if find_loser:
                            if board_num in boards_in_play:
                                boards_in_play.remove(board_num)
                                if len(boards_in_play) == 0:
                                    return board.calculate_score(number)
                        else:
                            return board.calculate_score(number)


if __name__ == '__main__':
    example = Game('example.txt')
    actual = Game('input.txt')

    # part 1
    assert example.find_winning_score() == 4512
    print(f'Part 1 solution: {actual.find_winning_score()}')

    # part 2
    assert example.find_winning_score(find_loser=True) == 1924
    print(f'Part 1 solution: {actual.find_winning_score(find_loser=True)}')