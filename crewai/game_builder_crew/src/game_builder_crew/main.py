#!/usr/bin/env python
import sys
import warnings

import yaml

from game_builder_crew.crew import GameBuilderCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    print("## Welcome to the Game Crew")
    print("-------------------------------")

    with open(
        "src/game_builder_crew/config/gamedesign.yaml", "r", encoding="utf-8"
    ) as file:
        examples = yaml.safe_load(file)

    inputs = {"game": examples["example3_snake"]}
    game = GameBuilderCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("final code for the game:")
    print(game)


def train():
    """
    Train the crew for a given number of iterations.
    """

    with open(
        "src/game_builder_crew/config/gamedesign.yaml", "r", encoding="utf-8"
    ) as file:
        examples = yaml.safe_load(file)

    inputs = {"game": examples["example1_pacman"]}
    try:
        GameBuilderCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
