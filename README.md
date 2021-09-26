# nornir3_create_inventory
Create Inventory for Devices with Get Facts of NAPALM and create a YAML File with following Informations:
- Hostname
- OS Version
- Serial Number
- Device Model

Author: nouse4it <github@schlueter-online.net>

## Use Case Description

The script is intended to automatically gather facts from devices to create a inventory to store all gathered informations.
The script is able to perform the gathering of the facts on multiple devices in parallel.

# csv_to_yaml_inventory
Create an Nornir Inventory YAML file from a csv.

CSV should have the following format:

IP,HOSTNAME,SITE,SWITCH LAYER,MODEL,STACKDETAIL,SOFTWAREVERSION

If you have less data in the csv you may need to adapt the Script accordingly.

Author: nouse4it <github@schlueter-online.net>

## Use Case Description

The script is intended to automatically create Nornir Inventory from a CSV file.
Here the CSV file is called KL ("Komponenten Liste").
While running the Script you are asked about some filters you want to set for creating the file.
Leave everything blank if you want to create a YAML Inventory from all Devices of the CSV.


## Installation
Pleae use NORNIR Version 3.0
Following Packtes, Modules and Requirements are needed:
    
    nornir==3.0.0
    nornir-napalm==0.1.1
    nornir-netmiko==0.1.1
    paramiko==2.7.2
    
For more informations see ---> https://github.com/nornir-automation/nornir
Python Version must be at least v3.6.8

## Usage

## Getting help
