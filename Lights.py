import FreeCAD as App
import FreeCADGui as Gui
import os

class PointLight:
    def __init__(self, obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self, obj):
        if not "Color" in obj.PropertiesList:
            obj.addProperty("App::PropertyColor", "Color").Color = (1.0, 1.0, 1.0, 0.0)
        if not "Fade Distance" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "Fade Distance")
        if not "Fade Distance" in obj.PropertiesList:
            obj.addProperty("App::PropertyInteger", "Fade Power") #XXX negative values are not allowed

    def execute(self, obj):
        return True

class ViewProviderPointLight:
    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.Object = vobj.Object

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def getDisplayModes(self, vobj):
        return ["Default"]

    def getDefaultDisplayMode(self):
        return "Default"

    def setDisplayMode(self, mode):
        return mode

    def isShow(self):
        return True

    def getIcon(self):
        return os.path.join(os.path.dirname(__file__),"icons","pointLight.svg")
