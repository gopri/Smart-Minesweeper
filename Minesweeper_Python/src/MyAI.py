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
import random
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
		self.boardState = {"uncovered": {(self.sX,self.sY)}, "covered": set()}
		self.lastTile = (self.sX, self.sY)
		self.safeTiles = set()
		self.mineTiles = set()
		self.tilesProb = collections.defaultdict(int)
		self.grid = [(['c']* self.colDim) for i in range(self.rowDim)]	#'u'->uncovered, 'c'->covered, 'f'->flag, else number
		self.adjTiles = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

		#filling up "covered" list with all the tiles except the start tile
		#here matrix is according to colDim*rowDim
		#accordingly, have to retrieve item from grid, as grid and minesweeper matrix treat (3,4) as different
		for i in range(self.colDim):
			for j in range(self.rowDim):
				if i!=self.sX or j!=self.sY:
					self.boardState["covered"].add((i,j))
					

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	#to add adjTiles of given tile in safe list (for instances, when curtile is 0)
	def addToSafeTiles(self, curTile):
		lastx = curTile[0]
		lasty = curTile[1]

		for i,j in self.adjTiles:
			x = lastx + i
			y = lasty + j

			if x>=0 and x<self.colDim and y>=0 and y<self.rowDim and (x,y) not in self.boardState["uncovered"]:
				self.safeTiles.add((x,y))

	#to add covered adjTiles in mines list (for instances when number of tile is equal to number of cov tiles - flags in adj tiles)
	def addToMineTiles(self, curTile):
		lastx = curTile[0]
		lasty = curTile[1]

		for i,j in self.adjTiles:
			x = lastx + i
			y = lasty + j

			if x>=0 and x<self.colDim and y>=0 and y<self.rowDim and (x,y) not in self.boardState["uncovered"]:
				self.mineTiles.add((x,y))
		
	#after taking some action, check its neighbours, if some adjTiles of curTile can go to safe or mine list, if its uncovered and has some number>0
	def checkSurroundings(self, curTile):

		#check curtile number
		number = self.grid[self.rowDim-1-curTile[1]][curTile[0]]

		if number not in ('f', 'c', '0'):

			flagNo = 0
			tilesCov = 0
			lastx = curTile[0]
			lasty = curTile[1]

			for i,j in self.adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.colDim and y>=0 and y<self.rowDim:
					if self.grid[self.rowDim-1-y][x] == 'f':
						flagNo+=1
					elif self.grid[self.rowDim-1-y][x] == 'c':
						tilesCov+=1
						#self.tilesProb[(x,y)] += 1

			#flag marked to curtile = number of curtile, then all covered tiles are safe
			if flagNo == int(number):
				self.addToSafeTiles(curTile)
			#if total number of covered tiles = (number - flags already marked), then all coveredare mines
			elif tilesCov == int(number)-flagNo:
				self.addToMineTiles(curTile)

		#if for covered tiles, there are 3 adjacent flas, prob is more of being safe?
		'''if number == 'c':
			adjTilesCount = [(1,0),(1,-1),(0,-1)]
			flagCount = 0
			lastx = curTile[0]
			lasty = curTile[1]
			for i,j in adjTilesCount:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.colDim and y>=0 and y<self.rowDim:
					
					if self.grid[self.rowDim-1-y][x] == 'f':
						flagCount+=1
			
			if flagCount==3:
				self.safeTiles.add(curTile))'''

	#Function to check 1-2 Patterns in horizontal alignment
	def check12PatternH(self,x1,y,y1,y2):

		adjTilesCount = 0
		uncovAndUnflag = 0
		tileToFlag = None

		if x1>=0 and x1<self.colDim and y1>=0 and y1<self.rowDim:
			adjTilesCount += 1
			if (x1,y1) in self.boardState['uncovered'] and self.grid[self.rowDim-y1-1][x1]!='f':
				uncovAndUnflag += 1
			elif (x1,y1) in self.boardState['covered']:
				tileToFlag = (x1,y1)
				
		if x1>=0 and x1<self.colDim and y>=0 and y<self.rowDim:
			adjTilesCount += 1
			if (x1,y) in self.boardState['uncovered'] and self.grid[self.rowDim-y-1][x1]!='f':
				uncovAndUnflag += 1
			elif (x1,y) in self.boardState['covered']:
				tileToFlag = (x1,y)

		if x1>=0 and x1<self.colDim and y2>=0 and y2<self.rowDim:
			adjTilesCount += 1
			if (x1,y2) in self.boardState['uncovered'] and self.grid[self.rowDim-y2-1][x1]!='f':
				uncovAndUnflag += 1
			elif (x1,y2) in self.boardState['covered']:
				tileToFlag = (x1,y2)

		if adjTilesCount - uncovAndUnflag == 1 and tileToFlag!= None:
			self.mineTiles.add(tileToFlag)

	#Function to check 1-2 Patterns in vertical alignment
	def check12PatternV(self,y1,x,x1,x2):

		adjTilesCount = 0
		uncovAndUnflag = 0
		tileToFlag = None

		if x1>=0 and x1<self.colDim and y1>=0 and y1<self.rowDim:
			adjTilesCount += 1
			if (x1,y1) in self.boardState['uncovered'] and self.grid[self.rowDim-y1-1][x1]!='f':
				uncovAndUnflag += 1
			elif (x1,y1) in self.boardState['covered']:
				tileToFlag = (x1,y1)
				
		if x>=0 and x<self.colDim and y1>=0 and y1<self.rowDim:
			adjTilesCount += 1
			if (x,y1) in self.boardState['uncovered'] and self.grid[self.rowDim-y1-1][x]!='f':
				uncovAndUnflag += 1
			elif (x,y1) in self.boardState['covered']:
				tileToFlag = (x,y1)

		if x2>=0 and x2<self.colDim and y1>=0 and y1<self.rowDim:
			adjTilesCount += 1
			if (x2,y1) in self.boardState['uncovered'] and self.grid[self.rowDim-y1-1][x2]!='f':
				uncovAndUnflag += 1
			elif (x2,y1) in self.boardState['covered']:
				tileToFlag = (x2,y1)

		if adjTilesCount - uncovAndUnflag == 1 and tileToFlag!= None:
			self.mineTiles.add(tileToFlag)
		
	#Function to check 1-1 Patterns in horizontal alignment
	def check11PatternH(self, x1, y1, y, y2):

		if y1>=0 and y1<self.rowDim and (x1,y1) in self.boardState['covered']:
			self.safeTiles.add((x1,y1))
		if y>=0 and y<self.rowDim and (x1,y) in self.boardState['covered']:
			self.safeTiles.add((x1,y))
		if y2>=0 and y2<self.rowDim and (x1,y2) in self.boardState['covered']:
			self.safeTiles.add((x1,y2))
		
	#Function to check 1-1 Patterns in vertical alignment
	def check11PatternV(self, x1, x, x2, y1):

		if x1>=0 and x1<self.colDim and (x1,y1) in self.boardState['covered']:
			self.safeTiles.add((x1,y1))
		if x>=0 and x<self.colDim and (x,y1) in self.boardState['covered']:
			self.safeTiles.add((x,y1))
		if x2>=0 and x2<self.colDim and (x2,y1) in self.boardState['covered']:
			self.safeTiles.add((x2,y1))

	#Function to check patterns for uncovered tiles, uses above helper functions
	def checkPatterns(self):
		uncovTiles = self.boardState["uncovered"]

		for m,n in uncovTiles:

			#all 1-2 patterns
			#1-2 patterns horizontally
			x = m+1
			y = n
			if self.grid[self.rowDim-n-1][m] == '1' and x>=0 and x<self.colDim and self.grid[self.rowDim-y-1][x] == '2':
				x1 = x+1
				y1 = y+1
				y2 = y-1
				
				self.check12PatternH(x1,y,y1,y2)

			#2-1 patterns horizontally
			x = m-1
			y = n
			if self.grid[self.rowDim-n-1][m] == '1' and x>=0 and x<self.colDim and self.grid[self.rowDim-y-1][x] == '2':
				x1 = x-1
				y1 = y+1
				y2 = y-1
				
				self.check12PatternH(x1,y,y1,y2)

			#1, then below 2 (1-2) patterns vertically
			x = m
			y = n-1
			if self.grid[self.rowDim-n-1][m] == '1' and y>=0 and y<self.rowDim and self.grid[self.rowDim-y-1][x] == '2':
				y1 = y-1
				x1 = x+1
				x2 = x-1
				
				self.check12PatternV(y1,x,x1,x2)

			#2, then below 1 (2-1) patterns vertically
			x = m
			y = n+1
			if self.grid[self.rowDim-n-1][m] == '1' and y>=0 and y<self.rowDim and self.grid[self.rowDim-y-1][x] == '2':
				y1 = y+1
				x1 = x+1
				x2 = x-1
				
				self.check12PatternV(y1,x,x1,x2)

			#all 1-1 pattern at edges
			#1-1 pattern horizontally at left side of matrix
			x = m+1
			y = n
			if m==0 and self.grid[self.rowDim-n-1][m] == '1' and x>=0 and x<self.colDim and self.grid[self.rowDim-y-1][x] == '1':
				x1 = x+1
				y1 = y+1
				y2 = y-1
				if x1>=0 and x1<self.colDim:
					self.check11PatternH(x1,y1,y,y2)

			#1-1 pattern horizontally at right side of matrix
			x = m-1
			y = n
			if m==self.colDim-1 and self.grid[self.rowDim-n-1][m] == '1' and x>=0 and x<self.colDim and self.grid[self.rowDim-y-1][x] == '1':
				x1 = x-1
				y1 = y+1
				y2 = y-1
				if x1>=0 and x1<self.colDim:
					self.check11PatternH(x1,y1,y,y2)

			#1-1 pattern vertically at bottom of matrix
			x = m
			y = n+1
			if n==0 and self.grid[self.rowDim-n-1][m] == '1' and y>=0 and y<self.rowDim and self.grid[self.rowDim-y-1][x] == '1':
				x1 = x+1
				x2 = x-1
				y1 = y+1
				if y1>=0 and y1<self.rowDim:
					self.check11PatternV(x1,x,x2,y1)
			
			#1-1 pattern vertically at top of matrix
			x = m
			y = n-1
			if n==self.rowDim-1 and self.grid[self.rowDim-n-1][m] == '1' and y>=0 and y<self.rowDim and self.grid[self.rowDim-y-1][x] == '1':
				x1 = x+1
				x2 = x-1
				y1 = y-1
				if y1>=0 and y1<self.rowDim:
					self.check11PatternV(x1,x,x2,y1)


	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		'''
		print("####")
		print("-grid  ", self.grid)
		print("-boardState  ", self.boardState)
		print("-prob   ", self.tilesProb)
		print("-safeTiles  ", self.safeTiles)
		print("-mineTiles   ", self.mineTiles)
		print("-lastTile ", self.lastTile)
		print("####")
		'''

		#setting grid values according to last action
		if number>=0:
			self.grid[self.rowDim-1-self.lastTile[1]][self.lastTile[0]] = str(number)
		else:
			self.grid[self.rowDim-1-self.lastTile[1]][self.lastTile[0]] = 'f'

		#If its solved, Leave
		if not self.boardState["covered"]:
			return Action(AI.Action.LEAVE)

		#if hint is 0, add its adjacent tiles in safe set if its covered
		if not number:
			self.addToSafeTiles(self.lastTile)

		#If number greater than 0, put in tileState with its number and adjacent covered tiles
		#else it will be Flag or unflag action, and do nothing
		elif number > 0:

			flagNo = 0
			tilesCov = 0
			lastx = self.lastTile[0]
			lasty = self.lastTile[1]

			for i,j in self.adjTiles:
				x = lastx + i
				y = lasty + j

				if x>=0 and x<self.colDim and y>=0 and y<self.rowDim:
					if self.grid[self.rowDim-1-y][x] == 'f':
						flagNo+=1
					elif self.grid[self.rowDim-1-y][x] == 'c':
						tilesCov+=1
						self.tilesProb[(x,y)] += 1

			if flagNo == number:
				self.addToSafeTiles(self.lastTile)
			elif tilesCov == number-flagNo:
				self.addToMineTiles(self.lastTile)
		
		#Check neighbours after every action by calling checksurroundings function, if some tiles can be added in safe or mine list
		lastx = self.lastTile[0]
		lasty = self.lastTile[1]

		for i,j in self.adjTiles:
			x = lastx + i
			y = lasty + j

			if x>=0 and x<self.colDim and y>=0 and y<self.rowDim and (x,y) in self.boardState["uncovered"]:
				self.checkSurroundings((x,y))

		#if neither all flags are marked, nor covered tiles = flags left, and there is no safe tiles and mine tiles
		#then check entire matrix to find any safe or mine tiles
		#then check patterns
		if self.totMines and self.totMines != len(self.boardState["covered"]) and not self.safeTiles and not self.mineTiles:
			for i in range(self.colDim):
				for j in range(self.rowDim):
					self.checkSurroundings((i,j))
			self.checkPatterns()

		#If all mines flagged - Uncover all covered tiles
		if not self.totMines:
			nextTile = self.boardState["covered"].pop()
			self.boardState["uncovered"].add(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#If covered tiles equal to mines, flag them all
		elif self.totMines == len(self.boardState["covered"]):
			self.totMines -= 1
			nextTile = self.boardState["covered"].pop()
			self.boardState["uncovered"].add(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

		#Uncover one of safetiles and proceed
		elif self.safeTiles:
			nextTile = self.safeTiles.pop()
			self.boardState["uncovered"].add(nextTile)
			self.boardState["covered"].discard(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#flag one of mine tiles and proceed
		elif self.mineTiles:
			self.totMines -= 1
			nextTile = self.mineTiles.pop()
			self.boardState["uncovered"].add(nextTile)
			self.boardState["covered"].discard(nextTile)
			if nextTile in self.tilesProb: del self.tilesProb[nextTile]
			self.safeTiles.discard(nextTile)
			self.mineTiles.discard(nextTile)
			self.lastTile = nextTile
			return Action(AI.Action.FLAG, nextTile[0], nextTile[1])

		#If no safe or mine tiles left
		#uncover one of corner tiles, if covered, as prob of being safe is more?
		#If no corner tiles is covered, flag one from probabilities list which has maximum value (this is according to how many numbered tiles are adjacnet to it,kind of a guess)
		#else, uncover random tile and proceed
		else:
			#Corner tiles
			nextTile = None
			if (0,0) in self.boardState['covered']:
				nextTile = (0,0)
			elif (0,self.rowDim-1) in self.boardState['covered']:
				nextTile = (0,self.rowDim-1)
			elif (self.colDim-1,0) in self.boardState['covered']:
				nextTile = (self.colDim-1,0)
			elif (self.colDim-1,self.rowDim-1) in self.boardState['covered']:
				nextTile = (self.colDim-1,self.rowDim-1)
			
			if nextTile:
				self.boardState["uncovered"].add(nextTile)
				self.boardState["covered"].discard(nextTile)
				if nextTile in self.tilesProb: del self.tilesProb[nextTile]
				self.safeTiles.discard(nextTile)
				self.mineTiles.discard(nextTile)
				self.lastTile = nextTile
				return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

			#flag tile with max value in probTiles list
			if self.tilesProb:
				nextTile = max(self.tilesProb.items(), key=operator.itemgetter(1))[0]
				if nextTile:
					self.totMines -= 1
					self.boardState["uncovered"].add(nextTile)
					self.boardState["covered"].discard(nextTile)
					if nextTile in self.tilesProb: del self.tilesProb[nextTile]
					self.safeTiles.discard(nextTile)
					self.mineTiles.discard(nextTile)
					self.lastTile = nextTile
					return Action(AI.Action.FLAG, nextTile[0], nextTile[1])
				
			#If didnot get anything from above, uncover random tile and proceed
			nextTile = self.boardState["covered"].pop()
			if nextTile:
				self.boardState["uncovered"].add(nextTile)
				if nextTile in self.tilesProb: del self.tilesProb[nextTile]
				self.safeTiles.discard(nextTile)
				self.mineTiles.discard(nextTile)
				self.lastTile = nextTile
				return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		### Output ###
		#Beginner (8x810 mines): 78% (approx)
		#Intermediate (16x16 40 mines): 67.5% (approx)
		#Expert (16x30 99 mines): 8% (approx)
		#take less than a minute for sample size of 1000 of each level (total 3000 sample size)
