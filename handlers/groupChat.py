from tornado import web,websocket
from pymongo import *
import time
import json
import ast

phonebook={}

class WSHandler(websocket.WebSocketHandler):
	def open(self):
		pass
	def on_message(self,msg):
		client_msg = ast.literal_eval(msg)

		msg_type = str(client_msg['type'])
		gid 	 = int(client_msg['gid'])
		if msg_type == 'set':
			try:
				phonebook.gid.append(self)
			except KeyError:
				phonebook.gid =[]
				phonebook.gid.append(self)
		if msg_type == 'send':
			for handler in phonebook.gid:
				response =  str(client_msg['name']) + " : " + str(client_msg['msg'])
				handler.write(response)
	def close(self):
		for key in phonebook.keys():
			for handler in phonebook.key:
				if handler == self:
					phonebook.key.remove(self)
