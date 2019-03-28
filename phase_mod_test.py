import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

freq = 1
amp = 1
carry_freq = 0.2
carry_amp = 1
x = np.arange(0, 20, 0.01)

#аналоговый сигнал
y_signal = np.sin(x*freq) *amp 
y_carry = 2*np.sin(2*np.pi*x)
#y_carry_phase_mod = 2*np.sin(2*np.pi*x - 2*np.cos(2*np.pi*0.25*x))
y_carry_phase_mod = 2*np.sin(2*np.pi*x - 2*y_signal)

fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax.set_ylim(-2, 2)
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2.set_ylim(-2, 2)
ax2.spines['bottom'].set_position('center')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

line, = ax.plot(x, y_signal)
line1, = ax2.plot(x, y_carry)
line2, = ax2.plot(x, y_carry_phase_mod)

plt.fill_between(x, y_carry_phase_mod,y_carry, color='grey', alpha='0.5')
plt.show()