import os
import asyncio
import functions
import plugins
import aiohttp
from aiohttp import web

import sys
from PIL import Image, ImageEnhance
import json
import webbrowser
import io
import tkinter
from tkinter import *
import webview 
import threading
import inspect
import pathlib
import zipfile
import shutil
import requests
import base64
import logger
import traceback
import project
#sys.stdout.reconfigure(encoding='utf-8')

webui_dir = "webui"
if( hasattr(sys,"_MEIPASS") ):
	webui_dir = sys._MEIPASS + "/webui"



req_types = {
	"html":"text/html",
	"ini": "text/html",
	"json":"application/javascript",
	"png":"image/*",
	"js":"application/javascript",
	"css":"text/css",
	"woff2":"application/x-font-woff2",
	"jpg":"image/*",
	"jpeg":"image/*",
	"ttf":"application/octet-stream",
	"ico":"image/x-icon",
	"hdr":"image/vnd.radiance",
	"mp3": "audio/*"
}

cache_types = {
	"html":False,
	"json":False,
	"png":False,
	"js":False,
	"css":False,
	"woff2":True,
	"jpg":False,
	"jpeg":False,
	"ttf":True,
	"ico":True,
	"hdr":False,
	"mp3":False
}

neededDirectories = ["plugins,system"]

class StoppableThread(threading.Thread):
	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()
		os._exit(1)

	def stopped(self):
		return self._stop_event.is_set()

for directory in neededDirectories:
	isExist = os.path.exists(directory)
	if not isExist:
		os.makedirs(directory)

def preprocess(html):
	lines = html.split("\n")

	for x in range(len(lines)):
		line = lines[x]
		if( "@import" in line ):
			file = line.split("@import ")[1]

			f = open((webui_dir + "/" + file), "r", encoding="utf8")
			content = f.read()
			f.close()
			
			lines[x] = content

		if( "@download" in line ):
			url = line.split("@download ")[1]

			resp = requests.get(url)
			lines[x] = resp.text


	return "\n".join(lines)

def callback_object(request):
	className = request.match_info.get('class', "error")
	classFunction = request.match_info.get('function', "error")

	#print(className)
	#print(classFunction)

	try:
		obj_done = functions.container[className]
		func_done = getattr(obj_done, classFunction)
	except Exception as e:
		print( traceback.format_exc() )
		return web.Response(text=json.dumps(["error",str(e)]))


	params = request.rel_url.query
	normal_params = {}
	like_parameters = []
	for k in set(params.keys()):
		normal_params[k] = params.getall(k)
	
	#param_keys = list( normal_params.keys() ) 
	

	try:
		func_params = inspect.signature(func_done);
		func_param_names = [param.name for param in func_params.parameters.values()]

		for x in range( len(func_param_names) ):
			like_parameters.append( f"normal_params[ \"{func_param_names[x]}\" ][0]" )
	except Exception as e:
		print( traceback.format_exc() )
		return web.Response(text=json.dumps(["error",str(e)]))


	code = """
try:
	result = func_done(""" + ",".join(like_parameters) + """)
except Exception as e:
	result = "Error: " + str(e)
	"""
	#print(code)
	env = globals()
	envl = locals()

	try:
		exec(code, env, envl)
		result = envl['result']
	except Exception as e:
		print( traceback.format_exc() )
		return web.Response(text=json.dumps(["error",str(e)]))

	#print( result )
	#print(f"\n\n\n\n{result}\n\n\n\n\n")
	#if( "texture" in params ):
	#	result = func_done( params["texture"] )
	#else:
	#	result = func_done()

	if( "Response" in str(type(result)) ):
		return result

	if( "tuple" in str(type(result)) or "list" in str(type(result)) ):
		return web.Response(text=json.dumps(result))


	return web.Response(text=result)

async def all_routing( request, index = False ):
	requestNew = str(request).replace("<Request GET ","").replace(" >","")
	if( requestNew == "/<" ):
		return

	if( index ):
		requestNew = "index.html"

	fileType = requestNew.split(".")
	if( "." not in requestNew ):
		requestNew = requestNew + ".html"
		fileType = [requestNew,"html"]


	if( fileType[len(fileType)-1].split("?")[0] == "map" ):
		return

	reqType = req_types[ fileType[len(fileType)-1].split("?")[0] ]

	cache = cache_types[ fileType[len(fileType)-1].split("?")[0] ]

	if( "image" in reqType or "octet" in reqType or "woff2" in reqType or "audio" in reqType ):
		try:
			f = open( (webui_dir + "/" + requestNew), "rb")
			file = f.read()
			f.close()
			return web.Response( body=file, content_type=reqType)
		except Exception as e:
			try:
				requestNew = requestNew.replace("upscaled","diffuse")
				f = open((webui_dir + "/" + requestNew), "rb")
				file = f.read()
				f.close()
				return web.Response( body=file, content_type=reqType)
			except Exception as e:
				return


	f = open((webui_dir + "/" + requestNew), "r", encoding="utf8")
	file = f.read()
	f.close()

	file = preprocess(file)

	headers = {}
	if( cache ):
		headers.update( {'Cache-Control': "max-age=86400"} )

	response = web.Response( text=file, content_type=reqType, headers=headers)
	return response

async def index_routing( request ):
	return await all_routing(request, True)


async def plugins_routing( request ):
	pluginName = request.match_info.get('name', "error")
	f = open("plugins/" + pluginName + "/index.html", "r", encoding="utf8")
	file = f.read()
	f.close()

	response = web.Response( text=file, content_type="text/html")
	return response

def aiohttp_server():
	#plugins.load()
	logger.log.start()
	print("Welcome to OctoTex Neo!")
	functions.load()

	app = web.Application()
	app.add_routes([web.get(r'/object/{class}/{function}', callback_object)])

	app.add_routes([web.get(r"/plugin/{name}", plugins_routing)])
	app.add_routes([web.get("/{key:.+}", all_routing)])
	app.router.add_get('/', index_routing)

	runner = web.AppRunner(app)
	return runner


def run_server(runner):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(runner.setup())
	#print("http://localhost:27575")
	#webbrowser.open('http://localhost:27575', new=2)

	site = web.TCPSite(runner, 'localhost', 27576)
	loop.run_until_complete(site.start())
	loop.run_forever()




t = StoppableThread(target=run_server, args=(aiohttp_server(),))
# define an instance of tkinter
def on_closed():
	t.stop()

# Open website
project.window = webview.create_window('OctoTex Neo', 'http://localhost:27576/project', width=1280, height=720)
project.window.events.closed += on_closed
t.start()
webview.start(gui='edgechromium')