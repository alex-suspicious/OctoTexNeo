import time

class test:
	def success(self):
		print("Success function was called!")
		return ["success","Success callback!"]

	def info(self):
		print("Info function was called!")
		return ["info","Info callback!"]

	def sleep(self):
		global time
		print("Waiting...")
		time.sleep(10)
		return ["info","Sleep is working!"]

	def error(self):
		print("Error function was called!")
		return ["error","Error callback!"]

	def message(self, test_message):
		return ["info", test_message]