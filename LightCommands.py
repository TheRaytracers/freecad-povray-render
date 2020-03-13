# -*- coding: utf-8 -*-

#  Export FreeCAD models to POV-Ray
#  Copyright (C) 2019  Usb Hub and DerUhrmacher
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import FreeCAD as App
import FreeCADGui as Gui

class PointLightCommand:
    "Insert a point light"

    def GetResources(self):
        return {"MenuText": "Insert Point Light",
				"Accel": "Ctrl+P",
				"ToolTip": "Insert a point light (shining in every direction)",
				"Pixmap"  : "pointLight.svg"}
                
    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True
            
    def Activated(self):
        from Lights import PointLight
        from Lights import ViewProviderPointLight

        light = App.ActiveDocument.addObject("Part::FeaturePython","PointLight")
        PointLight(light)
        ViewProviderPointLight(light.ViewObject)
        App.ActiveDocument.recompute()

Gui.addCommand('PointLightCommand', PointLightCommand())


class AreaLightCommand:
    "Insert an area light"

    def GetResources(self):
        return {"MenuText": "Insert an Area Light",
				"Accel": "Ctrl+A",
				"ToolTip": "Insert an area light (array of lights)",
				"Pixmap"  : "areaLight.svg"}
                
    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True
            
    def Activated(self):
        from Lights import AreaLight
        from Lights import ViewProviderAreaLight

        light = App.ActiveDocument.addObject("Part::FeaturePython","AreaLight")
        AreaLight(light)
        ViewProviderAreaLight(light.ViewObject)
        App.ActiveDocument.recompute()

Gui.addCommand('AreaLightCommand', AreaLightCommand())
