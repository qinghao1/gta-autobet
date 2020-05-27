from pynput import keyboard
from autobet.clicker import Clicker
from autobet.reader import Reader
from autobet.bettor import Bettor
from autobet.constants import START_STOP_KEY, HORSE_RACE_DURATION_SECONDS, SAFE_CLICK_X_Y
from autobet.util import *

import time

class App:
	def on_press(self, key):
		if key == START_STOP_KEY:
			return False

	def __init__(self):
		self.started = False
		self.odds = []
		self.winnings = []

	def start(self):
		if self.started:
			log("Already started.")
			return
		if not check_game_running():
			log("Game is not running.")
			return self.stop()
		if not check_aspect_ratio():
			log("Wrong aspect ratio.")
			return self.stop()
		if not at_start_screen():
			log("Not on betting screen.")
			return self.stop()
		log('Started.')
		self.started = True
		with keyboard.Listener(on_press=self.on_press) as listener:
			while True:
				self.main_loop()
				if not listener.running:
					break
		self.stop()

	def stop(self):
		self.started = False
		log('Stopped.')
		self.run()

	def run(self):
		log("Waiting for key input.")
		with keyboard.Listener(on_press=self.on_press) as listener:
			listener.join()
		self.start()

	def main_loop(self):
		Clicker.click_place_bet_start_screen()
		odds = Reader.read_odds()
		self.odds.append(odds)
		bet_position, bet_amount = Bettor.bet(odds)
		Clicker.place_bet(bet_position, bet_amount)
		log(f'Placing bet on {bet_position} for {bet_amount}')
		time.sleep(HORSE_RACE_DURATION_SECONDS)
		while not at_results_screen():
			# Sometimes it lags here, need to click
			time.sleep(0.5)
			Clicker.click(*SAFE_CLICK_X_Y)
		winning = Reader.read_winning()
		net_won = winning - bet_amount
		log(f'Made ${net_won}')
		self.winnings.append(net_won)
		Clicker.click_bet_again()
		# Exit and re-enter betting game here because of bug
		Clicker.click(*SAFE_CLICK_X_Y, button='right')
		Clicker.click(*SAFE_CLICK_X_Y, button='left')
