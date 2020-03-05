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
import platform
import subprocess
import xml.etree.ElementTree as xml
import csv
import hashlib
import tempfile

from helpDefs import *
from Exporter import ExportToPovRay

class Dialog(QtGui.QDialog): #the pyside class for the dialog window
    def __init__(self):
        super(Dialog, self).__init__()
        self.exporter = ExportToPovRay()
        self.initUI()
        self.setDefaultValues()

    def initUI(self): #create the objects in the dialog window
        self.setWindowTitle("Export to POV-Ray")

        #pov file selection
        self.pathLineEdit = QtGui.QLineEdit()
        self.pathLineEdit.setPlaceholderText("Path to INI File")
        self.pathLineEdit.setToolTip("Path to the INI file (kind of a project file)")
        self.pathLineEdit.setFixedWidth(300)
        #self.pathLineEdit.textChanged.connect(self.handlePath)
        self.pathLineEdit.setEnabled(False)

        self.openFileDialogButton = QtGui.QPushButton("Open Project File (*.ini)")
        self.openFileDialogButton.clicked.connect(self.openFileDialog)
        self.openFileDialogButton.setToolTip("Open file dialog for choosing a INI file")

        self.warnLabel = QtGui.QLabel("")
        self.warnLabel.setStyleSheet("QLabel { color : #ff0000; }")

        self.horizLayout1 = QtGui.QGridLayout()
        self.horizLayout1.addWidget(self.pathLineEdit, 0, 0)
        self.horizLayout1.addWidget(self.openFileDialogButton, 0, 1)
        self.horizLayout1.addWidget(self.warnLabel, 1, 0, 1, 2)

        self.pathGroup = QtGui.QGroupBox("Output File Selection")
        self.pathGroup.setLayout(self.horizLayout1)

        #Width & Height of rendered image
        self.imageWidthLabel = QtGui.QLabel("Width")
        self.imageWidth = QtGui.QSpinBox()
        self.imageWidth.setMinimum(1)
        self.imageWidth.setMaximum(999999)
        self.imageWidth.setSuffix(" px")
        self.imageWidth.setValue(800)
        self.imageWidth.setToolTip("Width of the rendered image in pixels")
        self.imageHeightLabel = QtGui.QLabel("Height")
        self.imageHeight = QtGui.QSpinBox()
        self.imageHeight.setMinimum(1)
        self.imageHeight.setMaximum(999999)
        self.imageHeight.setSuffix(" px")
        self.imageHeight.setValue(600)
        self.imageHeight.setToolTip("Height of the rendered image in pixels")

        self.vertLayout1 = QtGui.QVBoxLayout()
        self.vertLayout1.addWidget(self.imageWidthLabel)
        self.vertLayout1.addWidget(self.imageWidth)
        self.vertLayout1.addWidget(self.imageHeightLabel)
        self.vertLayout1.addWidget(self.imageHeight)
        self.WHImageGroup = QtGui.QGroupBox("Width and Height of rendered Image")
        self.WHImageGroup.setLayout(self.vertLayout1)

        #Options
        self.expBg = QtGui.QCheckBox("Export FreeCAD Background")
        self.expBg.setToolTip("Export the FreeCAD background like you see it (editable via the settings)<br>Define your own background if you uncheck this option")
        
        self.expLight = QtGui.QCheckBox("Export FreeCAD Light")
        self.expLight.setToolTip("Export the light FreeCAD uses. Define your own light if you uncheck this option")

        self.repRot = QtGui.QCheckBox("Repair Rotation")
        self.repRot.setToolTip("Repair the rotation of all objects. Visit the Help tab for more information.")
        
        self.expFcView = QtGui.QCheckBox("Export FreeCAD View")
        self.expFcView.setToolTip("Take a screenshot of the scene view and save it with the same resolution as the image")

        self.vertLayout2 = QtGui.QVBoxLayout()
        self.vertLayout2.addWidget(self.expBg)
        self.vertLayout2.addWidget(self.expLight)
        self.vertLayout2.addWidget(self.repRot)
        self.vertLayout2.addWidget(self.expFcView)
        self.optionGroups = QtGui.QGroupBox("Options")
        self.optionGroups.setLayout(self.vertLayout2)

        #add widgets to the main layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.pathGroup)
        self.mainLayout.addWidget(self.WHImageGroup)
        self.mainLayout.addWidget(self.optionGroups)

        #create macro group
        self.macroGroup = QtGui.QGroupBox("")
        self.macroGroup.setLayout(self.mainLayout)

        #crate help group
        self.helpLabel = QtGui.QLabel("")

        #create tabs
        self.textureTab = TextureTab()

        self.tabs = QtGui.QTabWidget(self)
        self.tabs.addTab(self.macroGroup, "Macro")
        self.tabs.addTab(self.textureTab, "Textures")
        self.tabs.addTab(self.helpLabel, "Help")

        # ok cancel buttons
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.onOk)
        self.buttonBox.rejected.connect(self.onCancel)

        self.wrapLayout = QtGui.QVBoxLayout()
        self.wrapLayout.addWidget(self.tabs)
        self.wrapLayout.addWidget(self.buttonBox)
        self.setLayout(self.wrapLayout)
        self.show()

    def setDefaultValues(self): #set the default values of the input objects
        helpText = """
        <style>
        div { margin: 15;}
        </style>
        <div>
        <h3>General</h3>
        <p>This macro exports solid CSG primitives to POV-Ray.<br>
        The resulting POV code is readable and intended for further editing.<br>
        You can add user defined material for each object in a <br>
        seperate .inc file that won't be overwritten.</p>
        <h3>Pov File Selection</h3>
        <p>Select the ini file by typing the path into the text field or choose a .ini file <br>
        with the '…' button.<br>
        Be careful not to use spaces or special chars in pathname for POV-Ray compatibility.</p>
        <h3>Width and Height of the Image</h3>
        <p>Select the width and height in pixels of the image to be rendered with POV-Ray.</p>
        <h3>Options</h3>
        <h5>Export Background</h5>
        <p>Export the FreeCAD background</p>
        <h5>Export Light</h5>
        <p>Export the FreeCAD light. Define your own light in the inc file if you uncheck this option</p>
        <h5>Repair Rotation</h5>
        <p>Use this option if objects in your scene appear in a wrong rotation.<br>
        This is a workaround for a FreeCAD bug.</p>
        <h5>Export FreeCAD View</h5>
        <p>Export the current FreeCAD view in the same size as the image rendered by POV-Ray<br></p>
        <p>For more information look in our <a href='https://gitlab.com/usbhub/exporttopovray/blob/master/doc/index.md'>Wiki</a></p>
        </div>"""
        self.helpLabel.setText(helpText)
        self.helpLabel.setOpenExternalLinks(True)


        #get saved input
        settings = QtCore.QSettings("Usb Hub, DerUhrmacher", "Export to POV-Ray")
        settings.beginGroup("userInput")

        if App.ActiveDocument.Name in settings.allKeys():
            iniPath = settings.value(App.ActiveDocument.Name)
        else:
            iniPath = -1

        settings.endGroup()

        self.setIniSettings(iniPath)

        self.textureTab.setDefaultValues(settings)
        self.textureTab.setIniSettings(iniPath)

    def setIniSettings(self, iniPath):
        #open ini file and extract CSV
        try:
            iniFile = open(iniPath, "r")
        except:
            App.Console.PrintWarning("Could not open ini file\n")
            iniPath = -1
                
        if iniPath == -1 or iniPath == "" or iniPath == None:
            #set some good standardValues
            system = platform.system()
            if system == "Linux":
                defaultPath = "/home/"
            elif system == "Darwin":
                defaultPath = "/Users/"
            elif system == "Windows":
                defaultPath = "C:\\Users\\%UserName%\\"
            else:
                defaultPath = ""

            self.pathLineEdit.setText(defaultPath)
            self.checkPath(defaultPath)

            self.imageWidth.setValue(800)
            self.imageHeight.setValue(600)

            self.expBg.setChecked(True)
            self.expLight.setChecked(True)
            self.expFcView.setChecked(False)
            self.repRot.setChecked(False)

        else:
            self.pathLineEdit.setText(iniPath)
            self.checkPath(iniPath)

            lines = iniFile.readlines()
            iniFile.close()

            csvLines = []

            for line in lines:
                if line.startswith(";"):
                    csvLines.append(line[1:])

            #parse CSV
            csvReader = csv.reader(csvLines, delimiter=',')

            for row in csvReader:
                if row[0].startswith("stg_"):
                    name = row[0][4:]

                    if name == "width":
                        self.imageWidth.setValue(int(row[1]))
                    elif name == "height":
                        self.imageHeight.setValue(int(row[1]))
                    elif name == "expBg":
                        self.expBg.setChecked(strToBool(row[1]))
                    elif name == "expLight":
                        self.expLight.setChecked(strToBool(row[1]))
                    elif name == "repRot":
                        self.repRot.setChecked(strToBool(row[1]))
                    elif name == "expFcView":
                        self.expFcView.setChecked(strToBool(row[1]))

            self.textureTab.setIniSettings(csvLines)

    def openFileDialog(self): #open the file dialog for the pov file
        defaultPath = self.pathLineEdit.text()

        fileName = QtGui.QFileDialog.getSaveFileName(None, 'Select path and name of the *.ini file', defaultPath, "POV-Ray INI Files (*.ini)")

        if fileName and fileName != (u'', u''):
            self.pathLineEdit.setText(str(fileName[0]))
            self.handlePath(str(fileName[0]))

    def handlePath(self, path):
        pathLegal = self.checkPath(path)

        if pathLegal:
            #ask to apply settings from selected file
            content = "Do you want to apply the settings from the selected file?\n"
            content += "Click 'Apply' if you want to adopt the settings from the file."
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Question, "Apply settings from file?", content, QtGui.QMessageBox.Apply | QtGui.QMessageBox.No)
            dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            answer = dialog.exec_()

            if answer == QtGui.QMessageBox.Apply:
                self.setIniSettings(path)
    
    def checkPath(self, path): #check if the path to pov file is valid
        if path.find(" ") == -1 and isAscii(path) == True and path != "" and path[-4:].lower() == ".ini":
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
            self.warnLabel.setText("")
            return True
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
            if path == "":
                self.warnLabel.setText("Please type a path or get one with clicking on '…'")
            else:
                self.warnLabel.setText("Your path contains a space or a mutated vowel or is not a .ini file")

            return False

    def saveActiveDocName(self): #save the user inputs
        settings = QtCore.QSettings("Usb Hub, DerUhrmacher", "Export to POV-Ray")
        settings.beginGroup("userInput")
        settings.setValue(App.ActiveDocument.Name, self.pathLineEdit.text())
        settings.endGroup()

        self.textureTab.saveUserInput(settings)

    def writeIni(self):
        self.iniFile = open(self.renderSettings.iniPath, "w")
        self.iniFile.write(self.iniContent)
        self.iniFile.close()

    def settingsToCSV(self):
        csv = ""

        #add render settings
        csv += ";stg_povPath," + self.renderSettings.povPath + "\n"
        csv += ";stg_width," + str(self.renderSettings.width) + "\n"
        csv += ";stg_height," + str(self.renderSettings.height) + "\n"
        csv += ";stg_expBg," + str(self.renderSettings.expBg) + "\n"
        csv += ";stg_expLight," + str(self.renderSettings.expLight) + "\n"
        csv += ";stg_repRot," + str(self.renderSettings.repRot) + "\n"
        csv += ";stg_expFcView," + str(self.renderSettings.expFcView) + "\n"

        csv += self.textureTab.settingsToCSV()

        self.csv = csv

    def createIniContent(self):
        self.settingsToCSV()
        
        self.iniContent = ""
        self.iniContent += self.csv + "\n"
        self.iniContent += "Input_File_Name='" + self.renderSettings.povName + "'\n"
        self.iniContent += "Width=" + str(self.renderSettings.width) + "\n"
        self.iniContent += "Height=" + str(self.renderSettings.height) + "\n"
        self.iniContent += "Fatal_File='" + self.renderSettings.errorName + "'\n"

    def onCancel(self): #called if "Cancel" button is pressed
        self.result = "Canceled"
        self.close()
        App.Console.PrintMessage("\n\nCanceled\n\n")

    def onOk(self): #called if "OK" button is pressed
        self.result = "OK"
        self.close()
        self.saveActiveDocName()

        iniPath = self.pathLineEdit.text()
        directory = os.path.dirname(iniPath) + os.sep
        projectName = os.path.basename(iniPath)[:-4]

        #create renderSettings object
        self.renderSettings = RenderSettings(directory, projectName,
                                             self.imageWidth.value(),
                                             self.imageHeight.value(),
                                             self.expBg.isChecked(),
                                             self.expLight.isChecked(),
                                             self.repRot.isChecked(),
                                             self.expFcView.isChecked())

        self.textureTab.finish(self.renderSettings)

        self.createIniContent()
        self.writeIni()

        self.exporter.initExport(self.renderSettings)


