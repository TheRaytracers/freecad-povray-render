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
        firstchar = ord(uniString[0])                         # POV-Ray doesn't like numbers as first charakter
        if firstchar >= 48 and firstchar <= 57:
            uniString = "_" + uniString
        uniString = uniString.replace(u"Ä", "Ae")             # replacement of german "Umlaute"
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

#set the icon path because InitGui.py can't import os
initGui__iconPath = os.path.join(os.path.dirname(__file__), "icons")
initGui__prefPagePath = os.path.join(os.path.dirname(__file__), "prefPage.ui")

class __Preferences__:
    def __init__(self):
        self.prefPath = "User parameter:BaseApp/Preferences/Mod/POV-Ray"

preferences = __Preferences__()