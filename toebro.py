#! /usr/bin/env python
"""
	A simple tic-tac-toe game written with pyglet

	Copyright (C) 2012 Steven E. Kendall 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#globals
import pyglet
from pyglet.gl import *
import math

WIGGLE_ROOM = 55 #arbitrary wiggle room pixels

class GameState:
	"""
		maintains all gamestate required for a tic-tac-toe game
	"""
	singleton = None

	def __init__(self):
		"""
			should only be used indirectly through the getState() singleton interface 
		"""
		self.cur_sym = 'o'	
		self.winner = False
		row_1 = ['e', 'e', 'e']
		row_2 = ['e', 'e', 'e']
		row_3 = ['e', 'e', 'e']
		self.board = [row_1, row_2, row_3] 
		self.num_moves = 0

	def switchSym(self):
		if self.cur_sym == 'x':
			self.cur_sym = 'o'
		else:
			self.cur_sym = 'x'
		self.num_moves = self.num_moves + 1

	@staticmethod
	def getState():
		if GameState.singleton == None:
			GameState.singleton = GameState()
		return GameState.singleton

	def printBoard(self):
		"""
			debug method
		"""
		print self.board

	def getWinner(self):
		"""
			checks all possible combinations for three in a row
		"""
		#if the same symbol fills a whole row then that symbol won
		for i in range(3):
			win = True
			root2 = self.board[i][0]
			for j in range(3):
				if self.board[i][j] != root2:
					win = False	
			if win == True and root2 != 'e': 
				self.winner = root2
				return root2 
		for i in range(3):
			win = True
			root2 = self.board[0][i]
			for j in range(3):
				if self.board[j][i] != root2:
					win = False	
			if win == True and root2 != 'e': 
				self.winner = root2 
				return root2 
		#if the same symbol fills a diagonal then that symbol won
		if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 'e':
			self.winner = self.board[0][0]
			return self.board[0][0]
		if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] != 'e':
			self.winner = self.board[0][2]
			return self.board[0][2]
		return False

	def getCurStr(self):
		"""
			returns an appropriate, if boring, string to notify the users of the game's state
		"""
		if self.winner == 'x':
			return "X wins!"
		elif self.winner == 'o':
			return "O wins!"
		elif self.num_moves >= 9:
			return "Cat's game!"
		elif self.cur_sym == 'x':
			return "It is X's turn"
		else:
			return "It is 0's turn"

#openGL commands now use this window
WINDOW_HEIGHT = pyglet.window.get_platform().get_default_display().get_screens()[0].height - WIGGLE_ROOM 
WINDOW_WIDTH = WINDOW_HEIGHT 
#openGL commands now use this window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)  
LINE_WIDTH = window.height / 20.0
TRIANGLES_PER_CIRCLE = 64 
X_RED = 1 
X_GREEN = 0
X_BLUE = 0
O_RED = 0 
O_GREEN = 0
O_BLUE = 1 
event_loop = pyglet.app.EventLoop()

@window.event
def on_draw():
	GameState.getState().getWinner()
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	draw_grid()
	draw_occupants()
		 
	label = pyglet.text.Label(GameState.getState().getCurStr(), font_name='Times New Roman',font_size = 20, x = 10, y = 10)
	label.draw()

@window.event
def on_key_press(symbol, modifiers):
	board = GameState.getState().board
	if symbol == pyglet.window.key.ESCAPE:
		pyglet.app.exit() 
	if GameState.getState().getWinner() == False:
		if symbol == pyglet.window.key.Q and board[2][0] == 'e':
			board[2][0] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.W and board[2][1] == 'e':
			board[2][1] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.E and board[2][2] == 'e': 
			board[2][2] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.A and board[1][0] == 'e': 
			board[1][0] = GameState.getState().cur_sym 
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.S and board[1][1] == 'e':
			board[1][1] = GameState.getState().cur_sym 
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.D and board[1][2] == 'e':
			board[1][2] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.Z and board[0][0] == 'e':
			board[0][0] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.X and board [0][1] == 'e':
			board[0][1] = GameState.getState().cur_sym
			GameState.getState().switchSym()
		elif symbol == pyglet.window.key.C and board[0][2] == 'e':
			board[0][2] = GameState.getState().cur_sym
			GameState.getState().switchSym()

def draw_grid():
	#make a vertical line @ 1/3rd
	glBegin(GL_QUADS)
	glVertex2f(window.width / 3.0 - LINE_WIDTH / 2.0, window.height) 
	glVertex2f(window.width / 3.0 + LINE_WIDTH / 2.0, window.height) 
	glVertex2f(window.width / 3.0 + LINE_WIDTH / 2.0, 0) 
	glVertex2f(window.width / 3.0 - LINE_WIDTH / 2.0, 0) 
	glEnd()
	#etc.
	glBegin(GL_QUADS)
	glVertex2f(2 * window.width / 3.0 - LINE_WIDTH / 2.0, window.height) 
	glVertex2f(2 * window.width / 3.0 + LINE_WIDTH / 2.0, window.height) 
	glVertex2f(2 * window.width / 3.0 + LINE_WIDTH / 2.0, 0) 
	glVertex2f(2 * window.width / 3.0 - LINE_WIDTH / 2.0, 0) 
	glEnd()
	glBegin(GL_QUADS)
	glVertex2f(0, window.height / 3.0 - LINE_WIDTH / 2.0) 
	glVertex2f(window.width, window.height / 3.0 - LINE_WIDTH / 2.0) 
	glVertex2f(window.width, window.height / 3.0 + LINE_WIDTH / 2.0) 
	glVertex2f(0, window.height / 3.0 + LINE_WIDTH / 2.0) 
	glEnd()
	glBegin(GL_QUADS)
	glVertex2f(0, 2 * window.height / 3.0 - LINE_WIDTH / 2.0) 
	glVertex2f(window.width, 2 * window.height / 3.0 - LINE_WIDTH / 2.0) 
	glVertex2f(window.width, 2 * window.height / 3.0 + LINE_WIDTH / 2.0) 
	glVertex2f(0, 2 * window.height / 3.0 + LINE_WIDTH / 2.0) 
	glEnd()

def draw_x():
	glPushMatrix()
	glColor3f(X_RED, X_GREEN, X_BLUE)
	#move to middle to center rotation
	glTranslatef(window.width / 2.0, window.height / 2.0, 0)
	glRotatef(45, 0, 0, 1)
	#move back to resume drawing from origin in lower left 
	glTranslatef(-1 * window.width / 2.0, -1 * window.height / 2.0, 0)
	glBegin(GL_QUADS)
	glVertex2f(0, window.width / 2.0 - LINE_WIDTH / 2.0)
	glVertex2f(0, window.width / 2.0 + LINE_WIDTH / 2.0)
	glVertex2f(window.height, window.width / 2.0 + LINE_WIDTH / 2.0)	
	glVertex2f(window.height, window.width / 2.0 - LINE_WIDTH / 2.0)	
	glEnd()
	glPopMatrix()
	glPushMatrix()
	glTranslatef(window.width / 2.0, window.height / 2.0, 0)
	glRotatef(-45, 0, 0, 1)
	#move back to resume drawing from origin in lower left 
	glTranslatef(-1 * window.width / 2.0, -1 * window.height / 2.0, 0)
	glBegin(GL_QUADS)
	glVertex2f(0, window.width / 2.0 - LINE_WIDTH / 2.0)
	glVertex2f(0, window.width / 2.0 + LINE_WIDTH / 2.0)
	glVertex2f(window.height, window.width / 2.0 + LINE_WIDTH / 2.0)	
	glVertex2f(window.height, window.width / 2.0 - LINE_WIDTH / 2.0)	
	glEnd()
	glPopMatrix()
	glColor3f(1, 1, 1)

def draw_circle(scale, red, green, blue):
	glPushMatrix()
	glTranslatef(window.width / 2.0, window.height / 2.0, 0)
	glColor3f(red, green, blue)
	for x in range(0, TRIANGLES_PER_CIRCLE):
		glBegin(GL_TRIANGLES)
		glVertex2f(0, 0)
		inside1 = 2.0 * math.pi * (1.0 * x / TRIANGLES_PER_CIRCLE)
		inside2 = 2.0 * math.pi * (1.0 * (x + 1) / TRIANGLES_PER_CIRCLE)
		glVertex2f(scale * 0.5 * window.width * math.sin(inside1), scale * 0.5 * window.height * math.cos(inside1))  
		glVertex2f(scale * 0.5 * window.width * math.sin(inside2), scale * 0.5 * window.height * math.cos(inside2))  
		glEnd()
	glPopMatrix()
	glColor3f(1, 1, 1)

def draw_o():
	draw_circle(0.7, O_RED, O_GREEN, O_BLUE)
	draw_circle(0.6, 0, 0, 0)

#we'll iterate over each cell and draw the appropriate letter
def draw_occupants():
	board = GameState.getState().board
	#for each row
	for i in range(3):
		#for each cell within each row
		for j in range(3):
			glPushMatrix()
			glTranslatef(1.0 * j / 3 * window.width, 1.0 * i / 3 * window.height, 0) 
			glScalef(1/3.0, 1/3.0, 1)
			if board[i][j] == 'x':
				draw_x()
			elif board[i][j] == 'o':
				draw_o()
			glPopMatrix()

pyglet.app.run()
