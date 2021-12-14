import os
import itertools
from collections import Counter
from typing import List, Tuple

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> Tuple[List[List[List[str]]],List[List[List[str]]]]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        input_, output_ = list(zip(*list(map(lambda x: x.strip().split(' | '), file.readlines()))))
        parse = lambda y: list(map(lambda x: [[char for char in dig] for dig in x.split(' ')], y))
        return parse(input_), parse(output_)

def find_easy_digits(data:List[List[List[str]]]) -> int:
    counter = 0
    for row in data:
        counter += sum(list(map(lambda x: len(x) in [2,3,4,7], row)))
    return counter


def find_output_sum(input_:List[List[List[str]]], output_:List[List[List[str]]]) -> int:
    correct = {1:{'c','f'},
               2:{'a','c','d','e','g'},
               3:{'a','c','d','f','g'},
               4:{'b','c','d','f'},
               5:{'a','b','d','f','g'},
               6:{'a','b','d','e','f','g'},
               7:{'a','c','f'},
               8:{'a','b','c','d','e','f','g'},
               9:{'a','b','c','d','f','g'},
               0:{'a','b','c','e','f','g'}}
    freq = {chr(97+i):0 for i in range(7)}
    for segments in correct.values():
        for char in segments:
            freq[char] +=1
    scores = {sum([freq.get(char) for char in segments]): val for val, segments in correct.items()}
    output_score = 0    
    for in_, out_ in zip(input_, output_):
        local_freq = {chr(97+i):0 for i in range(7)}
        for segments in in_:
            for char in segments:
                local_freq[char] += 1
        local_scores = [scores.get(sum([local_freq.get(char) for char in segments])) * 10**(3-i) for i, segments in enumerate(out_)]
        output_score += sum(local_scores)
    return output_score

if __name__ == '__main__':
    example_input, example_output = read_file('example.txt')
    actual_input, actual_output = read_file('input.txt')

    # part 1
    assert find_easy_digits(example_output) == 26
    print(f'Part 1 solution: {find_easy_digits(actual_output)}')

    # part 2
    assert find_output_sum(example_input, example_output) == 61229
    print(f'Part 2 solution: {find_output_sum(actual_input, actual_output)}')