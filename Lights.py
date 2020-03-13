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
            obj.addProperty("App::PropertyColor", "Color", "Light", "Color of the Light").Color = (1.0, 1.0, 1.0, 0.0)
        if not "Fade Distance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "Fade Distance", "Light", "Distance of full light intensity").Fade_Distance = 0
        if not "Fade Power" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "Fade Power", "Light", "Potency of light decrease (2=quadratic, 3=cubic, etc.)").Fade_Power = 0 #XXX negative values are not allowed

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

class AreaLight:
    def __init__(self, obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self, obj):
        if not "Color" in obj.PropertiesList:
            obj.addProperty("App::PropertyColor", "Color", "Light", "Color of the Light").Color = (1.0, 1.0, 1.0, 0.0)
        if not "Fade Distance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "Fade Distance", "Light", "Distance of full light intensity").Fade_Distance = 0
        if not "Fade Power" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "Fade Power", "Light", "Potency of light decrease (2=quadratic, 3=cubic, etc.)").Fade_Power = 0 #XXX negative values are not allowed

        if not "Width" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "Width", "AreaLight", "The width of the area light").Width = 50
        if not "Length" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "Length", "AreaLight", "The length of the area light").Length = 50

        if not "WidthLights" in obj.PropertiesList:
            obj.addProperty("App::PropertyIntegerConstraint", "WidthLights", "AreaLight", "Number of lights in width axis").WidthLights = (5, 1, 9999, 1)
        if not "LengthLights" in obj.PropertiesList:
            obj.addProperty("App::PropertyIntegerConstraint", "LengthLights", "AreaLight", "Number of lights in length axis").LengthLights = (5, 1, 9999, 1)

        if not "Adaptive" in obj.PropertiesList:
            obj.addProperty("App::PropertyIntegerConstraint", "Adaptive", "AreaLight", "The higher the number, the better the rendering result, but also the slower").Adaptive = (1, 0, 9999, 1)
        if not "Jitter" in obj.PropertiesList:
            obj.addProperty("App::PropertyBool", "Jitter", "AreaLight", "Random shadow softening").Jitter = True

    def execute(self, obj):
        return True

class ViewProviderAreaLight:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
 
    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.defaultStyle = coin.SoGroup()
        obj.addDisplayMode(self.defaultStyle, "Default")
 
    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        # fp is the handled feature, prop is the name of the property that has changed
        self.defaultStyle.removeAllChildren()

        self.length = fp.getPropertyByName("Length").getValueAs("mm").Value
        self.width = fp.getPropertyByName("Width").getValueAs("mm").Value
        self.lengthLights = int(fp.getPropertyByName("LengthLights"))
        self.widthLights = int(fp.getPropertyByName("WidthLights"))

        x = self.length / self.lengthLights
        y = self.width / self.widthLights

        for i in range(self.lengthLights):
            for k in range(self.widthLights):
                sep = coin.SoSeparator()
                trans = coin.SoTranslation()
                trans.translation.setValue([x * i, y * k, 0])

                img = coin.SoImage()
                img.filename = os.path.join(os.path.dirname(__file__),"icons","pointLight.svg")
                sep.addChild(trans)
                sep.addChild(img)

                self.defaultStyle.addChild(sep)
 
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
        return os.path.join(os.path.dirname(__file__),"icons","areaLight.svg")
 
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None
 
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None