from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
         bg='#90EE90', bd=1, relief=GROOVE,
         font=('Segoe UI Emoji', 8, 'bold'),
         activebackground='#98FB98'
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
        self.button.config(bg="#EAB71D", text="▶️", fg="white", font=('Segoe UI Emoji', 12, 'bold'))
        self.start = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg="#4ECDC4", text="🏁", fg="white", font=('Segoe UI Emoji', 12, 'bold'))
        self.end = True
        self.clicked = True
        Spot.end_point = (self.col, self.row)
        
    def make_obstacle(self):
        self.button.config(bg="#2C3E50", text="🌲", fg="white", font=('Segoe UI Emoji', 10, 'bold'))
        self.obstacle = True
        self.clicked = True

    def reset(self):
        self.button.config(bg="#90EE90", text="", fg="black", font=('Segoe UI Emoji', 8, 'bold'))
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
            current_spot.button.config(bg="#EAB71D", text="▶️", fg="white")

        else:
            current_spot.button.config(bg="#87CEEB", text="👣", fg="white", font=('Segoe UI Emoji', 10, 'bold'))

        
        # Update position
        player_position[0] = (new_x, new_y)
        next_spot.button.config(bg="#EAB71D", text="🧭", fg="white", font=('Segoe UI Emoji', 12, 'bold'))

        # Record move if not already visited
        if (new_x, new_y) not in player_path:
            player_path.append((new_x, new_y))

        if next_spot.end:
            end_game()

def reset_path():
    for x, y in player_path:
        if (x, y) == Spot.start_point:
            grid[y][x].button.config(bg="#EAB71D", text="▶️", fg="white", font=('Segoe UI Emoji', 12, 'bold'))

        elif (x, y) == Spot.end_point:
            grid[y][x].button.config(bg="#00A846", text="🏁", fg="white", font=('Segoe UI Emoji', 12, 'bold'))
        else:
            grid[y][x].button.config(bg="#6B6B6B", text="", fg="black")
    
    # Set initial player position
    col, row = Spot.start_point
    player_position[0] = (col, row)
    grid[row][col].button.config(bg="#EAB71D", text="🧭", fg="white", font=('Segoe UI Emoji', 12, 'bold'))  # Starting player color

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
            spot.button.config(bg='#90EE90', text="", fg="black", state=NORMAL)
            
    start_button.grid()  # Menampilkan kembali tombol Start Game
    if reset_button:
        reset_button.grid_remove()  # Remove reset button if it exists

def end_game():
    shortest_path = dijkstra(Spot.start_point, Spot.end_point)

    # Warnai shortest path (kecuali start dan end)
    for x, y in shortest_path:
        if (x, y) != Spot.start_point and (x, y) != Spot.end_point:
            grid[y][x].button.config(bg="#FFD700", text="⭐", fg="white", font=('Segoe UI Emoji', 10, 'bold'))

    if player_path == shortest_path:
        messagebox.showinfo("🎉 You Win! 🎉", "Congratulations! You followed Dijkstra's shortest path!\n\n🏆 Perfect Navigation! 🏆")
    else:
        messagebox.showinfo("🤔 Try Again!", f"That's not the optimal path.\n\nYour path: {len(player_path)} steps\nShortest path: {len(shortest_path)} steps\n\n💡 The golden stars show the optimal route!")


    print("Player path:", player_path)
    print("Shortest path:", shortest_path)

def start_game():
    global reset_button  # <--- Tambah ini
    if not Spot.start_point or not Spot.end_point: 
        messagebox.showinfo("⚠️ Setup Required", "Please place both starting point (▶️) and ending point (🏁) first!")
        return
    for row in grid:
        for spot in row:
            spot.disable()
    start_button.grid_remove()

    col, row = Spot.start_point
    player_position[0] = (col, row)
    grid[row][col].button.config(bg="#EAB71D", text="🧭", fg="white", font=('Segoe UI Emoji', 12, 'bold'))

    player_path.clear()
    player_path.append((col, row))

    # Reset button
    reset_button = Button(UI_frame, text='🔄 Reset Path', command=reset_path, 
                         font=("Segoe UI Emoji", 12, 'bold'), bg='#E67E22', fg='white',
                         relief=RAISED, bd=3, padx=10, pady=5)
    reset_button.grid(row=6, column=0, padx=10, pady=10, sticky='ew')  # Ubah kolom agar tak bentrok
    

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
        messagebox.showerror("❌ Invalid Input", "Please enter a number between 0.0 and 1.0")
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
root.title('🎮 Guess the Dijkstra shortest path')
root.maxsize(1000, 700)
root.config(bg='#34495E')
root.bind("<Key>", on_key)

