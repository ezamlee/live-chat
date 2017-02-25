from tornado import web,ioloop
import os
#from handlers.ajax import APIHandler

class MainHandler(web.RequestHandler):
    def get(self):
        self.render("../templates/index.html")

