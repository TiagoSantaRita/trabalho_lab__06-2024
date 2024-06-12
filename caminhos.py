import matplotlib.pyplot as plt
import numpy as np

def dfs(maze, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]

    visited.add(start)

    if start == end:
        return [path]
    else:
        x, y = start
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        paths = []
        for neighbor in neighbors:
            nx, ny = neighbor
            if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and
                neighbor not in visited and maze[ny][nx] in {1, 3}):
                new_paths = dfs(maze, neighbor, end, visited, path + [neighbor])
                paths.extend(new_paths)
        return paths

if __name__ == "__main__":
    with open("matriz.txt", "r") as f:
        maze = [[int(x) for x in line.split()] for line in f]

    start = end = None
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 2:
                start = (x, y)
            elif maze[y][x] == 3:
                end = (x, y)

    if start and end:
        paths = dfs(maze, start, end)
        print(f"Found {len(paths)} paths.")
        for i, path in enumerate(paths):
            maze_with_path = [row.copy() for row in maze]
            for x, y in path:
                maze_with_path[y][x] = 4
            plt.imshow(maze_with_path, cmap='jet', interpolation='nearest')
            plt.savefig(f"path_{i+1}.png")
    else:
        print("No entrance or exit found in the maze.")