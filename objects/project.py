import webview
import project as sysProject

class project:
	name = ""
	directory = ""

	def load(self):
		global sysProject, webview
		file_types = ('Exe Files (*.exe)', 'All files (*.*)')

		result = sysProject.window.create_file_dialog(
			webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
		)
		print(result)

		print("Project was loaded!")
		return ["js","""
			window.location.href = "/";
		"""]

	def save(self, project_name):
		print("Project was saved!")
		self.name = project_name
		return ["success","Project was saved!"]

	def get_name(self):
		#print("Error function was called!")
		return self.name
