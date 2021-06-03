# Execute Multiple CLI Commands on Multiple Network Devices

# Introduction
This is a simple script that uses the [Netmiko](https://pypi.org/project/netmiko/) library in combination with a simple configuration file to execute multiple commands on multiple devices and capture the output to a file.

## Why?
This script was written to aid an NX-OS upgrade where I didn't have GIR (Graceful Insertion and Removal) available and therefore had no "snapshot" capability and wanted to take some pre and post statistics that could be diff'd. There were several VDCs and so this script ensured the same commands were executed across all devices in a consistent manner, as well as saving time during the maintenance window.

# Requirements
* Python 3 (tested on Linux only but should work on macOS and Windows).
* Netmiko Python library.
* ConfigParser Python library.

# Installation
1. Clone this repository.
2. Install Python requirements via pip3: `pip3 install -r requirements.txt`

# Usage
A configuration file is required which contains the hosts to connect to and the commands to execute. The configuration file is in INI format. An example configuration file is included in the repository. If the configuration file contains an `[all]` section, any commands here will be executed on all devices.

## Required arguments:
* `-c <config file>` / `--config <config file>`: The configuration file to use.
* `-o <output file` / `--output <outputfile>`: The file to write the output to.

## Optional arguments:
* `-u <username>` / `--username <username>`: The username to log in to the device with. If not specified uses the username of the user executing the script.
* `-d <device type>` / `--device <device type>`: The device type of the devices in the configuration file. Defaults to 'cisco_nxos'. If the device type is '?', a list of supported platforms will be displayed.

# Limitations
1. The device type can only be specified as an argument and not in the configuration file (i.e. per device).
2. It is assumed the user will have an appropriate privilege level and doesn't need to elevate.
