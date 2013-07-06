'''
Created on 20/04/2013

@author: Moses Wan
'''

import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import tornado.websocket

import subprocess
import sqlite3
from crontab import CronTab

from tornado.options import define, options
import json
import GPIO_handler, GPIO_on, GPIO_off

#plug_status = "0000"
cron = CronTab()

job_list = []

define("port", default=80, help="run on the given port", type=int)


# Handles the storing of task details for the "atd" package
# Used for once-off tasks
class databaseHandler:
    def __init__(self):
        self.db_connection = sqlite3.connect('at_jobs.db')
        self.cur = self.db_connection.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS jobs (Id TEXT, name TEXT, state TEXT, hour TEXT, minute TEXT)')
        self.clean()
    def get_table(self):
        self.cur.execute("SELECT * FROM jobs")
        data = self.cur.fetchall()
        return data
    def insert(self, name, state, hour, minute):
        command = 'echo "sudo python /home/pi/node-fyp/GPIO_handler.py %s" | at %s:%s' %(state, hour, minute)
        subprocess.call(command, shell=True)
        job_ids = at_get()
        id = max(job_ids)
        self.cur.execute("INSERT INTO jobs VALUES('%s','%s','%s', '%s', '%s')" %(id, name, state, hour, minute))
        self.db_connection.commit()
        return id
    def delete(self, Id):
        subprocess.call("atrm %d" %(Id), shell=True)
        self.cur.execute("DELETE FROM jobs WHERE Id = %s" %(Id))
        self.db_connection.commit()
    def clean(self):
	
	# Cleans the database to only have the tasks that are yet to run
        job_ids = at_get()
        if not job_ids:
            self.cur.execute('DROP TABLE IF EXISTS jobs')
            self.cur.execute('CREATE TABLE IF NOT EXISTS jobs (Id TEXT, name TEXT, state TEXT, hour TEXT, minute TEXT)')
            self.cur.execute("SELECT * FROM jobs")
            self.db_connection.commit()
        else:
            self.cur.execute('CREATE TEMPORARY TABLE clean (Id TEXT, name TEXT, state TEXT, hour TEXT, minute TEXT)')
            for id in job_ids:
                self.cur.execute('INSERT INTO clean SELECT * FROM jobs WHERE Id = %s' %(id))
                                 
            self.cur.execute('DROP TABLE jobs')
            self.cur.execute('CREATE TABLE IF NOT EXISTS jobs AS SELECT * FROM clean')
            self.cur.execute('DROP TABLE clean')
            self.cur.execute("SELECT * FROM jobs")
            self.db_connection.commit()
    def close(self):
            self.db_connection.close()
            del self

# Get the atd jobs that are pending to run            
def at_get():
    output = subprocess.check_output("atq")
    output = output.split('\n')
    output.pop()
    for index in range(len(output)):
        output[index] = output[index].split('\t')
        output[index] = int(output[index][0])
    return output

# Redirects the URLs to the correct handler
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/control", MainHandler),
            (r"/ws", WebSocketHandler),
            (r"/schedule", ScheduleHandler),
            (r"/ws_schedule", WebSocketScheduleHandler),
        ]
        
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

# Generates the webpage for "/" and "/control"
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        plugs = [["plug1","Plug 1", "light1", "11"],
                ["plug2","Plug 2", "light2", "12"],
                ["plug3", "Plug 3", "light3", "13"],
                ["plug4", "Plug 4", "light4", "14"]]

        self.render("index.html",
                    plugs=plugs)

# Handles the WebSockets for "/" and "/control"
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    # Stores a list of connections
    connections = []
    def open(self):

	# When a client connects to the WebSocket, the server will re-transmit the status of plugs
        self.connections.append(self)
	plug_status = GPIO_handler.read()
        self.write_message(plug_status)
        print "WebSocket opened"
        
    def on_message(self, message):
        print "Message Received: %s" %message
        
	# When a client changes something, the server will execute the change, then will transmit that change to all 
	# the clients connected to the WebSocket
        if message[0] == "1":
#            global plug_status
#            plug_status = plug_status + plug_status[:(int(message[1])-1)] + message[2] + plug_status[(int(message[1])):]
#            plug_status = plug_status[4:]
#            print plug_status
            
            if message[2] == "1":
                 GPIO_on.run_script(message[1])
            else:
                 GPIO_off.run_script(message[1])
             
        plug_status = GPIO_handler.read()
            
        for connections in self.connections:
            connections.write_message(plug_status)
        
    def on_close(self):
	# Remove the client's connection from the list
        self.connections.remove(self)
        print "WebSocket closed:"
        print self.connections

# Generates the webpage for "/schedule"
class ScheduleHandler(tornado.web.RequestHandler):
    def get(self):
        at_jobs = databaseHandler()
        jobs = at_jobs.get_table()
        at_jobs.close()
        list = cron.find_command("sudo python /home/pi/node-fyp/GPIO_handler.py")
        for index in range(len(list)):
            list[index] = list[index].render()
            list[index] = list[index].split(' # ')
            list[index][0] = list[index][0].split(' ', 5)
            list[index][0][0] = ("0" + list[index][0][0])[:2]
            list[index][0][1] = ("0" + list[index][0][1])[:2]
            list[index][0][4] = list[index][0][4].split(',')
            list[index][0][5] = list[index][0][5][46:]
        print list
        self.render("schedule.html", at_jobs = jobs, cron_list = list)


# Handles the WebSockets for "/schedule"
class WebSocketScheduleHandler(tornado.websocket.WebSocketHandler):
    connections = []
    def open(self):
        self.connections.append(self)
        print "WebSocket opened"
        print self.connections
        
    def on_message(self, message):
        data = json.loads(message)
        if 'name' in data:
            data["name"] = data["name"].replace(" ", "_")

        if data["method"] == "0":
	    # Create a once-off task
            at = databaseHandler()
            id = at.insert(data["name"],str(data["plugs"]), str(data["hours"]), str(data["minutes"]))
            at.close()
            data["id"] = str(id)
          
        if data["method"] == "1":
	    # Delete a once-off task
            at = databaseHandler()
            at.delete(data["id"])
            at.close()
              
        if data["method"] == "2":
	    # Delete a repeated task
            list = cron.find_comment(data["name"])
            for cron_job in list:
                cron.remove(cron_job)
            cron.write()
              
        if data["method"] == "3":
	    # Create a repeated task
            command_line = "sudo python /home/pi/node-fyp/GPIO_handler.py %s" %(str(data["plugs"]))
            job = cron.new(command=command_line, comment=data["name"])
            job.minute.on(data["minutes"])
            job.hour.on(data["hours"])
              
            dow_info = str(data["dow"])
            dow = []
            for index in range(len(dow_info)):
                if dow_info[index] == "1":
                    job.dow.on(index)
              
            cron.write()
            
        print data
        if 'name' in data:
            data["name"] = data["name"].replace("_", " ")
        
	# Retransmit the change to all clients    
        for connection in self.connections:
            connection.write_message(json.dumps(data))
        
    def on_close(self):
	# Remove client's connection from the list
        self.connections.remove(self)
        print "WebSocket closed:"
        print self.connections


def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
