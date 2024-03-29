import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

class MergedEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    observation_space = spaces.Box(low=0,high=8,shape=(6,5))

    def __init__(self):
        self.reset()
        self.action_space = spaces.Discrete(len(self.x.possibleMoves))
    
    def step(self, action):
        prevScore = self.x.score
        self.x.updateBoard(self.x.currentTile,self.x.possibleMoves[action])
        return [self.getObservation(), self.x.score - prevScore, self.x.gameOver, {}]

    def reset(self):
        self.x = MergedGame()
        return self.getObservation()

    def getObservation(self):
        top = np.concatenate([np.array(self.x.currentTile),np.zeros(3)]).reshape((1,5))
        return np.concatenate([top,np.array(self.x.board)])
        #return (np.array(self.x.currentTile),np.array(self.x.board))

    def render(self, mode='human'):
        self.x.render()

    def close(self):
        pass


from random import choice

class MergedGame():
    orients = [(0,1),(1,0),(0,-1),(-1,0)]
    locations = [(r,c) for c in range(5) for r in range(5)]

    def __init__(self):
        self.board = [[0 for c in range(5)] for r in range(5)]
        self.maxTile = 2
        self.score = 0
        self.gameOver = False
        self.possibleMoves = []
        for k in range(25):
            for j in range(4):
                move = (self.locations[k],self.plus(self.locations[k],self.orients[j]))
                if 0<=move[1][0]<5 and 0<=move[1][1]<5:
                    self.possibleMoves.append(move)
        self.makeTiles()
        self.currentTile = choice(self.tiles)

    def makeTiles(self):
        self.tiles = [(a,b) for a in range(1,self.maxTile+1) for b in range(1,self.maxTile+1) if a<b]

    def plus(self,t1,t2):
        return (t1[0]+t2[0],t1[1]+t2[1])

    def updateBoard(self,tile,move):
        if self.board[move[0][0]][move[0][1]]!=0 or self.board[move[1][0]][move[1][1]]!=0:
            self.score = -100
            return
        self.board[move[0][0]][move[0][1]] = tile[0]
        self.board[move[1][0]][move[1][1]] = tile[1]
        self.merge(move[0])
        self.merge(move[1])
        self.endGame()
        self.currentTile = choice(self.tiles)

    def endGame(self):
        if self.gameOver:
            return
        hasMove = False
        for move in self.possibleMoves:
            if self.board[move[0][0]][move[0][1]]==0 and self.board[move[1][0]][move[1][1]]==0:
                hasMove = True
        if not hasMove:
            self.score -= 100
            self.gameOver = True

    def merge(self,loc):
        self.mergeTiles = []
        self.findSquares(loc)
        if len(self.mergeTiles)>=3:
            val = self.board[loc[0]][loc[1]]
            for square in self.mergeTiles:
                self.board[square[0]][square[1]] = 0
            self.board[loc[0]][loc[1]] = val+1
            self.score += len(self.mergeTiles)*val*val
            if val == 7:
                self.score += 200
                self.gameOver = True
                return
            if val+1>self.maxTile:
                self.maxTile = val+1
                self.makeTiles()
            self.merge(loc)

    def findSquares(self,loc):
        self.mergeTiles.append(loc)
        for orient in self.orients:
            tile = self.plus(loc,orient)
            if not tile in self.mergeTiles and 0<=tile[0]<5 and 0<=tile[1]<5 and self.board[loc[0]][loc[1]]==self.board[tile[0]][tile[1]]:
                self.findSquares(tile)

    def render(self):
        print('-'*7 + '\n' + '\n'.join(['|'+''.join([str(c) for c in row]) + '|' for row in self.board]) + '\n' + '-'*7)
