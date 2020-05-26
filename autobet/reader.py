from autobet.constants import *
from autobet.util import get_screen_size, log
from PIL import ImageOps

import re
import platform
import pytesseract
import pyautogui

if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class Reader:
	odd_regex = re.compile('^(\d+)\/1$')

	def screenshot_odd(i):
		left = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_X)
		top = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_YS[i])
		width = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_WIDTH)
		height = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_HEIGHT)
		return pyautogui.screenshot(region=(left, top, width, height))

	def ocr(img):
		raw_img = pytesseract.image_to_string(img)
		# Convert to binary then invert
		return ImageOps.invert(raw_img.convert('1'))

	def parse_odd(string):
		if string == 'EVENS':
			return 1
		else:
			matched = Reader.odd_regex.match(string)
			if not matched:
				log(f'Error! {string} is not a valid odd.')
				return 1
			return matched[1]

	def parse_winning(string):
		if not string:
			log(f'Error! Empty winning.')
			return 0
		if string[0] != '+':
			return 0
		# '+X30000' where X is the currency symbol
		return int(string[2:])

	def read_odds():
		odds = []
		for i in range(NUM_BETS):
			screenshot = Reader.screenshot_odd(i)
			ocred = Reader.ocr(screenshot)
			print(f'Read {ocred} in position {i}')
			parsed = Reader.parse_odd(ocred)
			odds.append(parsed)
		return odds

	def screenshot_winning():
		left = int(get_screen_size()[0] * RESULTS_SCREEN_WINNING_X)
		top = int(get_screen_size()[1] * RESULTS_SCREEN_WINNING_Y)
		width = int(get_screen_size()[0] * RESULTS_SCREEN_WINNING_WIDTH)
		height = int(get_screen_size()[1] * RESULTS_SCREEN_WINNING_HEIGHT)
		raw_img = pyautogui.screenshot(region=(left, top, width, height))
		# Convert to binary then invert
		return ImageOps.invert(raw_img.convert('1'))

	def read_winning():
		screenshot = Reader.screenshot_winning()
		ocred = Reader.ocr(screenshot)
		return Reader.parse_winning(ocred)
