# Nawapon Nuangjumnong <3

import pymycobot
from pymycobot import MyAgv
from time import sleep

# ----------- DEVICE SETUP -----------
# parameters
# - comport: serial port to connect to device. eg. ttyAMA2 = motors
# - buadrate: default value is 115200
# - timeout: default value is 0.1
# - debug: default value is False
ama2 = MyAgv(comport="/dev/ttyAMA2")


# ------------- STARTING -------------
print("\n------ Starting... ------")


# ---------- CHECKING DEVICE ----------
# led turn red and blinking during checking
ama2.set_led(2, 255,0,0)

# show device status and detail
sleep(3)
print("pymycobot version: ",pymycobot.__version__)
print("Firmware version: ", ama2.get_firmware_version())

# everything working! led turn static green
sleep(1)
ama2.set_led(1, 0,255,0)

# ---------- BASIC MOVE COMMAND ----------
# parameters
# - 1: speed (1-127)
# - 2: timeout (second)

# move forward
# ama2.go_ahead(127, 5)

# move backward
# ama2.retreat(5, 3)

# pan to the left
ama2.pan_left(127, 4)

# pan to the right
# ama2.pan_right(10, 5)

# rotate clockwise
ama2.clockwise_rotation(127, 5)

# rotate counter clockwise
# ama2.counterclockwise_rotation(15, 3)

# turn led to blue color as stand by mode
sleep(1)
ama2.set_led(1, 0,0,255)


# -------------- END --------------
print("\n---------- End ----------")