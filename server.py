'''
Created on 20/04/2013

@author: Moses Wan
'''

import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import tornado.websocket
from tornado import gen

import subprocess
import sqlite3
from crontab import CronTab
from configobj import ConfigObj
import threading
import time

from tornado.options import define, options
import json
import GPIO_handler, GPIO_on, GPIO_off, startup

#plug_status = "0000"
cron = CronTab()

job_list = []

define("port", default=45381, help="run on the given port", type=int)

# Access to 'config/general.ini' to read and write preferences
class Parser:
    def __init__(self, file):
        self.parser = ConfigObj(file)
    def get(self, section, item=None):
        if item != None:
            return self.parser[section][item]
        else:
            return self.parser[section]
        
    def write(self, section, value, item=None):
        if item != None:
            self.parser[section][item] = value
        else:
            self.parser[item] = value
            
        self.parser.write()

# Handles the storing of task details for the "atd" package
# Used for once-off tasks
class DatabaseHandler:
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

# Thread to handle the network scans and results
class NetworkManager(threading.Thread):
    def __init__(self, callback=None, *args, **kwargs):
        super(NetworkManager, self).__init__(*args, **kwargs)
        self.callback = callback
        
    def run(self):
        subprocess.call("wpa_cli scan", shell=True)
        time.sleep(3)
        output = subprocess.check_output("wpa_cli scan_results", shell=True)
        output = output.split('\n')
        output.pop(0)
        output.pop(0)
        output.pop()

        unique_networks = []
        filter_output = []
        for index in range(len(output)):
            #print output[index]
            output[index] = output[index].split('\t')
            if output[index][4] not in unique_networks:
                unique_networks.append(output[index][4])
                filter_output.append(output[index])

        del output

        self.callback(filter_output)
        return

# Thread that handles the connection to new networks
class NetworkConnection(threading.Thread):
    def __init__(self, data, callback=None, *args, **kwargs):
        super(NetworkConnection, self).__init__(*args, **kwargs)
        self.callback = callback
        self.data = data


    def run(self):
        if self.data[0] == "connect":  
            subprocess.call("wpa_cli select_network " + self.data[1], shell=True)
        elif self.data[0] == "wps-push":
            subprocess.call("wpa_cli wps_pbc any", shell=True)
        elif self.data[0] == "wps-pin":
            subprocess.call("wpa_cli wps_pin any " + self.data[1], shell=True)
        else:
            network_id = subprocess.check_output("wpa_cli add_network", shell=True)
            network_id = network_id.split('\n')
            network_id = network_id[1]

            if self.data[0] == "wpa":
		subprocess.call('echo "set_network ' + network_id + ' ssid \\"' + self.data[1] + '\\"" | wpa_cli', shell=True)
		subprocess.call('echo "set_network ' + network_id + ' psk \\"' + self.data[2] + '\\"" | wpa_cli', shell=True)
                
	    elif self.data[0] == "eap":
		subprocess.call('echo "set_network ' + network_id + ' ssid \\"' + self.data[1] + '\\"" | wpa_cli', shell=True)
		subprocess.call('echo "identity ' + network_id + ' \\"' + self.data[2] + '\\"" | wpa_cli', shell=True)
		subprocess.call('echo "password ' + network_id + ' \\"' + self.data[3] + '\\"" | wpa_cli', shell=True)
                
	    else:
		subprocess.call('echo "set_network ' + network_id + ' ssid \\"' + self.data[1] + '\\"" | wpa_cli', shell=True)
		subprocess.call('echo "set_network ' + network_id + ' key_mgmt NONE" | wpa_cli', shell=True)
            
            subprocess.call("wpa_cli select_network " + network_id, shell=True)
        
        for i in range(5):
            time.sleep(3)
            output = subprocess.check_output("wpa_cli status", shell=True)
            if "wpa_state=COMPLETED" in output:
                subprocess.call("wpa_cli save_config", shell=True)
                break

        self.callback('Finish up')
        return    
    
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
            (r"/settings", SettingsHandler),
            (r"/ws_settings", WebSocketSettingsHandler),
            (r"/wifiwizard", WifiWizardHandler),
            (r"/extend", ExtendWizardHandler),
            (r"/monitor", MonitorHandler)
        ]
        
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

