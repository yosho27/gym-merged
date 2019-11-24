import gym
from gym import error, spaces, utils
from gym.utils import seeding
from merged import MergedGame

class MergedEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        reset()
    
    def step(self, action):
        prevScore = x.score
        x.updateBoard(x.currentTile,action)
        return [(x.board,x.currentTile), x.score - prevScore, x.gameOver, {}]

    def reset(self):
        self.x = MergedGame()
        return (x.board,x.currentTile)

    def render(self, mode='human'):
        x.render()

    def close(self):
        pass
