# -*- coding: utf-8 -*-

#### Auteurs ###
# Dkhissi Youness
# Do Nicolas

''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

from itertools import count
import time
import Goban 
from random import choice
from playerInterface import *
import math
import json

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.turn_count = 0
        self.start_search = 0
        self.moves_history = []#the list of moves played so far
        # we have stored the openings lists from games.json
        with open('games.json') as mon_fichier:
            data = json.load(mon_fichier)
        # black_openings contains the list of pro games gained by the black player
        self.black_openings = []
        # white_openings contains the list of pro games gained by the white player
        self.white_openings =  []
        for opening in data:
            if opening['winner'] == 'W':
                self.white_openings.append(opening["moves"])
            elif opening['winner'] == 'B':
                self.black_openings.append(opening["moves"])

    def getPlayerName(self):
        return "Average Player EUW"

    def getPlayerMove(self):        
        start = time.time()

        # Extend depth for MiniMax and alpha-beta depending on empties 
        if len(self._board._empties) <= 7:
            depth = 3
        elif len(self._board._empties) <= 15:
            depth = 2
        else:
            depth = 1

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 

        if self._mycolor == Goban.Board._BLACK:
            if (self.black_openings != []): #Use pro openings
                move = Goban.Board.name_to_flat(self.play_openings())
            else:
                #Find best moves with MiniMax search
                #move = self.best_moves_MinMax(self._board, True, depth)

                #Find best moves with Alpha-beta search
                #move = self.best_moves(self._board, True, depth, False) 

                #Find best move with iterative Deepening
                move = self.IterativeDeepening(self._board, True)
                move = choice(move)
           
        else: 
            if (self.white_openings != []): #Use pro openings
                move = Goban.Board.name_to_flat(self.play_openings())
            else:
                #Find best moves with MiniMax search
                #move = self.best_moves_MinMax(self._board, False, depth)

                #Find best moves with Alpha-beta search
                #move = self.best_moves(self._board, False, 2, False)

                #Find best moves with iterative Deepening
                move = self.IterativeDeepening(self._board, False)
                move = choice(move)    


        self.turn_count +=1
        self._board.push(move)
        self.moves_history.append(Goban.Board.flat_to_name(move))
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        n = len(self.moves_history)
        if self._mycolor == Goban.Board._BLACK:
            for opening in self.black_openings:
                if len(opening)<=n or opening[n] != move:
                    self.black_openings.remove(opening)
        else:
            for opening in self.white_openings:
                if len(opening)<=n or opening[n] != move:
                    self.white_openings.remove(opening)

        # print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 
        self.moves_history.append(move)

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    #Get move from pro openings
    def play_openings(self):
        n = len(self.moves_history)
        if self._mycolor == Goban.Board._BLACK:
            opening_played = choice(self.black_openings)
            move = opening_played[n]
            while (self.black_openings != []):
                if Goban.Board.name_to_flat(move) not in self._board._empties:
                    self.black_openings.remove(opening_played)
                    if self.black_openings != []:
                        opening_played = choice(self.black_openings)
                        move = opening_played[n]
                else:
                    break
            if self.black_openings == []:
                return Goban.Board.flat_to_name(choice(self.IterativeDeepening(self._board, True)))
            for opening in self.black_openings:
                if len(opening)<=n:
                    continue
                if opening[n] != move:
                    self.black_openings.remove(opening)
        else :
            opening_played = choice(self.white_openings)
            move = opening_played[n]
            while (self.white_openings != []):
                if Goban.Board.name_to_flat(move) not in self._board._empties:
                    self.white_openings.remove(opening_played)
                    if self.white_openings != []:
                        opening_played = choice(self.white_openings)
                        move = opening_played[n]
                else:
                    break

            if self.white_openings == []:
                return Goban.Board.flat_to_name(choice(self.IterativeDeepening(self._board, False)))

            for opening in self.white_openings:
                if len(opening)<=n:
                    continue
                if opening[n] != move:
                    self.white_openings.remove(opening)
        return move


    # Return best score for MinMax search
    def MinMax(self, b,isMinimizing,depth):
        if b.is_game_over():
            res = b.result()
            if isMinimizing == False:
                return -1000 if res == "1-0" else 1000 if res == "0-1" else 0
            else:
                return 1000 if res == "1-0" else -1000 if res == "0-1" else 0
        if depth == 0:
            return self.go_evaluation(b)
        if isMinimizing==False:
            bestScore=-math.inf
            moves = b.generate_legal_moves()
            for move in moves:
                b.push(move)
                Score=self.MinMax(b,False,depth-1)
                bestScore=max(Score,bestScore)
                b.pop()
        else:
            bestScore=math.inf
            moves = b.generate_legal_moves()
            for move in moves:
                b.push(move)
                Score=self.MinMax(b,True,depth-1)
                bestScore = min(Score,bestScore)
                b.pop()
        return bestScore

    # Return best moves for MinMax search
    def best_moves_MinMax(self, b,isMinimizing,depth):
        moves=b.generate_legal_moves()
        if isMinimizing:
            bestScore=math.inf
        else:
            bestScore=-math.inf
        bestMoves=[]
        for move in moves:
            b.push(move)
            score=self.MinMax(b,isMinimizing,depth)
            if score == bestScore:
                bestMoves.append(move)
            if isMinimizing:
                if score<bestScore:
                    bestMoves = []
                    bestScore=score
                    bestMoves.append(move)
            else:
                if score>bestScore:
                    bestMoves = []
                    bestScore=score
                    bestMoves.append(move)
            b.pop()
        return bestMoves

    # Return best score for alpha beta search
    def alpha_beta(self,b,isMinimizing,depth,alpha,beta,IterDeep=False):
        if b.is_game_over():
            res = b.result()
            return math.inf if res == "1-0" else -math.inf if res == "0-1" else 0
        if depth == 0:
            return self.go_evaluation(b)
        if isMinimizing==True:
            Score=math.inf
            moves = b.generate_legal_moves()
            for move in moves:
                if (IterDeep==True and time.time() - self.start_search > 15):
                    break
                b.push(move)
                Score=min(Score,self.alpha_beta(b,False,depth-1,alpha,beta))
                b.pop()
                beta=min(beta,Score)
                if(alpha>=beta):
                    break
        else:
            Score=-math.inf
            moves = b.generate_legal_moves()
            for move in moves:
                if (IterDeep==True and time.time() - self.start_search > 15):
                    break
                b.push(move)
                Score=max(Score,self.alpha_beta(b,True,depth-1,alpha,beta))
                b.pop()
                alpha=max(alpha,Score)
                if(beta<=alpha):
                    break
        return Score

    # Return best score and best moves for alpha beta search
    def best_moves(self, b, isMinimizing, depth, IterDeep=False):
        moves=b.weak_legal_moves()
        if isMinimizing:
            bestScore=math.inf
        else:
            bestScore=-math.inf
        bestMoves=[]
        for move in moves:
            b.push(move)
            score=self.alpha_beta(b,isMinimizing,depth,-math.inf,math.inf, IterDeep)
            if score == bestScore:
                bestMoves.append(move)
            elif isMinimizing:
                if score<bestScore:
                    bestMoves = []
                    bestScore=score
                    bestMoves.append(move)
            else:
                if score>bestScore:
                    bestMoves = []
                    bestScore=score
                    bestMoves.append(move)
            b.pop()
        return bestScore, bestMoves


    # functions to count connected stones
    def count_connected_stones(self, b, color):
        connected_stones = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if b._board[Goban.Board.flatten((i, j))] == color:
                    connected_stones += self.count_connected_stones_rec(b._board, i, j, color)
        return connected_stones
        
    def count_connected_stones_rec(self, b, i, j, color):
        if i < 0 or i > 8 or j < 0 or j > 8:
            return 0
        if b[Goban.Board.flatten((i, j))] != color:
            return 0
        board = b.copy()
        board[Goban.Board.flatten((i, j))] = 0
        connected_stones = 1
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            connected_stones += self.count_connected_stones_rec(board, i + direction[0], j + direction[1], color)
        return connected_stones
        
    #Heuristic value
    def go_evaluation(self,b):
        score = -b.diff_stones_board()+3*b.diff_stones_captured()
        #score += 2*(self.count_connected_stones(b, b._WHITE) - self.count_connected_stones(b, b._BLACK))
        areas = b._count_areas()
        score += 6*(areas[1]-areas[0])
        return score


    # Iterative deepening
    def IterativeDeepening(self,b,isMinimizing):        
        self.start_search = time.time()
        depth = 1
        moves = []
        while (time.time() - self.start_search < 15):
            moves.append(self.best_moves(b,isMinimizing,depth, True))
            depth +=1

        #Get best moves found within 15 seconds
        bestMoves = []
        print("#################### depth:",depth)
        if isMinimizing==False:
            bestScore=-math.inf
            for move in moves:
                if move[0] > bestScore:
                    bestScore = move[0]
                    bestMoves = move[1]
            return bestMoves
        else:
            bestScore=math.inf
            for move in moves:
                if move[0] < bestScore:
                    bestScore = move[0]
                    bestMoves = move[1]
            return bestMoves
       
