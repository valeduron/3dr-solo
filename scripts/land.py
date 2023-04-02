import dronekit
from dronekit import  connect, VehicleMode, LocationGlobalRelative
import time
import socket
import exceptions
import argparse
import sys

def connectMyCopter():

    target = sys.argv[1] if len(sys.argv) >= 2 else 'udpout:10.1.1.10:14560'
    print('Connecting to ' +  target + '....')
    vehicle = connect(target, wait_ready=False)

    return vehicle

#Mission

vehicle=connectMyCopter()
print("About to land..")

vehicle.mode=VehicleMode("LAND")

time.sleep(2)

print("End of function")
print("Arducopter version: %s"%vehicle.version)

while True:
    time.sleep(2)

vehicle.close()
