#!/usr/bin/env python3

import os
import sys

if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soma.settings')
	os.environ.setdefault('SOMA_HOME', 'soma_home')
	try:
		os.mkdir(os.environ['SOMA_HOME'])
	except OSError:
		pass

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
