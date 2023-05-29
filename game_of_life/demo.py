"""This module contains functions to demonstrate the usage
of the Game class
"""

from .class_game import Game

import matplotlib.pyplot as plt
import numpy as np


def randomize_grid(n_timesteps:"int"=5, rules:"str"='basic') -> None:
    """Uses a randomized grid with either basic (nearest neighbor detection) or
    experimental (second-nearest neighbor detection) rules. Prints timesteps to
    console.

    Args:
        n_timesteps (int): number of timesteps. Defaults to 5.
        rules (str): neighbor detection rules. Defaults to 'basic'.
    """
    
    # setup game
    game = Game(length=10, height=10)
    
    # initialize game
    game.randomize_grid(0.5)
    game.print_to_console()
    
    # timestepping
    for _ in range(n_timesteps):
        game.timestep_grid(rules=rules)
        game.print_to_console()
    
    # finished
    print('All done!')
    return None
        


def compare_rules(n_timesteps:"int"=100, length:"int"=50, height:"int"=30, p_live:"float"=0.5) -> None:
    """Compares survivability of cells depending on the ruleset. Plots a graph of the results

    Args:
        n_timesteps (int, optional): Used timesteps. Defaults to 100.
        length (int, optional): Grid size in x. Defaults to 50.
        height (int, optional): Grid size in y. Defaults to 30.
        p_live (float, optional): Grid size in y. Defaults to 0.5.
    Returns:
        None
    """
    # setting up
    ruleset_list:"list[str]" = ['basic', 'experimental']
    alive_cells_list:"list[np.ndarray[float]]" = []
    
    
    for rules in ruleset_list:
        # initialize
        game = Game(length=length, height=height)
        game.randomize_grid(p_live=p_live)
        
        game.timestepping(n_timesteps=n_timesteps, rules=rules)
        
        # save results
        cellsAlive_percentage = np.array(game.n_cells_over_time) / game.n_cells_over_time[0]
        alive_cells_list.append(cellsAlive_percentage)
    
    
    # plotting
    fig, ax = plt.subplots()
    
    ls_list = ['-', '--']
    for ylist, rules, ls in zip(alive_cells_list, ruleset_list, ls_list):
        ax.plot(ylist, label=rules, ls=ls)
    
    ax.legend(title='rules')
    
    ax.set_xlabel('timesteps')
    ax.set_ylabel('surviving cells')
    
    ax.set_xlim(0,n_timesteps)
    
    fig.savefig('rule_comparison.png', dpi=200, bbox_inches='tight')
    
    return None