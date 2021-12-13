import os
from typing import List
DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[int]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return list(map(lambda x: int(x.strip()), file.readlines()))

def individual_increase(data: List[int]) -> int:
    last = data[0]
    increases = 0
    for step in data[1:]:
        if step > last:
            increases+=1
        last = step
    return increases

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
    assert individual_increase(example) == 7
    print(f'Part 1 solution: {individual_increase(actual)}')

    # part 2
    assert window_increase(example) == 5
    print(f'Part 2 solution: {window_increase(actual)}')