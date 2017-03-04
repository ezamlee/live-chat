from tornado import web,ioloop
import os
from pymongo import MongoClient

class userHandler(web.RequestHandler):

	def get(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		
		#Query The DATA
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})
		
		#Construct JSON to send back to Client and count up data
		dic_coll ={}
		count = 0
		
		for value in frienddata['friend']:
			
			#Prepare a query to get each friend data
			dic_rep = {}
			username = value[0]
			query = usercol.find_one({"_id": int(username)},{"userName":1,"image":1,"_id":1})

			#append data in json sent file
			dic_rep['_id'] = int(query['_id'])
			dic_rep['userName'] = query['userName']
			dic_rep['img'] = query['image']
			dic_rep['status'] = int(value[1])

			dic_coll[count] = dic_rep
			count += 1
	

		#Send the final result
		self.write(dic_coll)


	def post(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		
		#Query The DATA
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})
		
		#Construct JSON to send back to Client and count up data
		dic_coll ={}
		count = 0
		
		for value in frienddata['friend']:
			
			#Prepare a query to get each friend data
			dic_rep = {}
			username = value[0]
			query = usercol.find_one({"_id": int(username)},{"userName":1,"image":1,"_id":1})

			#append data in json sent file
			dic_rep['_id'] = int(query['_id'])
			dic_rep['userName'] = query['userName']
			dic_rep['img'] = query['image']
			dic_rep['status'] = int(value[1])

			dic_coll[count] = dic_rep
			count += 1

		#Send the final result
		self.write(dic_coll)
