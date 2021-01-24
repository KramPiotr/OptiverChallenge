from optibook.synchronous_client import Exchange
import time
import logging
from statistics import mean
import random
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

e = Exchange()
a = e.connect()


print(e.get_positions())
for s, p in e.get_positions().items():
    if p > 0:
        e.insert_order(s, price=1, volume=p, side='ask', order_type='ioc')
    elif p < 0:
        e.insert_order(s, price=100000, volume=-p, side='bid', order_type='ioc')  
print(e.get_positions())

instrument_id = 'PHILIPS_A'
book = e.get_last_price_book(instrument_id)

print(book.bids)
instrument_id = 'PHILIPS_A'
#result = e.insert_order(instrument_id, price=98, volume=40, side='bid', order_type='limit')
#print(f"Order Id: {result}")
tradeticks = e.poll_new_trade_ticks(instrument_id)

def moving_avg(price_book):
    average = []
    t_end = time.time() + 10
    count = 0
    while time.time() < t_end:
        for i in price_book.bids:
            average.append(i.price)
    #for j in average:
    count = sum(average)
    mean = count / len(average)
    return(mean)


while True:
    avg = moving_avg(book)
    positions = e.get_positions()
    number = random.randint(0,2)
    print(number)
    for p in positions:
        if number == 1:
            e.insert_order(p, price=avg+1, volume=50, side='ask', order_type='limit')
        else:
            e.insert_order(p, price=avg-1, volume=50, side='bid', order_type='limit')
        
    
    # for p in positions:
    #     print(positions[p])
    #     if positions[p] >= 450:
    #         e.insert_order(p, price=avg+1, volume=50, side='ask', order_type='limit')
    #         continue
    #     else: 
    #         if positions[p] <= -450:
    #             e.insert_order(p, price=avg-1, volume=50, side='bid', order_type='limit')
    #             continue
         
    # e.insert_order(p, price=avg+1, volume=25, side='bid', order_type='limit')
