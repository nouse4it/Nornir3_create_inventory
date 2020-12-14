#!/usr/bin/python3
__author__ = "Benjamin Schlüter"
__author_email__ = "benjamin.schlueter@hirschvogel.com"
__copyright__ = "Copyright (c) 2020 Benjamin Schlüter (ITT4 / Hirschvogel Holding GmbH)"

"""
Category: Python Nornig  Script
Author: Benjamin Schlüter <benjamin.schlueter@hirschvogel.com>

nornir_create_inventory.py
Illustrate the following conecepts:
- Create a detailed YAML Inventory for using with Nornig from HIVO-KL
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

nr = InitNornir(config_file="/home/schlueterbe/config_files/nornir/nornir3_config.yaml")

access_user = input('Enter Access Username: ') # Enter Username for Access Switch
access_password = getpass.getpass(prompt ="Access Switch password: ") # Enter password for Device in Access Group in Hosts.yaml

nr.inventory.groups['a'].username = access_user # set Username for Access Group
nr.inventory.groups['a'].password = access_password # set password for Core Group

core_user = input('Enter Core Username: ') # Enter Username for Access Switch
core_password = getpass.getpass(prompt ="Core Switch password: ") # Enter password for Device in Access Group in Hosts.yaml

nr.inventory.groups['c'].username = core_user # set Username for Access Group
nr.inventory.groups['c'].password = core_password # set password for Core Group

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
                  'Model': model} # create dictionary of device objects ..., [] is used so that value is used as a list inside yaml-file, [2] is used to get correct value from kl

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