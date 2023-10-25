# path-finding-ai
A semester assignment that focuses on utilizing various path finding algorithms such as A Star and then comparing the results with evolutionary searches such as Genetic Algorithms. The second part of this assignment explores different tools for routing purposes.

# A Star algorithm
We first begin by importing essential libraries: heapq for efficient priority queue operations, math for mathematical calculations, and tkinter for creating a graphical user interface (GUI).

### Heuristic Function (h_of_n_calculator)
The h_of_n_calculator function calculates the heuristic (estimated cost) using the Euclidean distance between two points. It's an important part of the A* algorithm.

### Checking Moves (is_move_acceptable)
This function checks whether a potential move is valid. It ensures the move is within the grid boundaries and does not collide with obstacles.

### Tracking the Path (track_path)
This function helps in tracking and reconstructing the path from the destination back to the starting point based on the previously stored 'previous' nodes.

### A Algorithm (a_star_algo)
The A* (A-star) algorithm implemented in this code is a highly efficient pathfinding method widely used for finding the shortest route from a starting point to a destination on a grid. This algorithm takes into account obstacles and grid boundaries and operates by maintaining a priority queue, the open_list, which determines the order in which nodes (representing grid positions) are explored. Each node is assigned two critical values which is the the g_score, which signifies the cost of reaching that node from the starting point, and the f_score, which is the sum of the g_score and a heuristic estimate, h_score. We base the heuristic on Euclidean Distance. 

We explore the closest nodes, selecting the one with the lowest f_score from the open_list. For each node explored, the algorithm evaluates its neighbors, checking if moving to a neighbor results in a shorter path. If a shorter path is found, the g_score and f_score for the neighbor node are updated. This optimization process continues until the destination node is reached or if no other possible move exists.

### Drawing the Grid (draw_grid)
This function is responsible for the whole GUI process.

### Thoughts
After seeing the results, the A* algorithm is an optimal approach for finding the shortest path in various applications. It consistently provides the shortest cost path due to its ability to consider both the distance from the start (the g_score) and the estimated distance to the end (the heuristic h_score), shown by the optimal f_score. 

### Example

Moving from (1,2) to (7,8) with a few obstacles in between, let's see how A star works out:
![a_star](https://github.com/dark-coder12/path-finding-ai/assets/82564549/6d215fba-9288-444e-9add-6167c9530888)
