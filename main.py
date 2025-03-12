import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from iks01a3.hts221 import HTS221
from plot_config_api.hts221 import HTS221Config

# sensor config
hts221 = HTS221(1)
hts221.power_on()
hts221.set_bdu()
hts221.set_odr()

ROWS_NUMBER = 2
COLS_NUMBER = 1

SAMPLES_NR = 100
TIME_MIN = 0
TIME_MAX = 10

fig, (humidity_ax, temperature_ax) = plt.subplots(nrows=ROWS_NUMBER, ncols=COLS_NUMBER)

time_s = np.linspace(TIME_MIN, TIME_MAX, SAMPLES_NR)
humidity_y = [0] * SAMPLES_NR
temperature_y = [0] * SAMPLES_NR

hts221_config = HTS221Config("./plot_config_json/hts221_config.json")


def update(axis, values, new_value, config_dict):
    axis.clear()
    axis.set_xlim(config_dict["xlim"]["left"], config_dict["xlim"]["right"])
    axis.set_ylim(config_dict["ylim"]["bottom"], config_dict["ylim"]["top"])
    axis.set_title(config_dict["title"]["label"], loc=config_dict["title"]["loc"])
    axis.set_xlabel(config_dict["xlabel"]["xlabel"], loc=config_dict["xlabel"]["loc"])
    axis.set_ylabel(config_dict["ylabel"]["ylabel"], loc=config_dict["ylabel"]["loc"])
    axis.grid(config_dict["grid"]["visible"])
    del values[-1]
    values.insert(0, new_value)
    axis.plot(time_s, values)


def animate(i):
    update(humidity_ax, humidity_y, hts221.read_humidity(), hts221_config.get_humidity_dict())
    update(temperature_ax, temperature_y, hts221.read_temperature(), hts221_config.get_temperature_dict())


if __name__ == '__main__':
    ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)
    mng = plt.get_current_fig_manager()
    mng.set_window_title("iks01a3 sensor readings")
    mng.window.state('zoomed')
    plt.show()
