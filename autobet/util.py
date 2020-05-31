from functools import lru_cache
from autobet.constants import GAME_EXECUTABLE, ASPECT_RATIO, START_SCREEN_TOP_LEFT_PIXEL_RGB, RESULTS_SCREEN_TOP_LEFT_PIXEL_RGB, PLACE_BET_SCREEN_TOP_LEFT_PIXEL_RGB

import psutil
import pyautogui
import autobet.constants

def log(msg):
	# TODO proper logging
	print(msg)

def check_game_running():
	for p in psutil.process_iter():
		try:
			if p.name() == GAME_EXECUTABLE:
				return True
		except (PermissionError, psutil.AccessDenied):
			pass
	return False

@lru_cache(maxsize=1)
def get_screen_size():
	return pyautogui.size()

def check_aspect_ratio():
	x,y = pyautogui.size()
	return abs(x/y - ASPECT_RATIO) < 0.1

def at_start_screen():
	return pyautogui.pixelMatchesColor(0, 0, START_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)

def at_place_bet_screen():
	return pyautogui.pixelMatchesColor(0, 0, PLACE_BET_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)

def at_results_screen():
	return pyautogui.pixelMatchesColor(0, 0, RESULTS_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)
