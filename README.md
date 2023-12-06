# Visualizer-of-A*-for-large-graphs
Repository for a simple visualizer of the A* algorithm used on graphs, user input of the start and end nodes is required. The output visualization is the shortest path between the nodes and their neighbors. The latest update has a function to save the shortest path as GIF. <br>

The Simple GUI contains: <br>
- Load file button
- Start and End nodes textbox
- Scroll Textbox - with a little hint for names of nodes
- Info Textbox - Time performance for each action
- Seed - textbox where you can input seed for the [NetworkX Spring Layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html)
- Iterations - iterations of spring_layout
- Draw Graph button
  
## Example on the Karate Club
![Initial karate club](https://github.com/lowoncuties/Visualizer-of-A-for-large-graphs/assets/16253955/dd808cf6-2977-47d3-9b2e-7f52642b79cd)

The DPI and Figsize needs to be changed accordingly to the size of a graph<be>

**More fine-tuned visualization with 100 iterations**
![100iter_karate](https://github.com/lowoncuties/Visualizer-of-A-for-large-graphs/assets/16253955/17242297-e99d-4fb6-90a5-20a18fd7569b)


## Example on the [Belgium-OSM network](https://networkrepository.com/road-belgium-osm.php)
Pretty large network with 1.4M nodes and 1.5M edges. <br>

Settings as seen in image: Starting node - 1 => End node - 41, Seed - 1, Iteration - 200

![Belgium_osm_final](https://github.com/lowoncuties/Visualizer-of-A-for-large-graphs/assets/16253955/d873f3e4-7143-4cc4-aec8-9909707ca2d4)

**GIF created from the nodes 1 => 40 (seed - 1, iterations 500)**
![1_40_500iter](https://github.com/lowoncuties/Visualizer-of-Astar-for-large-graphs/assets/16253955/c30f399f-8a09-4fdd-8fee-c9c717c12c37)


## Some Benchmarks (non-parallel on Ryzen 7 5700X, 16GB ram, 1000 runs) 
| Algorithm             | Nodes | Time (seconds) |
|-----------------------|-------|----------------|
| My A*                 |  1 => 41     |      0.83 sec         |
| NX Djikstra (default) |  1 => 41     |      0.22 sec          |
| My A*                 |  1 => 120000     |      97.83 sec         |
| NX Djikstra (default) |  1 => 120000     |      0.16sec          |

For some reason the NX A* was not working for me. As seen in the table above, I'd highly recommend using the NX functions since they're far more optimized.

## Technologies used:
- Python
- Tkinter + Matplotlib
- NetworkX




