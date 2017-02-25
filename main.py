from tornado import web,ioloop
import os
from handlers.MainHandler import *

app = web.Application(
    [(r"/", MainHandler)	
     ],
    static_path='static',
    debug=True
    )

app.listen(8888)
ioloop.IOLoop.current().start()
