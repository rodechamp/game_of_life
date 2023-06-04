"""Is run when the package is invoced with
python -m game_of_life
"""

from .class_game import Game
from .demo import compare_rules




print('DEMONSTRATING CONWAYS GAME OF LIFE')


# saving images in ...
saveDirectory:"str" = 'readme_example'
print('- results will be saved in {0}'.format(saveDirectory))


print('- initializing game')
game = Game(length=20, height=20)


# make results reproducible
seed:"int" = 12345
game.set_seed(seed)
print('- seed is set to {0}'.format(seed))


# random starting conditions
print('- randomizing the grid')
p_live = 0.33
print('\t-> a cell lives with {0:.0f} percent chance'.format(p_live*100.))
game.randomize_grid(p_live)


# plotting starting data
print('- saving initial conditions')
game.plot_image(saveDirectory)


print('- performing a timestep')
game.timestep_grid()
print('- saving results')
game.plot_image(saveDirectory)


print('- performing a timestep (again)')
game.timestep_grid()
print('- saving results (again)')
game.plot_image(saveDirectory)



# compare rulesets
print('- comparing normal and experimental rules')
compare_rules(
    n_timesteps=100, 
    length=100, 
    height=100, 
    p_live=0.2, 
    saveDir=saveDirectory
    )