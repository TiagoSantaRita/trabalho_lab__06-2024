import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    paths = []

    while stack:
        x, y = stack.pop()
        if (x, y) not in visited:
            if (x, y) == end:
                paths.append((x, y))
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] != 1:
                    stack.append((nx, ny))

    return paths

def generate_maze(width, height):
    maze = [[0] * width for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 1

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            stack.append((nx, ny))
            maze[ny][nx] = 1
            maze[(y + ny) // 2][(x + nx) // 2] = 1
        else:
            stack.pop()

    entrance = random.choice([(i, random.choice(range(1, width, 2))) for i in range(4)])
    exit = random.choice([(i, random.choice(range(1, width, 2))) for i in range(height - 4, height)])
    while exit == entrance:
        exit = random.choice([(i, random.choice(range(1, width, 2))) for i in range(height - 4, height)])

    maze[entrance[0]][entrance[1]] = 2  # Entrance
    maze[exit[0]][exit[1]] = 3  # Exit

    return maze, entrance, exit

def generate_maze_with_multiple_paths(width, height, extra_paths=3, max_attempts=100):
    for _ in range(max_attempts):
        maze, start, end = generate_maze(width, height)
        for _ in range(extra_paths):
            x, y = random.randrange(1, width - 1, 2), random.randrange(1, height - 1, 2)
            while maze[y][x] != 1:
                x, y = random.randrange(1, width - 1, 2), random.randrange(1, height - 1, 2)
            maze[y][x] = 0

        paths = dfs(maze, start, end)
        if len(paths) >= 2:
            break

    return maze

def save_maze_to_txt(maze, filename="matriz"):
    with open(filename, "w") as f:
        for row in maze:
            f.write(" ".join(map(str, row)) + "\n")

def save_maze_image(maze, filename="maze.png", cell_size=20):
    colors = {0: (255, 255, 255), 1: (0, 0, 0), 2: (0, 0, 255), 3: (0, 255, 0)}
    width, height = len(maze[0]), len(maze)
    img = Image.new("RGB", (width * cell_size, height * cell_size + 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for y in range(height):
        for x in range(width):
            color = colors[maze[y][x]]
            draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill=color)

    legend_text = "Legend: White=Wall, Black=Path, Blue=Entrance, Green=Exit"
    draw.text((10, height * cell_size + 5), legend_text, font=font)

    img.save(filename)

def display_maze(maze):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=len(maze[0])*10, height=len(maze)*10)
    canvas.pack()

    colors = {0: "white", 1: "black", 2: "blue", 3: "green"}

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = colors[maze[y][x]]
            canvas.create_rectangle(x*10, y*10, (x+1)*10, (y+1)*10, fill=color)

    root.mainloop()

if __name__ == "__main__":
    maze = generate_maze_with_multiple_paths(20, 20, extra_paths=3)
    save_maze_to_txt(maze, "matriz.txt")
    save_maze_image(maze, cell_size=15)
    display_maze(maze)