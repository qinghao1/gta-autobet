from autobet.constants import *
from autobet.util import get_screen_size, log
from PIL import ImageOps, ImageEnhance
from datetime import datetime

import re
import time
import platform
import pytesseract
import pyautogui
import autobet.ocr_model as ocr_model

if platform.system() == 'Windows':
	pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

MODEL = ocr_model.load_model()

class Reader:
	#'X/1' can sometimes be OCRed as 'XN'
	ODD_REGEX = re.compile('^(\d+)\/?1?N?$')
	# Assume that if '+' is read, it's always followed by the currency symbol
	WINNING_REGEX = re.compile('^(?:\+.)?(\d+)$')

	def generate_screenshot_name(fmt):
		return f'Screenshot on {time.ctime()}-{datetime.now().microsecond}.{fmt}'\
			.replace(' ','_').replace(':','-')

	def enhance_screenshot(img):
		# Invert then enhance contrast
		return ImageEnhance.Contrast(ImageOps.invert(img)).enhance(5)

	def screenshot_odd(i):
		left = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_X)
		top = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_YS[i])
		width = int(get_screen_size()[0] * PLACE_BET_SCREEN_ODDS_WIDTH)
		height = int(get_screen_size()[1] * PLACE_BET_SCREEN_ODDS_HEIGHT)
		raw_img = pyautogui.screenshot(region=(left, top, width, height))
		enhanced_img = Reader.enhance_screenshot(raw_img)
		return enhanced_img.convert('L')

	def parse_winning(img):
		ocr_res = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=+0123456789')

		# Good OCR
		matched = Reader.WINNING_REGEX.match(ocr_res)
		if matched:
			return int(matched[1])

		# Bad OCR
		return 0

	def read_odds():
		screenshots = [Reader.screenshot_odd(i) for i in range(NUM_BETS)]
		odds = ocr_model.parse_multiple(MODEL, screenshots)
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
