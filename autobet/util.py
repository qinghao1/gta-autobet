from functools import lru_cache
from autobet.constants import GAME_EXECUTABLE, ASPECT_RATIO, START_SCREEN_TOP_LEFT_PIXEL_RGB, RESULTS_SCREEN_TOP_LEFT_PIXEL_RGB, PLACE_BET_SCREEN_TOP_LEFT_PIXEL_RGB

import pyautogui
import autobet.constants

def log(msg):
	# TODO proper logging
	print(msg)

@lru_cache(maxsize=1)
def get_screen_size():
	return pyautogui.size()

def check_aspect_ratio(width=None, height=None):
	if width is None or height is None:
		width, height = pyautogui.size()
	return abs(width/height - ASPECT_RATIO) < 0.1

def at_start_screen(x, y):
	return pyautogui.pixelMatchesColor(int(x), int(y), START_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)

def at_place_bet_screen(x, y):
	return pyautogui.pixelMatchesColor(int(x), int(y), PLACE_BET_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)

def at_results_screen(x, y):
	return pyautogui.pixelMatchesColor(int(x), int(y), RESULTS_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)
