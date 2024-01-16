import glob
import project as sysProject

class io:
	def get_files(self, directory):

		def sortKeyFunc(s):
			return "." in s.replace("\\\\","/").replace("\\","/").split("/")[-1]



		global glob, sysProject
		dirs = glob.glob(f"{sysProject.directory}/{directory}")
		dirs.sort(key=sortKeyFunc)

		for x in range(len(dirs)):
			dirs[x] = dirs[x].replace("\\\\","/").replace("\\","/")

		#print(dirs)
		return dirs
