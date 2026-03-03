from robodk import robolink
import serial
import time

RDK = robolink.Robolink()
robot = RDK.Item("", robolink.ITEM_TYPE_ROBOT)

arduino = serial.Serial("COM7", 115200)
time.sleep(2)

print("Sistema listo")

while True:
    joints = robot.Joints()
    base_angle = joints[0]  # Joint 1 = Base

    arduino.write((str(base_angle) + "\n").encode())

    time.sleep(0.05)
