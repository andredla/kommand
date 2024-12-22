#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import sqlite3
import json
import base64
import subprocess
import time
import speech_recognition as sr

localPath = os.path.dirname(os.path.realpath(__file__))
lang = sys.argv[1]
sound = "/usr/share/sounds/ubuntu/notifications/Positive.ogg"
dev = False
flag_command = False

conn = sqlite3.connect(localPath+"/db.sqlite")
cur = conn.cursor()

def dbGetType(type):
	cur.execute("select * from database where type = '"+type+"'")
	rows = cur.fetchall()
	return rows

def commandEncodeDecode(data, encdec):
	if encdec == "encode":
		return base64.b64encode(data.encode("ascii")).decode("ascii")
	if encdec == "decode":
		return base64.b64decode(data).decode("ascii")
	return True

def talk(command, out):
	if flag_command:
		os.system("echo '"+out+"' | python3 "+os.path.join(localPath, "talk.py")+" '"+lang+"'")
	return True

def clearCommand(command, arr):
	command_out = command
	for a in arr:
		command_out = command_out.replace(a+" ", "")
	return command_out

def commandOk(command_in, type):
	row = None
	command = dbGetType(type)
	command_command = command[0][2]
	command_data = command[0][3]
	command_out = command_in
	if command_command:
		if command_in.startswith(command_command):
			command_out = clearCommand(command_in, [command_command])
		else:
			return row
	if command_data:
		data = json.loads(command_data)
		for row in data["data"]:
			if(command_out == row["word"]):
				return row
	row = None
	return row

def findCommand(cmd):
	global flag_command
	flag_command = False
	command_in = cmd.lower()
	command_out = command_in
	if flag_command == False:
		row = commandOk(command_in, "command")
		if row:
			flag_command = True
			if(row["talk"] != ""):
				talk(command_out, row["talk"])
			os.system(commandEncodeDecode(row["command"], "decode"))
	if flag_command == False:
		row = commandOk(command_in, "terminal")
		if row:
			flag_command = True
			if(row["talk"] != ""):
				talk(command_out, row["talk"])
			proc = subprocess.Popen("konsole", shell=True)
			time.sleep(1)
			os.system("xdotool type \""+commandEncodeDecode(row["command"], "decode")+"\"")
			os.system("xdotool key Return")
	return command_out

def ouvir_microfone(arg):
	command = ""
	mic = sr.Recognizer()
	with sr.Microphone() as source:
		mic.adjust_for_ambient_noise(source)
		print("Say something:")
		os.system("paplay --volume="+str(65536 * 50 / 100)+" "+sound)
		audio = mic.listen(source)
		try:
			command = mic.recognize_google(audio,language=arg)
			if dev:
				os.system("echo '"+command+"' >> "+localPath+"log.txt")
		except:
			print("Can you repeat please?")
		if command != "":
			findCommand(command)
			if(flag_command == False):
				os.system("qdbus org.kde.klipper /klipper setClipboardContents \""+command+"\"")
				print("Copy to clipboard...")
			else:
				sys.exit(2)
	return True

def main():
	while(True):
		ouvir_microfone(lang)
	return True

main()