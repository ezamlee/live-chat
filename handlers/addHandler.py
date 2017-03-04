from tornado import web,ioloop
import os
from pymongo import MongoClient

#handler of accept request
class addHandler(web.RequestHandler):

	def get(self):
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]
		friendid = self.get_query_arguments("friendid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user
		

		#Query The DATA
		r = usercol.update({"_id": int(userid)},{"$push":{"friend":[int(friendid),0]}})

		ret = usercol.update({"_id": int(friendid)},{"$push":{"friend":[int(userid),0]}})		
				
		
		
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})

		
		#Send the final result
		self.write(frienddata)

	
