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

from PySide import QtCore, QtGui
import os

def showError(text, title): #show an error box
    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title, text)
    dialog.setWindowModality(QtCore.Qt.ApplicationModal)
    dialog.exec_()

def isAscii(string): #test whether the string is an ASCII string
    return all(ord(c) < 128 for c in string)

def stringCorrection(inputString): # String correction for compatibility with POV-Ray 
        utfString = inputString.encode("utf8", "replace")     # conversion from ??? to utf8
        uniString = utfString.decode("utf8", "replace")       # conversion from utf8 to unicode
        firstchar = ord(uniString[0])                         # POV-Ray doesn't like numbers as first character
        if firstchar >= 48 and firstchar <= 57:
            uniString = "_" + uniString
        uniString = uniString.replace(u"Ä", "Ae")             # replacement of mutated vowels (german "Umlaute")
        uniString = uniString.replace(u"ä", "ae")
        uniString = uniString.replace(u"Ü", "Ue")
        uniString = uniString.replace(u"ü", "ue")
        uniString = uniString.replace(u"Ö", "Oe")
        uniString = uniString.replace(u"ö", "oe")
        uniString = uniString.replace(u"ß", "ss")
        uniString = uniString.replace(u"(", "_")
        uniString = uniString.replace(u")", "_")
        uniString = uniString.replace(u"#", "_")
        uniString = uniString.replace(u".", "_")
        uniString = uniString.replace(u",", "_")
        uniString = uniString.replace(u"-", "_")
        uniString = uniString.replace(u"+", "_")
        uniString = uniString.replace(u"*", "_")
        uniString = uniString.replace(u"/", "_")
        uniString = uniString.replace(" ", "_")
        outString = uniString.encode("ASCII", "replace")      # conversion to ASCII for POV-Ray compatibility
        return outString.decode("utf-8")                      #return and redecode to unicode but with converted chars

def strToBool(str):
    if str == True:
        return True
    elif str == False:
        return False

    return str.lower() in ['true', '1', 'y']

class __Preferences__:
    def __init__(self):
        self.prefPath = "User parameter:BaseApp/Preferences/Mod/POV-Ray-Rendering"

preferences = __Preferences__()

def setDefaultPovRayExe():
    if App.ParamGet(preferences.prefPath).GetString("PovRayExe", "") == "":
        renderWbExe = App.ParamGet(
            "User parameter:BaseApp/Preferences/Mod/Render").GetString("PovRayPath", "")
        if renderWbExe == "":
            raytracingWbExe = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing").GetString("PovrayExecutable", "")
            
            if raytracingWbExe != "":
                App.ParamGet(preferences.prefPath).SetString(
                    "PovRayExe", raytracingWbExe)
        else:
            App.ParamGet(preferences.prefPath).SetString("PovRayExe", renderWbExe)


class RenderSettings:
    """Class to store all settings from the dialog, passed to Exporter as argument."""

    def __init__(self, directory, projectName, width, height, expLight, repRot, expFcView, radiosity, hdriDict):
        self.projectName = projectName
        self.directory = directory

        self.iniName = self.projectName + ".ini"
        self.iniPath = self.directory + self.iniName
        self.povName = self.projectName + ".pov"
        self.povPath = self.directory + self.povName

        import re
        numOfImages = 0

        for fileName in os.listdir(self.directory):
            # is a file
            if os.path.isfile(os.path.join(self.directory, fileName)):
                # does the filename fits the regex pattern
                matchObj = re.search(self.projectName +
                                     ' \(([0-9]+)\)\.png', fileName)
                if matchObj:
                    # is the number bigger than the number of the other images
                    if int(matchObj.group(1)) > numOfImages:
                        numOfImages = int(matchObj.group(1))

        self.pngName = self.projectName + " (" + str(numOfImages + 1) + ").png"
        self.pngPath = self.directory + self.pngName

        self.incName = self.projectName + "_user.inc"
        self.incPath = self.directory + self.incName
        self.meshName = self.projectName + "_meshes.inc"
        self.meshPath = self.directory + self.meshName
        self.errorName = self.projectName + "_FatalError.out"
        self.errorPath = self.directory + self.errorName
        self.fcViewName = self.projectName + "_FC-View.png"
        self.fcViewPath = self.directory + self.fcViewName
        self.texIncName = self.projectName + "_textures.inc"
        self.texIncPath = self.directory + self.texIncName

        # get all output options
        self.width = width
        self.height = height

        self.expLight = expLight
        self.repRot = repRot
        self.expFcView = expFcView

        # radiosity
        self.radiosity = radiosity

        # environment
        self.hdriDict = hdriDict

#set the icon path because InitGui.py can't import os
initGui__iconPath = os.path.join(os.path.dirname(__file__), "icons")
initGui__logoPath = os.path.join(os.path.dirname(__file__), "icons", "logo.svg")
initGui__prefPagePath = os.path.join(os.path.dirname(__file__), "prefPage.ui")

# path to thumbnails
thumbnailPath = os.path.join(os.path.dirname(__file__), "thumbnails")