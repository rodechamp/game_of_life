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
        


def compare_rules(
        n_timesteps:"int"=100, 
        length:"int"=50, 
        height:"int"=30, 
        p_live:"float"=0.5,
        saveDir:"str"='.'
        ) -> None:
    """Compares survivability of cells depending on the ruleset. Plots a graph of the results

    Args:
        n_timesteps (int, optional): Used timesteps. Defaults to 100.
        length (int, optional): Grid size in x. Defaults to 50.
        height (int, optional): Grid size in y. Defaults to 30.
        p_live (float, optional): Grid size in y. Defaults to 0.5.
        saveDir (str, optional): Folder, where results grafic is saved to. Defaults to '.'
    Returns:
        None
    """
    # setting up
    ruleset_list:"list[str]" = ['basic', 'experimental']
    alive_cells_list:"list[np.ndarray[float]]" = []
    
    
    for rules in ruleset_list:
        print('timestepping rules: {0}'.format(rules))
        # initialize
        game = Game(length=length, height=height)
        game.randomize_grid(p_live=p_live)
        
        game.timestepping(n_timesteps=n_timesteps, rules=rules)
        
        # save results
        cellsAlive_percentage = np.array(game.n_cells_over_time) / game.n_cells_over_time[0]
        alive_cells_list.append(cellsAlive_percentage)
    
    
    # plotting
    fig, ax = plt.subplots(
        figsize=(3,2.5)
    )
    
    ls_list = ['-', '--']
    for ylist, rules, ls in zip(alive_cells_list, ruleset_list, ls_list):
        ax.plot(ylist, label=rules, ls=ls)
    
    ax.legend(title='rules')
    
    ax.set_xlabel('timesteps')
    ax.set_ylabel('surviving cells')
    
    ax.set_xlim(0,n_timesteps)
    
    saveName = '{0}/rule_comparison.png'.format(saveDir)
    fig.savefig(saveName, dpi=100, bbox_inches='tight')
    
    return None




def main() -> None:
    print('DEMONSTRATING CONWAYS GAME OF LIFE')

    # make results reproducible
    randomSeed:"int" = 12345
    np.random.seed(randomSeed)
    print('- random seed is {0}'.format(randomSeed))


    # saving images in ...
    saveDirectory:"str" = 'readme_example'

    print('- results will be saved in {0}'.format(saveDirectory))



    print('- initializing game')
    game = Game(length=20, height=20)
    game.randomize_grid()

    game.plot_image(saveDirectory)
    
    return None


if __name__ == '__main__':
    main()