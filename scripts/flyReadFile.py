#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time
import json
from dronekit import connect, VehicleMode, LocationGlobalRelative
import socket
import exceptions
import argparse
import sys

class Point:
  def __init__(self, index, lat, lng, alt, speed):
    self.index = index
    self.lat = lat
    self.lng = lng
    self.alt = alt
    self.speed = speed
    

def getFlightPlan():
   # val =input("Enter Flight Plan Name:") #
#    val = raw_input("Enter Flight Plan Name:")
#    f = open(val) 

    file = open("cord.txt", 'r')
    json_data = json.load(file)

    for index,element in enumerate(json_data):
      p = Point(json_data[index]['index'],json_data[index]['lat'],json_data[index]['lng'],json_data[index]['alt'],json_data[index]['speed'])
      points.append(p) 
    
    file.close()
    return points

# Set up option parsing to get connection string
def connectMyCopter():

# Connect to the Vehicle
    target = 'udpout:10.1.1.10:14560'
    print('Connecting to ' +  target + '....')
    vehicle = connect('udpout:10.1.1.10:14560', wait_ready=True)

    return vehicle


def goToPoint(point):
    print("Going towards point for 30 seconds ...")
    vehicle.airspeed = point.speed
    vehicle.simple_goto(LocationGlobalRelative(point.lat, point.lng, point.alt))
    print("XXXXXXXXXXXXXXXXXX")

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)



points = []
points = getFlightPlan()

vehicle=connectMyCopter()
print("About to takeoff..")

vehicle.mode=VehicleMode("GUIDED")

arm_and_takeoff(2)

print ("1")

for index, point in enumerate(points):
    goToPoint(point)
    # sleep so we can see the change in map
    time.sleep(10)

print("Returning to Launch")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()


