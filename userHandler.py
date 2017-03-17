from tornado import web,ioloop
import os
from pymongo import MongoClient


#handler of get all friends request
class userHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
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
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
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

#handler of get all users request
class FriendsHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET')
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user

		#Query The DATA
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})
		print("frienddata: ",frienddata)

		#find all users the output cursor so use list or for loop
		allusers = list(usercol.find( {"_id":{'$not':{'$in':frienddata['friend']} }} ))
		print('all users', allusers)


		#Construct JSON to send back to Client and count up data
		dic_coll ={}
		arrList = {}
		frnds = {}
		count = 0
		c = 0
		j = 0
		#
		for value in frienddata['friend']:
			#Prepare a query to get each friend data
			dic_rep = {}
			username = value[0]
			query = usercol.find_one({"_id": int(username)},{"_id":1})

			#append data in json sent file
			dic_rep['_id'] = int(query['_id'])

			dic_coll[count] = dic_rep
			count += 1

		print("dic_coll", dic_coll)


		for t in dic_coll:
			frnds[j] = t
			j +=1

		print("frnds = ", frnds)


		# get all users
		ll = list(usercol.find( {"_id":{'$not':{'$in':frienddata['friend']} }} ))

		for i in ll:
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
		print("arrList", arrList)

		#Send the final result
		self.write(arrList)



#handler of accept request
class addHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		# GET THE URL DATA
		userid = self.get_query_arguments("userid")[0]
		friendid = self.get_query_arguments("friendid")[0]

		print("userid = ", userid)
		print("friendid = ", friendid)

		#MAKE DATABASE CONNECTION
		client = MongoClient()
		db_livechat = client.livechat
		usercol = db_livechat.user

		#Query The DATA
		r = usercol.update({"_id": int(userid)},{"$push":{"friend":[int(friendid),-1]}})
		ret = usercol.update({"_id": int(friendid)},{"$push":{"friend":[int(userid),0]}})
		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})

		#Send the final result
		self.write(frienddata)


#handler of remove friend
class removeHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
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

#handler of accept request
class updateHandler(web.RequestHandler):

	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
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
			if getid == int(friendid):   #[13.0, 0.0]
				r0 = usercol.update({"_id": int(userid)},{"$pull":{"friend":[getid,0]}})
				r = usercol.update({"_id": int(userid)},{"$push":{"friend":[getid,1]}})

		for j in frienddata2['friend']:
			usr = int(j[0])
			if usr == int(userid):
				ret0 = usercol.update({"_id": int(friendid)},{"$pull":{"friend":[usr,0]}})
				ret = usercol.update({"_id": int(friendid)},{"$push":{"friend":[usr,1]}})


		frienddata = usercol.find_one({"_id":int(userid) },{"friend":1,"_id":0})

		#Send the final result
		self.write(frienddata)



app = web.Application([
	(r"/people", userHandler),
	(r"/allpeople", FriendsHandler),
	(r"/add", addHandler)
	,(r"/update", updateHandler),
	(r"/remove", removeHandler)
	],

    static_path='../static',
    debug=True
    )

app.listen(2222)
ioloop.IOLoop.current().start()
