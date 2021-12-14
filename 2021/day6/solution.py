import os
from collections import Counter
from typing import List

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[List[int]]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        pop_with_fish = dict(Counter(map(int, file.readline().strip().split(','))))
        return {key:pop_with_fish.get(key,0) for key in range(9)} # take the extra step so population always has keys from 0-8

def spawn(population:dict, days:int) -> int:
    for _ in range(days):
        population = {key-1:val for key,val in population.items()}
        population[6] += population[-1]
        population[8] = population[-1]
        del population[-1]
    return sum(population.values())


if __name__ == '__main__':
    example = read_file('example.txt')
    actual = read_file('input.txt')

    # part 1
    assert spawn(example, 80) == 5934
    print(f'Part 1 solution: {spawn(actual, 80)}')

    # # part 2
    assert spawn(example, 256) == 26984457539
    print(f'Part 2 solution: {spawn(actual, 256)}')