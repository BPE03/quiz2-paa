from tkinter import *
from tkinter import messagebox
import random
import heapq

reset_button = None  # Dideklarasikan global

# define class - spot
class Spot:
    
    start_point = None
    end_point = None
    
    __slots__ = ['button','row', 'col', 'width', 'start', 'end', 'obstacle', 'clicked', 'total_rows']
    
    def __init__(self, row, col, width, offset, total_rows):
        
        self.button = Button(canvas,
         command = lambda: self.click(),
         bg='gray90', bd=2, relief=GROOVE
        )
        
        self.row = row
        self.col = col
        self.width = width
        
        self.button.place(x=row * width + offset, y=col * width + offset, 
                          width=width, height=width)
        self.start = False
        self.end = False
        self.obstacle = False
        self.clicked = False
        self.total_rows = total_rows
    
    def make_start(self):
        self.button.config(bg = "Orange")
        self.start = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg = "lime green")
        self.end = True
        self.clicked = True
        Spot.end_point = (self.col, self.row)
        
    def make_obstacle(self):
        self.button.config(bg = "black")
        self.obstacle = True
        self.clicked = True

    def reset(self):
        self.button.config(bg = "gray90")
        self.clicked = False
    
    def click(self):
        if self.clicked == False:
            if not Spot.start_point:   
                self.make_start()
            elif not Spot.end_point:
                self.make_end()
            else :
                self.make_obstacle()
        else:
            self.reset()
            if self.start == True:
                self.start = False
                Spot.start_point = None
            elif self.end == True:
                self.end = False
                Spot.end_point = None
            else :
                self.obstacle = False

    def disable(self):
        self.button.config(state=DISABLED)
    
    def enable(self):
        self.button.config(state=NORMAL)

def make_grid(width, rows):
    gap = width // rows
    offset = 2
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, offset, rows)
            grid[i].append(spot)
    return grid

# Player movement tracking
player_position = [None]  # Using list to make it mutable inside key handlers
player_path = []  # Stores each (col, row) that the player visits

def move_player(dx, dy):
    if player_position[0] is None:
        return

    x, y = player_position[0]
    new_x = x + dx
    new_y = y + dy

    if 0 <= new_x < ROWS and 0 <= new_y < ROWS:
        next_spot = grid[new_y][new_x]
        if next_spot.obstacle:
            return
        
        # Reset previous
        current_spot = grid[y][x]
        if current_spot.start:  # Keep start color if it's the starting point
            current_spot.button.config(bg="Orange")
        else:
            current_spot.button.config(bg="deepskyblue")
        
        # Update position
        player_position[0] = (new_x, new_y)
        next_spot.button.config(bg="red")

        # Record move if not already visited
        if (new_x, new_y) not in player_path:
            player_path.append((new_x, new_y))

        if next_spot.end:
            shortest_path = dijkstra(Spot.start_point, Spot.end_point)

            # Warnai shortest path (kecuali start dan end)
            for x, y in shortest_path:
                if (x, y) != Spot.start_point and (x, y) != Spot.end_point:
                    grid[y][x].button.config(bg="yellow")

            if player_path == shortest_path:
                messagebox.showinfo("You win!", "You followed the correct shortest path!")
            else:
                messagebox.showinfo("Incorrect path", "That's not the shortest path.")

            print("Player path:", player_path)
            print("Shortest path:", shortest_path)

def reset_path():
    for x, y in player_path:
        if (x, y) == Spot.start_point:
            grid[y][x].button.config(bg="Orange")
        else:
            grid[y][x].button.config(bg="gray90")
    
    # Set initial player position
    col, row = Spot.start_point
    player_position[0] = (col, row)
    grid[row][col].button.config(bg="red")  # Starting player color

    # Reset and initialize player path
    player_path.clear()
    player_path.append((col, row))
    
def reset_all():
    Spot.start_point = None
    Spot.end_point = None
    player_path.clear()
    player_position[0] = None

    for row in grid:
        for spot in row:
            spot.start = False
            spot.end = False
            spot.obstacle = False
            spot.clicked = False
            spot.button.config(bg='gray90', state=NORMAL)
            
    start_button.grid()  # Menampilkan kembali tombol Start Game
    if reset_button:
        reset_button.grid_remove()  # Remove reset button if it exists


