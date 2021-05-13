#!/usr/bin/env python3
#
# Copyright (c) 2021 David Ramsden
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#

import sys, getopt, getpass
from netmiko import ConnectHandler
from configparser import ConfigParser

def usage():
	print(f'{__file__} -c <config ini> -o <output file> [-u <username>] [-d <device type>]')
	return

def command_header(switch, command, fh):
	print('*' * 80, file=fh)
	print(f'* {switch.upper()}: {command}', file=fh)
	print('*' * 80, file=fh)
	return

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'c:o:u:d:', ['config=', 'output=', 'username=', 'device='])
		if not len(opts):
			raise Exception('option missing')
	except Exception as err:
		usage()
		print(err)
		sys.exit(2)

	try:
		for opt, arg in opts:
			if opt in ('-c', '--config'):
				if arg is None:
					raise Exception('no config ini provided')
				config_file = arg
			elif opt in ('-o', '--output'):
				if arg is None:
					raise Exception('no output file provided')
				output_file = arg
			elif opt in ('-u', '--username'):
				if arg is None:
					raise Exception('no username provided')
				username = arg
			elif opt in ('-d', '--device')
				if arg is None:
					raise Exception('no device type provided')
				device_type = arg
			else:
				raise Exception('unknown option')
	except Exception as err:
		usage()
		print(err)
		sys.exit(2)

	# Instansiate ConfigParser.
	config = ConfigParser()

	# Get current user if the username option was not provided.
	try:
		username
	except NameError:
		username = getpass.getuser()

	# Get device type if specified, otherwise default to 'cisco_nxos'
	try:
		device_type
	except NameError:
		device_type = 'cisco_nxos'

	# Get password to use.
	password = getpass.getpass(f'Password for {username}: ')

	# Read config file.
	try:
		with open(config_file) as f:
			config.read_file(f)
			f.close()
	except Exception as err:
		print(f'Unable to read config file: {err}')
		sys.exit(2)

	# Open output file for writing.
	try:
		outfile = open(output_file, 'w')
	except Exception as err:
		print(f'Unable to open {output_file} for writing: {err}')
		sys.exit(2)

	# Parse each section, where a section represents a switch.
	for switch in config.sections():
		# Ignore the 'all' section.
		if switch == 'all':
			continue

		# Set up device to connect to.
		device = {
			'device_type': device_type,
			'host': config.get(switch, 'ip'),
			'username': username,
			'password': password,
			'fast_cli': True,
		}

		# Connect.
		print(f"Connecting to {switch.upper()} ({config.get(switch, 'ip')}):")
		try:
			net_connect = ConnectHandler(**device)
		except Exception as err:
			print(f'Unable to connect: {err}')
			continue

		# Execute commands from the 'all' section.
		for command in config.get('all', 'commands').split(','):
			print(f'\tSend: {command}')
			command_header(switch, command, outfile)
			print(net_connect.send_command(command), file=outfile)

		# Execute commands specific to this switch.
		for command in config.get(switch, 'commands').split(','):
			print(f'\tSend: {command}')
			command_header(switch, command, outfile)
			print(net_connect.send_command(command), file=outfile)

		# Disconnect.
		print('Disconnecting.')
		net_connect.disconnect()

	outfile.close()

if __name__ == '__main__':
	main()
