import FreeCAD as App
import FreeCADGui as Gui
import os
from pivy import coin
import math
from helpDefs import preferences

class PointLight:
    def __init__(self, obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self, obj):
        if not "Color" in obj.PropertiesList:
            obj.addProperty("App::PropertyColor",
                            "Color",
                            "Light",
                            "Color of the Light")
            obj.Color = (1.0, 1.0, 1.0, 0.0)

        if not "FadeDistance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength",
                            "FadeDistance",
                            "Light",
                            "Distance of full light intensity")
            obj.FadeDistance = 0

        if not "FadePower" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat",
                            "FadePower", "Light",
                            "Potency of light decrease (2=quadratic, 3=cubic, etc.)")
            obj.FadePower = 0 #XXX negative values are not allowed

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
        img.filename = os.path.join(os.path.dirname(__file__), "icons", "pointLight.svg")
        img.vertAlignment = img.CENTER
        img.horAlignment = img.CENTER
        img.width = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)
        img.height = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)
        self.defaultStyle.addChild(img)
        obj.addDisplayMode(self.defaultStyle, "Default")

    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        pass

    def getDisplayModes(self, obj):
        '''Return a list of display modes.'''
        modes = []
        modes.append("Default")
        return modes

    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Default"

    def setDisplayMode(self, mode):
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

    def __setstate__(self, state):
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
        if not "FadeDistance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "FadeDistance", "Light", "Distance of full light intensity").FadeDistance = 0
        if not "FadePower" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "FadePower", "Light", "Potency of light decrease (2=quadratic, 3=cubic, etc.)").FadePower = 0 #XXX negative values are not allowed

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

        if not "Area Illumination" in obj.PropertiesList:
            obj.addProperty("App::PropertyBool", "Area Illumination", "AreaLight", "TOOLTIP NEEDED").Area_Illumination = False

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

        if self.lengthLights == 1:
            x = self.length / 2
        else:
            x = self.length / (self.lengthLights - 1)

        if self.widthLights == 1:
            y = self.width / 2
        else:
            y = self.width / (self.widthLights - 1)

        for i in range(self.lengthLights):
            for k in range(self.widthLights):
                sep = coin.SoSeparator()
                trans = coin.SoTranslation()
                trans.translation.setValue([-self.length / 2 + x * i, -self.width / 2 + y * k, 0])

                img = coin.SoImage()
                img.filename = os.path.join(os.path.dirname(__file__),"icons","pointLight.svg")
                img.vertAlignment = img.CENTER
                img.horAlignment = img.CENTER
                img.width = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)
                img.height = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)

                sep.addChild(trans)
                sep.addChild(img)

                self.defaultStyle.addChild(sep)
 
    def getDisplayModes(self, obj):
        '''Return a list of display modes.'''
        modes = []
        modes.append("Default")
        return modes
 
    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Default"
 
    def setDisplayMode(self, mode):
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
 
    def __setstate__(self, state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None


class SpotLight:
    def __init__(self, obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self, obj):
        if not "Color" in obj.PropertiesList:
            obj.addProperty("App::PropertyColor", "Color", "Light", "Color of the Light").Color = (1.0, 1.0, 1.0, 0.0)
        if not "FadeDistance" in obj.PropertiesList:
            obj.addProperty("App::PropertyLength", "FadeDistance", "Light", "Distance of full light intensity").FadeDistance = 0
        if not "FadePower" in obj.PropertiesList:
            obj.addProperty("App::PropertyFloat", "FadePower", "Light", "Potency of light decrease (2=quadratic, 3=cubic, etc.)").FadePower = 0 #XXX negative values are not allowed

        if not "Radius" in obj.PropertiesList:
            obj.addProperty("App::PropertyAngle", "Radius", "SpotLight", "Angle of the bright center").Radius = 30
        if not "FallOff" in obj.PropertiesList:
            obj.addProperty("App::PropertyAngle", "FallOff", "SpotLight", "Angle of the outer light circle").FallOff = 45
        if not "Tightness" in obj.PropertiesList:
            obj.addProperty("App::PropertyIntegerConstraint", "Tightness", "SpotLight", "Exponential softening of the edges").Tightness = (0, 0, 100, 1)

    def execute(self, obj):
        return True

class ViewProviderSpotLight:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.addProperty("App::PropertyLength", "RadiusHeight", "SpotLight", "Height of the radius cone")
        obj.RadiusHeight = 100

        obj.addProperty("App::PropertyLength", "FallOffHeight", "SpotLight", "Height of the fall off cone")
        obj.FallOffHeight = 100

        obj.addProperty("App::PropertyBool", "ShowCones", "SpotLight", "Show the cones, that are representing the light")
        obj.ShowCones = True

        obj.Proxy = self

    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.radiusHeight = 100
        self.fallOffHeight = 100
        self.showCones = True
        self.defaultStyle = coin.SoGroup()


        self.radiusSep = coin.SoSeparator()
        self.radiusCone = coin.SoCone()
        self.radiusCone.height = self.radiusHeight

        self.radiusTrans = coin.SoTranslation()
        self.radiusTrans.translation.setValue([0, -self.radiusHeight / 2, 0])

        radiusMaterial = coin.SoMaterial()
        radiusMaterial.transparency.setValue(0.75)
        radiusMaterial.diffuseColor.setValue(coin.SbColor(1, 1, 0))

        radiusComplexity = coin.SoComplexity()
        radiusComplexity.value = 0.99

        self.radiusSep.addChild(self.radiusTrans)
        self.radiusSep.addChild(radiusMaterial)
        self.radiusSep.addChild(radiusComplexity)
        self.radiusSep.addChild(self.radiusCone)
        self.defaultStyle.addChild(self.radiusSep)


        self.fallOffSep = coin.SoSeparator()
        self.fallOffCone = coin.SoCone()
        self.fallOffCone.height = self.fallOffHeight

        self.fallOffTrans = coin.SoTranslation()
        self.fallOffTrans.translation.setValue([0, -self.fallOffHeight / 2, 0])

        fallOffMaterial = coin.SoMaterial()
        fallOffMaterial.transparency.setValue(0.75)
        fallOffMaterial.diffuseColor.setValue(coin.SbColor(1, 1, 0))

        fallOffComplexity = coin.SoComplexity()
        fallOffComplexity.value = 0.9

        self.fallOffSep.addChild(self.fallOffTrans)
        self.fallOffSep.addChild(fallOffMaterial)
        self.fallOffSep.addChild(fallOffComplexity)
        self.fallOffSep.addChild(self.fallOffCone)

        img = coin.SoImage()
        img.filename = os.path.join(os.path.dirname(__file__), "icons", "pointLight.svg")
        img.vertAlignment = img.CENTER
        img.horAlignment = img.CENTER
        img.width = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)
        img.height = App.ParamGet(preferences.prefPath).GetInt("LightIconSize", 16)

        self.defaultStyle.addChild(self.fallOffSep)
        self.defaultStyle.addChild(img)

        obj.addDisplayMode(self.defaultStyle, "Default")

    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        # fp is the handled feature, prop is the name of the property that has changed
        self.radius = fp.getPropertyByName("Radius").getValueAs("rad").Value
        self.fallOff = fp.getPropertyByName("FallOff").getValueAs("rad").Value

        self.updateConeRadius()

    def updateConeRadius(self):
        radius_r = math.tan(self.radius) * self.radiusHeight
        fallOff_r = math.tan(self.fallOff) * self.fallOffHeight

        self.radiusCone.bottomRadius = radius_r
        self.fallOffCone.bottomRadius = fallOff_r

    def getDisplayModes(self, obj):
        '''Return a list of display modes.'''
        modes = []
        modes.append("Default")
        return modes

    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Default"

    def setDisplayMode(self, mode):
        '''Map the display mode defined in attach with those defined in getDisplayModes.\
                Since they have the same names nothing needs to be done. This method is optional'''
        return mode

    def onChanged(self, vp, prop):
        '''Here we can do something when a single property got changed'''
        if prop == "RadiusHeight":
            height = vp.getPropertyByName("RadiusHeight").getValueAs("mm").Value
            self.radiusHeight = height
            self.radiusCone.height = height
            self.radiusTrans.translation.setValue([0, -height / 2, 0])

            self.updateConeRadius()

        elif prop == "FallOffHeight":
            height = vp.getPropertyByName("FallOffHeight").getValueAs("mm").Value
            self.fallOffHeight = height
            self.fallOffCone.height = height
            self.fallOffTrans.translation.setValue([0, -height / 2, 0])

            self.updateConeRadius()

        elif prop == "ShowCones":
            self.showCones = vp.getPropertyByName("ShowCones")

            if self.showCones:
                self.defaultStyle.addChild(self.radiusSep)
                self.defaultStyle.addChild(self.fallOffSep)
            else:
                self.defaultStyle.removeChild(self.radiusSep)
                self.defaultStyle.removeChild(self.fallOffSep)

    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
                optional and if not defined a default icon is shown.'''
        return os.path.join(os.path.dirname(__file__), "icons", "spotLight.svg")

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self, state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None
