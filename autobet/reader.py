from autobet.constants import *
from autobet.util import get_screen_size, log
from PIL import ImageOps, ImageEnhance
from datetime import datetime

import re
import time
import platform
import pytesseract
import pyautogui

if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class Reader:
	#'X/1' can sometimes be OCRed as 'XN'
	odd_regex = re.compile('^(\d+)\/?1?N?$')
	# Assume that if '+' is read, it's always followed by the currency symbol
	winning_regex = re.compile('^(?:\+.)?(\d+)$')

	def generate_screenshot_name():
		return f'Screenshot on {time.ctime()}-{datetime.now().microsecond}.png'\
			.replace(' ','_').replace(':','-')

	def enhance_screenshot(img):
		# Invert then enhance contrast
		return ImageEnhance.Contrast(ImageOps.invert(img)).enhance(3)

	def screenshot_odd(i):
		left = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_X)
		top = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_YS[i])
		width = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_WIDTH)
		height = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_HEIGHT)
		raw_img = pyautogui.screenshot(region=(left, top, width, height))
		return Reader.enhance_screenshot(raw_img)

	def parse_odd(img):
		ocr_res = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=0123456789/EVNS')

		# Good OCR
		if ocr_res == 'EVENS':
			return 1
		matched = Reader.odd_regex.match(ocr_res)
		if matched:
			return int(matched[1])

		# Bad OCR
		img_name = Reader.generate_screenshot_name()
		img.save(img_name)
		log(f'Error! Read {ocr_res} for odd screenshot "{img_name}"')
		return 1


	def parse_winning(img):
		ocr_res = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=+0123456789')

		# Good OCR
		matched = Reader.winning_regex.match(ocr_res)
		if matched:
			return int(matched[1])

		# Bad OCR
		img_name = Reader.generate_screenshot_name()
		img.save(img_name)
		log(f'Error! Read {ocr_res} for winning screenshot "{img_name}"')
		return 0


	def read_odds():
		odds = []
		for i in range(NUM_BETS):
			screenshot = Reader.screenshot_odd(i)
			parsed = Reader.parse_odd(screenshot)
			log(f'Parsed {parsed} in position {i}')
			odds.append(parsed)
		return odds

	def screenshot_winning():
		left = int(get_screen_size()[0] * RESULTS_SCREEN_WINNING_X)
		top = int(get_screen_size()[1] * RESULTS_SCREEN_WINNING_Y)
		width = int(get_screen_size()[0] * RESULTS_SCREEN_WINNING_WIDTH)
		height = int(get_screen_size()[1] * RESULTS_SCREEN_WINNING_HEIGHT)
		raw_img = pyautogui.screenshot(region=(left, top, width, height))
		return Reader.enhance_screenshot(raw_img)

	def read_winning():
		screenshot = Reader.screenshot_winning()
		return Reader.parse_winning(screenshot)
