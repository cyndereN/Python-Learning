class Solution(object):
    # check boundries of board
    def validate(self, i, j, board):
        r = len(board)
        c = len(board[0])
        if i >= 0 and i < r and j >= 0 and j < c:
            return True
        return False
    
    # go through all 8 neighbour cells of board
    # and count number of live(1) neighbour cells
    def countLives(self, i, j, board):
        noOfLives = 0
        # right, left, bottom, up, up-left, down-right, up-right, down-left 
        directions = [(i, j+1), (i, j-1), (i+1, j), (i-1, j), (i-1, j-1), (i+1, j+1), (i-1, j+1), (i+1, j-1)]
        # check each direction
        for d in directions:
            r, c = d[0], d[1]
            # if it is in boundry, increment count of live neighbours
            if self.validate(r, c, board):
                if board[r][c] == 1:
                    noOfLives += 1
        return noOfLives
                
            
    def gameOfLife(self, board):
        """
        :type board: List[List[int]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        # if board is empty return none
        if not board:
            return None
        # track the positions and cell value to be update on the baisis of rules
        # key = cell position to be update, value = value to be updated
        trackmap = {}
        # traverse through entire board
        for i in range(len(board)):
            for j in range(len(board[0])):
                # count number of live neighbours
                noOfLives = self.countLives(i, j, board)
                # if current cell is live
                if board[i][j] == 1:
                    # rule 1 and 3
                    if noOfLives < 2 or noOfLives > 3:
                        # update value to be updated at current position
                        trackmap[(i, j)] = 0
                    # for rule 2, cell value remains same
                # if current cell is dead
                else:
                    # rule 4
                    if noOfLives == 3:
                        # update value to be updated at current position
                        trackmap[(i, j)] = 1
        # for every cell to be updated
        for k in trackmap.keys():
            board[k[0]][k[1]] = trackmap[k]
        return board
                    