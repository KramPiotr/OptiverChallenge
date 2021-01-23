from utils import weighted_average
import numpy as np

exponent = 1
maximal_volume = 100
aggressor_bias = 0.05
time_steepness = 0.2
forget = 0.2
price = None

name = "hack-cambridge-team-05"


class Prediction:
    def __init__(self, side, price, confidence):
        self.side = side
        self.price = price
        self.confidence = confidence

class PriceBook_:
    def calculate_averages(self):
        bids = [(pv.price, pv.volume) for pv in self.price_book.bids]
        asks = [(pv.price, pv.volume) for pv in self.price_book.asks]

        self.bids_avg = weighted_average(bids, exponent, maximal_volume)
        self.asks_avg = weighted_average(asks, exponent, maximal_volume)

    def __init__(self, price_book):
        self.price_book = price_book
        self.calculate_averages()

def update_estimates(price_book, trade_ticks):
    global price
    trade_ticks = filter(lambda ticks: ticks.buyer != name and ticks.seller != name, trade_ticks)
    prices = map(lambda t: t.price * (100 + aggressor_bias)/100 if t.aggressor_bias == "ask" else t.price * (100 - aggressor_bias)/100, trade_ticks)
    timestamps = [t.timestamp for t in trade_ticks]
    seconds = [(t.timestamp - timestamps[0]).seconds for t in timestamps]
    mean_diff = 1 - np.mean(seconds)
    std_diff = time_steepness/np.std(seconds)
    price_weights = [(s + mean_diff) * std_diff for s in seconds]
    price_avg = [p * w for p, w in zip(prices, price_weights)]
    price = price * (1 - forget) + price_avg * forget if price else price_avg













