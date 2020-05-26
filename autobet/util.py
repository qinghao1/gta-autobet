from functools import lru_cache
from autobet.constants import GAME_EXECUTABLE, ASPECT_RATIO, BETTING_SCREEN_TOP_LEFT_PIXEL_RGB

import psutil
import pyautogui
import autobet.constants

def log(msg):
	# TODO proper logging
	print(msg)

def check_game_running():
	return GAME_EXECUTABLE in (p.name() for p in psutil.process_iter())

@lru_cache(maxsize=1)
def get_screen_size():
	return pyautogui.size()

def check_aspect_ratio():
	x,y = pyautogui.size()
	return abs(x/y - ASPECT_RATIO) < 0.1

def check_betting_screen():
	return pyautogui.pixelMatchesColor(0, 0, BETTING_SCREEN_TOP_LEFT_PIXEL_RGB, tolerance=5)
