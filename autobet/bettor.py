class Bettor:
	MIN_BET_AMOUNT = 100
	SMALL_BET_AMOUNT = 1000
	MEDIUM_BET_AMOUNT = 5000
	BIG_BET_AMOUNT = 10000

	def expected_return(odds):
		win_percentages = [1/(1+odd) for odd in odds]
		return 1 / sum(win_percentages)

	def bet(odds):
		lowest_odd_idx = odds.index(min(odds))
		if Bettor.expected_return(odds) < 1:
			return (lowest_odd_idx, Bettor.MIN_BET_AMOUNT)
		elif Bettor.expected_return(odds) < 1.1:
			return (lowest_odd_idx, Bettor.SMALL_BET_AMOUNT)
		elif Bettor.expected_return(odds) < 1.2:
			return (lowest_odd_idx, Bettor.MEDIUM_BET_AMOUNT)
		else:
			return (lowest_odd_idx, Bettor.BIG_BET_AMOUNT)
