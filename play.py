import os
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import time, localtime
from time import sleep
# from time import ctime

intensity_val = 55

black_col = (0,) * 3
white_col = ((intensity_val, intensity_val, intensity_val))
red_col = ((intensity_val, 0, 0))
green_col = ((0, intensity_val, 0))
blue_col = ((0, 0, intensity_val))
yellow_col = ((intensity_val, intensity_val, 0))
cyan_col = ((0, intensity_val, intensity_val))
magenta_col = ((intensity_val, 0, intensity_val))

house_temp_col = ((110, intensity_val, 0))
house_raus_col = ((0, intensity_val, intensity_val))
cal_col = blue_col
hor_col = white_col

def paint_row(row, num, max_bits = 8, color = white_col):
    bit_pos = 7
    while max_bits > 0: 
        hat.set_pixel(bit_pos, row, color if num & 1 else (0, 0, 0))
        bit_pos -= 1
        max_bits -= 1
        num >>= 1

def paint_col(col, num, max_bits = 8, color = white_col):
    bit_pos = 7
    while max_bits > 0:
        hat.set_pixel(col, bit_pos, color if num & 1 else (0,) * 3)
        bit_pos -= 1
        max_bits -= 1
        num >>= 1



PIXLS_DOW = ((2,3), (2,2), (2,1))

def dow(num, color):
    for pix in PIXLS_DOW:
        hat.set_pixel(pix[0], pix[1], color if num & 1 else (0,) * 3)
        num >>= 1

# def get_ip():
#    return os.system("ip addr show dev wlan0 | sed -n -e '3,4p' | cut -d " " -f 6")

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python
import psutil

def get_cpu():
    return int(psutil.cpu_percent())

def get_ram():
    return int(psutil.virtual_memory().percent)

# Start HAT

hat = SenseHat()

def clear_hat():
    hat.clear((0,) * 3)

clear_hat()


# Entre loop in wawtch mode 

face = 'watch' # False for orientation etc

while True:
    for event in hat.stick.get_events():
        if event.action != ACTION_RELEASED:
            # print("The joystick was {} {}".format(event.action, event.direction))
            if event.direction == 'down':
                face = 'imu'
            elif event.direction == 'left':
                face = 'cpu'
            elif event.direction == 'right':
                face = 'message'
            else:
                face = 'watch'
            clear_hat()

    if face == 'watch':
        now = time()
        tim = localtime(now) 
        y = tim.tm_year % 2000
        m = tim.tm_mon
        d = tim.tm_mday
        w = tim.tm_wday
        h = tim.tm_hour
        min = tim.tm_min
        sec = tim.tm_sec
        paint_row(0, y, 7, cal_col) 
        paint_row(1, m, 4, cal_col) 
        paint_row(2, d, 5, cal_col) 
        paint_row(3, h%12, 5, hor_col) 
        hat.set_pixel(3, 3, red_col if h//12 else (0,) * 3)
        paint_row(4, min, 6, hor_col) 
        paint_row(5, sec, 6, hor_col) 
        temp = hat.get_temperature()
        paint_row(6, int(temp), 6, house_temp_col)
        hum = hat.get_humidity()
        paint_col(1, int(hum), 8, (0, intensity_val, 0))
        pres= hat.get_pressure()
        paint_col(0, int(pres) >> 2, 8, (intensity_val, intensity_val, 0))
        dow(w + 1, (intensity_val, 0, intensity_val))
        north = hat.get_compass()
        if north >= 180: north = -(360 - north)
        paint_row(7, int(abs(north)) >> 2, 6, cyan_col if north > 0 else blue_col)

    elif face == 'imu':

        hat.set_imu_config(True, True, True)

        orientation_deg = hat.get_orientation_degrees()
        #print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_deg))

        roll = int(orientation_deg.get('roll', 0))
        if roll >= 180: roll = -(360 - roll)
        paint_row(0, abs(roll), 8, (intensity_val, 0, 0) if roll > 0 else (0, intensity_val, 0))

        pitch = int(orientation_deg.get('pitch', 0))
        if pitch >= 180: pitch = -(360 - pitch)
        paint_row(1, abs(pitch), 8, (intensity_val, 0, 0) if pitch > 0 else (0, intensity_val, 0))

        yaw = int(orientation_deg.get('yaw', 0))
        if yaw >= 180: yaw = -(360 - yaw)
        paint_row(2, abs(yaw), 8, (intensity_val, 0, 0) if yaw > 0 else (0, intensity_val, 0))

    elif face == 'cpu':
        ip = get_ip()
        for i, octet in enumerate(ip.split('.')):
            paint_row(i, int(octet), 8, cyan_col)
        paint_row(4, get_cpu(), 8, red_col)
        paint_row(5, get_ram(), 8, yellow_col)

    elif face == 'message':
        hat.show_message('Me gusta este aparato', text_colour=blue_col)
    sleep(1)



