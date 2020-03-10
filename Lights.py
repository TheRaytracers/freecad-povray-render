import FreeCAD as App
import FreeCADGui as Gui
import os
from pivy import coin

class PointLight:
    def __init__(self, obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self, obj):
        if not "Color" in obj.PropertiesList:
            obj.addProperty("App::PropertyColor", "Color").Color = (1.0, 1.0, 1.0, 0.0)
        if not "Fade Distance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "Fade Distance")
        if not "Fade Power" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "Fade Power") #XXX negative values are not allowed

    def execute(self, obj):
        return True

class ViewProviderPointLight:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
 
    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.defaultStyle = coin.SoGroup()

        img = coin.SoImage()
        img.filename = os.path.join(os.path.dirname(__file__),"icons","pointLight.svg")
        self.defaultStyle.addChild(img)
        obj.addDisplayMode(self.defaultStyle, "Default")
 
    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        pass
 
    def getDisplayModes(self,obj):
        '''Return a list of display modes.'''
        modes=[]
        modes.append("Default")
        return modes
 
    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Default"
 
    def setDisplayMode(self,mode):
        '''Map the display mode defined in attach with those defined in getDisplayModes.\
                Since they have the same names nothing needs to be done. This method is optional'''
        return mode
 
    def onChanged(self, vp, prop):
        '''Here we can do something when a single property got changed'''
        pass
 
    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
                optional and if not defined a default icon is shown.'''
        return os.path.join(os.path.dirname(__file__),"icons","pointLight.svg")
 
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None
 
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None