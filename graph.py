import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from colorama import Fore


class Graph:
    """Represents a Graph.

    Constructs a undirected graph in adjacency matrix representation based
    on an input file. The undirected graph has nodes and edges like any graph,
    but it also has special nodes and can have colored edges, which get a
    value of 2 in the adjacency matrix.
    """

    def __init__(self, file: str) -> None:
        """Initializes a Graph object.

        Args:
            file (str): Path of input file.
        """
        self.num_nodes = 0
        self.spec_nodes = []
        edges = []

        # Get info from file and convert to proper format
        with open(file, "r") as f:
            lines = f.read().split("\n")

        found_edges = False
        for lnum, line in enumerate(lines):
            if line == "":
                continue
            if line[0] == "N":
                self.num_nodes = int(lines[lnum + 1])
            if line[0] == "S":
                self.spec_nodes = [int(s) for s in lines[lnum + 1].split(" ")]
            # Use a boolean to indicate where the edge lines in the file start
            if line[0] == "E":
                found_edges = True
                continue
            if found_edges:
                edge = tuple([int(e) for e in line.split(",")])
                edges.append(edge)

        # Construct adjacency matrix based on edges found in input file
        self.adj_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        for n1, n2 in edges:
            self.adj_matrix[n1, n2] = 1
            self.adj_matrix[n2, n1] = 1

        np.set_printoptions(formatter={"int": self.color_value})  # type: ignore

    def color_value(self, x: int) -> str:
        """Return string colored version of input based on value.

        Args:
            x (int): The number given.

        Returns:
            str: The string with optional color from colorama.
        """
        if x == 2:
            return f"{Fore.RED}{x}{Fore.RESET}"
        if x == 1:
            return f"{Fore.BLUE}{x}{Fore.RESET}"
        return f"{x}"

    def color_edge(self, n1: int, n2: int):
        """Color an edge between node n1 and node n2.

        Args:
            n1 (int): The first node of the edge.
            n2 (int): The second node of the edge.
        """
        self.adj_matrix[n1, n2] = 2
        self.adj_matrix[n2, n1] = 2

    def delete_edge(self, n1: int, n2: int):
        """Delete an edge between node n1 and node n2.

        Args:
            n1 (int): The first node of the edge.
            n2 (int): The second node of the edge.
        """
        self.adj_matrix[n1, n2] = 0
        self.adj_matrix[n2, n1] = 0

    def show(self):
        """Print the graph representation."""
        print(self.adj_matrix)


class VisGraph(Graph):
    """Represents a Graph with networkx visualizations."""

    def __init__(self, file: str) -> None:
        """Initializes a Graph object with plot visualizations.

        Args:
            file (str): Path of input file.
        """
        super().__init__(file)
        self.nxgraph = nx.Graph()
        # Add edges to graph
        normal_edges = np.argwhere(self.adj_matrix == 1).tolist()
        colored_edges = np.argwhere(self.adj_matrix == 2).tolist()
        self.nxgraph.add_edges_from(normal_edges)
        self.nxgraph.add_edges_from(colored_edges)
        # Get position once
        self.pos = nx.spring_layout(self.nxgraph)

    def show(self) -> None:
        """Create and plot the networkx visualization."""
        # Add edges to graph
        normal_edges = np.argwhere(self.adj_matrix == 1).tolist()
        colored_edges = np.argwhere(self.adj_matrix == 2).tolist()
        self.nxgraph.add_edges_from(normal_edges)
        self.nxgraph.add_edges_from(colored_edges)

        color_map = ["lightblue" for _ in range(self.num_nodes)]
        for node in self.spec_nodes:
            color_map[node] = "green"
        nx.draw_networkx_nodes(self.nxgraph, self.pos, node_color=color_map)
        nx.draw_networkx_labels(self.nxgraph, self.pos)
        nx.draw_networkx_edges(self.nxgraph, self.pos, edgelist=normal_edges)
        nx.draw_networkx_edges(
            self.nxgraph,
            self.pos,
            edgelist=colored_edges,
            edge_color="red",
        )
        plt.show()
