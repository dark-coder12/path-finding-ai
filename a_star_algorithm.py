import heapq
import math
import tkinter as tk

# calculating euclidean distance as an estimate of the heuristic
def h_of_n_calculator(node, goal, data):
    
    x1, y1 = node
    x2, y2 = goal
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# checking if the next move is within the boundaries and not in obstacles
def is_move_acceptable(x, y, data):
    
    is_within_grid = 0 <= x < data['grid_width'] and 0 <= y < data['grid_height']
    is_not_obstacle = (x, y) not in data['obstacles']

    return is_within_grid and is_not_obstacle

# tracking initial path
def track_path(prev, current):
    
    p = [current]
    
    while current in prev:
        current = prev[current]
        p.append(current)
        
    p.reverse()
    return p
    
def a_star_algo(start, destination, data):
    
    open_list = []
    
    # we push the first node at 0
    heapq.heappush(open_list, (0, start))
    
    # we keep a track of the path
    prev = {}
   
    # we initialize the scores
    for x in range(data['grid_width']):
        for y in range(data['grid_height']):
            data['g_score'][(x, y)] = float('inf')
            data['f_score'][(x, y)] = float('inf') 
            
    # for the first iteration g_score = 0 (from start to start itself) and h(n) is calculated by the euclidean distance
    data['g_score'][start] = 0
    data['f_score'][start] = h_of_n_calculator(start, destination, data) 

    while open_list:
        i, current = heapq.heappop(open_list)

        # stop if direction has reached
        if current == destination:
            return track_path(prev, current)

        # traversing all directions around the current cell
        for x_cord, y_cord in data['directions']:
            neighbor = (current[0] + x_cord, current[1] + y_cord)

            # check if the new node is even valid (not an obstacle and within the grid)
            if not is_move_acceptable(neighbor[0], neighbor[1], data):
                continue
            
            # add 1 to the currently traversed path
            new_g_of_n = data['g_score'][current] + 1

            # in case a shorter path exists to the neighbor
            if new_g_of_n < data['g_score'][neighbor]:
                
                prev[neighbor] = current
                data['g_score'][neighbor] = new_g_of_n
                data['f_score'][neighbor] = data['g_score'][neighbor] + h_of_n_calculator(neighbor, destination, data)
                heapq.heappush(open_list, (data['f_score'][neighbor], neighbor))

    return None

def draw_grid(data):
    
    # making the grid
    for x in range(data['grid_width']):
        for y in range(data['grid_height']):
            
            # calculating cell size
            x0, y0 = x * data['cell_size'], y * data['cell_size'] + 50
            x1, y1 = x0 + data['cell_size'], y0 + data['cell_size']
            
            cell = data['canvas'].create_rectangle(x0, y0, x1, y1, fill="black", outline="white")  # Set outline to white

            if (x, y) in data['obstacles']:
                data['canvas'].itemconfig(cell, fill="red")

            if (x, y) == data['start']:
                data['canvas'].itemconfig(cell, fill="green")

            if (x, y) == data['destination']:
                data['canvas'].itemconfig(cell, fill="red")

            if (x, y) in data['path']:
                data['canvas'].itemconfig(cell, fill="green")

            # displaying the g and h values
            h_value = h_of_n_calculator((x, y), data['destination'], data)
            g_value = data['g_score'].get((x, y), 0)
            data['canvas'].create_text(x0 + 5, y0 + 5, text=f"g:{g_value:.2f}", anchor="nw", fill="white")
            data['canvas'].create_text(x0 + 5, y1 - 5, text=f"h:{h_value:.2f}", anchor="sw", fill="white")

def main():
    
    # defining the data for the grid - it can be efficiently changed in one place.
    data = {
        'grid_width': 10,
        'grid_height': 10,
        'start': (1, 2),
        'destination': (7, 8),
        'obstacles': {(3, 5), (4, 5), (5, 5), (6, 5)},
        'directions': [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
        'g_score': {},
        'f_score': {},
        'cell_size': None,
        'canvas': None,
        'path': None
    }

    root = tk.Tk()
    root.title("A Star Route Optimization!")

    canvas_width = 1000
    canvas_height = 750
    data['cell_size'] = 50
    data['canvas'] = tk.Canvas(root, width=canvas_width, height=canvas_height) 
    data['canvas'].pack()

    data['path'] = a_star_algo(data['start'], data['destination'], data)

    if data['path']:
        print("The path found is = ")
        for step in data['path']:
            print(step)
        print("The total cost is = ", len(data['path']) - 1)
    else:
        print("No possible path unfortunately")

    draw_grid(data)

    # displaying details on the grid (path taken and the cost for it (optimized))
    path_coords = "Path found: " + " -> ".join([f'({x},{y})' for (x, y) in data['path']])
    total_cost = f'Total cost: {len(data["path"]) - 1}'
    data['canvas'].create_text(canvas_width // 2, 15, text=path_coords, font=("Helvetica", 9), fill="black")
    data['canvas'].create_text(canvas_width // 2, 35, text=total_cost, fill="black", font=("Helvetica", 12, "bold"))

    root.mainloop()

if __name__ == "__main__":
    main()
