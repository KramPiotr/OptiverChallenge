from utils import *
import numpy as np
from optibook.synchronous_client import Exchange
import logging
import collections

ia = 0.9
safety = 1
volume_part = 0.5

class Params:
    def __init__(self):
        self.exponent = 1
        self.maximal_volume = 100
        self.aggressor_bias = 0.05
        self.time_steepness = 0.2
        self.forget = 0.2
        self.book = 0.4

    def unpack(self):
        return (self.exponent, self.maximal_volume, self.aggressor_bias, self.time_steepness, self.forget, self.book)

name = "hack-cambridge-team-05"

PA = "PHILIPS_A"
PB = "PHILIPS_B"

class Instrument_:
    def __init__(self, instrument_id, params):
        self.id = instrument_id
        self.params = params
        self.price = update_estimates(self)

    def update_price(self):
        self.price = update_estimates(self, self.price)

    def update(self):
        self.update_price()

class Prediction:
    def __init__(self, side, price, confidence):
        self.side = side
        self.price = price
        self.confidence = confidence

class PriceBook_:
    def calculate_averages(self, exponent, maximal_volume):
        bids = [(pv.price, pv.volume) for pv in self.price_book.bids]
        asks = [(pv.price, pv.volume) for pv in self.price_book.asks]

        self.bids_avg = weighted_average(bids, exponent, maximal_volume)
        self.asks_avg = weighted_average(asks, exponent, maximal_volume)
        self.avg = (self.bids_avg + self.asks_avg) / 2

    def __init__(self, price_book, exponent, maximal_volume):
        self.price_book = price_book
        self.calculate_averages(exponent, maximal_volume)

def update_estimates(instrument, curr_price=None):
    global exchange
    exponent, maximal_volume, aggressor_bias, time_steepness, forget, book = instrument.params.unpack()

    price_book = PriceBook_(exchange.get_last_price_book(instrument.id), exponent, maximal_volume)

    trade_ticks = exchange.poll_new_trade_ticks(instrument.id)
    trade_ticks = filter(lambda ticks: ticks.buyer != name and ticks.seller != name, trade_ticks)
    prices = map(lambda t: t.price * (100 + aggressor_bias)/100 if t.aggressor_bias == "ask" else t.price * (100 - aggressor_bias)/100, trade_ticks)

    timestamps = [t.timestamp for t in trade_ticks]
    seconds = [(t.timestamp - timestamps[0]).seconds for t in timestamps]
    price_weights = switch_mean_and_std(seconds, 1, time_steepness)
    price_avg = sum([p * w for p, w in zip(prices, price_weights)])

    new_price = price_avg * (1 - book) + price_book.avg * book
    return (1 - forget) * curr_price + forget * new_price if curr_price else new_price

def delete_outstanding_orders():
    global exchange
    global instruments
    for i in instruments:
        outstanding = exchange.get_outstanding_orders(i.id)
        for o in outstanding.values():
            result = exchange.delete_order(i.id, order_id=o.order_id)
            print(f"Deleted order id {o.order_id}: {result}")

def update_positions():
    global exchange
    global positions
    positions = exchange.get_positions()
    for p in positions:
        print(p, positions[p])

def connect():
    global exchange
    exchange = Exchange()
    return exchange.connect()

if __name__ == "__main__":
    logger = logging.getLogger('client')
    logger.setLevel('ERROR')
    print("Setup was successful.")
    connect()

    IA = Instrument_(PA, Params())
    IB = Instrument_(PB, Params())
    instruments = [IA, IB]
    iteration = 0
    pnls = collections.deque(5*[0], 5)

    while(True):
        sleep(0.5)
        delete_outstanding_orders()
        IA.update()
        IB.update()
        update_positions()
        price = ia * IA.price + (1 - ia) * IB.price
        ask_price = price + safety
        bid_price = price - safety
        for i in instruments:
            bid_volume = volume_part * (500 - positions[i.id])
            ask_volume = volume_part * (500 + positions[i.id])
            exchange.insert_order(i.id, price=bid_price, volume=bid_volume, side='bid', order_type='limit')
            exchange.insert_order(i.id, price=ask_price, volume=ask_volume, side='ask', order_type='limit')

        if iteration % 5 == 0:
            pnls.append(exchange.get_pnl())
            print(f"Recent pnls: {pnls}")

















