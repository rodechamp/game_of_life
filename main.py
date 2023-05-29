import numpy as np
import os

import matplotlib.pyplot as plt

from game_of_life import Game

def main():

    game_list:"list[Game]" = []
    name_list:"list[str]" = ['svea', 'birgit', 'tom']

    np.random.seed(112314)

    plot_images:"bool" = True

    for name in name_list:
        print(name)
        imageDir = 'output/{0}'.format(name)

        gol = Game()
        
        # initialize
        image_name = 'input_images/name_{0}_small.png'.format(name)
        gol.initialize_with_image(image_name)
        # gol.add_noise_to_grid(0.1, 1.0)
        gol.save_cellcount()

        if plot_images: gol.plot_image(imageDir)

        n_timesteps = 200

        for tt in range(n_timesteps):
            print('\ttimestep {0}'.format(tt))
            gol.timestep_grid(rules='experimental')
            
            if plot_images: gol.plot_image(imageDir)
    
        game_list.append(gol)


    # plot cell counts
    fig, ax = plt.subplots(figsize=(3,3))

    for gol, name, ls in zip(game_list, name_list, ['-', '--', '-.']):
        ax.semilogy(gol.n_cells_over_time, label=name, ls=ls)

    ax.legend(title='name')

    ax.set_xlabel('timesteps')
    ax.set_ylabel('cells alive')

    fig.savefig('cellcount.png', dpi=300, bbox_inches='tight')
    plt.close(fig)



if __name__ == '__main__':
    main()