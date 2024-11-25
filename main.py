import time
import numpy as np
from mss import mss
import pyautogui as pg
import keyboard

with open("config.txt", "r") as config:
    config_path = config.readline().strip()
    print(config_path)

with open(config_path) as config:
    program_name = config.readline().strip()
    xpos = int(config.readline())
    ypos = int(config.readline())
    mon_width = int(config.readline())
    mon_height = int(config.readline())
    color = [int(i) for i in config.readline().split(",")]
    tolerance = int(config.readline())
    script_control_key = config.readline().strip()
    start_stop_key = config.readline().strip()
    close_program_key = config.readline().strip()
    move_mouse = config.readline().strip()
    move_mouse = move_mouse.lower() == 'true'

print(f'config:{program_name}\n'
      f'xpos:{xpos}\n'
      f'ypos:{ypos}\n'
      f'window_size:{mon_width}x{mon_height}\n'
      f'color:{color}\n'
      f'gamma:{tolerance}\n'
      f'script_control_key:{script_control_key}\n'
      f'start_stop_key:{start_stop_key}\n'
      f'close_program_key:{close_program_key}\n'
      f'move_mouse:{move_mouse}\n')

#1366 768 - full monitor
monitor = {
    "left": xpos,
    "top": ypos,
    "width": mon_width,
    "height": mon_height
}
def find_color(color, monitor={}, tolerance=10):
    m = mss()
    img = m.grab(monitor)
    img_arr = np.array(img)

    r, g, b = color

    lower_bound = np.array([b - tolerance, g - tolerance, r - tolerance, 255])
    upper_bound = np.array([b + tolerance, g + tolerance, r + tolerance, 255])

    mask = np.all((img_arr >= lower_bound) & (img_arr <= upper_bound), axis=-1)
    indexes = np.where(mask)

    our_crd = np.transpose(indexes)
    m.close()
    return our_crd


def main():
    while True:
        if keyboard.is_pressed(start_stop_key):
            print("start")
            time.sleep(1)  #для корректной работы start_stop_key

            while True:
                result = find_color(color, monitor, tolerance=tolerance)
                if keyboard.is_pressed(start_stop_key):
                    print("stop")
                    break

                if len(result):
                    x_coord = result[0][1] + monitor.get('left')
                    y_coord = result[0][0] + monitor.get('top')
                    if move_mouse:
                        pg.moveTo(x_coord, y_coord)

                    pg.press(script_control_key)
                    print(f"\tColor was found:{str(x_coord)} {str(y_coord)}")

                time.sleep(0.01)
            time.sleep(1)
        if keyboard.is_pressed(close_program_key):
            break


if __name__ == "__main__":
    print(f"press {start_stop_key} to start...")
    main()
    print("Closed")
