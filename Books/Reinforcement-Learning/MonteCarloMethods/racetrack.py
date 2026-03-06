import gymnasium as gym
import skimage.draw
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

class RacetrackEnv(gym.Env):
    """ Racetrack environment
        This custom environment is taken from: https://github.com/vojtamolda/reinforcement-learning-an-introduction/blob/main/chapter05/racetrack.py
    """

    def __init__(self, racetrack_txt, noisy=True):
        self.racetrack = np.genfromtxt(racetrack_txt, dtype=int)

        self.ax = None

    def render(self, mode='human', reset=None):
        if self.ax is None:
            fig = plt.figure()
            self.ax = fig.gca()

        # Racetrack background
        cmap = mcolors.ListedColormap(['white', 'gray', 'red', 'green'])
        self.ax.imshow(self.racetrack, aspect='equal', origin='lower', cmap=cmap)
