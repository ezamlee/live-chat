from tornado import web,ioloop
import os
from pymongo import MongoClient
from operator import sub

class FriendsHandler(web.RequestHandler):

	def get(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		
		#Query The DATA
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})

		#find all users the output cursor so use list or for loop
		allusers = list( usercol.find({}, {"friend": 0}) )
		
		
		#Construct JSON to send back to Client and count up data
		dic_coll ={}
		arrList = {}
		frnds = {}
		count = 0
		c = 0
		j = 0	

		for value in frienddata['friend']:
			#Prepare a query to get each friend data
			dic_rep = {}
			username = value[0]
			query = usercol.find_one({"_id": int(username)},{"_id":1})

			#append data in json sent file
			dic_rep['_id'] = int(query['_id'])
			
			dic_coll[count] = dic_rep
			count += 1

				
		for t in dic_coll:
			frnds[j] = t
			j +=1			
	
		

		#get all users
		for i in usercol.find({}, {"friend": 0, "image": 0, "userName": 0}):
			i = int(i["_id"])
			ID = int(allusers[i-1]['_id'])
			name = allusers[i-1]['userName']
			img = allusers[i-1]['image']
			
			if i  not in frnds:
				arr = {}
				arr["_id"] = ID
				arr['username'] = name
				arr["image"] = img
				
				arrList[c]  = arr						
				c += 1


		#Send the final result
		self.write(arrList)

	def post(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		
		#Query The DATA
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})

		#find all users the output cursor so use list or for loop
		allusers = list( usercol.find({}, {"friend": 0}) )
		
		
		#Construct JSON to send back to Client and count up data
		dic_coll ={}
		arrList = {}
		frnds = {}
		count = 0
		c = 0
		j = 0	

		for value in frienddata['friend']:
			#Prepare a query to get each friend data
			dic_rep = {}
			username = value[0]
			query = usercol.find_one({"_id": int(username)},{"_id":1})

			#append data in json sent file
			dic_rep['_id'] = int(query['_id'])
			
			dic_coll[count] = dic_rep
			count += 1

				
		for t in dic_coll:
			frnds[j] = t
			j +=1			
	
		

		#get all users
		for i in usercol.find({}, {"friend": 0, "image": 0, "userName": 0}):
			i = int(i["_id"])
			name = allusers[i-1]['userName']
			img = allusers[i-1]['image']
			
			if i  not in frnds:
				arr = {}
				arr['username'] = name
				arr["image"] = img

				arrList[c]  = arr						
				c += 1


		#Send the final result
		self.write(arrList)
