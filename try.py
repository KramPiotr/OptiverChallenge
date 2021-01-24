from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

IA = 'PHILIPS_A'
IB = 'PHILIPS_B'

e = Exchange()
a = e.connect()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import statistics 

def moving_avg_bids(price_book):
    average = []
    t_end = time.time() + 5
    while time.time() < t_end:
        for i in price_book.bids:
            average.append(i.price)
    return statistics.mean(average)
    
def moving_avg_asks(price_book):
    average = []
    t_end = time.time() + 5
    while time.time() < t_end:
        for i in price_book.asks:
            average.append(i.price)
    return statistics.mean(average)
    
res = []
t_end = time.time() + 100
while time.time() < t_end:
    book_A = e.get_last_price_book(IA)
    book_B = e.get_last_price_book(IB)
    res.append([time.time(), moving_avg_bids(book_A), moving_avg_asks(book_B)])
res = np.array(res)
fig,ax = plt.subplots(figsize=(10, 6))
for col,lbl in zip([1,2], ['bid','ask']):
    ax.plot(res[:,0], res[:,col], label=lbl)
ax.set_xlabel('time')
plt.legend()
plt.show()