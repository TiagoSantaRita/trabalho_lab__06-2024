import random
import tkinter as tk
from tkinter import Label, Toplevel
import time

from PIL import Image, ImageDraw, ImageTk

N, S, E, W = 1, 2, 4, 8
CELL_SIZE = 10  # Define a cell size menor

current_grid = None
current_img = None
bfs_iterations = 0
dfs_iterations = 0
bfs_time = 0.0
dfs_time = 0.0


def generate_maze(width, height):
    grid = [[0 for x in range(width)] for y in range(height)]
    for y in range(height):
        run_start = 0
        for x in range(width):
            if y > 0 and (x+1 == width or random.randint(0, 1) == 0):
                cell = run_start + random.randint(0, x - run_start)
                grid[y][cell] |= N
                grid[y-1][cell] |= S
                run_start = x+1
            elif x+1 < width:  # Ensure x+1 is within the grid
                grid[y][x] |= E
                grid[y][x+1] |= W
    return grid


def generate_image(grid, cell_size=CELL_SIZE):
    width = len(grid[0])
    height = len(grid)
    img_width = width * cell_size
    img_height = height * cell_size
    img = Image.new('RGB', (img_width, img_height), color='white')
    d = ImageDraw.Draw(img)

    # Draw the walls with thicker lines
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell & S == 0:
                d.line([(x*cell_size, (y+1)*cell_size), ((x+1) *
                       cell_size, (y+1)*cell_size)], fill='black', width=2)
            if cell & E == 0:
                d.line([((x+1)*cell_size, y*cell_size), ((x+1) *
                       cell_size, (y+1)*cell_size)], fill='black', width=2)
            if cell & N == 0:
                d.line([(x*cell_size, y*cell_size),
                       ((x+1)*cell_size, y*cell_size)], fill='black', width=2)
            if cell & W == 0:
                d.line([(x*cell_size, y*cell_size), (x*cell_size,
                       (y+1)*cell_size)], fill='black', width=2)

    # Highlight the start and end points
    d.rectangle([(0, 0), (cell_size, cell_size)], fill='green')  # Start point
    d.rectangle([(img_width-cell_size, img_height-cell_size),
                (img_width, img_height)], fill='blue')  # End point

    return img


def solve_maze(grid, img, cell_size=CELL_SIZE):
    global bfs_iterations, bfs_time
    start_time = time.time()

    width = len(grid[0])
    height = len(grid)
    start = (0, 0)  # Start cell
    end = (width-1, height-1)  # End cell
    queue = [start]
    visited = set()
    paths = {start: []}  # Dictionary to keep track of paths
    bfs_iterations = 0

    while queue:
        bfs_iterations += 1
        cell = queue.pop(0)
        if cell == end:
            path = paths[cell]  # Get the path when the end is reached
            break
        # Down, up, right, left
        for direction, bit in [((0, 1), S), ((0, -1), N), ((1, 0), E), ((-1, 0), W)]:
            x, y = cell[0] + direction[0], cell[1] + direction[1]
            # Check if the cell is valid and not a wall
            if 0 <= x < width and 0 <= y < height and grid[cell[1]][cell[0]] & bit and (x, y) not in visited:
                queue.append((x, y))
                visited.add((x, y))
                # Add the direction to the path
                paths[(x, y)] = paths[cell] + [direction]
    else:
        return None  # Return None if no path is found

    d = ImageDraw.Draw(img)
    current = (0, 0)
    for direction in path:
        next_cell = (current[0] + direction[0], current[1] + direction[1])
        d.rectangle([(next_cell[0]*cell_size, next_cell[1]*cell_size), ((next_cell[0]+1)
                    * cell_size, (next_cell[1]+1)*cell_size)], fill='red', outline='black')
        current = next_cell

    end_time = time.time()
    bfs_time = end_time - start_time
    tk_img = ImageTk.PhotoImage(img)
    generate_maze_and_image.img_label.config(image=tk_img)
    generate_maze_and_image.img_label.image = tk_img


