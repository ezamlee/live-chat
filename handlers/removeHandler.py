from tornado import web,ioloop
import os
from pymongo import MongoClient

#handler of remove friend
class removeHandler(web.RequestHandler):

	def get(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]
		friendid = self.get_query_arguments("friendid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		

		#Query The DATA
		frienddata1 = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})
		frienddata2 = usercol.find_one({"_id":int(friendid) },{"friend":1,"_id":0})

		for i in frienddata1['friend']:
			getid = int(i[0])
			if getid == int(friendid):
				r0 = usercol.update({"_id": int(userid)},{"$pull":{"friend":[getid,1]}})

		for j in frienddata2['friend']:
			usr = int(j[0])
			if usr == int(userid):   
				ret0 = usercol.update({"_id": int(friendid)},{"$pull":{"friend":[usr,1]}})	
				
		
		
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})
		
		#Send the final result
		self.write(frienddata)

	