class TextureTab(QtGui.QWidget):
    def __init__(self):
        super(TextureTab, self).__init__()
        self.exporter = ExportToPovRay()
        self.qSettingsGroup = "textureTab"
        self.initTab()

    def initTab(self): #create all necessary stuff for texture tab and connect signals
        self.textureLayout = QtGui.QVBoxLayout() #the wrapper layout for the tab
        
        self.addObjectsTexturesLists() #add the two lists at the top
        self.addScaleRotateTranslate() #add the menu for scaling and rotating at the bottom
        self.addPreview()

        # signals and slots
        self.connectSignals()

        self.previewDisableCheckBox.stateChanged.connect(self.updateSelectedListObject)
        self.zoomIn.pressed.connect(self.largerPreview)
        self.zoomOut.pressed.connect(self.smallerPreview)

        #set layouts
        self.textureLayout.addWidget(self.listWidget)
        self.textureLayout.addWidget(self.textureSettingsWidget)
        self.textureLayout.addWidget(self.previewWidget)

        self.setLayout(self.textureLayout)

    def setDefaultValues(self, settingsObject):
        #get saved input
        settingsObject.beginGroup(self.qSettingsGroup)

        #set preview disable checkbox
        previewDisable = settingsObject.value("previewDisable")
        if previewDisable != None:
            self.previewDisableCheckBox.setChecked(strToBool(previewDisable))
        else:
            self.previewDisableCheckBox.setChecked(True)

        previewWidth = settingsObject.value("previewWidth")
        if previewWidth != None and previewWidth != 0 and previewWidth != -1:
            self.previewWidth = int(previewWidth)
        else:
            self.previewWidth = 300

        previewHeight = settingsObject.value("previewHeight")
        if previewHeight != None and previewHeight != 0 and previewHeight != -1:
            self.previewHeight = int(previewHeight)
        else:
            self.previewHeight = 225

        if App.ActiveDocument.Name in settingsObject.allKeys():
            iniPath = settingsObject.value(App.ActiveDocument.Name)
        else:
            iniPath = -1

        settingsObject.endGroup()

    def saveUserInput(self, settingsObject):
        settingsObject.beginGroup(self.qSettingsGroup)
        settingsObject.setValue("previewDisable", self.previewDisableCheckBox.isChecked())
        settingsObject.setValue("previewWidth", self.previewWidth)
        settingsObject.setValue("previewHeight", self.previewHeight)
        settingsObject.endGroup()

    def largerPreview(self):
        self.previewWidth += 40
        self.previewHeight += 30

        self.updateSelectedListObject()

    def smallerPreview(self):
        if self.previewWidth < 45:
            return

        self.previewWidth -= 40
        self.previewHeight -= 30

        self.updateSelectedListObject()

    def connectSignals(self): #connect all necessary signals for the texture tab
        self.objectList.itemSelectionChanged.connect(self.updateTextureSettings)
        self.textureList.itemSelectionChanged.connect(self.updateSelectedListObject)

        self.scaleX.valueChanged.connect(self.updateSelectedListObject)
        self.scaleY.valueChanged.connect(self.updateSelectedListObject)
        self.scaleZ.valueChanged.connect(self.updateSelectedListObject)

        self.rotationX.valueChanged.connect(self.updateSelectedListObject)
        self.rotationY.valueChanged.connect(self.updateSelectedListObject)
        self.rotationZ.valueChanged.connect(self.updateSelectedListObject)

        self.translationX.valueChanged.connect(self.updateSelectedListObject)
        self.translationY.valueChanged.connect(self.updateSelectedListObject)
        self.translationZ.valueChanged.connect(self.updateSelectedListObject)

    def disconnectSignals(self): #disconnect all signals for the texture tab
        self.objectList.itemSelectionChanged.disconnect()
        self.textureList.itemSelectionChanged.disconnect()

        self.scaleX.valueChanged.disconnect()
        self.scaleY.valueChanged.disconnect()
        self.scaleZ.valueChanged.disconnect()

        self.rotationX.valueChanged.disconnect()
        self.rotationY.valueChanged.disconnect()
        self.rotationZ.valueChanged.disconnect()
        
        self.translationX.valueChanged.disconnect()
        self.translationY.valueChanged.disconnect()
        self.translationZ.valueChanged.disconnect()

    def addObjectsTexturesLists(self): #add the two lists with the objects and textures
        self.listWidget = QtGui.QWidget() #wrapper widget for the two lists
        self.listLayout = QtGui.QGridLayout() #wrapper layout for the two lists

        #texture list
        self.textureList = QtGui.QTreeWidget()
        self.textureList.setHeaderLabel("Type of Predefined")

        self.textureListLabel = QtGui.QLabel("<b>Texture</b>")

        self.predefines = []
        #add FreeCAD texture
        self.fcTexItem = QtGui.QTreeWidgetItem(self.textureList, ["FreeCAD Texture"])
        self.predefines.append(Predefined("FreeCAD Texture", None, None, None, None, None, None, None, "", self.fcTexItem))
        self.fcTexItem.setSelected(True)

        #get the predefined.xml
        predefinedPath = App.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString('MacroPath') #get macro path
        predefinedPath += os.sep + "predefined.xml"

        predefined = xml.parse(predefinedPath).getroot()
        categories = predefined.getchildren()

        #read the predefined.xml and add the predefined defined in the XML
        for categorie in categories:
            #categorieItem = QtGui.QTreeWidgetItem(self.textureList, [categorie.tag])
            #predefs = categorie.getchildren()
            self.predefXmlToList(categorie, self.textureList)


        #add the list to the layouts and widgets
        self.listLayout.addWidget(self.textureListLabel, 0, 1)
        self.listLayout.addWidget(self.textureList, 1, 1)

        self.listWidget.setLayout(self.listLayout)

        #object list
        self.objectList = QtGui.QListWidget()

        self.objectListLabel = QtGui.QLabel("<b>Object</b>")

        #get objects
        objs = App.ActiveDocument.Objects
        self.listFcObjects = []
        for obj in objs:
            #has object a shape color
            try:
                obj.ViewObject.ShapeColor
                shapeColor = True
            except:
                shapeColor = False
            #has object a shape
            try:
                obj.Shape
                obj.Shape.Area
                obj.Shape.isValid()
                shape = True
            except:
                shape = False

            #test for the conditions for a object for the object list
            if obj.ViewObject.Visibility and shapeColor and shape:
                self.listFcObjects.append(obj)

        self.listObjects = []
        #create the listObjects
        for obj in self.listFcObjects:
            try:
                listItem = QtGui.QListWidgetItem(obj.ViewObject.Icon, obj.Label)
            except:
                listItem = QtGui.QListWidgetItem(obj.Label)
            predefined = self.predefines[0]
            self.listObjects.append(ListObject(obj, listItem, self.predefines[0], 1, 1, 1, 0, 0, 0, 0, 0, 0))

            self.objectList.addItem(listItem)
        
        #add the object list to the layouts
        self.listLayout.addWidget(self.objectListLabel, 0, 0)
        self.listLayout.addWidget(self.objectList, 1, 0)

    def predefXmlToList(self, xmlNode, parentNode):
        childNodes = xmlNode.getchildren()

        if childNodes == []:
            treeItem = QtGui.QTreeWidgetItem(parentNode, [xmlNode.text])
            #get all attributes
            attr = xmlNode.attrib
            if "material" in attr:
                material = attr["material"]
            else:
                material = ""

            if "texture" in attr:
                texture = attr["texture"]
            else:
                texture = ""

            if "pigment" in attr:
                pigment = attr["pigment"]
            else:
                pigment = ""

            if "finish" in attr:
                finish = attr["finish"]
            else:
                finish = ""
            
            if "normal" in attr:
                normal = attr["normal"]
            else:
                normal = ""

            if "interior" in attr:
                interior = attr["interior"]
            else:
                interior = ""
                
            if "media" in attr:
                media = attr["media"]
            else:
                media = ""    

            if "inc" in attr:
                inc = attr["inc"]
            else:
                inc = ""

            self.predefines.append(Predefined(xmlNode.text, material, texture, pigment, finish, normal, interior, media, inc, treeItem))

        else:
            categorieItem = QtGui.QTreeWidgetItem(parentNode, [xmlNode.tag])
            for node in childNodes:
                #call method for child nodes
                self.predefXmlToList(node, categorieItem)

    def addScaleRotateTranslate(self): #add the scale and rotate menu
        # scale, rotate, preview
        self.textureSettingsWidget = QtGui.QWidget()
        self.textureSettingsLayout = QtGui.QGridLayout()

        # scale
        self.scalingLabel = QtGui.QLabel("Scale")
        self.textureSettingsLayout.addWidget(self.scalingLabel, 0, 0)

        self.scaleX = QtGui.QDoubleSpinBox()
        self.scaleX.setMaximum(9999999)
        self.scaleX.setMinimum(-9999999)
        self.scaleX.setPrefix("x: ")
        self.textureSettingsLayout.addWidget(self.scaleX, 0, 1)

        self.scaleY = QtGui.QDoubleSpinBox()
        self.scaleY.setMaximum(9999999)
        self.scaleY.setMinimum(-9999999)
        self.scaleY.setPrefix("y: ")
        self.textureSettingsLayout.addWidget(self.scaleY, 0, 2)

        self.scaleZ = QtGui.QDoubleSpinBox()
        self.scaleZ.setMaximum(9999999)
        self.scaleZ.setMinimum(-9999999)
        self.scaleZ.setPrefix("z: ")
        self.textureSettingsLayout.addWidget(self.scaleZ, 0, 3)

        # rotate
        self.rotationLabel = QtGui.QLabel("Rotate")
        self.textureSettingsLayout.addWidget(self.rotationLabel, 1, 0)

        self.rotationX = QtGui.QDoubleSpinBox()
        self.rotationX.setMaximum(360)
        self.rotationX.setMinimum(-360)
        self.rotationX.setPrefix("x: ")
        self.rotationX.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationX, 1, 1)

        self.rotationY = QtGui.QDoubleSpinBox()
        self.rotationY.setMaximum(360)
        self.rotationY.setMinimum(-360)
        self.rotationY.setPrefix("y: ")
        self.rotationY.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationY, 1, 2)

        self.rotationZ = QtGui.QDoubleSpinBox()
        self.rotationZ.setMaximum(360)
        self.rotationZ.setMinimum(-360)
        self.rotationZ.setPrefix("z: ")
        self.rotationZ.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationZ, 1, 3)

        # translation
        self.translationLabel = QtGui.QLabel("Translate")
        self.textureSettingsLayout.addWidget(self.translationLabel, 2, 0)

        self.translationX = QtGui.QDoubleSpinBox()
        self.translationX.setMaximum(9999999)
        self.translationX.setMinimum(-9999999)
        self.translationX.setPrefix("x: ")
        #self.translationX.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.translationX, 2, 1)

        self.translationY = QtGui.QDoubleSpinBox()
        self.translationY.setMaximum(9999999)
        self.translationY.setMinimum(-9999999)
        self.translationY.setPrefix("y: ")
        #self.translationY.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.translationY, 2, 2)

        self.translationZ = QtGui.QDoubleSpinBox()
        self.translationZ.setMaximum(9999999)
        self.translationZ.setMinimum(-9999999)
        self.translationZ.setPrefix("z: ")
        #self.translationZ.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.translationZ, 2, 3)

        self.textureSettingsWidget.setLayout(self.textureSettingsLayout)

    def addPreview(self):
        #disable checkbox
        self.previewDisableCheckBox = QtGui.QCheckBox("Disable Live Preview")

        #zoom buttons
        self.zoomIn = QtGui.QPushButton("Zoom In")
        self.zoomOut = QtGui.QPushButton("Zoom Out")

        #preview setting layout
        self.previewSettingsLayout = QtGui.QHBoxLayout()
        self.previewSettingsLayout.addWidget(self.previewDisableCheckBox)
        self.previewSettingsLayout.addWidget(self.zoomIn)
        self.previewSettingsLayout.addWidget(self.zoomOut)

        #preview image
        self.previewLabel = QtGui.QLabel()
        self.previewLabel.setStyleSheet("QLabel { color : #ff0000; }")

        #main layout
        self.previewLayout = QtGui.QVBoxLayout()
        self.previewLayout.addLayout(self.previewSettingsLayout)
        self.previewLayout.addWidget(self.previewLabel)

        self.previewWidget = QtGui.QWidget()
        self.previewWidget.setLayout(self.previewLayout)

    def updateTextureSettings(self): #get the selected object and select the right predefined
        self.disconnectSignals()
        listObj = self.getSelectedListObject() #get the current selected object

        if listObj == -1: #is an object selected
            self.connectSignals()
            return -1

        #set all values for scaling and rotating
        self.scaleX.setValue(listObj.scaleX)
        self.scaleY.setValue(listObj.scaleY)
        self.scaleZ.setValue(listObj.scaleZ)

        self.rotationX.setValue(listObj.rotationX)
        self.rotationY.setValue(listObj.rotationY)
        self.rotationZ.setValue(listObj.rotationZ)

        self.translationX.setValue(listObj.translationX)
        self.translationY.setValue(listObj.translationY)
        self.translationZ.setValue(listObj.translationZ)

        #unselect all textures
        for predefine in self.predefines:
            predefine.treeItem.setSelected(False)

        #select the right predefined
        listObj.predefObject.treeItem.setSelected(True)

        #expand categories
        self.expandParentItems(listObj.predefObject.treeItem)

        self.renderPreview(listObj)

        self.connectSignals()

    def expandParentItems(self, item):
        parent = item.parent()
        if type(parent) == QtGui.QTreeWidgetItem:
            parent.setExpanded(True)
            self.expandParentItems(parent)

    def updateSelectedListObject(self): #get the selected predefined and update the listObject
        listObj = self.getSelectedListObject()
        predefine = self.getSelectedPredefined()
        if listObj == -1 or predefine == -1: #is no object or predefine selected
            if predefine == -1: #is only a categorie selected
                #expand and select predef under the categorie
                self.disconnectSignals()
                selectedItems = self.textureList.selectedItems()
                selected = selectedItems[0]
                selected.setSelected(False)
                selected.setExpanded(True)
                childItem = selected.child(0)
                self.connectSignals()
                childItem.setSelected(True)

            return -1 #abort

        #get the values for scaling and rotating
        listObj.scaleX = self.scaleX.value()
        listObj.scaleY = self.scaleY.value()
        listObj.scaleZ = self.scaleZ.value()

        listObj.rotationX = self.rotationX.value()
        listObj.rotationY = self.rotationY.value()
        listObj.rotationZ = self.rotationZ.value()

        listObj.translationX = self.translationX.value()
        listObj.translationY = self.translationY.value()
        listObj.translationZ = self.translationZ.value()

        listObj.predefObject = predefine #apply the read values to the predefObject in the listObject

        self.renderPreview(listObj)

    def renderPreview(self, listObj):
        if self.previewDisableCheckBox.isChecked():
            self.previewLabel.setText(" ")
            return

        if listObj.predefObject.material == None: #for FreeCAD materials
            self.previewLabel.setText("The FreeCAD texture is just like you see it in the FreeCAD scene\n so this texture is disabled.")
            return
        elif listObj.predefObject.media != "":
            self.previewLabel.setText("The texture is too complex for a preview and would need a lot of time\nso this texture is disabled.")
            return

        #write file
        fileContent =""
        fileContent += '#version 3.6; // 3.7\n'
        fileContent += 'global_settings { assumed_gamma 1.0 }\n'
        fileContent += '#default { finish { ambient 0.2 diffuse 0.9 } }\n'
        fileContent += '#default { pigment { rgb <0.871, 0.871, 0.871> } }\n'
        fileContent += '//------------------------------------------\n'
        fileContent += '#include "colors.inc"\n'
        fileContent += '#include "textures.inc"\n'
        fileContent += '#declare CamUp = <0, 0, 1>;\n'
        fileContent += '#declare CamRight = <1.33, 0, 0>;\n'
        fileContent += '#declare CamRotation = <-35.264390534, 1.9538003485e-05, 45.0000026303>;\n'
        fileContent += '#declare CamPosition = <25.9077129364, -15.9076957703, 20.907699585>;\n'
        fileContent += 'camera {\n'
        fileContent += '\tlocation <0, 0, 0>\n'
        fileContent += '\tdirection <0, 1, 0>\n'
        fileContent += '\tup CamUp\n'
        fileContent += '\tright CamRight\n'
        fileContent += '\trotate CamRotation\n'
        fileContent += '\ttranslate CamPosition\n'
        fileContent += '\tangle 57.82\n'
        fileContent += '}\n'
        fileContent += 'light_source { CamPosition color rgb <0.5, 0.5, 0.5> }\n'
        fileContent += 'sky_sphere {\n'
        fileContent += '\t\tpigment {\n'
        fileContent += '\t\tgradient z\n'
        fileContent += '\t\tcolor_map {\n'
        fileContent += '\t\t\t[0 rgb<0,0,0>]\n'
        fileContent += '\t\t\t[0.2 rgb<0,0,0>]\n'
        fileContent += '\t\t\t[0.75 rgb<1,1,1>]\n'
        fileContent += '\t\t\t[1 rgb<1,1,1>]\n'
        fileContent += '\t\t\t}\n'
        fileContent += '\t\tscale 2\n'
        fileContent += '\t\ttranslate -1\n'
        fileContent += '\t\t}\n'
        fileContent += '}\n'

        fileContent += self.exporter.listObjectToPov(listObj, "predef")

        fileContent+= 'box { <0,0,0>, <10.0, 10.0, 10.0>\n'
        fileContent += '\ttranslate <5.0, 5.0, -5.0>\n'
        fileContent += '\tmaterial { predef_material }\n'
        fileContent += '}\n'
        fileContent += 'sphere { <0, 0, 0> 5 \n'
        fileContent += '\tmaterial { predef_material }\n'
        fileContent += '}\n'

        povFile = tempfile.NamedTemporaryFile(suffix=".pov") #pov file handler
        povFile.delete = False
        povFile.write(fileContent)

        povName = povFile.name
        povFile.close()

        #render
        povExec = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing").GetString('PovrayExecutable')
        if os.path.isfile(povExec) == False:
            povExec = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Render").GetString('PovrayExecutable')
            if os.path.isfile(povExec) == False:
                errorText = "To get a preview of the texture settings you must\n"
                errorText += "set the path to the POV-Ray executable\n"
                errorText += "either in the settings of Render workbench\n"
                errorText += "or in the settings of Raytracing workbench\n"
                showError(errorText, "POV-Ray executable not found")
                return -1
            povOptions = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Render").GetString('OutputParameters')
        povOptions = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing").GetString('OutputParameters')

        #start povray
        subprocess.call([povExec, "-d", "width=" + str(self.previewWidth), "height=" + str(self.previewHeight), povName])
        
        #update preview widget
        pixmap = QtGui.QPixmap(povName[:-4])
        self.previewLabel.setPixmap(pixmap)

    def getSelectedListObject(self): #get the current selected listObject
        for listObj in self.listObjects:
            if listObj.listItem.isSelected():
                return listObj

        return -1

    def getSelectedPredefined(self): #get the current selected predefined
        for predefine in self.predefines:
            if predefine.treeItem.isSelected():
                return predefine

        return -1

    def setIniSettings(self, csvLines):
        #parse CSV
        csvReader = csv.reader(csvLines, delimiter=',')
        for row in csvReader:
            if row[0].startswith("obj_"):
                name = row[0][4:]
                hash = row[1]

                for listObj in self.listObjects:
                    if listObj.fcObj.Name == name:
                        for predef in self.predefines:
                            if predef.getHash() == hash:
                                listObj.predefObject = predef
                                break

                        listObj.scaleX = float(row[2])
                        listObj.scaleY = float(row[3])
                        listObj.scaleZ = float(row[4])

                        listObj.rotationX = float(row[5])
                        listObj.rotationY = float(row[6])
                        listObj.rotationZ = float(row[7])

                        listObj.translationX = float(row[8])
                        listObj.translationY = float(row[9])
                        listObj.translationZ = float(row[10])

    def settingsToCSV(self):
        csv = ""

        #add settings for every listobject
        for obj in self.listObjects:
            csv += ";obj_" + obj.fcObj.Name + "," + obj.predefObject.getHash() + ","
            csv += str(obj.scaleX) + "," + str(obj.scaleY) + "," + str(obj.scaleZ) + ","
            csv += str(obj.rotationX) + "," + str(obj.rotationY) + "," + str(obj.rotationZ) + ","
            csv += str(obj.translationX) + "," + str(obj.translationY) + "," + str(obj.translationZ) + "\n"

        return csv

    def writeTextureInc(self): #write the texture in content to a file
        self.texIncFile = open(self.renderSettings.texIncPath, "w")
        self.texIncFile.write(self.texIncContent)
        self.texIncFile.close()

    def createTexIncContent(self): #create the content of the texture inc file
        self.texIncContent = ""

        for obj in self.listObjects: #iterate over all listObjects
            self.texIncContent += self.exporter.listObjectToPov(obj)

    def finish(self, renderSettings):
        self.renderSettings = renderSettings

        self.createTexIncContent()
        self.writeTextureInc()


