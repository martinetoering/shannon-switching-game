from typing import Callable, Optional, Union

import numpy as np
from colorama import Style
from graph import Graph, VisGraph


class Game:
    """Representation of the Shannon switching game.

    Implements the Shannon Switching Game, a two-player game between players
    named CUT and SHORT on a graph with special nodes. CUT needs to separate
    the special nodes and can delete an edge each turn, while SHORT can color
    an edge each turn and wants to make a colored path between the special
    nodes.

    """

    def __init__(self, file: str, player: str, plot: Optional[bool] = False) -> None:
        """Initializes Shannon switching game.

        Args:
            file (str): Input file with board state.
            player (str): Name of player which has first turn.
            plot (bool, optional): Whether to plot instead of print. Defaults to False.
        """
        if plot:
            self.graph: Union[Graph, VisGraph] = VisGraph(file)
        else:
            self.graph = Graph(file)

        self.turn = player.lower()
        print("Welcome to Shannon switching game!")

    def check_path_bfs(
        self,
        n1: int,
        n2: int,
        condition: Callable[[int], bool],
    ) -> bool:
        """Performs breadth-first search to check condition in graph.

        Args:
            n1 (int): The first node.
            n2 (int): The second node.
            condition (Callable[[int], bool]): The condition to check.

        Returns:
            bool: Indicates whether there is a path.
        """
        path_found = False

        visited_nodes = [False for _ in range(self.graph.num_nodes)]
        queue = []
        queue.append(n1)
        visited_nodes[n1] = True

        # Breadth-first search to determine whether there is a path
        while queue:
            n = queue.pop(0)

            for i, _ in enumerate(self.graph.adj_matrix[n]):
                adj_n = self.graph.adj_matrix[n, i]
                if not condition(adj_n):
                    continue
                if visited_nodes[i]:
                    continue
                queue.append(i)
                visited_nodes[i] = True
                if i == n2:
                    path_found = True
        return path_found

    def check_player_win(
        self,
        condition: Callable[[int], bool],
        truth_value: bool,
    ) -> bool:
        """Checks winning state for a player.

        Args:
            condition (Callable[[int], bool]): Condition corresponding to player.
            truth_value (bool): The truth value of the condition for the winning state.

        Returns:
            bool: Winning state for player corresponding to condition and truth_value.
        """
        player_win = False
        n1, n2 = self.graph.spec_nodes
        if self.check_path_bfs(n1, n2, condition) is truth_value:
            player_win = True
        return player_win

    def run_game(self) -> None:
        """Runs the Shannon switching game."""
        print("Initial state:")
        self.graph.show()

        for i in range(100):
            if self.check_player_win(condition=lambda x: x == 2, truth_value=True):
                print("Short won!")
                break
            if self.check_player_win(condition=lambda x: x != 0, truth_value=False):
                print("Cut won!")
                break

            if (i % 2) == 0:
                print(f"\n{Style.BRIGHT}Round {(i//2)+1}!{Style.RESET_ALL}")

            # Choose a random edge
            edge_choices = np.argwhere(self.graph.adj_matrix == 1)
            random_index = np.random.randint(edge_choices.shape[0])
            (n1, n2) = edge_choices[random_index]

            if self.turn == "short":
                print(f"Short colors {n1, n2}")
                self.graph.color_edge(n1, n2)
                self.turn = "cut"

            elif self.turn == "cut":
                print(f"Cut deletes {n1, n2}")
                self.graph.delete_edge(n1, n2)
                self.turn = "short"

            if i % 2 != 0:
                self.graph.show()
