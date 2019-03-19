import math

x = [i for i in range(1280)]
y = [math.sin(i * 0.4) * 40 for i in x]
xy = list(zip(x, y))
for xy_ in sorted(xy):
    if xy_[1] == max(y):
        print(xy_)