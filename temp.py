from scipy import signal
import numpy as np

x = np.arange(0, 10, 0.01)
y = signal.square((np.pi*x)*1) + 1

i = 0
counter = 0
while y[i] == 2:
    counter+=1
    i+=1
print(counter)