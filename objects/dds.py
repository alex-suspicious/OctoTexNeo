import glob
import project as sysProject
from PIL import Image
from io import BytesIO
from aiohttp import web

class dds:
	def read(self, file):
		global Image, sysProject, BytesIO, web
		im = Image.open(file)

		with BytesIO() as f:
			im.save(f, format='PNG')

			print(f"{file} converted")
			return web.Response( body=f.getvalue(), content_type="Image/*")
