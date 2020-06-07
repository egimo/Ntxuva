# -*- coding: utf-8 -*-
"""Ntxuva.ipynb

Automatically generated by Colaboratory.

Original file is located at
	https://colab.research.google.com/drive/1SCJHVvc2eFNy9AzTYQ2tBEQtYrhJ9CtG
"""
#@title Default title text

import numpy as np

class  Ntxuva:

	def __init__(self, rows, columns, seeds):
		self.rows = rows
		self.columns = columns
		self.ROW_ZERO = 0
		self.ROW_ONE = 1
		self.ROW_TWO = 2
		self.ROW_THREE = 3
		self.BAD_REWARD = -100
		self.seeds = seeds
		self.board = np.full((self.rows,self.columns),seeds)
		self.player1_score = 0
		self.player2_score = 0
		self.turn = 'x'  # turn can be represented by x or o -  x for computer and o for Human player
		self.is_over = False

	def reset(self, seeds=2):
		self.__init__(rows=self.rows, columns=self.columns, seeds=seeds)
		return self.board

	def player_side(self):
		if self.turn == 'x':
			return self.ROW_ZERO, self.ROW_ONE
		return self.ROW_TWO, self.ROW_THREE

	def change_turn(self):
		if self.turn == 'x':
			self.turn = 'o'
		else:
			self.turn = 'x'
		return self.turn

	# this method change position from current to next in two modes anticlockwise and clockwise
	# return the next position
	def move(self, position):
		current_row = position[0]
		current_column = position[1]
		first_row, second_row = self.player_side()

		if current_row != first_row and current_row != second_row:
			print(f"{current_column}")
			return None

		if current_column > self.columns - 1 or current_column < 0:
			print(f"{current_column}x{self.columns}")
			return None

		lower_bound = 0
		highest_bound = self.columns - 1

		pos = tuple()

		if self.turn == 'o' and self.ROW_TWO == current_row:
			pos = (current_row, current_column - 1)
		elif self.turn == 'o' and self.ROW_THREE == current_row:
			pos = pos = (current_row, current_column + 1)

		if self.turn == 'x' and self.ROW_ZERO == current_row:
			pos = (current_row, current_column - 1)
		elif self.turn == 'x' and self.ROW_ONE == current_row:
			pos = pos = (current_row, current_column + 1)

		if current_row == first_row and current_column == lower_bound:
			pos = (second_row, current_column)

		if current_row == second_row and current_column == highest_bound:
			pos = (first_row, current_column)

		return pos

	def more_than_one_piece(self):
		row1, row2 = self.player_side()
		merged = np.concatenate((self.board[row1], self.board[row2]))
		for i in range(len(merged)):
			if merged[i] > 1:
				return True
		return False

   
	# is atack_position method return true if corresponding position is on  atack row, false if not.
	def is_atack_position(self, position):
		return True if position[0] == self.ROW_ONE or position[0] == self.ROW_TWO else False

	def is_invalid_move(self, position):
		ZERO = 0
		row1, row2 = self.player_side();
		if position[0] == row1 or position[0] == row2:
			if position[1] < ZERO or position[1] > self.columns:
				return False
		return  True


	# the position is a tuple of (row,column)
	# return the number of stones that it has captured
	def capture_stones(self, position):
		ZERO = 0

		#if the current position is on atack line then we can capture the opposite stone...
		if self.is_atack_position(position) and self.is_invalid_move(position):

			front_slot = None
			rear_slot = None

			if self.turn == 'x':
				front_slot = (position[0] + 1, position[1])
				rear_slot = (position[0] + 2, position[1])
			elif self.turn == 'o':
				front_slot = (position[0] - 1, position[1])
				rear_slot = (position[0] - 2, position[1])

			sum = self.board[front_slot] + self.board[rear_slot]

			self.board[front_slot] = ZERO
			self.board[rear_slot] = ZERO
			return sum
		return 0


	def is_terminal_state(self):
		row1, row2, row3, row4 = 0,1,2,3,
		side1 = np.concatenate(([i for i in self.board[row1]],[i for i in self.board[row2]]))
		side2 = np.concatenate(([i for i in self.board[row3]], [i for i in self.board[row4]]))
		size_side1 = len([i for i in side1 if i != 0])
		size_side2 = len([i for i in side2 if i != 0])

		if  size_side1 != 0 and size_side2 != 0:
			return False
		self.is_over = True
		return True


	# Action is a tuple of rowXcolumn. that represent one slot on the current player side.
	def step(self,action):
		current_pos = action

		# The selected position have just one stone and other's on player side have more
		# By the rule this move is not allowed
		# This player receives an bad reward for taking that action
		if self.board[current_pos] == 1 and self.more_than_one_piece():
			return self.board, self.BAD_REWARD, False

		# the selected slot is empty so the next state is going to be the same and the ai will receive a negative penalty
		# the state is going to be the same and tha state is going to be the same, done flag is False
		if self.board[action] == 0:
			return self.board, self.BAD_REWARD * 2,False

		stones = self.board[current_pos]
		self.board[current_pos] = 0

		captured_stones = 0

		counter = 0

		old_board = self.board

		while True:

			while stones > 0:
				current_pos = self.move(current_pos)
				self.board[current_pos] += 1
				stones -= 1

				if current_pos is None:
					print("{current_pos} -- {self.turn}")

			if self.board[current_pos] == 1:
				captured_stones += self.capture_stones(current_pos)
				break
			else:
				stones = self.board[current_pos]
				self.board[current_pos] = 0


		new_board = self.board

		if np.array_equal(old_board, new_board):
			counter += 1
		else:
			counter = 0

		if counter == 20:
			print(f"same board configuration found")
			print(f"old board {old_board}")
			print(f"new board {new_board}")
			exit(1)

		new_board = old_board

		is_terminal = self.is_terminal_state()
		self.change_turn()
		#return self.make_key(), captured_stones , is_terminal

		return self.board, captured_stones, is_terminal

	# this method returns the availables moves on the board, following the rule of more than one piece method
	def available_moves(self, side):
		temp_board = self.board
		row1, row2 = side
		if  self.more_than_one_piece():
			return [(i,j) for i in (row1,row2) for j in range(self.columns) if temp_board[i][j] > 1]
		return [(i, j) for i in (row1,row2) for j in range(self.columns) if temp_board[i][j] == 1 ]


	# In this method the game state represented by the Board is encoded to a integer in order to use on the Q table.
	def make_key(self):
		encoded_state = ""
		temp_board = np.reshape(self.board, (self.rows * self.columns ))
		for stone in temp_board:
			encoded_state += str(stone)
		return encoded_state

	def declare_winner(self):
		temp_board  = self.board
		side1= np.concatenate((temp_board[self.ROW_ZERO],temp_board[self.ROW_ONE]))
		side2 = np.concatenate((temp_board[self.ROW_TWO],temp_board[self.ROW_THREE]))

		if len([data for data in side1 if data != 0]) == 0:
			return 'o'

		if len([data for data in side2 if data != 0]) == 0:
			return 'x'
		return None