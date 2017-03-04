from tornado import web,ioloop 
import os
#from handlers.ajax import APIHandler

class MainHandler(web.RequestHandler):
    def get(self):
    	userid = self.get_query_arguments("userid")[0]
    	username = self.get_query_arguments("username")[0]
    	imgeurl = self.get_query_arguments("imgeurl")[0]
    	self.render("../templates/index.html",userid=userid,username=username,imgeurl=imgeurl)

