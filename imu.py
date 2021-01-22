from sense_hat import SenseHat

hat = SenseHat()
hat.clear((0,) * 3)
# hat.set_imu_config(True, True, True)

# Display the letter J

# while True:
    # acceleration = sense.get_accelerometer_raw()
    # x = acceleration['x']
    # y = acceleration['y']
    # z = acceleration['z']

    # x=round(x, 0)
    # y=round(y, 0)
    # z=round(z, 0)
	
    # print("x={0}, y={1}, z={2}".format(x, y, z))

# Update the rotation of the display depending on which way up the Sense HAT is
    # if x  == -1:
    #     sense.set_rotation(180)
    # elif y == 1:
    #     sense.set_rotation(90)
    # elif y == -1:
    #   sense.set_rotation(270)
    # else:
    #     sense.set_rotation(0)

rep = 0
while True:
    # orientation_deg = hat.get_orientation()
    raw = hat.get_orientation()
    if rep == 20:
        # print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_deg))
        print(raw)
        # print(raw)
        rep = 0
    rep += 1
