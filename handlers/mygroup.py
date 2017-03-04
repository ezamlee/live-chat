from tornado import web,ioloop
from pymongo import *
import os

class mygroupHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		client = MongoClient()
		uid  = self.get_query_arguments("userid")[0]
		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups

		query = collec_groups.find({},{"groupmember":1,"groupName":1,"_id":1,"image":1})
		groupnames = []
		groupid = []
		groupstat=[]
		groupimage=[]
		for doc in query:
				for array in doc['groupmember']:
					if int(array[0]) == (int(uid)):
						groupnames.append(doc['groupName'])
						groupid.append(doc['_id'])
						groupstat.append(int(array[1]))
						groupimage.append(doc['image'])

		dict_ret ={}
		dict_ret['groupnames']= groupnames
		dict_ret['groupid']= groupid
		dict_ret['groupstat']= groupstat
		dict_ret['groupimage']=groupimage

		self.write(dict_ret)



app = web.Application(
    [(r"/mygroup", mygroupHandler)	],
    static_path='static',
    debug=True
    )

app.listen(6888)
ioloop.IOLoop.current().start()