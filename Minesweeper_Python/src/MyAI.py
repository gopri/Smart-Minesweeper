# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action

import operator
import collections

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDim = rowDimension
		self.colDim = colDimension
		self.totMines = totalMines
		self.sX = startX
		self.sY = startY
		self.boardState = {"uncovered": [(self.sX,self.sY)], "covered": []}
		#{(x,y):[1,[(x1,y1),(x2,y2)]]} -> number for that tile and its covered adjacent tiles
		#self.tileState = {}	#for tiles having number other than 0, and its adjacent tiles
		self.lastTile = (self.sX, self.sY)
		self.lastAction = 0
		self.safeTiles = set()
		self.mineTiles = set()
		self.tilesProb = collections.defaultdict(int)
		self.grid = [(['c']* self.colDim) for i in range(self.rowDim)]	#'u'->uncovered, 'c'->covered, 'f'->flag, else number
		self.adjTiles = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

		#filling up "covered" list with all the tiles except the start tile
		for i in range(self.rowDim):
			for j in range(self.colDim):
				if i!=self.sX or j!=self.sY:
					self.boardState["covered"].append((i,j))
					
		
		#print("sx ",self.sX, "sy ", self.sY)
		if self.grid:
			#print(self.grid)
			#print("rowdim ", self.rowDim, "col ", self.colDim)
			
			self.grid[self.colDim-1-self.sY][self.sX] = 0
			#print(self.grid)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def addToSafeTiles(self, curTile):
		#print("@in addsafe")
		lastx = curTile[0]
		lasty = curTile[1]

		for i,j in self.adjTiles:
			x = lastx + i
			y = lasty + j

			if x>=0 and x<self.rowDim and y>=0 and y<self.colDim and (x,y) not in self.boardState["uncovered"]:
				self.safeTiles.add((x,y))

	def addToMineTiles(self, curTile):
		#print("@in addmines")
		lastx = curTile[0]
		lasty = curTile[1]

		for i,j in self.adjTiles:
			x = lastx + i
			y = lasty + j

			if x>=0 and x<self.rowDim and y>=0 and y<self.colDim and (x,y) not in self.boardState["uncovered"]:
				self.mineTiles.add((x,y))
		
	def checkSurroundings(self, curTile):
		#print("@in checksur")
		number = self.grid[self.colDim-1-curTile[1]][curTile[0]]

		#if hint is 0, add its adjacent tiles in safe set if its covered
		if number not in ('f', 'c', '0'):
			#self.tileState[self.lastTile] = [number, []]

			flagNo = 0
			tilesCov = 0
			lastx = curTile[0]
			lasty = curTile[1]

			for i,j in self.adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.rowDim and y>=0 and y<self.colDim:
					if self.grid[self.colDim-1-y][x] == 'f':
						flagNo+=1
					elif self.grid[self.colDim-1-y][x] == 'c':
						tilesCov+=1
						self.tilesProb[(x,y)] += 1

			if flagNo == int(number):
				self.addToSafeTiles(curTile)
			elif tilesCov == int(number)-flagNo:
				self.addToMineTiles(curTile)


	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		'''
		print("####")
		print("-grid  ", self.grid)
		print("-boardS  ", self.boardState)
		print("-prob   ", self.tilesProb)
		print("-safeTil  ", self.safeTiles)
		print(" - mines   ", self.mineTiles)
		print("- lasttile ", self.lastTile)
		print("####")'''
		if number>=0:
			self.grid[self.colDim-1-self.lastTile[1]][self.lastTile[0]] = str(number)
		else:
			self.grid[self.colDim-1-self.lastTile[1]][self.lastTile[0]] = 'f'

		#If its solved, Leave
		if not self.boardState["covered"]:
			return Action(AI.Action.LEAVE)

		#if hint is 0, add its adjacent tiles in safe set if its covered
		if not number:
			#print("!!not number")
			self.addToSafeTiles(self.lastTile)

		#If number greater than 0, put in tileState with its number and adjacent covered tiles
		#else it will be Flag or unflag action, and do nothing
		elif number > 0:
			#print("!!number>0")
			#self.tileState[self.lastTile] = [number, []]

			flagNo = 0
			tilesCov = 0
			lastx = self.lastTile[0]
			lasty = self.lastTile[1]

			for i,j in self.adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.rowDim and y>=0 and y<self.colDim:
					if self.grid[self.colDim-1-y][x] == 'f':
						flagNo+=1
					elif self.grid[self.colDim-1-y][x] == 'c':
						tilesCov+=1
						self.tilesProb[(x,y)] += 1

			if flagNo == number:
				self.addToSafeTiles(self.lastTile)
			elif tilesCov == number-flagNo:
				self.addToMineTiles(self.lastTile)
		
		else:
			#print("!!number =-1")
			lastx = self.lastTile[0]
			lasty = self.lastTile[1]

			for i,j in self.adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.rowDim and y>=0 and y<self.colDim and (x,y) in self.boardState["uncovered"]:
					self.checkSurroundings((x,y))

		#If all mines flagged - Uncover all covered tiles
		if not self.totMines:
			#print("!!mines 0")
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			#self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			self.lastAction = 'u'
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#If covered tiles equal to mines, flag them all
		elif self.totMines == len(self.boardState["covered"]):
			#print("!!mies=cov")
			self.totMines -= 1
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			#self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			self.lastAction = 'f'
			return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

		#else, uncover one of safetiles and proceed
		elif self.safeTiles:
			#print("!!safe tile")
			nextTile = self.safeTiles.pop()
			self.boardState["uncovered"].append(nextTile)
			self.boardState["covered"].remove(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			#self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			self.lastAction = 'u'
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		elif self.mineTiles:
			#print("!!mine tile")
			self.totMines -= 1
			nextTile = self.mineTiles.pop()
			self.boardState["uncovered"].append(nextTile)
			self.boardState["covered"].remove(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			#self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			self.lastAction = 'f'
			return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

		#If no safetile left, flag tiles which has hint number equal to adj covered tiles - as only 1 mine it will work
		else:
			#print("!!else")
			
			nextTile = max(self.tilesProb.items(), key=operator.itemgetter(1))[0]
			if nextTile:
				self.totMines -= 1
				self.boardState["uncovered"].append(nextTile)
				self.boardState["covered"].remove(nextTile)
				if nextTile in self.tilesProb: del self.tilesProb[nextTile]
				self.safeTiles.discard(nextTile)
				self.mineTiles.discard(nextTile)
				#self.posFlagToSafe(nextTile)
				self.lastTile = nextTile
				self.lastAction = 'f'
				return Action(AI.Action.FLAG, nextTile[0], nextTile[1])
			
			#print("!!random")
			#If didnot get anything from above, uncover random tile
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			self.lastTile = nextTile
			self.lastAction = 'u'
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################