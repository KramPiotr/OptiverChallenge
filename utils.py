import numpy as np

def weighted_average(sample, exponent, maximal_volume):
    """
	:param sample: list of (element, weight)
	:param exponent:
	:param maximal_volume: the sum of all the weights cannot exceed this value, otherwise the last ones are diminished.
	:return: weighted exponential average value
	"""
    sum = 0
    total_volume = 0
    for x, w in sample:
        if total_volume + w > maximal_volume: w = maximal_volume - total_volume
        sum += w * (x ** exponent)
        total_volume += w
        if total_volume >= maximal_volume: break
    return (sum / total_volume) ** (1 / exponent)

def switch_mean_and_std(sequence, new_mean, new_std):
    mean_diff = new_mean - np.mean(sequence)
    std_diff = new_std/np.std(sequence)
    new_sequence = [(s + mean_diff) * std_diff for s in sequence]
    return new_sequence

from time import sleep
while(True):
    sleep(0.5)
    print("nice")