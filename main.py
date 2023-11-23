import argparse

from game import Game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input file which described the graph",
    )
    parser.add_argument(
        "--player",
        type=str,
        choices=["short", "cut"],
        required=True,
        help="Choose which player to go first, cut or short",
    )
    args = parser.parse_args()

    game = Game(args.input, args.player)
    game.run_game()
