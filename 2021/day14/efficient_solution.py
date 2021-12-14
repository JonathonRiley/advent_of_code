import os
from typing import List, Tuple
from collections import defaultdict

from .example_chains import example_chains_after_steps

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[int]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        starting_chain = [char for char in file.readline().strip()]
        directions = list(map(lambda x: [ch.strip() for ch in x.split(' -> ')], [row for row in file.readlines() if '->' in row]))
        return starting_chain, directions

class Polymer:
    def __init__(self, starting_chain:List[str], directions: List[Tuple[str,str]]):
        self.starting_chain = starting_chain
        self.directions = directions
        self.pairs = self.build_initial_pairs()
        self.first = starting_chain[0]
        self.last = starting_chain[-1]

    def build_initial_pairs(self) -> dict:
        pairs = {}
        for i in range(len(self.starting_chain)-1):
            pair = ''.join(self.starting_chain[i:i+2])
            if pair in pairs:
                pairs[''.join(self.starting_chain[i:i+2])] += 1
            else:
                pairs[''.join(self.starting_chain[i:i+2])] = 1
        return pairs

    def apply_rules(self) -> None:
        new_pairs = defaultdict(lambda x: 0)
        for pair, insert_ in self.directions:
            first_pair = pair[0]+insert_
            second_pair = insert_ + pair[1]
            if pair in self.pairs:
                if first_pair in new_pairs:
                    new_pairs[first_pair] += self.pairs[pair]
                else: 
                    new_pairs[first_pair] = self.pairs[pair]
                if second_pair in new_pairs:
                    new_pairs[second_pair] += self.pairs[pair]
                else: 
                    new_pairs[second_pair] = self.pairs[pair]
                del self.pairs[pair]
        for pair, freq in self.pairs:
            new_pairs[pair] += freq
        self.pairs = new_pairs

    def calculate_element_range(self) -> int:
        elements = dict()
        for pair, freq in self.pairs.items():
            if pair[0] in elements:
                elements[pair[0]] += freq
            else:
                elements[pair[0]] = freq
            if pair[1] in elements:
                elements[pair[1]] += freq
            else:
                elements[pair[1]] = freq
        elements[self.first] += 1
        elements[self.last] += 1
        elements = {key:val//2 for key, val in elements.items()}
        elements_sorted = sorted(list(elements.items()), key=lambda x: x[1])
        return abs(elements_sorted[-1][1] - elements_sorted[0][1])

if __name__ == '__main__':
    example_chain, example_directions = read_file('example.txt')
    actual_chain, actual_directions = read_file('input.txt')

    # # part 1
    example_polymer = Polymer(example_chain, example_directions)
    for i in range(10):
        example_polymer.apply_rules()
    assert example_polymer.calculate_element_range() == 1588
    
    actual_polymer = Polymer(actual_chain, actual_directions)
    for i in range(10):
        actual_polymer.apply_rules()
    print(f'Part 1 solution: {actual_polymer.calculate_element_range()}')

    # part 2
    for i in range(30):
        example_polymer.apply_rules()
    assert example_polymer.calculate_element_range() == 2188189693529
    
    for i in range(30):
        actual_polymer.apply_rules()
    print(f'Part 2 solution: {actual_polymer.calculate_element_range()}')