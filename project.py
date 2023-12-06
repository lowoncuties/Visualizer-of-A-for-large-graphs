import tkinter as tk
from tkinter import filedialog, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import re
import math
import time
import matplotlib.animation as animation

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualization App")
        self.master.geometry("1920x1080")

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.master, text="Load File", command=self.load_file)
        self.load_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.start_node_label = tk.Label(self.master, text="Starting Node:")
        self.start_node_label.grid(row=1, column=0, sticky="w", padx=10)
        self.start_node_entry = tk.Entry(self.master)
        self.start_node_entry.grid(row=1, column=1, padx=10)

        self.end_node_label = tk.Label(self.master, text="Ending Node:")
        self.end_node_label.grid(row=2, column=0, sticky="w", padx=10)
        self.end_node_entry = tk.Entry(self.master)
        self.end_node_entry.grid(row=2, column=1, padx=10)

        self.node_names_text = scrolledtext.ScrolledText(self.master, height=10, width=30)
        self.node_names_text.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="w")

        self.time_text = scrolledtext.ScrolledText(self.master, height=5, width=30)
        self.time_text.grid(row=3, column=2, columnspan=2, pady=10, sticky="w")

        self.seed_label = tk.Label(self.master, text="Seed:")
        self.seed_label.grid(row=4, column=0, sticky="w", padx=10)
        self.seed_entry = tk.Entry(self.master)
        self.seed_entry.grid(row=4, column=1, padx=10)

        self.iterations_label = tk.Label(self.master, text="Iterations:")
        self.iterations_label.grid(row=5, column=0, sticky="w", padx=10)
        self.iterations_entry = tk.Entry(self.master)
        self.iterations_entry.grid(row=5, column=1, padx=10)

        self.draw_button = tk.Button(self.master, text="Draw Graph", command=self.draw_graph)
        self.draw_button.grid(row=6, column=0, columnspan=1, pady=10)

        self.fig, self.ax = plt.subplots(1,figsize=(60,30),dpi=20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=7, column=5, columnspan=3, pady=10, sticky="nsew")

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky="nsew")

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_file(self):
        start_time = time.time()
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.graph = self.create_graph_from_file(file_path)
            self.update_node_names()
            self.draw_graph()

        end_time = time.time()
        load_time = end_time - start_time
        self.time_text.insert(tk.END, f"Graph Loading Time: {load_time:.4f} seconds\n")

    def create_graph_from_file(self, file_path):
        G = nx.Graph()

        with open(file_path, 'r') as file:
            for line in file:
                nodes = [int(node) for node in re.split(r'[ ;]', line.strip()) if node]
                if len(nodes) == 2:
                    G.add_edge(nodes[0], nodes[1])

        return G

    def update_node_names(self):
        if hasattr(self, 'graph'):
            node_names = "\n".join(map(str, self.graph.nodes()))
            self.node_names_text.delete(1.0, tk.END)
            self.node_names_text.insert(tk.END, node_names)

    def draw_graph(self):
        if hasattr(self, 'graph'):
            start_node = int(self.start_node_entry.get())
            end_node = int(self.end_node_entry.get())

            seed = int(self.seed_entry.get()) if self.seed_entry.get() else 5
            iterations = int(self.iterations_entry.get()) if self.iterations_entry.get() else 0

            # A* algorithm
            start_time = time.time()
            shortest_path = self.a_star(start_node, end_node)
            end_time = time.time()

            # NetworkX A*
            #start_time = time.time()
            #shortest_path = nx.shortest_path(self.graph, source=start_node, target=end_node)
            #end_time = time.time()
            
            self.fig = plt.figure(1, figsize=(200, 80), dpi=60)

            subgraph_nodes = set()
            for node in shortest_path:
                subgraph_nodes.add(node)
                subgraph_nodes.update(self.graph.neighbors(node))

            subgraph = self.graph.subgraph(subgraph_nodes)

            prep_start_time = time.time()
            pos = nx.spring_layout(subgraph, seed=seed, k=5/math.sqrt(subgraph.order()), iterations=iterations)
            prep_end_time = time.time()
            self.ax.clear()
            self.ax.set_title("Subgraph with Shortest Path and Neighbors")
            self.ax.set_aspect('equal')

            nx.draw_networkx(subgraph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black", ax=self.ax)

            path_edges = list(zip(shortest_path, shortest_path[1:]))
            nx.draw_networkx_nodes(subgraph, pos, nodelist=shortest_path, node_color="orange", node_size=700, ax=self.ax)
            nx.draw_networkx_edges(subgraph, pos, edgelist=path_edges, edge_color="red", width=2, ax=self.ax)

            nx.draw_networkx_nodes(subgraph, pos, nodelist=[start_node], node_color="green", node_size=1000, ax=self.ax)
            nx.draw_networkx_nodes(subgraph, pos, nodelist=[end_node], node_color="red", node_size=1000, ax=self.ax)


            calculation_time = end_time - start_time
            preprocessing_time = prep_end_time - prep_start_time
            self.time_text.insert(tk.END, f"A* for {start_node} -> {end_node} took: {calculation_time:.8f} seconds \n Visual preprocessing: {preprocessing_time} seconds\n Shortest path lenght: {len(shortest_path)} \n" )


            self.canvas.draw()

            
            def update(frame):
                current_node = shortest_path[min(frame, len(shortest_path) - 1)]
                nx.draw_networkx_nodes(subgraph, pos, nodelist=[current_node], node_color="blue", node_size=700, ax=self.ax)


            ani_start_time = time.time()
            ani = animation.FuncAnimation(self.fig, update, frames=len(shortest_path), interval=10, repeat=False)
            ani.save("shortest_path_animation.gif", writer="imagemagick")
            ani_end_time = time.time()

            animation_time = ani_end_time - ani_start_time
            self.time_text.insert(tk.END, f"Animation save time: {animation_time} \n" )


            

    def a_star(self, start_node, end_node):
        heuristic = self.euclidean_distance  
        open_set = {start_node}
        closed_set = set()
        g_score = {node: float('inf') for node in self.graph.nodes()}
        g_score[start_node] = 0
        f_score = {node: float('inf') for node in self.graph.nodes()}
        f_score[start_node] = heuristic(start_node, end_node)

        while open_set:
            current = min(open_set, key=lambda node: f_score[node])

            if current == end_node:
                path = [current]
                while current != start_node:
                    current = min(self.graph.neighbors(current), key=lambda node: g_score[node])
                    path.insert(0, current)
                return path

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.graph.neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node)

                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return []

    def euclidean_distance(self, node, goal):
         return abs(node - goal)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
