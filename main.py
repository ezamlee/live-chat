from tornado import web,ioloop
import os
from handlers.MainHandler import *
from handlers.userHandler import *
from handlers.FriendsHandler import *
from handlers.updateHandler import *
from handlers.addHandler import *
from handlers.removeHandler import *

app = web.Application(
    [
	(r"/", MainHandler),
	(r"/people", userHandler),
	(r"/allpeople", FriendsHandler), 
	(r"/update", updateHandler),
	(r"/remove", removeHandler),
	(r"/add", addHandler)
    ],
    static_path='static',
    debug=True
    )

app.listen(8888)
ioloop.IOLoop.current().start()
