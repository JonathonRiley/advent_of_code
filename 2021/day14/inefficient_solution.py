import os
from typing import List, Tuple
from collections import Counter

from .example_chains import example_chains_after_steps

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> List[int]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        starting_chain = [char for char in file.readline().strip()]
        directions = list(map(lambda x: [ch.strip() for ch in x.split(' -> ')], [row for row in file.readlines() if '->' in row]))
        return starting_chain, directions

class Link:
    def __init__(self, value:str):
        self.value = value
        self.next: Link = None

class Polymer:
    def __init__(self, starting_chain: List[str], directions: Tuple[str,str]):
        self.first = None
        self.directions = directions
        self.build_initial_chain(starting_chain)

    def build_initial_chain(self, starting_chain: List[str]):
        self.first = Link(starting_chain[0])
        link = self.first
        for char in starting_chain[1:]:
            link.next = Link(char)
            link = link.next

    def apply_rules(self) -> None:
        link = self.first
        while link.next is not None:
            future_link = link.next
            for rule, insert_ in self.directions:
                if link.value == rule[0] and future_link.value == rule[1]:
                    link.next = Link(insert_)
                    link.next.next = future_link
            link = future_link

    def fetch_chain(self) -> str:
        chain = ''
        if self.first is not None:
            link: Link = self.first
            chain += link.value
            while link.next is not None:
                link = link.next
                chain += link.value
        return chain

    def calculate_element_range(self) -> int:
        chain_freq = Counter([char for char in self.fetch_chain()])
        sorted_freq = sorted(list(chain_freq.items()), key=lambda x: x[1])
        return abs(sorted_freq[-1][1] - sorted_freq[0][1])


if __name__ == '__main__':
    example_chain, example_directions = read_file('example.txt')
    actual_chain, actual_directions = read_file('input.txt')

    # # part 1
    example_polymer = Polymer(example_chain, example_directions)
    assert example_polymer.fetch_chain() == 'NNCB'
    for i in range(10):
        example_polymer.apply_rules()
        if i < 4: assert example_polymer.fetch_chain() == example_chains_after_steps[i]
    assert example_polymer.calculate_element_range() == 1588
    
    actual_polymer = Polymer(actual_chain, actual_directions)
    assert actual_polymer.fetch_chain() == ''.join(actual_chain)
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