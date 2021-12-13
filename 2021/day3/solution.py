import os
from typing import List
from collections import Counter
DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[int]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return list(map(lambda x: [int(dig) for dig in x.strip()], file.readlines()))

def binary_to_decimal(binary:List[int]) -> int:
    return sum(val* 2**i for i, val in enumerate(reversed(binary)))

def calculate_power(data:List[List[int]]) -> int:
    digit_frequencies = map(lambda x: sorted(list(Counter(x).items()), key=lambda y: y[1]), zip(*data))
    epsilon, gamma = list(map(lambda x: list(zip(*x)), zip(*digit_frequencies) ))
    return binary_to_decimal(epsilon[0]) * binary_to_decimal(gamma[0])


def filter_lists(options:List[List[int]], index:int, most_common:bool=True) -> List[List[int]]:
    digits = [opt[index] for opt in options]
    if most_common:
        filter_digit = 1 if sum(digits) / len(digits) >= 0.5 else 0
    else:
        filter_digit = 0 if sum(digits) / len(digits) >= 0.5 else 1
    remaining = [opt for opt in options if opt[index] == filter_digit]
    if len(set(map(lambda x: ''.join(map(str, x)), remaining))) == 1:
        return remaining[0]
    else:
        return filter_lists(remaining, index+1, most_common)

def calculate_life_support(data: List[List[int]]) -> int:
    oxygen = filter_lists(data, 0, True)
    co2 = filter_lists(data, 0, False)
    return binary_to_decimal(oxygen) * binary_to_decimal(co2)

if __name__ == '__main__':
    example = read_file('example.txt')
    actual = read_file('input.txt')

    # part 1
    assert calculate_power(example) == 198
    print(f'Part 1 solution: {calculate_power(actual)}')

    # part 2
    assert calculate_life_support(example) == 230
    print(f'Part 2 solution: {calculate_life_support(actual)}')