# Generates the webpage for "/" and "/control"
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        config = Parser('/home/pi/node-fyp/config/general.ini')
        plugs = [["plug1",config.get('plug_names', 'plug1'), "light1", "11"],
                ["plug2", config.get('plug_names', 'plug2'), "light2", "12"],
                ["plug3", config.get('plug_names', 'plug3'), "light3", "13"],
                ["plug4", config.get('plug_names', 'plug4'), "light4", "14"]]

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
        at_jobs = DatabaseHandler()
        jobs = at_jobs.get_table()
        at_jobs.close()
        list = cron.find_command("sudo python /home/pi/node-fyp/GPIO_handler.py")
        for index in range(len(list)):
            list[index] = list[index].render()
            list[index] = list[index].split(' # ')
            list[index][0] = list[index][0].split(' ', 5)
            list[index][0][0] = ("0" + list[index][0][0])[1:]
            list[index][0][1] = ("0" + list[index][0][1])[1:]
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
            at = DatabaseHandler()
            id = at.insert(data["name"],str(data["plugs"]), str(data["hours"]), str(data["minutes"]))
            at.close()
            data["id"] = str(id)
          
        if data["method"] == "1":
	    # Delete a once-off task
            at = DatabaseHandler()
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

# Generates the webpage for "/settings"
class SettingsHandler(tornado.web.RequestHandler):
    def get(self):
        plug_names = []
        
        config = Parser('/home/pi/node-fyp/config/general.ini')
        plug_names.append(config.get('plug_names', 'plug1'))
        plug_names.append(config.get('plug_names', 'plug2'))
        plug_names.append(config.get('plug_names', 'plug3'))
        plug_names.append(config.get('plug_names', 'plug4'))

        output = subprocess.check_output("wpa_cli status", shell=True)
        output = output.split('\n')
        
        self.render('settings.html', plug_names = plug_names, wifi_status = output )

# Handles the WebSockets for "/settings"
class WebSocketSettingsHandler(tornado.websocket.WebSocketHandler):
    connections = []
    config = Parser('/home/pi/node-fyp/config/general.ini')
    def open(self):
        self.connections.append(self)

    def on_message(self, message):
        data = json.loads(message)
        print data

        if data['method'] == "0":
            self.config.write('plug_names', data['value'], data['id'])

            
        for connection in self.connections:
            connection.write_message(message)

    def on_close(self):
        self.connections.remove(self)

# Generates the webpage for "/wifiwizard"
class WifiWizardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        NetworkManager(self.job_done).start()
        
        
    def job_done(self, value):
        self.status = subprocess.check_output("wpa_cli status", shell=True)
        self.state = 'wpa_state=COMPLETED' in self.status
        self.status = self.status.split('\n')

        # Get the list of saved networks and the current network
        self.saved = subprocess.check_output("wpa_cli list_networks", shell=True)
        self.saved = self.saved.split('\n')
        self.saved.pop(0)
        self.saved.pop(0)
        self.saved.pop()

        # Find the current network form the list of saved networks
        self.current = 'none nothing useless string'
        for i in range(len(self.saved)):
                self.saved[i] = self.saved[i].split('\t')
                if ("[CURRENT]" in self.saved[i]) and self.state:
                    self.current = self.saved[i][1]


        self.render('net_wizard.html', current_status = self.status,
                    scan_group = value, current = self.current, saved_group = self.saved)
        
    @tornado.web.asynchronous
    def post(self):
	method = self.get_argument('method','')
        net_cat = self.get_argument('net_cat', '')
        
        if method == "delete":
	    net_id = self.get_argument('id','')
	    subprocess.call("wpa_cli remove_network " + net_id, shell=True)
	    subprocess.call("wpa_cli save_config", shell=True)
	    self.post_finish(None)
	elif method == "connect":
            net_id = self.get_argument('id','')
            NetworkConnection([method, net_id], self.post_finish).start()
        elif method == "wpa":
            net_id = self.get_argument('id', '')
            net_pass = self.get_argument('pass', '')
            NetworkConnection([method, net_id, net_pass], self.post_finish).start()
        elif method == "eap":
            net_id = self.get_argument('id', '')
            net_username = self.get_argument('identity', '')
            net_pass = self.get_argument('pass', '')
            NetworkConnection([method, net_id, net_username, net_pass], self.post_finish).start()
        elif method == "wps-push":
            NetworkConnection([method], self.post_finish).start()
        elif method == "wps-pin":
            net_pin = self.get_argument('pin','')
            NetworkConnection([method, net_pin], self.post_finish).start()
        else:
            net_id = self.get_argument('id', '')
            print net_id
            NetworkConnection([method, net_id], self.post_finish).start()

    def post_finish(self, value):
        print 'In post_finish'
        self.write('Finish It')
        self.finish()
            
