#!/usr/bin/python3
__author__ = "nouse4it"
__author_email__ = "github@schlueter-online.net"
__copyright__ = "Copyright (c) 2020 nouse4it"

"""
Category: Python Nornig  Script
Author: nouse4it <github@schlueter-online.net>

nornir_create_inventory.py
Illustrate the following conecepts:
- Create a detailed YAML Inventory including IOS Version and Serial Number
"""

# Importing all needed Modules
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from nornir.core.filter import F
import getpass
import os,sys
import yaml

nr = InitNornir(config_file="/home/<username>/config_files/nornir/nornir3_config.yaml")

access_user = input('Enter Access Username: ') # Enter Username for Access Switch
access_password = getpass.getpass(prompt ="Access Switch password: ") # Enter password for Device in Access Group in Hosts.yaml

nr.inventory.groups['a'].username = access_user # set Username for Access Switch Group
nr.inventory.groups['a'].password = access_password # set password for Access Switch Group

core_user = input('Enter Core Username: ') # Enter Username for Core Switch
core_password = getpass.getpass(prompt ="Core Switch password: ") # Enter password for Device in Core Switch Group in Hosts.yaml

nr.inventory.groups['c'].username = core_user # set Username for Core Switches Group
nr.inventory.groups['c'].password = core_password # set password for Core Switches Group

#==============================================================================
# Get Facts from Devices
def get_facts(task):
    r = task.run(task=napalm_get, getters=['facts'])
    
    return r
#==============================================================================
#Create Inventory for YAML Creation
def read_devices(get_facts):

    devices = {}  # create our dictionary for storing devices and their info

    for host, task_result in r.items():
        if  host in nr.data.failed_hosts:
            continue
        else:
            hostname = task_result[1].result['facts']['hostname']
            os_version_str = task_result[1].result['facts']['os_version']
            if 'IOS-XE Software' in os_version_str:
                os_version = os_version_str.split(',')[2].lstrip()
            elif ',' in os_version_str:
                os_version = os_version_str.split(',')[1].lstrip()
            else:
                os_version = task_result[1].result['facts']['os_version']
            sn = task_result[1].result['facts']['serial_number']
            model = task_result[1].result['facts']['model']

        device = {'hostname': hostname,
                  'IOS':   os_version,
                  'SN': sn,
                  'Model': model} # create dictionary of device objects

        devices[device['hostname']] = device  # store our device in the devices dictionary
                                          # note the key for devices dictionary entries is name
    return devices
#==============================================================================
# Create YAML
def create_inventory(devices):
    output_yml = input('Please enter desired Filename for YAML-Inventory: ')
    with open(output_yml, 'w') as f:
        data = yaml.dump(devices, f)
    print(yaml.dump(devices))
#==============================================================================
# ---- Main: Run Commands
#==============================================================================

r = nr.run(task=get_facts)
devices = read_devices(r)
create_inventory(devices)
