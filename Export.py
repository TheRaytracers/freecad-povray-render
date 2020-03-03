import FreeCAD as App
import FreeCADGui as Gui

class Export:
	"Open dialog and start export"

	def GetResources(self):
		return {"MenuText": "Export Model",
				"Accel": "Ctrl+E",
				"ToolTip": "Open Settings Dialog and start Export",
				"Pixmap"  : "export.svg"}

	def IsActive(self):
		if App.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		App.Console.PrintWarning("Start Export")

Gui.addCommand('Export', Export())
