# BlockWorldSolver

## Overview

This Python program solves the Block World Problem using the A* algorithm. The Block World Problem is a classic problem in artificial intelligence and robotics where the goal is to rearrange a set of blocks from an initial configuration to a target configuration, adhering to certain rules.

## Features

- **A* Algorithm:** The program employs the A* algorithm, a popular pathfinding and graph traversal algorithm, to efficiently find the optimal solution to the Block World Problem.

- **Heuristic Function:** The A* algorithm uses a heuristic function to guide the search for the optimal solution.

## How to run

- The program provide three different predicates: clear, on, and on_table. Clear is a list of characters represent the blocks that are clear on its top, on is a list of strings represent the blocks that stay on another block, on_table is a list of characters represent the blocks that are on table.
- For example:
- ![image](https://github.com/minhalo113/BlockWorldSolver/assets/115437688/8756ccb1-3c2b-4d86-b701-a41da7ccadc4)
  
- To represent the current state, we will set clear, on and on_table as follow: clear = ["e"]; on_table = ["a"]; on = ["da", "cd","bc", "eb"]
- To represent the goal state, we will set clear, on and on_table as follow: clear = ["a"]; on_table = ["e"]; on = ["ab", "bc", "cd", "de"]
- Return solution: ['move e from block b to table', 'move b from block c to table', 'move block c to block b', 'move block d to block e', 'move block c to block d', 'move b from table to block c', 'move a from table to block b']