class ExtendWizardHandler(tornado.web.RequestHandler):
    extension_settings = Parser('/home/pi/node-fyp/config/general.ini')
    
    def get(self):
        wifi_status = subprocess.check_output("wpa_cli status", shell=True)
        wifi_status = wifi_status.split('\n')
        extend_status = []
        extend_status.append("Enabled: " + self.extension_settings.get('range_extension', 'enable'))
        extend_status.append("SSID: " + self.extension_settings.get('range_extension', 'ssid'))
        extend_status.append("Channel: " + self.extension_settings.get('range_extension', 'channel'))
        extend_status.append("Address: " + self.extension_settings.get('range_extension', 'router'))
        extend_status.append("DHCP Range: " + self.extension_settings.get('range_extension', 'start') + " - " + self.extension_settings.get('range_extension', 'end'))
        extend_status.append("Password Protection: " + self.extension_settings.get('range_extension', 'pass_proc'))
        self.render('extend.html', wifi_status = wifi_status, extend_status = extend_status)
        
    def post(self):
        self.extension_settings.write('range_extension', self.get_argument('enable', ''), 'enable')
        self.extension_settings.write('range_extension', self.get_argument('ssid', ''), 'ssid')
        self.extension_settings.write('range_extension', self.get_argument('channel', ''), 'channel')
        self.extension_settings.write('range_extension', self.get_argument('pass-proc', ''), 'pass_proc')
        self.extension_settings.write('range_extension', self.get_argument('WPA', ''), 'wpa')
        self.extension_settings.write('range_extension', self.get_argument('psk', ''), 'wpa_passphrase')
        self.extension_settings.write('range_extension', self.get_argument('router', ''), 'router')
        self.extension_settings.write('range_extension', self.get_argument('start', ''), 'start')
        self.extension_settings.write('range_extension', self.get_argument('end', ''), 'end')
        self.extension_settings.write('range_extension', self.get_argument('netmask', ''), 'netmask')

        with open('/etc/udhcpd.conf', 'w') as udhcpd_file:
            udhcpd_file.write("start " + self.extension_settings.get('range_extension', 'start') + '\n')
            udhcpd_file.write("end " + self.extension_settings.get('range_extension', 'end') + '\n')
            udhcpd_file.write('interface wlan0\n')
            udhcpd_file.write('opt dns 8.8.8.8 4.2.2.2\n')
            udhcpd_file.write("option subnet " + self.extension_settings.get('range_extension', 'netmask') + '\n')
            udhcpd_file.write("opt router " + self.extension_settings.get('range_extension', 'router') + '\n')
            udhcpd_file.write('option lease 864000\n')

        hostapd_file = ConfigObj('/etc/hostapd/hostapd.conf')
        hostapd_file['ssid'] = self.extension_settings.get('range_extension', 'ssid')
        hostapd_file['channel'] = self.extension_settings.get('range_extension','channel')
        if self.extension_settings.get('range_extension', 'pass_proc') == 'true':
            hostapd_file['wpa'] = self.extension_settings.get('range_extension', 'wpa')
            hostapd_file['wpa_passphrase'] = self.extension_settings.get('range_extension', 'wpa_passphrase')
            hostapd_file['wpa_key_mgmt'] = 'WPA-PSK'
            hostapd_file['wpa_pairwise'] = 'TKIP'
            hostapd_file['rsn_pairwise'] = 'CCMP'
        else:
            hostapd_file['wpa'] = ''
            hostapd_file['wpa_passphrase'] = ''
            hostapd_file['wpa_key_mgmt'] = ''
            hostapd_file['wpa_pairwise'] = ''
            hostapd_file['rsn_pairwise'] = ''

        hostapd_file.write()
        with open('/etc/hostapd/hostapd.conf', 'r+') as hostapd_conf:
            text = hostapd_conf.read()
            text = text.replace(' = ', '=')
            hostapd_conf.seek(0)
            hostapd_conf.write(text)
            hostapd_conf.truncate()

        with open('/etc/network/interfaces', 'w') as network_conf:
            network_conf.write('auto lo\n\n')
            network_conf.write('iface lo inet loopback\n')
            network_conf.write('iface eth0 inet dhcp\n\n')
            network_conf.write('allow-hotplug wlan0\n')
            network_conf.write('iface wlan0 inet static\n')
            network_conf.write('\taddress '+ self.extension_settings.get('range_extension', 'router') +'\n')
            network_conf.write('\tnetmask '+ self.extension_settings.get('range_extension', 'netmask') +'\n\n')
            network_conf.write('allow-hotplug wlan1\n')
            network_conf.write('iface wlan1 inet manual\n')
            network_conf.write('wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf\n\n')
            network_conf.write('iface default inet dhcp\n')

        startup.update()
        
        self.write('Done')
        self.finish()

class MonitorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('monitor.html')



def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
