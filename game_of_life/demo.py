"""This module contains functions to demonstrate the usage
of the Game class
"""

from .class_game import Game

def randomize_grid(n_timesteps:"int"=5, rules:"str"='basic') -> None:
    """Uses a randomized grid with either basic (nearest neighbor detection) or
    experimental (second-nearest neighbor detection) rules. Prints timesteps to
    console.

    Args:
        n_timesteps (int): number of timesteps. (defaults to 5)
        rules (str): neighbor detection rules. (defaults to 'basic')
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
        
    