from autobet.constants import *
from autobet.util import get_screen_size

import pydirectinput
import bisect
import os
import random
import time

class Clicker:
	def get_random_mouse_duration():
		return random.uniform(MOUSE_MOVEMENT_MIN_DURATION_SECONDS,
			MOUSE_MOVEMENT_MAX_DURATION_SECONDS)

	def get_random_delay():
		return random.uniform(MIN_ACTION_DELAY_SECONDS, MAX_ACTION_DELAY_SECONDS)

	def get_random_pixel():
		x, y = get_screen_size()
		rand_x = int(random.random() * x)
		rand_y = int(random.random() * y)
		return rand_x, rand_y

	def get_absolute_path(relative_path):
		dirname = os.path.dirname(__file__)
		return os.path.join(dirname, relative_path)

	def click_curr():
		pydirectinput.mouseUp()
		time.sleep(Clicker.get_random_delay())
		pydirectinput.mouseDown()
		time.sleep(Clicker.get_random_delay())

	def move_mouse(x, y, frac=True):
		if frac:
			x = int(get_screen_size()[0] * x)
			y = int(get_screen_size()[1] * y)
		dx = int(get_screen_size()[0] * random.uniform(-MOUSE_X_RADIUS, MOUSE_X_RADIUS))
		dy = int(get_screen_size()[1] * random.uniform(-MOUSE_Y_RADIUS, MOUSE_Y_RADIUS))
		pyautogui.moveTo(x+dx, y+dy, Clicker.get_random_mouse_duration())
		time.sleep(Clicker.get_random_delay())

	def click(x, y, times=1, frac=True):
		Clicker.move_mouse(x, y, frac)
		for _ in range(times):
			Clicker.click_curr()

	def click_place_bet_start_screen():
		Clicker.click(START_SCREEN_PLACE_BET_X, START_SCREEN_PLACE_BET_Y)

	def click_bet_again():
		Clicker.click(RESULTS_SCREEN_BET_AGAIN_X, RESULTS_SCREEN_BET_AGAIN_Y)

	def place_bet(position, amount):
		# Click corresponding horse
		Clicker.click(PLACE_BET_SCREEN_BETS_X, PLACE_BET_SCREEN_BETS_YS[position])
		# Click bet amount
		num_clicks = bisect.bisect_left(BET_AMOUNTS, amount)
		Clicker.click(PLACE_BET_SCREEN_INCREMENT_X, PLACE_BET_SCREEN_INCREMENT_Y, times=num_clicks)
		# Click place bet
		Clicker.click(PLACE_BET_SCREEN_PLACE_BET_X, PLACE_BET_SCREEN_PLACE_BET_Y)