class Predefined:
    def __init__(self, identifier, material, texture, pigment, finish, normal, interior, media, inc, treeItem):
        self.identifier = identifier
        self.material = material
        self.texture = texture
        self.pigment = pigment
        self.finish = finish
        self.normal = normal
        self.interior = interior
        self.media = media
        self.inc = inc
        self.treeItem = treeItem

    def getHash(self):
        #parentCategorie = self.treeItem.parent().text(0)
        predefName = self.treeItem.text(0)

        stgStr = str(self.identifier) + str(self.material) + str(self.texture) + str(self.pigment) + str(self.finish) + str(self.normal) + str(self.interior) + str(self.media) + str(self.inc)
        hashStr = hashlib.md5(stgStr.encode("UTF-8")).hexdigest()[:4]

        #return parentCategorie + "/" + predefName + hashStr
        return predefName + hashStr

class ListObject:
    def __init__(self, fcObj, listItem, predefObject, scaleX, scaleY, scaleZ, rotationX, rotationY, rotationZ, translationX, translationY, translationZ):
        self.fcObj = fcObj
        self.label = stringCorrection(fcObj.Label)

        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ

        self.rotationX = rotationX
        self.rotationY = rotationY
        self.rotationZ = rotationZ

        self.translationX = translationX
        self.translationY = translationY
        self.translationZ = translationZ

        self.listItem = listItem
        self.predefObject = predefObject

class RenderSettings:
    def __init__(self, directory, projectName, width, height, expBg, expLight, repRot, expFcView):
        self.projectName = projectName
        self.directory = directory

        self.iniName = self.projectName + ".ini"
        self.iniPath = self.directory + self.iniName
        self.povName = self.projectName + ".pov"
        self.povPath = self.directory + self.povName
        
        self.incName = self.projectName + ".inc"
        self.incPath = self.directory + self.incName
        self.meshName = self.projectName + "_meshes.inc"
        self.meshPath = self.directory + self.meshName
        self.errorName = self.projectName + "_FatalError.out"
        self.errorPath = self.directory + self.errorName
        self.fcViewName = self.projectName + "_FC-View.png"
        self.fcViewPath = self.directory + self.fcViewName
        self.texIncName = self.projectName + "_textures.inc"
        self.texIncPath = self.directory + self.texIncName

        #get all output options
        self.width = width
        self.height = height

        self.expBg = expBg
        self.expLight = expLight
        self.repRot = repRot
        self.expFcView = expFcView
