from tkinter import *
from tkinter import messagebox

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
            messagebox.showinfo("Success", "You reached the goal!")
            print("Player path:", player_path)

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

def start_game():
    if not Spot.start_point or not Spot.end_point: 
        messagebox.showinfo("No start/end", "Place starting and ending points")
        return
    for row in grid:
        for spot in row:
            spot.disable() # Disable buttons in the grid when game starts
    start_button.grid_remove()

    # Set initial player position
    col, row = Spot.start_point
    player_position[0] = (col, row)
    grid[row][col].button.config(bg="red")  # Starting player color

    # Reset and initialize player path
    player_path.clear()
    player_path.append((col, row))

    # Reset button
    reset_button = Button(UI_frame, text='Reset', command=reset_path, font = ("Times New Roman", 14), bg='red')
    reset_button.grid(row=5, column=0, padx=5, pady=(10, 10))

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

grid = make_grid(WIDTH, ROWS)
root.mainloop()