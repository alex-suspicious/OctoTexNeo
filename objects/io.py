import glob
import project as sysProject

class io:
	def get_files(self, directory):

		def sortKeyFunc(s):
			return "." in s.split("/")[-1]



		global glob, sysProject
		dirs = glob.glob(f"{sysProject.directory}/{directory}")
		dirs.sort(key=sortKeyFunc)

		#print(dirs)
		return dirs
