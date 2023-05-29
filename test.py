"""Small rudimentary script to test out functionalities
"""

import numpy as np
import os

import matplotlib.pyplot as plt

from game_of_life import Game

def main():

    np.random.seed(1)


    gol = Game(length=10,height=5)
    
    # initialize
    gol.randomize_grid(0.5)
    print( gol.count_neighbors(1,1,usediagonals=False) )
    print( gol.count_neighbors(1,1,usediagonals=True) )
    gol.print_to_console()

    n_timesteps = 2

    for tt in range(n_timesteps):
        gol.timestep_grid(rules='experimental')

        gol.print_to_console()

        # print( gol.count_neighbors(1,1,usediagonals=False) )
        # print( gol.count_neighbors(1,1,usediagonals=True) )
    

    return






if __name__ == '__main__':
    main()