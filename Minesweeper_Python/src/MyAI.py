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
		self.tileState = {}	#for tiles having number other than 0, and its adjacent tiles
		self.lastTile = (self.sX, self.sY)
		self.safeTiles = set()

		#filling up "covered" list with all the tiles except the start tile
		for i in range(self.rowDim):
			for j in range(self.colDim):
				if i!=self.sX or j!=self.sY:
					self.boardState["covered"].append((i,j))

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# to remove tiles which gets uncovered
	def posFlagToSafe(self, curTile):
		for i in self.tileState:
			for j in self.tileState[i][1]:
				if j==curTile:
					self.tileState[i][1].remove(curTile)
		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		adjTiles = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

		#If its solved, Leave
		if not self.boardState["covered"]:
			return Action(AI.Action.LEAVE)

		#if hint is 0, add its adjacent tiles in safe set if its covered
		if not number:
			lastx = self.lastTile[0]
			lasty = self.lastTile[1]

			for i,j in adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.rowDim and y>=0 and y<self.colDim and (x,y) not in self.boardState["uncovered"]:
					self.safeTiles.add((x,y))

		#If number greater than 0, put in tileState with its number and adjacent covered tiles
		#else it will be Flag or unflag action, and do nothing
		elif number > 0:
			self.tileState[self.lastTile] = [number, []]

			lastx = self.lastTile[0]
			lasty = self.lastTile[1]

			for i,j in adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.rowDim and y>=0 and y<self.colDim and (x,y) not in self.boardState["uncovered"]:
					self.tileState[self.lastTile][1].append((x,y))

		#If all mines flagged - Uncover all covered tiles
		if not self.totMines:
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#If covered tiles equal to mines, flag them all
		elif self.totMines == len(self.boardState["covered"]):
			self.totMines -= 1
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

		#else, uncover one of safetiles and proceed
		elif len(self.safeTiles)>0:
			nextTile = self.safeTiles.pop()
			self.boardState["uncovered"].append(nextTile)
			self.boardState["covered"].remove(nextTile)
			self.posFlagToSafe(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#If no safetile left, flag tiles which has hint number equal to adj covered tiles - as only 1 mine it will work
		else:
			for i in self.tileState:
				if self.tileState[i][0] == len(self.tileState[i][1]):
					self.totMines -= 1
					nextTile = self.tileState[i][1].pop(0)
					self.boardState["uncovered"].append(nextTile)
					self.boardState["covered"].remove(nextTile)
					self.lastTile = nextTile
					return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

			#If didnot get anything from above, uncover random tile
			nextTile = self.boardState["covered"].pop(0)
			self.boardState["uncovered"].append(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
