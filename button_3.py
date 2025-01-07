import tkinter as tk
import math
from collections import deque

size_of_square = 25
square_map = []
Black = 0
Red = 0
start_pos = None
end_pos = None

def main():
    window = tk.Tk()

    def Start():
        global start_pos, end_pos
        if start_pos != None and end_pos != None:
            path = find_shortest_path(start_pos, end_pos)
            if path:
                for x, y in path:
                    rect_id, _, _ = square_map[x][y]
                    canvas.itemconfig(rect_id, fill='green')

    def Restart():
        global square_map, Black, Red, start_pos, end_pos
        square_map = []
        Black = 0
        Red = 0
        start_pos = None
        end_pos = None
        canvas.delete("all")
        for x in range(0, 700, size_of_square):
            row = []
            for y in range(0, 700, size_of_square):
                rect_id = canvas.create_rectangle(x, y, x + size_of_square, y + size_of_square, outline='black', fill='blue')
                row.append((rect_id, x, y))
            square_map.append(row)

    def change_colour_white(event):
        global square_map
        x = math.floor(event.x / size_of_square)
        y = math.floor(event.y / size_of_square)
        rect_id, _, _ = square_map[x][y]
        colour = canvas.itemcget(rect_id, 'fill')
        if colour == 'blue':
            canvas.itemconfig(rect_id, fill='white')

    def change_colour_red(event):
        global square_map, Red, start_pos
        if Red == 0:
            x = math.floor(event.x / size_of_square)
            y = math.floor(event.y / size_of_square)
            rect_id, _, _ = square_map[x][y]
            colour = canvas.itemcget(rect_id, 'fill')
            if colour == 'blue':
                canvas.itemconfig(rect_id, fill='red')
                start_pos = (x, y)
                Red = 1

    def change_colour_black(event):
        global square_map, Black, end_pos
        if Black == 0:
            x = math.floor(event.x / size_of_square)
            y = math.floor(event.y / size_of_square)
            rect_id, _, _ = square_map[x][y]
            colour = canvas.itemcget(rect_id, 'fill')
            if colour == 'blue':
                canvas.itemconfig(rect_id, fill='black')
                end_pos = (x, y)
                Black = 1

    def find_shortest_path(start, end):
        rows = len(square_map)
        cols = len(square_map[0])
        
        # Directions for moving in the grid (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def is_valid(x, y):
            return 0 <= x < rows and 0 <= y < cols and canvas.itemcget(square_map[x][y][0], 'fill') != 'white'
        
        queue = deque([(*start, [])])
        visited = set()
        visited.add(start)
        
        while queue:
            x, y, path = queue.popleft()
            
            if (x, y) == end:
                return path + [(x, y)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))
        
        return None

    simulation_frame = tk.Frame(window, highlightbackground='blue', highlightthickness=3)
    simulation_frame.pack(side='left', padx=10, pady=10)
    control_frame = tk.Frame(window)
    control_frame.pack(side='left', padx=10, pady=10)

    title = tk.Label(simulation_frame, text="Navigation Simulation", font=("Helvetica", 20, 'bold', 'underline'))
    title.pack(padx=5, pady=5)
    canvas = tk.Canvas(simulation_frame, width=700, height=700, bg='black', highlightthickness=1)
    canvas.pack(padx=5, pady=5)
    label = tk.Label(control_frame, text="White - Alt-Mouse - Block\nRed - Ctrl-Mouse - Start\nBlack - Shift-Mouse - End", font=("Helvetica", 10))
    label.pack(padx=15, pady=15)
    start = tk.Button(control_frame, width=10, height=2, text='Start', command=Start, bg='grey')
    start.pack(padx=15, pady=15)
    restart = tk.Button(control_frame, width=10, height=2, text='Restart', command=Restart, bg='grey')
    restart.pack(padx=15, pady=15)

    Restart()

    canvas.bind('<Alt-Motion>', change_colour_white)  
    canvas.bind('<Control-Motion>', change_colour_red) 
    canvas.bind('<Shift-Motion>', change_colour_black)  

    window.mainloop()

if __name__ == '__main__':
    main()
