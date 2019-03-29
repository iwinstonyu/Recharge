# coding: utf-8

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
from urllib.parse import urlparse
import urllib
import mysql.connector
from mysql.connector import errorcode

conf_file_path = "./config.json"
f_conf = open(conf_file_path, "r")
conf = json.load(f_conf)
print(("Load conf from {}".format(conf_file_path)))
f_conf.close()

class Server(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
        
	def do_HEAD(self):
		self._set_headers()
        
    # GET sends back a Hello world message
	def do_GET(self):
		self._set_headers()
		querypath = urlparse(self.path)
		path = querypath.path
		query = querypath.query

		if path == "/recharge":
			params = urllib.parse.parse_qs(query)
			if not ("number" in params) or not (len(params["number"]) > 0) :
				Server.response_fail(self, "no number")
				return
			elif not "key" in params or not (len(params["key"]) > 0) :
				Server.response_fail(self, "no key")
				return
			elif not "serverid" in params or not (len(params["serverid"]) > 0) :
				Server.response_fail(self, "no serverid")
				return
				
			number = params["number"][0]
			key = params["key"][0]
			serverid = params["serverid"][0]

			print(params)
			print(params["serverid"])
			print(conf["servers"])
			if not serverid in conf["servers"]:
				Server.response_fail(self, "invalid serverid")
				return

			serverconf = conf["servers"][serverid]	
			cnx = mysql.connector.connect(user=serverconf["user"], password=serverconf["password"], host=serverconf["host"], database=serverconf["database"], port=serverconf["port"])
			cursor = cnx.cursor(buffered=True)
			
			query = "select index_name, column_name from information_schema.STATISTICS where table_schema = '{}' and table_name = '{}'".format(database, auto_table);
			cursor.execute(query)

			cursor.close()
			cnx.close()
			self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode())
		else:
			Server.response_fail(self, "invalid operation")
        
    # POST echoes the message adding a JSON field
	def do_POST(self):
		response_fail(self, "invalid operation")
		'''
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
		'''
    
	def response_fail(self, reason):
		self.wfile.write(json.dumps({"result": "fail", "reason": reason}).encode())
        
def run(server_class=HTTPServer, handler_class=Server, port=9988):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()
  
try:   
	run()
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
		exit(1)
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
		exit(1)
	else:
		print(err)
		exit(1)