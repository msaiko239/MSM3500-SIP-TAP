#!/usr/bin/env python3

import serial
import re
from time import sleep
import logging
import logging.handlers
from configparser import ConfigParser
import sys
import asterisk
import asterisk.agi
from asterisk.agi import *

config = ConfigParser()
config.read('/var/www/html/config.ini')
LOG_LEVEL = logging.info('LOGGING', 'level')

# Initialize logging
LOGGER = logging.getLogger('axi')
LOGGER.setLevel(logging.INFO)
formatter = logging.Formatter('|%(asctime)s|%(levelname)-8s|%(name)s|%(message)s')
log_file = logging.handlers.TimedRotatingFileHandler('/var/log/axi/input.csv', when='midnight', backupCount=7)
log_file.setLevel(logging.INFO)
log_file.setFormatter(formatter)
LOGGER.addHandler(log_file)

# Only print to console if at DEBUG level
if LOG_LEVEL == 'DEBUG':
    log_console = logging.StreamHandler()
    log_console.setLevel(logging.INFO)
    log_console.formatter(formatter)
    LOGGER.addHandler(log_console)

BAUD = config.get('USB_Settings', 'baudrate')
PTY = config.get('USB_Settings', 'parity')
STPB = int(config.get('USB_Settings', 'stopbits'))
BTSZ = int(config.get('USB_Settings', 'bytesize'))

#agi = AGI()

pin = (sys.argv[1])
msg = (sys.argv[2])

geekspeak = {
    "<ESC>": '\\x1b',
    "<ETX>": '\\x03',
    "<CR>": '\\r',
    "<ACK>": '\\x06',
    "<NAK>": '\\x15',
    "<EOT>": '\\x04',
    "<STX>": '\\x02'
}

htmlspeak = {
    "&ltESC&gt": '\\x1b',
    "&ltETX&gt": '\\x03',
    "&ltCR&gt": '\\r',
    "&ltACK&gt": '\\x06',
    "&ltNAK&gt": '\\x15',
    "&ltEOT&gt": '\\x04',
    "&ltSTX&gt": '\\x02'
}


def str2geek(string):
    geekstr = str(string)
    for key, value in geekspeak.items():
        if key in geekstr:
            geekstr = geekstr.replace(key, value)
    return geekstr


def geek2str(string):
    sstr = str(string)
    for key, value in geekspeak.items():
        if value in sstr:
            sstr = sstr.replace(value, key)
    return sstr


def html2str(string):
    hstr = str(string)
    for key, value in htmlspeak.items():
        if value in hstr:
            hstr = hstr.replace(value, key)
    return hstr

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=BAUD,
    stopbits=(STPB),
    bytesize=(BTSZ),
    parity=(PTY),
    timeout=1)


ser.write(b'\r')
sleep(0.5)
ser.write(b'\x1bPG1\r')
resp1=(ser.readline())
if resp1:
	sleep(0.5)
	strng=(pin)+(msg)
	#New Code for Checksum
	list_ascii=[ord(i) for i in strng]
	#Prints each car decimal value
	#print(list_ascii)
	b=sum(list_ascii)+31
	#Convert sum to 12 bit binary and parse to 4 sections frist 4 middle 4 last 4
	h1=(bin(b)[2:].zfill(12)[8:])
	h2=(bin(b)[2:].zfill(12)[4:8])
	h3=(bin(b)[2:].zfill(12)[0:4])
	#Adds 48 decimal value per TAP 1.8
	i1=(int(h1, 2)+48)
	i2=(int(h2, 2)+48)
	i3=(int(h3, 2)+48)
	#Prints checksum value
	chks=chr(i3)+chr(i2)+chr(i1)
	LOGGER.info('---Pin:' + pin + ' - ' + 'Message:' + msg + ' - checksum:' + chks)
	ser.write('\x02'.encode() + (pin).encode() + '\r'.encode() + msg.encode() + '\r\x03'.encode() + (chks).encode() + '\r'.encode())
	resp=str(ser.readline())
	if '15' in resp:
		LOGGER.info('page not accepted')
	else:
		sleep(0.5)
		ser.write(b'\x04\r')
		sleep(0.5)
		LOGGER.info('---Page Accepted' + ' - checksum:' + chks)
else:
	LOGGER.info('Page Encoder Not Repsonding')