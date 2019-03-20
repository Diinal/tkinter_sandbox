import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

freq = 0.1
amp = 0.5
x = np.arange(0, 100, 0.1)
y_signal = np.sin(x*freq) *amp + 0.5

y_max = max(y_signal)
y_carry = np.sin(x)*(y_signal/y_max)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(-1, 1)

line, = ax.plot(x, y_signal)
line1, = ax.plot(x, y_carry)
plt.show()