def solve_maze_dfs(grid, img, cell_size=CELL_SIZE):
    global dfs_iterations, dfs_time
    start_time = time.time()

    width = len(grid[0])
    height = len(grid)
    start = (0, 0)  # Start cell
    end = (width-1, height-1)  # End cell
    stack = [start]
    visited = set()
    paths = {start: []}  # Dictionary to keep track of paths
    dfs_iterations = 0

    while stack:
        dfs_iterations += 1
        cell = stack.pop()
        if cell == end:
            path = paths[cell]  # Get the path when the end is reached
            break
        # Down, up, right, left
        for direction, bit in [((0, 1), S), ((0, -1), N), ((1, 0), E), ((-1, 0), W)]:
            x, y = cell[0] + direction[0], cell[1] + direction[1]
            # Check if the cell is valid and not a wall
            if 0 <= x < width and 0 <= y < height and grid[cell[1]][cell[0]] & bit and (x, y) not in visited:
                stack.append((x, y))
                visited.add((x, y))
                # Add the direction to the path
                paths[(x, y)] = paths[cell] + [direction]
    else:
        return None  # Return None if no path is found

    d = ImageDraw.Draw(img)
    current = (0, 0)
    for direction in path:
        next_cell = (current[0] + direction[0], current[1] + direction[1])
        d.rectangle([(next_cell[0]*cell_size, next_cell[1]*cell_size), ((next_cell[0]+1)
                    * cell_size, (next_cell[1]+1)*cell_size)], fill='red', outline='black')
        current = next_cell

    end_time = time.time()
    dfs_time = end_time - start_time
    tk_img = ImageTk.PhotoImage(img)
    generate_maze_and_image.img_label.config(image=tk_img)
    # Keep a reference to the image to prevent it from being garbage collected
    generate_maze_and_image.img_label.image = tk_img


def generate_maze_and_image():
    global current_grid, current_img
    width = width_scale.get()
    height = height_scale.get()
    current_grid = generate_maze(width, height)

    current_img = generate_image(current_grid)

    tk_img = ImageTk.PhotoImage(current_img)
    if hasattr(generate_maze_and_image, 'img_label'):
        generate_maze_and_image.img_label.config(image=tk_img)
    else:
        generate_maze_and_image.img_label = tk.Label(root, image=tk_img)
        generate_maze_and_image.img_label.pack()
    # Keep a reference to the image to prevent it from being garbage collected
    generate_maze_and_image.img_label.image = tk_img


def solve_current_maze():
    if current_grid is not None and current_img is not None:
        if solve_option.get() == "BFS":
            solve_maze(current_grid, current_img)
            bfs_label.config(text=f"BFS Iterations: {bfs_iterations}, Time: {bfs_time:.4f} seconds")
        elif solve_option.get() == "DFS":
            solve_maze_dfs(current_grid, current_img)
            dfs_label.config(text=f"DFS Iterations: {dfs_iterations}, Time: {dfs_time:.4f} seconds")


root = tk.Tk()
root.geometry("800x600")

# Frame para centralizar os rótulos e escalas
frame = tk.Frame(root)
frame.pack(pady=5)

width_label = tk.Label(frame, text="Largura")
width_label.grid(row=0, column=0, pady=1)
width_scale = tk.Scale(frame, from_=10, to=50, orient='horizontal')
width_scale.grid(row=1, column=0, pady=1)

height_label = tk.Label(frame, text="Altura")
height_label.grid(row=2, column=0, pady=1)
height_scale = tk.Scale(frame, from_=10, to=50, orient='horizontal')
height_scale.grid(row=3, column=0, pady=1)

generate_button = tk.Button(
    root, text="Gerar Labirinto", command=generate_maze_and_image)
generate_button.pack(pady=1)

solve_option = tk.StringVar()
solve_option.set("BFS")  # Default to BFS

solve_option_frame = tk.Frame(root)
solve_option_frame.pack(pady=5)

bfs_radio = tk.Radiobutton(solve_option_frame, text="BFS", variable=solve_option,
                           value="BFS", command=solve_current_maze)
bfs_radio.pack(side="left", padx=10)

dfs_radio = tk.Radiobutton(solve_option_frame, text="DFS", variable=solve_option,
                           value="DFS", command=solve_current_maze)
dfs_radio.pack(side="left", padx=10)

solve_button = tk.Button(root, text="Resolver", command=solve_current_maze)
solve_button.pack(pady=1)

bfs_label = tk.Label(root, text="", pady=5)
bfs_label.pack()

dfs_label = tk.Label(root, text="", pady=5)
dfs_label.pack()

root.mainloop()

