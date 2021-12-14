import os
import numpy as np
from typing import List, Tuple

DIRNAME = os.path.dirname(__file__)

def read_file(path:str) -> Tuple[List[List[List[str]]],List[List[List[str]]]]:
    relative_path = os.path.join(DIRNAME, path)
    with open(relative_path) as file:
        return np.array([[int(char) for char in row.strip()] for row in file.readlines()])

def calculate_risk(grid:np.array) -> int:
    padded = np.pad(grid, 1, mode='constant', constant_values=(99))
    risk = 0
    for i in range(len(grid)):
        for ii in range(len(grid[0])):
            y = i + 1
            x = ii + 1
            center = padded[y][x]
            if (center < padded[y-1][x]
                and center < padded[y+1][x]
                and center < padded[y][x-1]
                and center < padded[y][x+1]):
                risk += 1 + center
    return risk


def traverse_component(grid, i, j):
    grid[i][j] = False
    size = 1
    if i > 0 and grid[i-1][j]:
        size += traverse_component(grid, i-1, j)
    if j > 0 and grid[i][j-1]:
        size += traverse_component(grid, i, j-1)
    if i < len(grid)-1 and grid[i+1][j]:
        size += traverse_component(grid, i+1, j)
    if j < len(grid[0])-1 and grid[i][j+1]:
        size += traverse_component(grid, i, j+1)
    return size

def top_three_basins(nrows, ncols, grid):
    basin_size_1 = 0
    basin_size_2 = 0
    basin_size_3 = 0
    for i in range(nrows):
        for j in range(ncols):
            if grid[i][j]:
                temp = traverse_component(grid, i, j)
                if temp > basin_size_1:
                    basin_size_3 = basin_size_2
                    basin_size_2 = basin_size_1
                    basin_size_1 = temp
                elif temp > basin_size_2:
                    basin_size_3 = basin_size_2
                    basin_size_2 = temp
                elif temp > basin_size_3:
                    basin_size_3 = temp
    return basin_size_1, basin_size_2, basin_size_3


def find_largest_basins_product(grid:np.array) -> int:
    areas = np.zeros_like(grid)
    areas +=1
    for i in range(len(areas)):
        for ii in range(len(areas[0])):
            if grid[i][ii] == 9:
                areas[i][ii] = 0
    basin_1, basin_2, basin_3 = top_three_basins(len(grid), len(grid[0]), areas)
    return basin_1 * basin_2 * basin_3
    

if __name__ == '__main__':
    example = read_file('example.txt')
    actual = read_file('input.txt')

    # part 1
    assert calculate_risk(example) == 15
    print(f'Part 1 solution: {calculate_risk(actual)}')

    # part 2
    assert find_largest_basins_product(example) == 1134
    print(f'Part 2 solution: {find_largest_basins_product(actual)}')