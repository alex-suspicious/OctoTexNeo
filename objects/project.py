import webview
import project as sysProject
import sys

gloabl_dir = ""
if( hasattr(sys,"_MEIPASS") ):
	gloabl_dir = sys._MEIPASS

class project:
	def load(self):
		global sysProject, webview, glob, gloabl_dir
		file_types = ('Exe Files (*.exe)', 'All files (*.*)')

		result = sysProject.window.create_file_dialog(
			webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
		)
		exists = False

		result = result[0]
		result = result.split("/")
		result.pop()
		sysProject.directory = "/".join(result)
		print(sysProject.directory)

		dirs = glob.glob(f"{sysProject.directory}/*")

		for x in range(len(dirs)):
			if( "rtx-remix" in dirs[x] ):
				exists = True

		if( not exists ):
			return self.load()

		f = open( f"{gloabl_dir}/system/projects","r+")
		content = f.read()
		if( sysProject.directory not in content ):
			content = content.split("\n")
			content.append( sysProject.directory )
			f.write( "\n".join(content) )
		f.close()

		print("Project was loaded!")
		return ["js","""
			window.location.href = "/";
		"""]

	def get_list(self):
		global sysProject, webview, glob

		f = open( f"{gloabl_dir}/system/projects","r")
		content = f.read()
		f.close()

		return content.split("\n")

	def load_path(self, path):
		global sysProject, webview, glob
		sysProject.directory = path
		exists = False
		print(sysProject.directory)

		dirs = glob.glob(f"{sysProject.directory}/*")

		for x in range(len(dirs)):
			if( "rtx-remix" in dirs[x] ):
				exists = True

		if( not exists ):
			return self.load()

		print("Project was loaded!")
		return ["js","""
			window.location.href = "/";
		"""]

	def get_dir(self):
		global sysProject
		print(f"Project dir: {sysProject.directory}")
		return sysProject.directory

	def save(self, project_name):
		global sysProject
		print("Project was saved!")
		sysProject.project = project_name
		return ["success",f"Project {sysProject.project} was saved!"]

	def get_name(self):
		global sysProject
		print(sysProject.project)
		return sysProject.project
