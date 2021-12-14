import os
import numpy as np
from typing import List, Tuple

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[List[int]]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return [tuple(map(lambda x: tuple(map(int, x.split(','))), line.strip().split(' -> '))) for line in file.readlines()]

class Field:
    def __init__(self, coords:List[Tuple[Tuple[int,int],Tuple[int,int]]]):
        self.coords = coords
        self.grid = self.generate_blank_grid()

    def generate_blank_grid(self) -> np.array:
        max_x = 0
        max_y = 0
        for ((x1, y1), (x2,y2)) in self.coords:
            max_x = max([max_x, x1, x2])
            max_y = max([max_y, y1, y2])
        return np.zeros((max_y+1,max_x+1))

    def fill_field(self, diagonals:bool) -> None:
        for ((x1, y1), (x2,y2)) in self.coords:
            if not diagonals and (x1 == x2 or y1 == y2):
                from_ = min([x1,x2]), min([y1,y2])
                to_ = max([x1,x2]), max([y1,y2])
                for x in range(from_[0], to_[0]+1):
                    for y in range(from_[1], to_[1]+1):
                        self.grid[y][x] += 1
            elif diagonals and x1 != x2 and y1 != y2 and abs((y2-y1) / (x2-x1)) == 1:
                slope = (y2-y1) // (x2-x1)
                x_from = min([x1,x2])
                y_from = y1 if x1==x_from else y2
                for i in range(abs(x2-x1)+1):
                    self.grid[y_from+i*slope][x_from+i] += 1

    def calculate_overlaps(self, diagonals:bool=False) -> int:
        self.fill_field(diagonals)
        return sum(sum(self.grid > 1))

if __name__ == '__main__':
    example = Field(read_file('example.txt'))
    actual = Field(read_file('input.txt'))

    # # part 1
    assert example.calculate_overlaps() == 5
    print(f'Part 1 solution: {actual.calculate_overlaps()}')

    # part 2
    assert example.calculate_overlaps(diagonals=True) == 12
    print(f'Part 2 solution: {actual.calculate_overlaps(diagonals=True)}')