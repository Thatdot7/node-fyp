'''
Created on 20/04/2013

@author: Moses Wan
'''

import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import tornado.websocket
from crontab import CronTab
from tornado.options import define, options

plug_status = "0000"
cron = CronTab()

job_list = []

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/ws", WebSocketHandler),
            (r"/schedule", ScheduleHandler),
        ]
        
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        plugs = [["plug1","Plug 1", "light1", "11"],
                ["plug2","Plug 2", "light2", "12"],
                ["plug3", "Plug 3", "light3", "13"],
                ["plug4", "Plug 4", "light4", "14"]]

        self.render("index.html",
                    plugs=plugs)

        
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = []
    def open(self):
        self.connections.append(self)
        self.write_message(plug_status)
        print "WebSocket opened"
        
    def on_message(self, message):
        print "Message Received: %s" %message
        
        if message[0] == "1":
            global plug_status
            plug_status = plug_status + plug_status[:(int(message[1])-1)] + message[2] + plug_status[(int(message[1])):]
            plug_status = plug_status[4:]
            print plug_status
            
        for connections in self.connections:
            connections.write_message(plug_status)
        
    def on_close(self):
        self.connections.remove(self)
        print "WebSocket closed:"
        print self.connections

class ScheduleHandler(tornado.web.RequestHandler):
    def get(self):
        schedule_list = cron.find_command("sudo python")
        for jobs in schedule_list:
            job_list.append(jobs.render())
        print job_list
        self.render("schedule.html")

def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    