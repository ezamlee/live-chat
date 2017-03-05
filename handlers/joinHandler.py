from tornado import web,ioloop
from pymongo import *
import os

class joinHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		client = MongoClient()
		userid  = self.get_query_arguments("userid")[0]
		groupid = self.get_query_arguments("groupid")[0]
		print("uiiiiiid",uid)
		print("Giiiiiid",groupid)

		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups

		
		print("groupid",groupid);
		joingrp = collec_groups.find({"groupType":"public","_id":groupid},{"groupmember":1,"groupName":1,"_id":1,"image":1})
		result = collec_groups.update_one({'_id':groupid}, {'$push': {"groupmember":[userid,0]}})
		res = collec_groups.find({"groupType":"public","_id":gid},{"groupmember":1,"groupName":1,"_id":1,"image":1})
		self.write(res)

	



app = web.Application(
    [(r"/join",joinHandler)],
    static_path='static',
    debug=True
    )

app.listen(7888)
ioloop.IOLoop.current().start()