from pynput import keyboard
from pyautogui import locateOnScreen
from datetime import timedelta
from autobet.clicker import Clicker
from autobet.reader import Reader
from autobet.bettor import Bettor
from autobet.constants import HORSE_RACE_DURATION_SECONDS, SAFE_CLICK_X_Y
from autobet.util import *

import time

class App:
	START_STOP_KEY = keyboard.Key.f8
	START_SCREEN_IMAGE = 'images/start_screen.png'

	def on_press(self, key):
		if key == App.START_STOP_KEY:
			return False

	def __init__(self):
		self.started = False

	def start(self):
		if self.started:
			log("Already started.")
			return
		if not check_game_running():
			log("Game is not running.")
			return self.stop()
		self.screen_coord = locateOnScreen(App.START_SCREEN_IMAGE,
			confidence=0.95)
		if self.screen_coord is None:
			log("Not on start screen")
			return self.stop()
		log(f'Found coordinates {self.screen_coord}')
		width, height = self.screen_coord[2:]
		if not check_aspect_ratio(width, height):
			log("Wrong game aspect ratio.")
			return self.stop()

		log('Started.')
		self.started = True
		self.start_time = time.time()
		self.acc_winnings = 0
		self.winnings = []
		clicker = Clicker(self.screen_coord)
		reader = Reader(self.screen_coord)
		with keyboard.Listener(on_press=self.on_press) as listener:
			while True:
				self.main_loop(clicker, reader)
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

	def main_loop(self, clicker, reader):
		top_left_coord = self.screen_coord[:2]
		top_left_coord = [i+1 for i in top_left_coord]

		if not at_start_screen(*top_left_coord):
			time.sleep(3)
		if not at_start_screen(*top_left_coord):
			log("Game bug. Exiting and re-entering...")
			clicker.exit_and_reenter()
			return

		clicker.click_place_bet_start_screen()

		if not at_place_bet_screen(*top_left_coord):
			time.sleep(3)
		if not at_place_bet_screen(*top_left_coord):
			log('Game bug. Exiting and re-entering...')
			clicker.exit_and_reenter()
			return

		odds = reader.read_odds()
		bet_position, bet_amount = Bettor.bet(odds)
		log(f'Placing bet on {bet_position} for {bet_amount}')
		clicker.place_bet(bet_position, bet_amount)
		time.sleep(HORSE_RACE_DURATION_SECONDS)

		if not at_results_screen(*top_left_coord):
			time.sleep(3)
		if not at_results_screen(*top_left_coord):
			log('Game bug. Exiting and re-entering...')
			clicker.exit_and_reenter()
			return

		winning = reader.read_winning()
		net_won = winning - bet_amount
		self.winnings.append(net_won)
		self.acc_winnings += net_won
		log(f'Made ${net_won}. Session total: ${self.acc_winnings}')
		seconds_elapsed = time.time() - self.start_time
		hours_elapsed = seconds_elapsed / 3600
		winnings_per_hour = self.acc_winnings / hours_elapsed
		log(f'Time elapsed: {str(timedelta(seconds=seconds_elapsed)).split(".")[0]} Avg Earnings: ${round(winnings_per_hour)}/hr')
		clicker.click_bet_again()

		if not at_start_screen(*top_left_coord):
			time.sleep(3)
		if not at_start_screen(*top_left_coord):
			log('Game bug. Exiting and re-entering...')
			clicker.exit_and_reenter()
			return
