import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

freq = 1
amp = 1
carry_freq = 0.2
carry_amp = 1
x = np.arange(0, 10, 0.01)

#аналоговый сигнал
y_signal = np.sin(x*freq) *amp +1
y_max = max(y_signal)

y_carry = signal.square(10 * np.pi * 0.5 * x, duty=0.5) + 1


fig = plt.figure()
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax.set_ylim(-3, 3)
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2.set_ylim(-3, 3)
ax2.spines['bottom'].set_position('center')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax3.set_ylim(-3, 3)
ax3.spines['bottom'].set_position('center')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

line, = ax.plot(x, y_signal)
line1, = ax2.plot(x, y_carry)
line2, = ax3.plot(x, y_signal)

line3, = ax3.plot(x, signal.square(10 * np.pi * 0.5 * x, duty=(y_signal)*.5) + 1)


plt.show()