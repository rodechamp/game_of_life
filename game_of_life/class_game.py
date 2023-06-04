import numpy as np
from PIL import Image
import os

from .class_progressbar import ProgressBar

import matplotlib.pyplot as plt

class Game():
    def __init__(self,
            startingGrid:"np.ndarray|None"=None,
            length:"int"=30,
            height:"int"=20,
            ) -> None:
        """Initilizie game of life with empty starting grid or grid of spezified size.
        """

        self.grid:"np.ndarray"
        
        self.height:"int"
        self.width:"int"

        self.timesteps:"int" = 0
        self.n_cells_over_time:"list[int]" = []

        self.seed:"int|None" = None


        # using specified grid
        if startingGrid is not None:
            self.grid = startingGrid
            self.height, self.length = startingGrid.shape
        # initielize empty grid
        else:
            self.height = height
            self.length = length
            self.grid = np.zeros((self.height, self.length), dtype=int)



    ###########################################
    # properties
    ###########################################

    @property
    def n_alive_cells(self) -> int:
        """Number of cells in system"""
        return np.sum(self.grid)


    ###########################################
    # grid initializing
    ###########################################

    def set_seed(self, seed:"int") -> None:
        """Sets the seed for all random operations
        """
        self.seed = seed
        np.random.seed(seed)
        return None


    def randomize_grid(self, p_live:"float"=0.1) -> None:
        """Fills grid with random values, with the chance of a live cell being p_live
        """
        for ii in range(self.height):
            for jj in range(self.length):
                randomNumber = np.random.random()

                if randomNumber < p_live:
                    cell = 1
                else:
                    cell = 0

                self.grid[ii,jj] = cell
        
        return None


    def add_noise_to_grid(self, p_noise:"float"=0.001, p_live:"float"=0.5) -> None:
        """Each point on the grid has a percentage to be turned alive
        """

        cell_isAlive:"int"

        for ii in range(self.height):
            for jj in range(self.length):
                randomNumber_noise = np.random.random()
                if randomNumber_noise < p_noise:
                    randomNumber_live = np.random.random()
                    if randomNumber_live < p_live:
                        cell_isAlive = 1
                    else:
                        cell_isAlive = 0
                    self.grid[ii,jj] = cell_isAlive
            
        return None



    def initialize_with_image(self, fname:"str") -> None:
        """Initialize grid with an image
        """

        # load grayscale image
        img = Image.open(fname).convert('L')
        img.load()

        # convert it to numpy array, factors are so that 0 -> dead, 1 -> alive
        self.grid = (np.asarray(img, dtype=int) // 255) * (-1) + 1
        self.height, self.length = self.grid.shape
        
        return None
    


    ###########################################
    # timestepping
    ###########################################


    def check_cell_aliveNextGen(self, ii:"int", jj:"int", rules:"str"='basic') -> int:
        """checks at a gridpoint of cell is alive or dead at next generation.
        
        Implemented are the following rules:
        1. If a live cell has less than two neighbors, it dies.
        2. If a live cell has two or three neighbors, it lives to the next generation.
        3. If a live cell has more than three neighbors, it dies.
        4. If a dead cell has exactly three live neighbors, it lives.
        """
        cell_willBeAlive:"int"

        cell_isAlive:"int" = self.grid[ii, jj]

        if rules == 'basic':
            cell_neighbors:"int" = self.count_neighbors(ii, jj, usediagonals=False)
        elif rules == 'experimental':
            cell_neighbors:"int" = self.count_neighbors(ii, jj, usediagonals=True)
        else:
            raise ValueError('rules {0} not known'.format(rules))

        # other rules are for allive cells
        if cell_isAlive:
            # rule 1: solemnity
            if cell_neighbors < 2:
                cell_willBeAlive = 0
            # rule 2: nothing
            elif cell_neighbors < 4:
                cell_willBeAlive = 1
            # rule 3: overpopulation
            else:
                if rules == 'experimental': # cell dies with certain percentage
                    randomNumber = np.random.random()
                    if randomNumber < 0.95:
                        cell_willBeAlive = 0
                    else:
                        cell_willBeAlive = 1
                else:
                    cell_willBeAlive = 0
        # rule no 4 for dead cells
        else:
            if cell_neighbors == 3:
                cell_willBeAlive = 1
            else:
                cell_willBeAlive = 0
            
            if rules == 'experimental':
                if cell_neighbors == 4:
                    cell_willBeAlive = 1


        return cell_willBeAlive



    def count_neighbors(self, ii:"int", jj:"int", usediagonals:"bool"=False) -> int:
        """Counts the neighbors of gridposition at (ii,jj)
        """

        n_neighbors:"int" = 0

        # check position on grid
        awayFrom_upperBorder = ii > 0
        awayFrom_lowerBorder = ii < self.height-1
        awayFrom_leftBorder = jj > 0
        awayFrom_rightBorder = jj < self.length - 1


        # upper neighbor
        if awayFrom_upperBorder:
            n_neighbors += self.grid[ii-1,jj]
        
        # lower neighbor
        if awayFrom_lowerBorder:
            n_neighbors += self.grid[ii+1,jj]
        
        # left neighbor
        if awayFrom_leftBorder:
            n_neighbors += self.grid[ii, jj-1]
        
        # right neighbor
        if awayFrom_rightBorder:
            n_neighbors += self.grid[ii, jj+1]
        

        if usediagonals:
            # also count neighbors on diagonals

            # upper left
            if awayFrom_upperBorder and awayFrom_leftBorder:
                n_neighbors += self.grid[ii-1,jj-1]
            
            # upper right
            if awayFrom_upperBorder and awayFrom_rightBorder:
                n_neighbors += self.grid[ii-1, jj+1]
            
            # lower right
            if awayFrom_lowerBorder and awayFrom_rightBorder:
                n_neighbors += self.grid[ii+1, jj+1]
            
            # lower left
            if awayFrom_lowerBorder and awayFrom_leftBorder:
                n_neighbors += self.grid[ii+1, jj-1]



        return n_neighbors
    


    def timestep_grid(self, rules:"str"='basic') -> None:
        """Performs a timestep for the grid, where it is checked if a cell lives for each cell.
        """

        grid_new:"np.ndarray" = np.zeros((self.height, self.length), dtype='int')

        for ii in range(self.height):
            for jj in range(self.length):
                grid_new[ii, jj] = self.check_cell_aliveNextGen(ii, jj, rules=rules)
        
        self.grid = grid_new

        self.timesteps += 1
        self.save_cellcount()

        return None



    def save_cellcount(self) -> None:
        """Saves how many cells are alive in system.
        """
        self.n_cells_over_time.append(self.n_alive_cells)



    def timestepping(self, n_timesteps:"int", rules:"str"='basic', printing:"bool"=False) -> None:
        """Timesteps grid multiple times for convenience.

        Args:
            n_timesteps (int): Number of timesteps.
            rules (str, optional): Used rules. Defaults to 'basic'.
            printing (bool, optional): Turns on printing each timestep to console. Defaults to False.

        Returns:
            None
        """

        pb = ProgressBar(total=n_timesteps)
        pb.print(iteration=0)

        for ii in range(n_timesteps):
            self.timestep_grid(rules=rules)
            pb.print(iteration=ii+1)

        return None

    ###########################################
    # printing / plotting
    ###########################################

    def print_to_console(self, show_timestep=True) -> None:
        """Print cells to console.
        """
        if show_timestep: print('timestep {0}'.format(self.timesteps))

        for line in self.grid:
            for cell in line:
                # print('{0}'.format(cell), end=' ')
                if cell:
                    # print(1, end=' ')
                    print(u'\u25A9', end=' ')
                else:
                    # print(0, end=' ')
                    print(u'\u25A1', end=' ')
            print('')
        
        return None
    


    def plot_image(self, savedir:"str"='timesteps') -> None:
        """Plots a png image of grid.
        """

        os.makedirs(savedir, exist_ok=True)
        fileName = '{0}/timestep_{1:06d}.png'.format(savedir, self.timesteps)


        fig, ax = plt.subplots()

        ax.imshow(self.grid, cmap='binary')

        ax.set_axis_off()
        fig.savefig(fileName, bbox_inches='tight', dpi=50)
        plt.close(fig)

        return None

