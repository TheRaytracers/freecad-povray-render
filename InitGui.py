import FreeCADGui as Gui
import FreeCAD as App

class PovRayRendering (Workbench):
	"Workbench object to export models to POV-Ray"
				
	MenuText = "POV-Ray-Rendering"
	ToolTip = "Render your models easily with POV-Ray"

	def __init__(self):
		import helpDefs
		self.__class__.Icon = helpDefs.initGui__logoPath
	
	def GetClassName(self):
		return "Gui::PythonWorkbench"
	
	def Initialize(self):
		import ExportCommand, LightCommands, helpDefs

		self.appendToolbar("POV-Ray-Rendering", ["Export", "PointLightCommand", "AreaLightCommand", "SpotLightCommand"])
		self.appendMenu("&POV-Ray-Rendering", ["Export", "PointLightCommand", "AreaLightCommand", "SpotLightCommand"])

		Gui.addIconPath(helpDefs.initGui__iconPath)
		
		Gui.addPreferencePage(helpDefs.initGui__prefPagePath, "POV-Ray-Rendering")

		helpDefs.setDefaultPovRayExe()

		Log ("Loading POV-Ray-Rendering ... done\n")

	def Activated(self):
		# Msg ("PovRay.Activated()\n")
		pass

	def Deactivated(self):
		# Msg ("PovRay.Deactivated()\n")
		pass

Gui.addWorkbench(PovRayRendering)
