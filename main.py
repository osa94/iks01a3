import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from iks01a3.hts221 import HTS221

# sensor config
hts221 = HTS221(1)
hts221.power_on()
hts221.set_bdu()
hts221.set_odr()

HUMIDITY_MIN = 0
HUMIDITY_MAX = 100

TEMPERATURE_MIN = -40
TEMPERATURE_MAX = 120

TIME_MIN = 0
TIME_MAX = 10

ROWS_NUMBER = 2
COLS_NUMBER = 1

SAMPLES_NR = 100

fig, (humidity_ax, temperature_ax) = plt.subplots(nrows=ROWS_NUMBER, ncols=COLS_NUMBER)

humidity_ax.grid()
humidity_ax.set_ylim(HUMIDITY_MIN, HUMIDITY_MAX)
humidity_ax.set_xlim(TIME_MIN, TIME_MAX)

temperature_ax.grid()
temperature_ax.set_ylim(TEMPERATURE_MIN, TEMPERATURE_MAX)
temperature_ax.set_xlim(TIME_MIN, TIME_MAX)

time_s = np.linspace(TIME_MIN, TIME_MAX, SAMPLES_NR)

humidity_y = [0] * SAMPLES_NR
temperature_y = [0] * SAMPLES_NR

def update(axis, values, new_value, title, x_name, y_name):
    axis.clear()
    axis.grid()
    axis.set_ylim(HUMIDITY_MIN, HUMIDITY_MAX)
    axis.set_xlim(TIME_MIN, TIME_MAX)
    axis.set_title(title, loc='left')
    axis.set_xlabel(x_name)
    axis.set_ylabel(y_name)
    del values[-1]
    values.insert(0, new_value)
    axis.plot(time_s, values)

def animate(i):
    update(humidity_ax, humidity_y, hts221.read_humidity(), 'Humidity', 'time', 'relative humidity [%]')
    update(temperature_ax, temperature_y, hts221.read_temperature(), 'Temperature', 'time', 'temperature °C')

if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)
    plt.show()