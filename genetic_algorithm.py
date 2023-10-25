import random
import math
import heapq
import tkinter as tk

# functions obtained from a star search algorithm
def a_star_algo(data, start, destination):
    
    open_list = []
    
    # we keep a track of the path
    prev = {}

    # we initialize the scores
    for x in range(data['grid_width']):
        for y in range(data['grid_height']):
            
            data['g_score'][(x, y)] = float('inf')
            data['f_score'][(x, y)] = float('inf')

     # for the first iteration g_score = 0 (from start to start itself) and h(n) is calculated by the euclidean distance
    data['g_score'][start] = 0
    data['f_score'][start] = h_of_n_calculator(start, destination)
    
     # we push the first node at 0
    heapq.heappush(open_list, (0, start))

    while open_list:
        i, current = heapq.heappop(open_list)
        
         # stop if direction has reached
        if current == destination:
            return track_path(prev, current)

        # traversing all directions around the current cell
        for x_cord, y_cord in data['directions']:
            neighbor = (current[0] + x_cord, current[1] + y_cord)
            
             # check if the new node is even valid (not an obstacle and within the grid)
            if not is_move_acceptable(data, neighbor[0], neighbor[1]):
                continue
            
             # add 1 to the currently traversed path
            new_g_of_n = data['g_score'][current] + 1

            # in case a shorter path exists to the neighbor
            if new_g_of_n < data['g_score'][neighbor]:
                prev[neighbor] = current
                data['g_score'][neighbor] = new_g_of_n
                data['f_score'][neighbor] = data['g_score'][neighbor] + h_of_n_calculator(neighbor, destination)
                
                heapq.heappush(open_list, (data['f_score'][neighbor], neighbor))

    return None

# calculating euclidean distance as an estimate of the heuristic
def h_of_n_calculator(node, goal, ):
    
    x1, y1 = node
    x2, y2 = goal
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# checking if the next move is within the boundaries and not in obstacles
def is_move_acceptable(data, x, y):
    
    return 0 <= x < data['grid_width'] and  0 <= y < data['grid_height'] and (x, y) not in data['obstacles']

# tracking initial path
def track_path(prev, current):
    
    p = [current]
    while current  in prev:
        current = prev[current]
        p.append(current)
    p.reverse()
    
    return p

# randomly initializing population path
def create_random_path(data):
    
    return random.sample([(x, y) for x in range(data['grid_width']) for y in range(data['grid_height']) if (x, y) not in data['obstacles']], 5)

# randomly selected coordinate should be at minimum distance from both start and end
def fitness_function(data, path, start, end):
    
    total_cost = len(a_star_algo(data, start, path[0])) + len(a_star_algo(data, path[-1], end))
    
    for i in range(len(path) - 1):
        total_cost += len(a_star_algo(data, path[i], path[i + 1]))
    return total_cost

# helper function
def remove_duplicates(input_list):
    
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

def main():
    
     # defining the data for the grid - it can be efficiently changed in one place.
    data = {
        'grid_width': 10,
        'grid_height': 10,
        'start': (1, 2),
        'destination': (7, 8),
        'obstacles': {(3, 5), (4, 5),  (5, 5), (6, 5), },
        'directions': [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
        'g_score': {},
        'f_score': {},
        'cell_size': None,
        'canvas': None,
        'path': None
    }

    # can be finetuned
    # GA parameters
    population_size = 500
    rate_for_mutating = 0.1
    generations = 10

    best_path = None
    best_path_cost = float('inf')

    # running GA atleast 5 times to ensure a good solution
    for z in range(5):
      
        start = data['start']
        end = data['destination']
        
        # choosing random points initially on the grid
        population = [create_random_path(data) for i in range(population_size)]

        # running for specified generations
        for generation in range(generations):
            
            # we calculate fitness of each coordinate (wrt start and end)
            fitness_scores = [fitness_function(data, chromosome, start, end) for chromosome in population]
            
            # we choose parents with good values
            parents = [chromosome for chromosome , fitness_score in zip(population, fitness_scores) if fitness_score <= min(fitness_scores) + 2]

            # new population is currently empty
            new_population = []

            # placing good fitness coordinates in new population and creating offsprints from parents
            while len(new_population) < population_size:
                
                fit_p1, fit_p2 = random.choice(parents), random.choice(parents)
                
                # genetic operator(crossover to produce new offspring)
                random_cut_for_crossover = random.randint(1, len(fit_p1) - 1)
                
                # offspring created from parted data using crossover cut
                offspring = [fit_p1[i] if i < random_cut_for_crossover else fit_p2[i] for i in range(len(fit_p1))]
                
                # mutation for normalization reasons
                for i in range(len(offspring)):
                    
                    if random.random() < rate_for_mutating:
                        
                        offspring[i] = random.sample([(x, y) for x in range(data['grid_width']) for y in range(data['grid_height']) if (x, y) not in data['obstacles']], 1)[0]
                        
                new_population.append(offspring)

            population = new_population

        # choosing best possible coordinates
        current_best_path = min(population, key=lambda x: fitness_function(data, x, start, end))
        
        current_best_path_cost = fitness_function(data , current_best_path, start, end)

        # updating best solution each time if needed
        if current_best_path_cost < best_path_cost:
            
            best_path = current_best_path
            best_path_cost = current_best_path_cost
            
    final_path = [start]

    # connecting the minimized coordinates given by genetic algorithm using a star so that obstacles are catered and minimal cost is obtained
    final_path += a_star_algo(data, start, best_path[0])
    
    for i in range(len(best_path) - 1):
        
        final_path += a_star_algo(data, best_path[i], best_path[i + 1])

    final_path += a_star_algo(data, best_path[len(best_path) - 1], end)

    final_path = remove_duplicates(final_path)

    print("The best path is: ")
    print(final_path)

    window = tk.Tk()
    window.title("Genetic algorithm Path optimization!")

    canvas = tk.Canvas(window, width=700, height=800)
    canvas.pack()

    cell_width = 50
    cell_height = 50
    
    cell_colors = {
        "empty": "black",
        "obstacle": "red",
        "path": "green"
    }

    def draw_grid():
        
        for i in range(data['grid_width']):
            for j in range(data['grid_height']):
                
                x1, y1 = i * cell_width, j * cell_height
                x2, y2 = x1 + cell_width, y1 + cell_height
                cell_type = "empty"
                if (i, j) in data['obstacles']:
                    cell_type = "obstacle"
                if (i, j) in final_path:
                    cell_type = "path"

                canvas.create_rectangle(x1, y1, x2, y2, fill=cell_colors[cell_type], outline="white")

                label_x = (x1 + x2) / 2
                label_y = (y1 + y2) / 2
                canvas.create_text(label_x, label_y, text=f"({i}, {j})", fill="white")

    draw_grid()

    path_coords = "Path travelled: " + " -> ".join([f'({x},{y})' for (x, y) in final_path])
    total_cost = f'Total cost: {len(final_path) - 1}'

    canvas.create_text(350, 650, text=path_coords, font=("Helvetica", 9),  fill="black")
    canvas.create_text(350, 670, text=total_cost, font=("Helvetica", 12, "bold"),  fill="black")

    window.mainloop()

if __name__ == "__main__":
    main()
