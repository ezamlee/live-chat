from tornado import web,ioloop
from pymongo import *
import os
import json


class allgroupsHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		#connection
		client = MongoClient()
		db_livechat = client.livechat

		#get logged user id
		uid  = int(self.get_query_arguments("userid")[0])
		#get collection
		collec_groups = db_livechat.groups
		#get data of "groups" collection
		query = collec_groups.find({"groupType":"public"},{"groupmember":1,"groupName":1,"_id":1,"image":1})

		groupid =[]
		groupnames =[]
		groupimage =[]
		groupstat  =[]
		list_ret   ={}

		for doc in query:
			for array in doc['groupmember'] :
				if array[0] != uid :
					groupid.append(doc['_id'])
					groupnames.append(doc['groupName'])
					groupstat.append(array[1])
					groupimage.append( doc['image'] )
		print("groupnames",groupnames)
		
     
		list_ret['groupid'] = set(groupid )
		list_ret['groupnames'] = set(groupnames)
		list_ret['groupstat'] = set(groupstat)
		list_ret['groupimage'] = set(groupimage)

		def jdefault(o):
			    if isinstance(o, set):
			        return list(o)
			    return o.__dict__
					 
		res = json.dumps(list_ret,default=jdefault)
		self.write(res)

class mygroupHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		#connection
		client = MongoClient()
		db_livechat = client.livechat

		#get login user id
		uid  = int(self.get_query_arguments("userid")[0])

		#get collection
		collec_groups = db_livechat.groups

		#get data of "groups" collection
		query2 = collec_groups.find({"groupType":"public"},{"groupmember":1,"groupName":1,"_id":1,"image":1})

		groupid2 =[]
		groupnames2 =[]
		groupimage2 =[]
		groupstat2  =[]
		list_ret2   ={}

		for doc2 in query2:
			for array2 in doc2['groupmember'] :
				if int(array2[0]) == uid:
					groupid2.append(doc2['_id'])
					groupnames2.append(doc2['groupName'])
					groupstat2.append(int (array2[1]) )
					groupimage2.append( doc2['image'] )

		print("groupnames2",groupnames2)
		list_ret2['groupid'] = set(groupid2 )
		list_ret2['groupnames'] = set(groupnames2)
		list_ret2['groupstat'] = set(groupstat2)
		list_ret2['groupimage'] = set(groupimage2)

		def jdefault(o):
			    if isinstance(o, set):
			        return list(o)
			    return o.__dict__
					 
		res2 = json.dumps(list_ret2,default=jdefault)
		self.write(res2)

class joinHandler(web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		#connection 
		client = MongoClient()
		db_livechat = client.livechat

		#get login user id & group id
		userid  = int(self.get_query_arguments("userid")[0])
		groupid = int(self.get_query_arguments("groupid")[0])

		#get collection
		collec_groups = db_livechat.groups

		joingrp   = collec_groups.update({"groupType":"public","_id":(groupid+1)},{"$push":{"groupmember":[userid,1]}})
		self.write("")

class leaveHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		
		# DB connection 
		client = MongoClient()
		db_livechat = client.livechat

		#get collection
		collec_groups = db_livechat.groups

		# get login user id & group id
		userid  = int(self.get_query_arguments("userid")[0])
		groupid = int(self.get_query_arguments("groupid")[0])

		groupmembersCur = collec_groups.find({"_id":groupid},{"groupmember":1,"_id":0})

		# members ids
		res_arr=[]
		for iobject in groupmembersCur:
			for arr in iobject["groupmember"]:
				res_arr.append(arr[0])
			
		for id in res_arr:
			if ( userid == id ):
				leavegrp  = collec_groups.update({"groupType":"public","_id":groupid},{"$pull":{"groupmember":[userid,1]}})
		self.write("") 

class createHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		# DB connection 
		client = MongoClient()
		db_livechat = client.livechat

		#get collection
		collec_groups = db_livechat.groups
		
		# Get data from URL
		userid  = int(self.get_query_arguments("userid")[0])
		grpName = self.get_query_arguments("groupName")[0]
		grpImg  = self.get_query_arguments("groupImg")[0]
	
		max_id  = int(collec_groups.find_one({"$query":{},"$orderby":{"_id":-1}},{"_id":1})["_id"])
		group_id = max_id+1
		arri = []
		arrk = [userid,1]
		arri.append(arrk)
		creategrp  = collec_groups.insert({"_id":group_id,"groupmember":arri,"groupType":"public","groupName":grpName,"image":grpImg})
		self.write("")

app = web.Application(
    [(r"/allgroups",allgroupsHandler),(r"/mygroups",mygroupHandler),(r"/join",joinHandler),(r"/leave",leaveHandler),(r"/create",createHandler)],
    static_path='static',
    debug=True
    )

app.listen(1111)
ioloop.IOLoop.current().start()