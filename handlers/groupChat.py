from tornado import web,websocket,ioloop
from pymongo import *
import time
import json
import ast

phonebook={}

class WSHandler(websocket.WebSocketHandler):
	def open(self):
		print("connection opened")
	def on_message(self,msg):
		print(msg)
		client_msg = ast.literal_eval(msg)

		msg_type = str(client_msg['type'])
		gid 	 = int(client_msg['gid'])
		print(msg_type)
		print(gid)
		if msg_type == 'set':
			try:
				phonebook[gid].append(self)
			except KeyError:
				phonebook[gid] =[]
				phonebook[gid].append(self)
			except AttributeError:
				phonebook[gid] = []
				phonebook[gid].append(self)
		if msg_type == 'send':
			print(msg)
			print(client_msg['name'])
			print(client_msg['msg'])
			for handler in phonebook[gid]:
				response =  str(client_msg['name']) + " : " + str(client_msg['msg'])
				print(response)
				handler.write_message(str(response))
		print(phonebook)
	def close(self):
		for key in phonebook.keys():
			for handler in phonebook[key]:
				if handler == self:
					phonebook[key].remove(self)
		print(phonebook)
		print("server closed")
class renderHandler(web.RequestHandler):
	def get(self):
		self.render("../templates/chat.html")

app = web.Application(
    [	(r"/",renderHandler),(r"/ws",WSHandler)  ],
    static_path='../static',
    debug=True
    )

app.listen(1234)
ioloop.IOLoop.current().start()