def start_game():
    global reset_button  # <--- Tambah ini
    if not Spot.start_point or not Spot.end_point: 
        messagebox.showinfo("No start/end", "Place starting and ending points")
        return
    for row in grid:
        for spot in row:
            spot.disable()
    start_button.grid_remove()

    col, row = Spot.start_point
    player_position[0] = (col, row)
    grid[row][col].button.config(bg="red")

    player_path.clear()
    player_path.append((col, row))

    # Reset button
    reset_button = Button(UI_frame, text='Reset', command=reset_path, font=("Times New Roman", 14), bg='red')
    reset_button.grid(row=5, column=0, padx=5, pady=(10, 10))  # Ubah kolom agar tak bentrok
    

def dijkstra(start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = set()
    prev = {}
    dist = { (x, y): float('inf') for y in range(ROWS) for x in range(ROWS) }
    dist[start] = 0

    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        x, y = current
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < ROWS:
                neighbor = (nx, ny)
                if grid[ny][nx].obstacle or neighbor in visited:
                    continue
                new_dist = current_dist + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))

    # Reconstruct path
    path = []
    current = end
    while current in prev:
        path.append(current)
        current = prev[current]
    path.append(start)
    path.reverse()
    return path


def auto_generate_walls(density=0.2):
    """Mengisi grid dengan dinding secara acak. Density antara 0 dan 1."""
    for row in grid:
        for spot in row:
            if not spot.start and not spot.end:
                if random.random() < density:
                    spot.make_obstacle()


def generate_walls():
    try:
        density = float(density_entry.get())
        if not 0 <= density <= 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a number between 0.0 and 1.0")
        return

    # Reset semua obstacle dulu
    for row in grid:
        for spot in row:
            if spot.obstacle and not spot.start and not spot.end:
                spot.reset()
                spot.obstacle = False
                spot.clicked = False

    auto_generate_walls(density)


def on_key(event):
    key = event.keysym
    if key in ("Up", "w", "W"):
        move_player(-1, 0)
    elif key in ("Down", "s", "S"):
        move_player(1, 0)
    elif key in ("Left", "a", "A"):
        move_player(0, -1)
    elif key in ("Right", "d", "D"):
        move_player(0, 1)

# Main Window
root = Tk()
root.title('Guess the Dijkstra shortest path')
root.maxsize(900, 900)
root.config(bg='black')
root.bind("<Key>", on_key)

font = ("Helvetica", 11)

# Variables
WIDTH = 500
ROWS = 25
grid = []

# UI FRAME LAYOUT
UI_frame = Frame(root, width=800, height=600, bg='black')
UI_frame.grid(row=0, column=0, padx=10, pady=5)

# Create Canvas
canvas = Canvas(root, width=WIDTH, height=WIDTH, bg='white')
canvas.grid(row=0, column=1, padx=10, pady=5)

# UI
start_button = Button(UI_frame, text='Start Game', command=start_game, font = ("Times New Roman", 14), bg='lime')
start_button.grid(row=5, column=0, padx=5, pady=(10, 10))
Label(UI_frame, text="Wall Density (0.0 - 0.4):", font=font, fg='white', bg='black').grid(row=6, column=0, pady=(5, 0))
density_entry = Entry(UI_frame, width=10, font=font)
density_entry.grid(row=7, column=0, pady=(0, 10))
density_entry.insert(0, "0.1") # Nilai default
generate_button = Button(UI_frame, text='Generate Walls', command=generate_walls, font=("Times New Roman", 12), bg='orange')
generate_button.grid(row=8, column=0, pady=(5, 10))
reset_all_button = Button(UI_frame, text='Reset All', command=reset_all, font=("Times New Roman", 12), bg='red')
reset_all_button.grid(row=9, column=0, pady=(5, 10))

grid = make_grid(WIDTH, ROWS)


root.mainloop()