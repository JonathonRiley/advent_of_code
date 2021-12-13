import os
from typing import List
DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[int]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return [[direction, int(steps)] for direction, steps in map(lambda x: x.strip().split(' '), file.readlines())]

def navigate(data: List[int], with_aim:bool=False) -> int:
    horizontal = 0
    vertical = 0
    aim = 0
    for direction, steps in data:
        if direction == 'forward':
            horizontal += steps
            if with_aim: vertical += aim * steps
        elif direction == 'down':
            if with_aim:
                aim += steps
            else:
                vertical += steps
        else:
            if with_aim:
                aim -= steps
            else:
                vertical -= steps
    return horizontal * vertical

def window_increase(data: List[int]) -> int:
    increases = 0
    for step_index in range(len(data[3:])):
        step_ahead = data[3+step_index]
        step_behind = data[step_index]
        if step_ahead > step_behind:
            increases +=1
    return increases


if __name__ == '__main__':
    example = read_file('example.txt')
    actual = read_file('input.txt')

    # part 1
    assert navigate(example) == 150
    print(f'Part 1 solution: {navigate(actual)}')

    # part 2
    assert navigate(example, True) == 900
    print(f'Part 2 solution: {navigate(actual, True)}')