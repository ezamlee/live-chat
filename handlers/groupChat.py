from tornado import web,websocket
from pymongo import *
import time
import json

#on getting added by one of the users, a group is generated between those users with type private
# 
client = MongoClient()
db_livechat = client.livechat

collec_user = db_livechat.user
lOM= []
global clients
clients={}
#gId = 1
#userId = 2
 #{"groupid":[self,self ,self,self]}
# issue no.3 : user opens  chat and sees the old msgs between other group members
# issue 2 show the group member in a list with their current status

fConv="conversation location"
class WSHandler(websocket.WebSocketHandler):
	def open(self):
		print("gid "+str(gId)+" uId "+str(userId))

		global isMember
		global gMem
		global clientsId
		isMember=0

		try:
			clients[gId].append(self)
		except KeyError:
			clients[gId] = []
			clients[gId].append(self)
		print("clients")
		print(clients)
#db vars
		collec_group = db_livechat.groups
		clientsId=collec_group.find_one({"_id":gId,"groupType":"public" },{"groupmember":1, "_id":0, 'file':1})
		collec_user= db_livechat.user
		collec_stat= db_livechat.stat
		clientsNames=[]
		if clientsId is None:
			print("its private chat :O")
		else:
			#group chat
			LOM=[]
			LOMnames=[]
			LOMstat=[]
			gMem={}
			print(clientsId["groupmember"])
			for arr in clientsId["groupmember"]:
				print("ids of mems")
				print(clientsId["groupmember"])
				if arr[1]==1:
					LOM.append(arr[0])
					memNames=collec_user.find_one({"_id":arr[0] },{"userName":1, "_id":0})
					LOMnames.append(memNames["userName"])
					status=collec_stat.find_one({"userId":arr[0]},{"stat":1, "_id":0})
					status=status["stat"]
					if status==0:
						LOMstat.append(" :offline: ")
						gMem[memNames["userName"]]=	" :offline: "
					elif status==1 and arr[0]!=userId:
						LOMstat.append(" :online: ")
						gMem[memNames["userName"]]=	" :online: "
					elif status==1 and arr[0]==userId:
						isMember=1
						LOMstat.append(" ")	
						gMem[memNames["userName"]]=	""				
			if isMember==1:
				print("dic")
	#			print(str(gMem)
	#			jsonList = json.dumps(gMem)
	#			loaded_jsonList = json.loads(jsonList)

	def on_message(self,msg):
		if isMember==1:
			print("ektb")
		# one to selected group based on gId
			print(clients.keys())
			for c in clients.keys():
				print("c")
				print(c)
				if c==gId:
					print(clients[c])
			#	print(c[gId])
					for i in clients[c]:
						print(i)
						i.write_message(msg)
		#else
			# private chat
			conv=clientsId["file"]
			fConv=open(conv,'a')
			fConv.write(msg +"\n"+ time.strftime("%c") +"\n")
			fConv.close()
	def on_close(self):
		if self in clients[gId]:
			clients[gId].remove(self)
	# display the file in the text area --> text area= file content
   # def on_close(self):
   #    c.write_message("WebSocket closed")
        # replace file content with the new text content
        # save file

#	def on_message(self,msg):
#		for c in clients:
			#if c is not self:
#				c.write_message(msg)
			#	c.write_message(userName)

class GroupChatHandler(web.RequestHandler):
	def get(self):
		global userId,gId
		userId = int(self.get_query_argument('userId')[0])
		gId = int(self.get_query_argument('gId')[0])
		
		self.render("../templates/chat.html") 
############TESTING ##################
#http://localhost:8888/groupChat?userId=8&gId=5
#http://localhost:8888/groupChat?userId=9&gId=5

#http://localhost:8888/groupChat?userId=7&gId=1
#http://localhost:8888/groupChat?userId=6&gId=1

