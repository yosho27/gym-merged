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
            self.score = -1000000
            gameOver = True
            return
        self.board[move[0][0]][move[0][1]] = tile[0]
        self.board[move[1][0]][move[1][1]] = tile[1]
        self.merge(move[0])
        self.merge(move[1])
        endGame()
        self.currentTile = choice(self.tiles)

    def endGame(self):
        if gameOver:
            return
        hasMove = False
        for move in possibleMoves:
            if self.board[move[0][0]][move[0][1]]==0 and self.board[move[1][0]][move[1][1]]==0:
                hasMove = True
        if not hasMove:
            self.score -= 100
            gameOver = True

    def merge(self,loc):
        self.mergeTiles = []
        self.findSquares(loc)
        if len(self.mergeTiles)>=3:
            val = self.board[loc[0]][loc[1]]
            for square in self.mergeTiles:
                self.board[square[0]][square[1]] = 0
            self.board[loc[0]][loc[1]] = val+1
            self.score += len(self.mergeTiles)*val
            if val == 7:
                self.score += 100
                gameOver = True
                return
            if val+1>maxTile:
                maxTile = val+1
                makeTiles()
            merge(loc)

    def findSquares(self,loc):
        self.mergeTiles.append(loc)
        for orient in self.orients:
            tile = self.plus(loc,orient)            
            if (not tile in self.mergeTiles) and 0<=tile[0]<5 and 0<=tile[1]<5:
                if self.board[loc[0]][loc[1]]==self.board[tile[0]][tile[1]]:
                    self.findSquares(tile)

    def render(self):
        print('-'*7 + '\n' + '\n'.join(['|'+''.join([str(c) for c in row]) + '|' for row in self.board]) + '\n' + '-'*7)
