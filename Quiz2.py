from tkinter import *

# define class - spot
class Spot:
    
    start_point = None
    end_point = None
    
    __slots__ = ['button','row', 'col', 'width', 'start', 'end', 'barrier', 'clicked', 'total_rows']
    
    def __init__(self, row, col, width, offset, total_rows):
        
        self.button = Button(canvas,
         command = lambda: self.click(),
         bg='white', bd=2, relief=GROOVE
        )
        
        self.row = row
        self.col = col
        self.width = width
        
        self.button.place(x=row * width + offset, y=col * width + offset, 
                          width=width, height=width)
        self.start = False
        self.end = False
        self.barrier = False
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
        
    def make_barrier(self):
        self.button.config(bg = "black")
        self.barrier = True
        self.clicked = True

    def reset(self):
        self.button.config(bg = "white")
        self.clicked = False
    
    def click(self):
        if self.clicked == False:
            if not Spot.start_point:   
                self.make_start()
            elif not Spot.end_point:
                self.make_end()
            else :
                self.make_barrier()
        else:
            self.reset()
            if self.start == True:   
                self.start = False
                Spot.start_point = None
            elif self.end == True:
                self.end = False
                Spot.end_point = None
            else :
                self.barrier = False

def make_grid(width, rows):
    gap = width // rows
    offset = 2
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, offset, rows)
            grid[i].append(spot)
    return grid


# Main Window
root = Tk()
root.title('Guess the Dijkstra algorithm path')
root.maxsize(900, 900)
root.config(bg='black')

font = ("Helvetica", 11)

# Variabel
WIDTH = 500
ROWS = 25
grid = []

# UI FRAME LAYOUT
UI_frame = Frame(root, width=800, height=600, bg='black')
UI_frame.grid(row=0, column=0, padx=10, pady=5)

# create canvas
canvas = Canvas(root, width=WIDTH, height=WIDTH, bg='white')
canvas.grid(row=0, column=1, padx=10, pady=5)

# UI
Button(UI_frame, text='Start Search', font = ("Times New Roman", 14),
       bg='lime').grid(row=5, column=0, padx=5, pady=(10, 10))

grid = make_grid(WIDTH, ROWS)
root.mainloop()