# font = ("Helvetica", 11)

# Variables
WIDTH = 500
ROWS = 25
grid = []

# UI FRAME LAYOUT
UI_frame = Frame(root, width=300, height=600, bg='#2C3E50', relief=RIDGE, bd=2)
UI_frame.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
UI_frame.grid_propagate(False)

# Title Label
title_label = Label(UI_frame, text="🎯 Dijkstra Adventure", 
                   font=("Segoe UI Emoji", 18, 'bold'), fg='#ECF0F1', bg='#2C3E50')
title_label.grid(row=0, column=0, pady=(20, 10), padx=10)

# Instructions
instructions = """
🎮 How to Play:
1️⃣ Click to place Start (▶️)
2️⃣ Click to place Finish (🏁)  
3️⃣ Click to add Trees (🌲) or just use Generate trees button
4️⃣ Press Start Game
5️⃣ Use WASD or Arrow keys

🎯 Goal: Find the shortest path!
"""
instructions_label = Label(UI_frame, text=instructions, 
                          font=("Segoe UI Emoji", 10), fg='#BDC3C7', bg='#2C3E50',
                          justify=LEFT, wraplength=250)
instructions_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

# Create Canvas with border
canvas_frame = Frame(root, bg='#27AE60', relief=RIDGE, bd=3)
canvas_frame.grid(row=0, column=1, padx=15, pady=15)

canvas = Canvas(canvas_frame, width=WIDTH, height=WIDTH, bg='#58D68D', 
               relief=SUNKEN, bd=2)
canvas.pack(padx=5, pady=5)

# UI Buttons with better styling
button_style = {
    'font': ("Segoe UI Emoji", 12, 'bold'),
    'relief': RAISED,
    'bd': 3,
    'padx': 15,
    'pady': 8
}

start_button = Button(UI_frame, text='▶️ Start Game', command=start_game, 
                     bg='#27AE60', fg='white', **button_style)
start_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Separator
separator1 = ttk.Separator(UI_frame, orient='horizontal')
separator1.grid(row=3, column=0, sticky='ew', padx=20, pady=10)

# Wall Generation Section
# wall_label = Label(UI_frame, text="🌲 Generate Forest", 
#                   font=("Segoe UI Emoji", 14, 'bold'), fg='#E67E22', bg='#2C3E50')
# wall_label.grid(row=4, column=0, pady=(10, 5))

density_label = Label(UI_frame, text="Tree Density (0.0 - 0.4):", 
                     font=("Segoe UI Emoji", 10), fg='#BDC3C7', bg='#2C3E50')
density_label.grid(row=5, column=0, pady=(5, 0))

density_entry = Entry(UI_frame, width=15, font=("Segoe UI Emoji", 11), 
                     justify=CENTER, relief=SUNKEN, bd=2)
density_entry.grid(row=6, column=0, pady=(5, 10))
density_entry.insert(0, "0.15")  # Default value

generate_button = Button(UI_frame, text='🌳 Generate Trees', command=generate_walls, 
                        bg='#E67E22', fg='white', **button_style)
generate_button.grid(row=7, column=0, padx=10, pady=5, sticky='ew')

# Separator
separator2 = ttk.Separator(UI_frame, orient='horizontal')
separator2.grid(row=8, column=0, sticky='ew', padx=20, pady=15)

reset_all_button = Button(UI_frame, text='🔄 Reset All', command=reset_all, 
                         bg='#EAB71D', fg='white', **button_style)
reset_all_button.grid(row=9, column=0, padx=10, pady=10, sticky='ew')


# Make UI responsive
UI_frame.grid_columnconfigure(0, weight=1)

grid = make_grid(WIDTH, ROWS)

root.mainloop()