#!/usr/bin/python

"""
Category: Python Nornig Config Script
Author: nouse4it <github@schlueter-online.net>

csv_to_yaml_inventory.py
Illustrate the following conecepts:
- Create a Inventory in YAML for using with Nornig from CSV

v1 23.07.2020: Filter to Location and Switch Type
v2 28.08.2020: Filter to all Locations too and to Switchmodel
v3 11.12.2020: Added differantiation of Platforms for NX-OS
v4 07.01.2021: Added method to assign groups depending on location in hostname
"""

__author__ = "nouse4it"
__author_email__ = "github@schlueter-online.net"
__copyright__ = "Copyright (c) 2020 nouse4it"

# Importing all needed Modules
import os,sys,subprocess
import yaml

#==============================================================================
def read_devices( devices_filename ):

    devices = {}  # create our dictionary for storing devices and their info
    locations = ['xxx', 'yyy', 'zzz'] # location list to match hostnames against for group assingment

    devices_file = devices_filename.splitlines()

    for device_line in devices_file:

        device_info = device_line.split(',')  #extract device info from line

        loccheck = [loc for loc in locations if(loc in device_info[1])] # list comprehenssion used for checking if hostname contains string from list locations
        location = ' '
        location.join(loccheck)

        if "sw-nx" in device_info[1]:

            device = {'hostname': device_info[0],
                      'platform': 'nxos_ssh',
                      'name':   device_info[1],
                      'groups': [device_info[2],location.join(loccheck)]} # create dictionary of device objects ..., [] is used so that value is used as a list inside yaml-file, [2] is used to get correct value from kl

            devices[device['name']] = device  # store our device in the devices dictionary

        else:
            device = {'hostname': device_info[0],
            'platform': 'ios',
            'name':   device_info[1],
            'groups': [device_info[2],location.join(loccheck)]}

            devices[device['name']] = device  # store our device in the devices dictionary
                                               # note the key for devices dictionary entries is name
    return devices
#==============================================================================
def filter_location():
    while True:
        sw_loc = input('Location of Switches (Please enter location code!) Leave blank for all switches: ')
        if sw_loc in ('xxx', 'yyy', 'zzz', ''):
            break
        else:
            print('Only followoing values are accepted: xxx, yyy, zzz')
    
    return(sw_loc)
#==============================================================================
def filter_switch_type():
    while True:
        sw_type = input('Type of Switches (Please enter Type code f.e. "a" for access switch): ')
        if sw_type in ('a', 'c'):
            break
        else:
            sw_type = "''"
            print('All Switch Type will be used!')
            break
    
    return(sw_type)
#==============================================================================
def filter_switch_model():
    while True:
        sw_model = input('If you want to filter to certain Model, please Type in Model f.e. 2960X: ')
        if sw_model in ("2960X", "9300L", "3560", "3750", "3850"):
            break
        else:
            sw_model = "''"
            break

    return(sw_model)
#==============================================================================
#==============================================================================
# ---- Main: Run Commands
#==============================================================================

sw_loc = filter_location()
sw_type = filter_switch_type()
sw_model = filter_switch_model()


print(sw_loc)
print(sw_model)
print(sw_type)

if sw_type == "''":
    output_yml = input('Please enter desired Filename for YAML-Inventory SW-Type empty recognized: ')
    command = 'tail -n +2 /opt/nms/etc/kl | grep -i {}sw- | grep -i {} | cut -d, -f1-2,4'.format(sw_loc,sw_model) 
    kl = subprocess.getoutput(command)
    devices = read_devices(kl)
    
    with open(output_yml, 'w') as f:
        data = yaml.dump(devices, f)
    print(yaml.dump(devices))

else:
    output_yml = input('Please enter desired Filename for YAML-Inventory: ')
    command = 'tail -n +2 /opt/nms/etc/kl | grep -i {}sw- | grep -i ,{}, | grep -i {} | cut -d, -f1-2,4'.format(sw_loc,sw_type,sw_model) 
    kl = subprocess.getoutput(command)
    devices = read_devices(kl)

    with open(output_yml, 'w') as f:
        data = yaml.dump(devices, f)
    print(yaml.dump(devices))
