from autobet.constants import *
from autobet.util import get_screen_size

import pyautogui
import pydirectinput
import bisect
import random
import time

class Clicker:
	def __init__(self, game_coord):
		self.game_coord = game_coord

	# Translates fractional to actual coordinaates
	def translate_coord(self, x, y):
		new_x = int(self.game_coord.width * x) + self.game_coord.left
		new_y = int(self.game_coord.height * y) + self.game_coord.top
		return new_x, new_y

	def get_random_mouse_duration(self):
		return random.uniform(MOUSE_MOVEMENT_MIN_DURATION_SECONDS,
			MOUSE_MOVEMENT_MAX_DURATION_SECONDS)

	def get_random_delay(self):
		return random.uniform(MIN_ACTION_DELAY_SECONDS, MAX_ACTION_DELAY_SECONDS)

	def single_click(self, x, y):
		pydirectinput.mouseUp(x, y)
		time.sleep(self.get_random_delay())
		pydirectinput.mouseDown(x, y)
		time.sleep(self.get_random_delay())

	def press_key(self, key):
		pydirectinput.press(key)
		time.sleep(self.get_random_delay())

	def move_mouse(self, x, y):
		pyautogui.moveTo(x, y, self.get_random_mouse_duration())
		time.sleep(self.get_random_delay())

	def click(self, x, y, times=1, translate=False):
		if translate:
			x, y = self.translate_coord(x, y)
		for _ in range(times):
			self.single_click(x, y)

	def click_place_bet_start_screen(self):
		self.click(START_SCREEN_PLACE_BET_X, START_SCREEN_PLACE_BET_Y, translate=True)

	def click_bet_again(self):
		self.click(RESULTS_SCREEN_BET_AGAIN_X, RESULTS_SCREEN_BET_AGAIN_Y, translate=True)

	def exit_and_reenter(self):
		self.press_key('esc')
		time.sleep(self.get_random_delay())
		self.click(*SAFE_CLICK_X_Y, translate=True)

	def place_bet(self, position, amount):
		num_clicks = bisect.bisect_left(BET_AMOUNTS, amount)
		if num_clicks == 0:
			return
		# Click corresponding horse
		self.click(PLACE_BET_SCREEN_BETS_X, PLACE_BET_SCREEN_BETS_YS[position], translate=True)
		# Click bet amount
		self.click(PLACE_BET_SCREEN_INCREMENT_X, PLACE_BET_SCREEN_INCREMENT_Y, times=num_clicks, translate=True)
		# Click place bet
		self.click(PLACE_BET_SCREEN_PLACE_BET_X, PLACE_BET_SCREEN_PLACE_BET_Y, translate=True)



