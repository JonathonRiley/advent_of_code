import os
from collections import Counter
from typing import List

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[List[int]]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return list(map(int, file.readline().strip().split(',')))

def calculate_fuel_used(positions:List[int], linear:bool=True) -> int:
    positions_ = dict(Counter(positions))
    min_pos = min(positions_.keys())
    max_pos = max(positions_.keys())
    return min([sum([fuel_use(pos, move_to, linear)*fish for pos, fish in positions_.items()]) for move_to in range(min_pos, max_pos +1)])

def fuel_use(pos:int, move_to:int, linear:bool) -> int:
    if linear:
        return abs(move_to - pos)
    else:
        n = abs(move_to - pos)
        return n * (n+1) // 2

if __name__ == '__main__':
    example = read_file('example.txt')
    actual = read_file('input.txt')

    # part 1
    assert calculate_fuel_used(example) == 37
    print(f'Part 1 solution: {calculate_fuel_used(actual)}')

    # part 2
    assert calculate_fuel_used(example, linear=False) == 168
    print(f'Part 1 solution: {calculate_fuel_used(actual, linear=False)}')