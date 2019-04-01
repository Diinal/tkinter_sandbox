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
y_signal = np.sin(1*np.pi*x) + 1
y_max = max(y_signal)

y_carry = signal.square(5 * np.pi *x, duty = 0.5) + 1


fig = plt.figure()
ax = fig.add_subplot(411)
ax2 = fig.add_subplot(412)
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(414)

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
ax4.set_ylim(-3, 3)
ax4.spines['bottom'].set_position('center')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

line, = ax.plot(x, y_signal)
line1, = ax2.plot(x, y_carry)
line2, = ax3.plot(x, y_signal)

c_width = 0.5
y_max = 1
y_pwm = signal.square(10 * np.pi * 0.5 * x, duty=c_width*y_signal/(y_max*2)) + 1
line3, = ax3.plot(x, y_pwm)

line5, = ax4.plot(x, y_signal)
y_ppm = y_signal
y_ppm[:] = 0

prev = 0
for i, a in enumerate(y_pwm):
    if a == 0 and prev == 2:
        y_ppm[i-60:i-40] = 2
    prev = a

line4, = ax4.plot(x, y_ppm)



plt.show()