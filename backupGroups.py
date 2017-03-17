from tornado import web,ioloop
from pymongo import *
import os

class allgroupsHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		client = MongoClient()
		uid  = self.get_query_arguments("userid")[0]
		
		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups

		query = collec_groups.find({"groupType":"public"},{"groupmember":1,"groupName":1,"_id":1,"image":1})

		groupnames =[]
		groupid =[]
		groupstat =[]
		groupimage =[]

		for doc in query:
				for array in doc['groupmember']:
					if int( array[0] ) != (int (uid) ):
						groupnames.append(doc['groupName'])
						groupid.append(doc['_id'])
						groupstat.append(int (array[1]) )
						groupimage.append( doc['image'] )

		dict_ret = {}
		dict_ret['groupnames'] = groupnames
		dict_ret['groupid'] = groupid
		dict_ret['groupstat'] = groupstat
		dict_ret['groupimage'] = groupimage

		self.write(dict_ret)
		
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

		query = collec_groups.find({"groupType":"public"},{"groupmember":1,"groupName":1,"_id":1,"image":1})

		groupnames =[]
		groupid =[]
		groupstat =[]
		groupimage =[]

		for doc in query:
			print(doc)
			for array in doc['groupmember']:
				if int( array[0] ) == (int (uid) ):
					groupnames.append(doc['groupName'])
					groupid.append(doc['_id'])
					groupstat.append(int (array[1]) )
					groupimage.append( doc['image'] )

		dict_ret = {}
		dict_ret['groupnames'] = groupnames
		dict_ret['groupid'] = groupid
		dict_ret['groupstat'] = groupstat
		dict_ret['groupimage'] = groupimage

		self.write(dict_ret)

class joinHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		client = MongoClient()
		userid  = self.get_query_arguments("userid")[0]
		groupid = self.get_query_arguments("groupid")[0]
		#get data from URL
		print("uiiiiiid",userid)
		print("Giiiiiid",groupid)

		##DB connection 
		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups

		
		print("groupid",groupid);
		joingrp   = collec_groups.update({"groupType":"public","_id":int(groupid)},{"$push":{"groupmember":[int(userid),1]}})
		joined_db = collec_groups.find({"groupType":"public","_id":int(groupid)},{"groupmember":1,"groupName":1,"_id":1,"image":1})
		self.write("")

class leaveHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		
		# DB connection 
		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups

		# Get data from URL
		client = MongoClient()
		print("connected")
		userid  = self.get_query_arguments("userid")
		print("query userid",userid )
		groupid = self.get_query_arguments("groupid")[0]
		print("query groupid ",groupid)
		groupmembersCur = collec_groups.find({"_id":int(groupid)},{"groupmember":1,"_id":0})
		print("members",groupmembersCur)#cursor of objs

		#members ids
		res_arr=[]
		for iobject in groupmembersCur:
			for arr in iobject["groupmember"]:
				res_arr.append(arr[0])
			
		for id in res_arr:
			if ( userid == id ):
				leavegrp  = collec_groups.update({"groupType":"public","_id":int(groupid)},{"$pull":{"groupmember":[userid,1]}})
		self.write("") 

class createHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		
		# Get data from URL
		client  = MongoClient()
		userid  = self.get_query_arguments("userid")[0]
		# Get data from Body
		grpName = self.get_query_arguments("groupName")
		grpImg  = self.get_query_arguments("groupImg")
		
		
		# DB connection 
		client = MongoClient()
		db_livechat = client.livechat
		collec_groups = db_livechat.groups
	
		print("userid",userid);
		creategrp  = collec_groups.insert({"groupmember":"[[userid,1]]","groupType":"public","groupName":grpName,"image":grpImage})
		#created_db = collec_groups.find_one({"groupType":"public","groupName":grpName},{"groupmember":1,"groupName":1,"_id":1,"image":1})
		self.write(1)
	
app = web.Application(
    [(r"/allgroups",allgroupsHandler),(r"/mygroups",mygroupHandler),(r"/join",joinHandler),(r"/leave",leaveHandler),(r"/create",createHandler)],
    static_path='static',
    debug=True
    )

app.listen(1111)
ioloop.IOLoop.current().start()