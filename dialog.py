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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA

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
from exporter import ExportToPovRay


#########################
### Main Dialog Class ###
#########################

class Dialog(QtGui.QDialog):
    """The main class for the dialog. It creates only the tab independent elements."""

    def __init__(self):
        super(Dialog, self).__init__()
        self.exporter = ExportToPovRay()
        self.initUI()
        self.applyQSettings()

    def initUI(self):
        """Create the dialog window with its tabs, buttons, etc."""

        self.setWindowTitle("Export to POV-Ray")

        # create tabs
        self.generalTab = GeneralTab()
        self.textureTab = TextureTab()
        self.environmentTab = EnvironmentTab()
        self.radiosityTab = RadiosityTab()
        self.helpTab = HelpTab()

        self.tabs = QtGui.QTabWidget(self)
        self.tabs.addTab(self.generalTab, "General")
        self.tabs.addTab(self.textureTab, "Textures")
        self.tabs.addTab(self.environmentTab, "Environment (beta)")
        self.tabs.addTab(self.radiosityTab, "Indirect Lighting")
        self.tabs.addTab(self.helpTab, "Help")

        # ok cancel buttons
        self.renderButton = QtGui.QPushButton("Start Rendering")
        self.cancelButton = QtGui.QPushButton("Cancel")

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(
            self.renderButton,
            QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(
            self.cancelButton,
            QtGui.QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.onOk)
        self.buttonBox.rejected.connect(self.onCancel)

        self.wrapLayout = QtGui.QVBoxLayout()
        self.wrapLayout.addWidget(self.tabs)
        self.wrapLayout.addWidget(self.buttonBox)
        self.setLayout(self.wrapLayout)
        self.show()

        self.generalTab.iniPathChanged.connect(self.applyIniSettings)
        self.generalTab.iniPathValidityChanged.connect(
            self.setDialogAcceptable)

        self.environmentTab.hdrPathValidityChanged.connect(
            self.setDialogAcceptable)


    def setDialogAcceptable(self, acceptable):
        """Set if the "Start Rendering" button should be enabled.

        Args:
            acceptable (bool): True: Enabled; False: Disabled
        """

        self.renderButton.setEnabled(acceptable)


    ### Settings Stuff ###
    ######################

    def saveQSettings(self):
        """Call the saveQSettings() method from the tab classes to save
        the project independent settings with QSettings."""

        settings = QtCore.QSettings(
            "Usb Hub, DerUhrmacher", "Export to POV-Ray")

        self.generalTab.saveQSettings(settings)
        self.textureTab.saveQSettings(settings)
        self.environmentTab.saveQSettings(settings)
        self.radiosityTab.saveQSettings(settings)
        self.helpTab.saveQSettings(settings)

    def applyQSettings(self):
        """Call the applyQSettings() method from the tab classes to read
        the project independent settings and apply them to the UI."""

        settings = QtCore.QSettings(
            "Usb Hub, DerUhrmacher", "Export to POV-Ray")

        self.textureTab.applyQSettings(settings)
        self.environmentTab.applyQSettings(settings)
        self.radiosityTab.applyQSettings(settings)
        self.helpTab.applyQSettings(settings)
        # general tab as last one to avoid conflicts with order
        # (signal emitted by general tab, consequencing applyIniSettings() before QSettings)
        self.generalTab.applyQSettings(settings)

    def settingsToIniFormat(self):
        """Call the tab classes to convert the settings to the ini format."""

        csv = ""

        csv += self.generalTab.settingsToIniFormat()
        csv += self.textureTab.settingsToIniFormat()
        csv += self.environmentTab.settingsToIniFormat()
        csv += self.radiosityTab.settingsToIniFormat()
        csv += self.helpTab.settingsToIniFormat()

        self.csv = csv

    def applyIniSettings(self, iniPath):
        """Open the ini file and apply the settings stored in the file.

        Args:
            iniPath (str): Path to the ini file.
        """

        # open ini file and extract CSV
        try:
            iniFile = open(iniPath, "r")
        except:
            App.Console.PrintWarning("Could not open ini file\n")
            self.generalTab.setDefaultValues()
            iniFile = None

        if iniFile and iniPath != -1 and iniPath != "" and iniPath is not None:
            lines = iniFile.readlines()
            iniFile.close()

            csvLines = []

            for line in lines:
                if line.startswith(";"):
                    csvLines.append(line[1:])

            self.generalTab.applyIniSettings(csvLines)
            self.textureTab.applyIniSettings(csvLines)
            self.environmentTab.applyIniSettings(csvLines)
            self.radiosityTab.applyIniSettings(csvLines)
            self.helpTab.applyIniSettings(csvLines)


    ### Handling the ini file ###
    #############################

    def writeIni(self):
        """Write the content of the ini file into it."""

        self.iniFile = open(self.renderSettings.iniPath, "w")
        self.iniFile.write(self.iniContent)
        self.iniFile.close()

    def createIniContent(self):
        """Create the content of the ini file."""

        self.settingsToIniFormat()

        self.iniContent = ""
        self.iniContent += self.csv + "\n"
        self.iniContent += "Input_File_Name='" + self.renderSettings.povName + "'\n"
        self.iniContent += "Output_File_Name='" + self.renderSettings.pngName + "'\n"
        self.iniContent += "Width=" + str(self.renderSettings.width) + "\n"
        self.iniContent += "Height=" + str(self.renderSettings.height) + "\n"
        self.iniContent += "Fatal_File='" + self.renderSettings.errorName + "'\n"


    ### Slots for rendering start and cancelling ###
    ################################################

    def onCancel(self):
        """Called if "Cancel" button is pressed."""

        self.result = "Canceled"
        self.close()
        App.Console.PrintMessage("\n\nCanceled\n\n")

    def onOk(self):
        """Called if "Start Rendering" button is pressed."""

        self.result = "OK"
        self.close()
        self.saveQSettings()

        iniPath = self.generalTab.getIniPath()
        directory = os.path.dirname(iniPath) + os.sep
        projectName = os.path.basename(iniPath)[:-4]

        # create renderSettings object
        self.renderSettings = RenderSettings(
            directory,
            projectName,
            self.generalTab.getImageWidth(),
            self.generalTab.getImageHeight(),
            self.generalTab.isExpFcLightChecked(),
            self.generalTab.isRepRotChecked(),
            self.generalTab.isExpFcViewChecked(),
            self.radiosityTab.getRadiosity(),
            self.environmentTab.getHdriDict())

        self.textureTab.createTextureInc(self.renderSettings)

        self.createIniContent()
        self.writeIni()

        self.exporter.initExport(self.renderSettings)


###################
### General Tab ###
###################

class GeneralTab(QtGui.QWidget):
    """The class for the general tab (derived by QWidget)."""


    ### Signals ###
    ###############
    # emitted when ini path changed and ini file should be applied
    iniPathChanged = QtCore.Signal(str)
    # emitted when the validity of the ini path changed
    iniPathValidityChanged = QtCore.Signal(bool)


    ### Init UI elements and other stuff ###
    ########################################

    def __init__(self):
        super(GeneralTab, self).__init__()
        self.qSettingsGroup = "generalTab"
        self.iniPath = ""
        self.initUIElements()

    def initUIElements(self):
        """Create all UI elements and set layouts, signals, slots, etc."""

        # ini file selection
        self.iniPathLineEdit = QtGui.QLineEdit()
        self.iniPathLineEdit.setPlaceholderText("Path to INI File")
        self.iniPathLineEdit.setToolTip(
            "Path to the INI file (kind of a project file)")
        self.iniPathLineEdit.setEnabled(False)

        self.openFileDialogButton = QtGui.QPushButton(
            "Select Project File (*.ini)")
        self.openFileDialogButton.clicked.connect(self.openFileDialog)
        self.openFileDialogButton.setToolTip(
            "Open file dialog for choosing a INI file.\n"
            "Be careful to not use spaces or special chars in pathname for POV-Ray compatibility.")

        self.warnLabel = QtGui.QLabel("")
        self.warnLabel.setStyleSheet("QLabel { color : #ff0000; }")

        self.iniSelectionLayout = QtGui.QGridLayout()
        self.iniSelectionLayout.addWidget(self.iniPathLineEdit, 0, 0)
        self.iniSelectionLayout.addWidget(self.openFileDialogButton, 0, 1)
        self.iniSelectionLayout.addWidget(self.warnLabel, 1, 0, 1, 2)

        self.iniSelectionGroup = QtGui.QGroupBox("Output File Selection")
        self.iniSelectionGroup.setLayout(self.iniSelectionLayout)

        # Width & Height of rendered image
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

        self.WHImageLayout = QtGui.QVBoxLayout()
        self.WHImageLayout.addWidget(self.imageWidthLabel)
        self.WHImageLayout.addWidget(self.imageWidth)
        self.WHImageLayout.addWidget(self.imageHeightLabel)
        self.WHImageLayout.addWidget(self.imageHeight)
        self.WHImageGroup = QtGui.QGroupBox(
            "Width and Height of rendered Image")
        self.WHImageGroup.setLayout(self.WHImageLayout)

        # Options
        self.expLight = QtGui.QCheckBox("Export FreeCAD Light")
        self.expLight.setToolTip(
            "Export the light FreeCAD uses. Define your own light via a light object in FreeCAD "
            "or a light in the user inc file if you unchecked this option")

        self.repRot = QtGui.QCheckBox("Repair Rotation")
        self.repRot.setToolTip(
            "Repair the rotation of all objects.\n"
            "Use this option if objects in your scene appear in a wrong rotation.\n"
            "This is a workaround for a FreeCAD bug. Visit the Help tab for more information.")

        self.expFcView = QtGui.QCheckBox("Export FreeCAD View")
        self.expFcView.setToolTip(
            "Take a screenshot of the scene view and save it with the same resolution as the image")

        self.optionLayout = QtGui.QVBoxLayout()
        self.optionLayout.addWidget(self.expLight)
        self.optionLayout.addWidget(self.repRot)
        self.optionLayout.addWidget(self.expFcView)
        self.optionGroups = QtGui.QGroupBox("Options")
        self.optionGroups.setLayout(self.optionLayout)

        # add widgets to the main layout
        self.wrapperLayout = QtGui.QVBoxLayout()
        self.wrapperLayout.addWidget(self.iniSelectionGroup)
        self.wrapperLayout.addWidget(self.WHImageGroup)
        self.wrapperLayout.addWidget(self.optionGroups)

        self.setLayout(self.wrapperLayout)


    ### Handling of ini file selection ###
    ######################################

    def openFileDialog(self):
        """Open the file dialog to select a ini file."""

        defaultPath = self.iniPathLineEdit.text()

        fileDialog = QtGui.QFileDialog(self)
        fileDialog.setFileMode(QtGui.QFileDialog.AnyFile)
        fileDialog.setDefaultSuffix("ini")
        fileDialog.setNameFilter("POV-Ray ini Files (*.ini)")
        fileDialog.setViewMode(QtGui.QFileDialog.Detail)
        fileDialog.setDirectory(defaultPath)
        fileDialog.setWindowTitle("Select path and name of the *.ini file")

        if fileDialog.exec_():
            fileName = fileDialog.selectedFiles()
        else:
            fileName = None

        if fileName and fileName != (u'', u''):
            self.iniPath = str(fileName[0])
            self.iniPathLineEdit.setText(self.iniPath)
            self.handlePath(self.iniPath)

    def handlePath(self, path):
        """Check for validity and ask for applying the ini file settings.

        Args:
            path (str): Path of ini file
        """

        pathLegal = self.checkPath(path)

        if pathLegal and os.path.isfile(path):
            # ask to apply settings from selected file
            content = ""
            content += "Do you want to overwrite the current settings with those from the selected file?\n"
            content += "Settings not made in the selected file will not be overwritten.\n"
            content += "Click 'Apply' if you want to apply the settings from the file."
            dialog = QtGui.QMessageBox(
                QtGui.QMessageBox.Question,
                "Apply settings from file?",
                content,
                QtGui.QMessageBox.Apply | QtGui.QMessageBox.No)
            dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            answer = dialog.exec_()

            if answer == QtGui.QMessageBox.Apply:
                self.iniPathChanged.emit(self.iniPath)

    def checkPath(self, path):
        """Check if the path to the ini file is valid.

        Args:
            path (str): Path to ini file

        Returns:
            bool: False: not valid; True: valid
        """

        if path.find(
                " ") == -1 and isAscii(path) and path != "" and path[-4:].lower() == ".ini":
            self.iniPathValidityChanged.emit(True)

            self.warnLabel.setText("")
            return True
        else:
            self.iniPathValidityChanged.emit(False)

            if path == "" or os.path.isdir(path):
                self.warnLabel.setText(
                    "Please type a path or get one with clicking on '...'")
            else:
                self.warnLabel.setText(
                    "Your path contains a space or a mutated vowel or is not a .ini file")

            return False


    ### Getter Methods ###
    ######################

    def getIniPath(self):
        return self.iniPath

    def getImageWidth(self):
        return self.imageWidth.value()

    def getImageHeight(self):
        return self.imageHeight.value()

    def isExpFcLightChecked(self):
        return self.expLight.isChecked()

    def isRepRotChecked(self):
        return self.repRot.isChecked()

    def isExpFcViewChecked(self):
        return self.expFcView.isChecked()


    ### Settings Stuff ###
    ######################

    def saveQSettings(self, settingsObject):
        """Save the settings from the tab with QSettings.

        Args:
            settingsObject (QSettings Object): QSettings object to store the data
        """

        # The name of the active document together with the ini file is saved, to
        # make it possible to assign the ini file to the FreeCAD model at the
        # next opening.

        settingsObject.beginGroup(self.qSettingsGroup)
        settingsObject.setValue(App.ActiveDocument.Name,
                                self.iniPathLineEdit.text())
        settingsObject.endGroup()

    def applyQSettings(self, settingsObject):
        """Apply the settings stored with QSettings to the tab.

        Args:
            settingsObject (QSettings Object): The QSettings Object to read the data from
        """

        settingsObject.beginGroup(self.qSettingsGroup)

        if App.ActiveDocument.Name in settingsObject.allKeys():
            self.iniPath = settingsObject.value(App.ActiveDocument.Name)

        settingsObject.endGroup()

        self.iniPathChanged.emit(self.iniPath)

    def settingsToIniFormat(self):
        """Convert the settings from the tab to CSV.

        Returns:
            str: The created CSV with ";" for the ini file at the beginning.
        """

        csv = ""

        # add render settings
        csv += ";stg_width," + str(self.getImageWidth()) + "\n"
        csv += ";stg_height," + str(self.getImageHeight()) + "\n"
        csv += ";stg_expLight," + str(self.isExpFcLightChecked()) + "\n"
        csv += ";stg_repRot," + str(self.isRepRotChecked()) + "\n"
        csv += ";stg_expFcView," + str(self.isExpFcViewChecked()) + "\n"

        return csv

    def applyIniSettings(self, csvLines):
        """Apply the settings from the given lines from the ini file to the tab.

        Args:
            csvLines (Array): Array of lines for the CSV parser
        """

        # parse CSV
        csvReader = csv.reader(csvLines, delimiter=',')

        self.iniPathLineEdit.setText(self.iniPath)

        for row in csvReader:
            if row[0].startswith("stg_"):
                name = row[0][4:]

                if name == "width":
                    self.imageWidth.setValue(int(row[1]))
                elif name == "height":
                    self.imageHeight.setValue(int(row[1]))
                elif name == "expLight":
                    self.expLight.setChecked(strToBool(row[1]))
                elif name == "repRot":
                    self.repRot.setChecked(strToBool(row[1]))
                elif name == "expFcView":
                    self.expFcView.setChecked(strToBool(row[1]))

    def setDefaultValues(self):
        """Set some good default values for the tab (check "Export FreeCAD Light, etc.)."""

        if App.ActiveDocument.FileName == u"":
            system = platform.system()
            if system == "Linux":
                self.iniPath = "/home/"
            elif system == "Darwin":
                self.iniPath = "/Users/"
            elif system == "Windows":
                self.iniPath = "C:\\Users\\%UserName%\\"
            else:
                self.iniPath = ""
        else:
            # create ini path from FreeCAD file
            self.iniPath = os.path.splitext(
                App.ActiveDocument.FileName)[0] + ".ini"

        self.iniPathLineEdit.setText(self.iniPath)
        self.checkPath(self.iniPath)

        self.imageWidth.setValue(800)
        self.imageHeight.setValue(600)

        self.expLight.setChecked(True)
        self.expFcView.setChecked(False)
        self.repRot.setChecked(False)


###################
### Texture Tab ###
###################

class TextureTab(QtGui.QWidget):
    """The class for the texture tab (derived by QWidget)."""

    def __init__(self):
        super(TextureTab, self).__init__()
        self.exporter = ExportToPovRay()
        self.qSettingsGroup = "textureTab"
        self.initUIElements()


    ### Create the tab ###
    ######################

    def initUIElements(self):
        """Wrapper method to create the tab and the signals, etc."""

        self.wrapperLayout = QtGui.QVBoxLayout()

        self.addObjectsTexturesLists()  # add the two lists at the top
        # add the menu for scaling and rotating at the bottom
        self.addScaleRotateTranslate()

        self.preview = Preview("texture")  # preview widget

        # signals and slots
        self.connectSignals()

        # set layouts
        self.wrapperLayout.addWidget(self.listsWidget)
        self.wrapperLayout.addWidget(self.textureSettingsWidget)
        self.wrapperLayout.addWidget(self.preview)

        self.setLayout(self.wrapperLayout)

    def addObjectsTexturesLists(self):
        """Add the two lists with the objects and textures."""

        self.listsWidget = QtGui.QWidget()  # wrapper widget for the two lists
        self.listsLayout = QtGui.QGridLayout()  # wrapper layout for the two lists

        self.addTextureList()
        self.addObjectList()

    def addTextureList(self):
        """Add the nested list with the predefined textures on the right side."""

        # texture list
        self.textureList = QtGui.QTreeWidget()
        self.textureList.setHeaderLabel("Predefined")

        self.textureListHeading = QtGui.QLabel("<b>Texture</b>")

        self.predefines = []
        # add FreeCAD texture
        self.fcTexItem = QtGui.QTreeWidgetItem(
            self.textureList, ["FreeCAD Texture"])
        self.predefines.append(
            Predefined(
                "FreeCAD Texture",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "",
                "",
                self.fcTexItem))
        self.fcTexItem.setSelected(True)

        # get the predefined.xml
        predefinedPath = os.path.join(os.path.dirname(
            __file__), "predefined.xml")  # get workbench path

        predefined = xml.parse(predefinedPath).getroot()
        categories = predefined.getchildren()

        # read the predefined.xml and add the predefined defined in the XML
        for category in categories:
            self.predefXmlToList(category, self.textureList)

        # add the list to the layouts and widgets
        self.listsLayout.addWidget(self.textureListHeading, 0, 1)
        self.listsLayout.addWidget(self.textureList, 1, 1)

        self.listsWidget.setLayout(self.listsLayout)

    def addObjectList(self):
        """Add the list with the FreeCAD objects on the left side."""

        # object list
        self.objectList = QtGui.QListWidget()

        self.objectListHeading = QtGui.QLabel("<b>Object</b>")

        # get objects
        fcObjs = App.ActiveDocument.Objects
        self.listFcObjects = []
        for obj in fcObjs:
            if obj.ViewObject.Visibility:
                # has object a shape color
                try:
                    obj.ViewObject.ShapeColor
                    shapeColor = True
                except:
                    shapeColor = False
                # has object a shape
                try:
                    obj.Shape
                    obj.Shape.Area
                    obj.Shape.Volume

                    shape = True
                except:
                    shape = False

                # test for the conditions for a object for the object list
                if shapeColor and shape:
                    self.listFcObjects.append(obj)

        self.listObjects = []
        # create the listObjects
        for obj in self.listFcObjects:
            try:
                listItem = QtGui.QListWidgetItem(obj.ViewObject.Icon, obj.Label)
            except:
                listItem = QtGui.QListWidgetItem(obj.Label)

            self.listObjects.append(ListObject(
                obj, listItem, self.predefines[0], 1, 1, 1, 0, 0, 0, 0, 0, 0))

            self.objectList.addItem(listItem)

        # add the object list to the layouts
        self.listsLayout.addWidget(self.objectListHeading, 0, 0)
        self.listsLayout.addWidget(self.objectList, 1, 0)

        # add comment label
        self.commentLabel = QtGui.QLabel()
        self.commentLabel.setStyleSheet("QLabel { font-weight : bold;}")
        self.commentLabel.setWordWrap(True)
        self.listsLayout.addWidget(self.commentLabel, 2, 0, 1, 2)

    def addScaleRotateTranslate(self):
        """Add the scale, rotate, translate menu."""

        self.textureSettingsWidget = QtGui.QWidget()
        self.textureSettingsLayout = QtGui.QGridLayout()

        # scale
        self.scalingLabel = QtGui.QLabel("Scale")
        self.textureSettingsLayout.addWidget(self.scalingLabel, 0, 0)

        self.scaleX = QtGui.QDoubleSpinBox()
        self.scaleX.setMaximum(9999999)
        self.scaleX.setMinimum(-9999999)
        self.scaleX.setDecimals(5)
        self.scaleX.setPrefix("x: ")
        self.textureSettingsLayout.addWidget(self.scaleX, 0, 1)

        self.scaleY = QtGui.QDoubleSpinBox()
        self.scaleY.setMaximum(9999999)
        self.scaleY.setMinimum(-9999999)
        self.scaleY.setDecimals(5)
        self.scaleY.setPrefix("y: ")
        self.textureSettingsLayout.addWidget(self.scaleY, 0, 2)

        self.scaleZ = QtGui.QDoubleSpinBox()
        self.scaleZ.setMaximum(9999999)
        self.scaleZ.setMinimum(-9999999)
        self.scaleZ.setDecimals(5)
        self.scaleZ.setPrefix("z: ")
        self.textureSettingsLayout.addWidget(self.scaleZ, 0, 3)

        # rotate
        self.rotationLabel = QtGui.QLabel("Rotate")
        self.textureSettingsLayout.addWidget(self.rotationLabel, 1, 0)

        self.rotationX = QtGui.QDoubleSpinBox()
        self.rotationX.setMaximum(360)
        self.rotationX.setMinimum(-360)
        self.rotationX.setDecimals(3)
        self.rotationX.setPrefix("x: ")
        self.rotationX.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationX, 1, 1)

        self.rotationY = QtGui.QDoubleSpinBox()
        self.rotationY.setMaximum(360)
        self.rotationY.setMinimum(-360)
        self.rotationY.setDecimals(3)
        self.rotationY.setPrefix("y: ")
        self.rotationY.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationY, 1, 2)

        self.rotationZ = QtGui.QDoubleSpinBox()
        self.rotationZ.setMaximum(360)
        self.rotationZ.setMinimum(-360)
        self.rotationZ.setDecimals(3)
        self.rotationZ.setPrefix("z: ")
        self.rotationZ.setSuffix(" deg")
        self.textureSettingsLayout.addWidget(self.rotationZ, 1, 3)

        # translation
        self.translationLabel = QtGui.QLabel("Translate")
        self.textureSettingsLayout.addWidget(self.translationLabel, 2, 0)

        self.translationX = QtGui.QDoubleSpinBox()
        self.translationX.setMaximum(9999999)
        self.translationX.setMinimum(-9999999)
        self.translationX.setDecimals(3)
        self.translationX.setPrefix("x: ")
        self.textureSettingsLayout.addWidget(self.translationX, 2, 1)

        self.translationY = QtGui.QDoubleSpinBox()
        self.translationY.setMaximum(9999999)
        self.translationY.setMinimum(-9999999)
        self.translationY.setDecimals(3)
        self.translationY.setPrefix("y: ")
        self.textureSettingsLayout.addWidget(self.translationY, 2, 2)

        self.translationZ = QtGui.QDoubleSpinBox()
        self.translationZ.setMaximum(9999999)
        self.translationZ.setMinimum(-9999999)
        self.translationZ.setDecimals(3)
        self.translationZ.setPrefix("z: ")
        self.textureSettingsLayout.addWidget(self.translationZ, 2, 3)

        self.textureSettingsWidget.setLayout(self.textureSettingsLayout)

    def predefXmlToList(self, xmlNode, parentNode):
        """Convert the given XML node to a predefined object and add an item to the predef list (recursive method).

        Args:
            xmlNode (xmlNode Object): The XML node that should be converted.
            parentNode (QTreeWidgetItem): QTreeWidgetItem to which the newly created item should be added as a child.
        """

        childNodes = xmlNode.getchildren()

        if childNodes == []:
            treeItem = QtGui.QTreeWidgetItem(parentNode, [xmlNode.text])
            # get all attributes
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

            if "comment" in attr:
                comment = attr["comment"]
            else:
                comment = ""

            self.predefines.append(
                Predefined(
                    xmlNode.text,
                    material,
                    texture,
                    pigment,
                    finish,
                    normal,
                    interior,
                    media,
                    inc,
                    comment,
                    treeItem))

        else:
            categoryItem = QtGui.QTreeWidgetItem(parentNode, [xmlNode.tag])
            for node in childNodes:
                # call method for child nodes
                self.predefXmlToList(node, categoryItem)

    def connectSignals(self):
        """Connect all necessary signals for the texture tab."""

        self.objectList.itemSelectionChanged.connect(
            self.updateTextureSettings)
        self.textureList.itemSelectionChanged.connect(
            self.updateSelectedListObject)

        self.scaleX.editingFinished.connect(self.updateSelectedListObject)
        self.scaleY.editingFinished.connect(self.updateSelectedListObject)
        self.scaleZ.editingFinished.connect(self.updateSelectedListObject)

        self.rotationX.editingFinished.connect(self.updateSelectedListObject)
        self.rotationY.editingFinished.connect(self.updateSelectedListObject)
        self.rotationZ.editingFinished.connect(self.updateSelectedListObject)

        self.translationX.editingFinished.connect(
            self.updateSelectedListObject)
        self.translationY.editingFinished.connect(
            self.updateSelectedListObject)
        self.translationZ.editingFinished.connect(
            self.updateSelectedListObject)

    def disconnectSignals(self):
        """Connect all necessary signals for the texture tab."""

        self.objectList.itemSelectionChanged.disconnect()
        self.textureList.itemSelectionChanged.disconnect()

        self.scaleX.editingFinished.disconnect()
        self.scaleY.editingFinished.disconnect()
        self.scaleZ.editingFinished.disconnect()

        self.rotationX.editingFinished.disconnect()
        self.rotationY.editingFinished.disconnect()
        self.rotationZ.editingFinished.disconnect()

        self.translationX.editingFinished.disconnect()
        self.translationY.editingFinished.disconnect()
        self.translationZ.editingFinished.disconnect()


    ### Slots and their helping methods ###
    #######################################

    def updateTextureSettings(self):
        """Set the predefined settings for the currently selected FreeCAD
        object, when the object selection changed."""

        self.disconnectSignals()  # disconnect to avoid infinite recursive calls
        selectedListObj = self.getSelectedListObject()  # get the current selected object

        if selectedListObj == -1:  # is an object selected
            self.connectSignals()
            return -1

        # set all values for scaling and rotating
        self.scaleX.setValue(selectedListObj.scaleX)
        self.scaleY.setValue(selectedListObj.scaleY)
        self.scaleZ.setValue(selectedListObj.scaleZ)

        self.rotationX.setValue(selectedListObj.rotationX)
        self.rotationY.setValue(selectedListObj.rotationY)
        self.rotationZ.setValue(selectedListObj.rotationZ)

        self.translationX.setValue(selectedListObj.translationX)
        self.translationY.setValue(selectedListObj.translationY)
        self.translationZ.setValue(selectedListObj.translationZ)

        # unselect all textures
        for predefine in self.predefines:
            predefine.treeItem.setSelected(False)

        # select the right predefined
        selectedListObj.predefObject.treeItem.setSelected(True)

        # expand categories
        self.expandParentItems(selectedListObj.predefObject.treeItem)

        # set comment
        self.commentLabel.setText(selectedListObj.predefObject.comment)

        # update preview
        self.updatePreview(selectedListObj)

        self.connectSignals()

    def updateSelectedListObject(self):
        """Update the listObject of the currently selected FreeCAD
        object when a predefined setting changed."""

        selectedListObj = self.getSelectedListObject()
        selectedPredefine = self.getSelectedPredefined()
        if selectedListObj == -1 or selectedPredefine == -1:  # is no object or predefine selected
            if selectedPredefine == -1:  # is only a category selected
                # expand and select predef under the category
                self.disconnectSignals()
                selectedItems = self.textureList.selectedItems()
                selected = selectedItems[0]
                selected.setSelected(False)
                selected.setExpanded(True)
                childItem = selected.child(0)
                self.connectSignals()
                childItem.setSelected(True)

            return -1  # abort

        # get the values for scaling and rotating
        selectedListObj.scaleX = self.scaleX.value()
        selectedListObj.scaleY = self.scaleY.value()
        selectedListObj.scaleZ = self.scaleZ.value()

        selectedListObj.rotationX = self.rotationX.value()
        selectedListObj.rotationY = self.rotationY.value()
        selectedListObj.rotationZ = self.rotationZ.value()

        selectedListObj.translationX = self.translationX.value()
        selectedListObj.translationY = self.translationY.value()
        selectedListObj.translationZ = self.translationZ.value()

        # apply the read values to the predefObject in the listObject
        selectedListObj.predefObject = selectedPredefine

        # set comment
        self.commentLabel.setText(selectedListObj.predefObject.comment)

        # update preview
        self.updatePreview(selectedListObj)

    def updatePreview(self, listObj):
        """Render the preview for the given FreeCAD listObject.

        Args:
            listObj (ListObject): ListObject that should be previewed.
        """

        if listObj.predefObject.material is None:  # for FreeCAD materials
            self.preview.setErrorText(
                "The FreeCAD texture is just like you see it in the FreeCAD scene\n so this texture is disabled.")
            return
        elif listObj.predefObject.media != "":
            self.preview.setErrorText(
                "The texture is too complex for a preview and would need a lot of time\nso this texture is disabled.")
            return

        # create content of pov file
        fileContent = ""
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

        fileContent += 'box { <0,0,0>, <10.0, 10.0, 10.0>\n'
        fileContent += '\ttranslate <5.0, 5.0, -5.0>\n'
        fileContent += '\tmaterial { predef_material }\n'
        fileContent += '}\n'
        fileContent += 'sphere { <0, 0, 0> 5 \n'
        fileContent += '\tmaterial { predef_material }\n'
        fileContent += '}\n'

        self.preview.render(fileContent)

    def getSelectedListObject(self):
        """Get the currently selected listObject.

        Returns:
            ListObject or int: Currently selected ListObject, if nothing selected -1.
        """

        for listObj in self.listObjects:
            if listObj.listItem.isSelected():
                return listObj

        return -1

    def getSelectedPredefined(self):
        """Get the currently selected Predefined object.

        Returns:
            Predefined or int: Currently selected Predefined, if nothing selected -1.
        """

        for predefine in self.predefines:
            if predefine.treeItem.isSelected():
                return predefine

        return -1

    def expandParentItems(self, item):
        """Expand the parent item (recursive method).

        Args:
            item (QTreeWidgetItem): Child item
        """

        parent = item.parent()
        if isinstance(parent, QtGui.QTreeWidgetItem):
            parent.setExpanded(True)
            self.expandParentItems(parent)


    ### Stuff done at the end ###
    #############################

    def writeTextureInc(self):
        """Write the content of the texture inc file into the file."""

        self.texIncFile = open(self.renderSettings.texIncPath, "w")
        self.texIncFile.write(self.texIncContent)
        self.texIncFile.close()

    def createTexIncContent(self):
        """Create the content of the texture inc file."""

        self.texIncContent = ""

        for obj in self.listObjects:  # iterate over all listObjects
            self.texIncContent += self.exporter.listObjectToPov(obj)

    def createTextureInc(self, renderSettings):
        """Do the stuff for the texture inc file.

        Args:
            renderSettings (RenderSettings): The RenderSettings object for the rendering.
        """

        self.renderSettings = renderSettings

        self.createTexIncContent()
        self.writeTextureInc()


    ### Stuff for saving and reading settings ###
    #############################################

    def applyIniSettings(self, csvLines):
        """Apply the settings from the given lines from the ini file to the tab.

        Args:
            csvLines (Array): Array of lines for the CSV parser
        """

        # parse CSV
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

        # select first listObject
        if self.objectList.count() > 0:
            self.objectList.setCurrentRow(0)

    def settingsToIniFormat(self):
        """Convert the settings from the tab to CSV.

        Returns:
            str: The created CSV with ";" for the ini file at the beginning.
        """

        csv = ""

        # add settings for every listobject
        for obj in self.listObjects:
            csv += ";obj_" + obj.fcObj.Name + "," + obj.predefObject.getHash() + ","
            csv += str(obj.scaleX) + "," + str(obj.scaleY) + \
                "," + str(obj.scaleZ) + ","
            csv += str(obj.rotationX) + "," + str(obj.rotationY) + \
                "," + str(obj.rotationZ) + ","
            csv += str(obj.translationX) + "," + \
                str(obj.translationY) + "," + str(obj.translationZ) + "\n"

        return csv

    def applyQSettings(self, settingsObject):
        """Apply the settings stored with QSettings to the tab.

        Args:
            settingsObject (QSettings Object): The QSettings Object to read the data from
        """

        self.preview.applyQSettings(settingsObject)

    def saveQSettings(self, settingsObject):
        """Save the settings from the tab with QSettings.

        Args:
            settingsObject (QSettings Object): QSettings object to store the data
        """

        self.preview.saveQSettings(settingsObject)


class Preview(QtGui.QWidget):
    """Class for the preview. It is derived by QWidget."""

    def __init__(self, name):
        super(Preview, self).__init__()
        self.qSettingsGroup = "preview"
        self.name = name
        self.povCode = ""
        self.initUIElements()
        self.connectSignals()

    def initUIElements(self):
        """Create the UI elements and set the layouts."""

        # disable checkbox
        self.disableCheckBox = QtGui.QCheckBox("Disable Live Preview")

        # zoom buttons
        self.zoomIn = QtGui.QPushButton("Larger")
        self.zoomOut = QtGui.QPushButton("Smaller")

        # preview settings layout
        self.settingsLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addWidget(self.disableCheckBox)
        self.settingsLayout.addWidget(self.zoomIn)
        self.settingsLayout.addWidget(self.zoomOut)

        # preview image
        self.imageLabel = QtGui.QLabel("No Preview to show")
        self.imageLabel.setStyleSheet("QLabel { color : #ff0000; }")

        # main layout
        self.wrapperLayout = QtGui.QVBoxLayout()
        self.wrapperLayout.addLayout(self.settingsLayout)
        self.wrapperLayout.addWidget(self.imageLabel)

        self.setLayout(self.wrapperLayout)

    def render(self, povCode):
        """Render an image by the given POV-Ray code and show it.

        Args:
            povCode (str): The code for POV-Ray for the image
        """

        self.povCode = povCode

        if self.disableCheckBox.isChecked():
            return

        povFile = tempfile.NamedTemporaryFile(
            delete=False, suffix=".pov")  # pov file handler
        povFile.write(self.povCode.encode())

        povName = povFile.name
        povFile.close()

        # render
        povExec = App.ParamGet(preferences.prefPath).GetString("PovRayExe", "")
        if os.path.isfile(povExec) == False:
            errorText = "To get a preview of the texture settings you must\n"
            errorText += "set the path to the POV-Ray executable\n"
            errorText += "either in the settings of Render workbench\n"
            errorText += "or in the settings of Raytracing workbench\n"
            showError(errorText, "POV-Ray executable not found")
            return -1

        # start povray
        subprocess.call([povExec, "-d", "width=" + str(self.previewWidth),
                         "height=" + str(self.previewHeight), povName])

        # update image
        pixmap = QtGui.QPixmap(povName[:-4])
        self.imageLabel.setPixmap(pixmap)

    def setErrorText(self, text):
        """Shows an error in red text and remove the image.

        Args:
            text (str): error message
        """

        self.imageLabel.setText(text)
        self.povCode = ""

    def connectSignals(self):
        """Connect all necessary signals to all slots."""

        self.disableCheckBox.stateChanged.connect(self.disableChanged)
        self.zoomIn.pressed.connect(self.largerPreview)
        self.zoomOut.pressed.connect(self.smallerPreview)

    def disableChanged(self):
        """Slot, called when the state of the disable checkbox changes."""

        if self.disableCheckBox.isChecked():
            self.imageLabel.setVisible(False)
        else:
            self.imageLabel.setVisible(True)

            if self.povCode != "" and self.imageLabel.pixmap() == None:
                self.render(self.povCode)

    def largerPreview(self):
        """Increase the size of the preview image. Called when the "Larger" button is pressed."""

        self.previewWidth += 40
        self.previewHeight += 30

        self.render(self.povCode)

    def smallerPreview(self):
        """Decrease the size of the preview image. Called when the "Smaller" button is pressed."""

        if self.previewWidth < 45:
            return

        self.previewWidth -= 40
        self.previewHeight -= 30

        self.render(self.povCode)

    def applyQSettings(self, settingsObject):
        """Apply the settings stored with QSettings to the preview.

        Args:
            settingsObject (QSettings Object): The QSettings Object to read the data from
        """

        # get saved input
        settingsObject.beginGroup(self.qSettingsGroup + self.name)

        # set preview disable checkbox
        previewDisable = settingsObject.value("previewDisable")
        if previewDisable is not None:
            self.disableCheckBox.setChecked(strToBool(previewDisable))
        else:
            self.disableCheckBox.setChecked(False)

        previewWidth = settingsObject.value("previewWidth")
        if previewWidth is not None and previewWidth != 0 and previewWidth != -1:
            self.previewWidth = int(previewWidth)
        else:
            self.previewWidth = 300

        previewHeight = settingsObject.value("previewHeight")
        if previewHeight is not None and previewHeight != 0 and previewHeight != -1:
            self.previewHeight = int(previewHeight)
        else:
            self.previewHeight = 225

        settingsObject.endGroup()

    def saveQSettings(self, settingsObject):
        """Save the settings from the preview with QSettings.

        Args:
            settingsObject (QSettings Object): QSettings object to store the data
        """
        settingsObject.beginGroup(self.qSettingsGroup + self.name)
        settingsObject.setValue(
            "previewDisable", self.disableCheckBox.isChecked())
        settingsObject.setValue("previewWidth", self.previewWidth)
        settingsObject.setValue("previewHeight", self.previewHeight)
        settingsObject.endGroup()


class Predefined:
    """Class to store all stuff from a predefined (stored in predefined.xml)."""

    def __init__(
            self,
            identifier,
            material,
            texture,
            pigment,
            finish,
            normal,
            interior,
            media,
            inc,
            comment,
            treeItem):
        self.identifier = identifier
        self.material = material
        self.texture = texture
        self.pigment = pigment
        self.finish = finish
        self.normal = normal
        self.interior = interior
        self.media = media
        self.inc = inc
        self.comment = comment
        self.treeItem = treeItem

    def getHash(self):
        """Create a hash from all parts of the predefined (for identifying the predefined later).

        Returns:
            str: The hash
        """
        predefName = self.treeItem.text(0)

        stgStr = (str(self.identifier) +
                  str(self.material) +
                  str(self.texture) +
                  str(self.pigment) +
                  str(self.finish) +
                  str(self.normal) +
                  str(self.interior) +
                  str(self.media) +
                  str(self.inc) +
                  str(self.comment))
        hashStr = hashlib.md5(stgStr.encode("UTF-8")).hexdigest()[:4]

        return stringCorrection(predefName) + hashStr


class ListObject:
    """Class to store all stuff of an object in the object list of the texture tab."""

    def __init__(
            self,
            fcObj,
            listItem,
            predefObject,
            scaleX,
            scaleY,
            scaleZ,
            rotationX,
            rotationY,
            rotationZ,
            translationX,
            translationY,
            translationZ):
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


################
### Help Tab ###
################

class HelpTab(QtGui.QWidget):
    """The class for the help tab (derived by QWidget)."""

    def __init__(self):
        super(HelpTab, self).__init__()
        self.qSettingsGroup = "helpTab"
        self.initUIElements()

    def initUIElements(self):
        """Create all UI elements for the tab."""

        self.wrapperLayout = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel("")  # label to show the text

        helpText = """
        <style>
        div { margin: 15;}
        </style>
        <div>
        <h3>General</h3>
        <p>This workbench is specialized for rendering with <a href='http://povray.org/'>POV-Ray</a>.<br>
        You will get best results if you focus on using solid CSG primitives from the part workbench.<br>
        The resulting POV code is readable and can be modified with a
        separate include file that <br> won't be overwritten.</p>
        <h3>Output File Selection</h3>
        <p>The *.ini file sticks your render project together. Select an existing file or create a new one. <br>
        Be careful not to use spaces or special chars in pathname for POV-Ray compatibility.</p>
        <h3>Textures</h3>
        <p>Textures can be easily added by choosing an object from the left list and after that<br>
        choosing a texture from the right list. These two steps can be repeated for all objects</p>
        <h3>Lights</h3>
        <p>Lightsources can be added via the workbench and will appear as objects in your FreeCAD model.<br>
        Overall lightning can be influenced via the "Indirect Lightning" Tab.<br>
        Usage is directly explained in the tab.</p>
        <h3>Help</h3>
        <p>For detailed information look in our <a href='https://gitlab.com/usbhub/exporttopovray/blob/master/doc/index.md'>Wiki</a></p>
        </div>"""
        self.label.setText(helpText)
        self.label.setOpenExternalLinks(True)

        self.wrapperLayout.addWidget(self.label)
        self.setLayout(self.wrapperLayout)


    def applyIniSettings(self, csvLines):
        """Apply the settings from the given lines from the ini file
        to the tab (unnecessary for this tab).

        Args:
            csvLines (Array): Array of lines for the CSV parser
        """

        pass

    def settingsToIniFormat(self):
        """Convert the settings from the tab to CSV.

        Returns:
            str: The created CSV with ";" for the ini file at the
            beginning (unnecessary for this tab)
        """

        return ""

    def applyQSettings(self, settingsObject):
        """Apply the settings stored with QSettings to the tab (unnecessary for this tab).

        Args:
            settingsObject (QSettings Object): The QSettings Object to read the data from
        """

        pass

    def saveQSettings(self, settingsObject):
        """Save the settings from the tab with QSettings (unnecessary for this tab).

        Args:
            settingsObject (QSettings Object): QSettings object to store the data
        """

        pass


#####################
### Radiosity Tab ###
#####################

class RadiosityTab(QtGui.QWidget):
    """The class for the radiosity / indirect lightning tab (derived by QWidget)."""

    def __init__(self):
        super(RadiosityTab, self).__init__()
        self.qSettingsGroup = "radiosityTab"
        self.initUIElements()

    def initUIElements(self):
        """Generate all UI elements for the tab."""

        self.wrapperLayout = QtGui.QVBoxLayout()

        # explanation of radiosity
        explanationText = "Theoretically there is no light in the shadows and therefore "
        explanationText += "not directly illuminated objects would be completely black. In reality, of course, this is not the case, "
        explanationText += "because light from other objects is reflected into the shadow. "
        explanationText += "Indirect lighting imitates exactly this effect when rendering and thus produces much better images. "
        explanationText += "Ambient tries to simulate this effect by giving the objects a color even though they are in the dark. "
        explanationText += "This usually looks very unrealistic, but is not as computationally intensive. "
        explanationText += "If you activate indirect lighting, you should deactivate ambient so that the image doesn't get too bright. "
        self.explanationText = QtGui.QLabel(explanationText)
        self.explanationText.setWordWrap(True)

        self.explanationImg = QtGui.QLabel()
        pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(
            __file__), "img/radiosityDescription.png"))
        self.explanationImg.setPixmap(pixmap)

        self.wrapperLayout.addWidget(self.explanationText)
        self.wrapperLayout.addWidget(self.explanationImg)

        self.groupBox = QtGui.QGroupBox("Use Indirect Lighting")
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)

        self.groupBoxLayout = QtGui.QVBoxLayout()

        self.radiosityModes = [
            "Default",
            "Debug",
            "Fast",
            "Normal",
            "2Bounce",
            "Final",
            "OutdoorLQ",
            "OutdoorHQ",
            "OutdoorLight",
            "IndoorLQ",
            "IndoorHQ"]

        self.modesComboBox = QtGui.QComboBox()
        self.modesComboBox.insertItems(0, self.radiosityModes)
        self.groupBoxLayout.addWidget(self.modesComboBox)

        self.ambientTo0 = QtGui.QCheckBox("Set default Ambient to 0")
        self.ambientTo0.setChecked(True)
        self.ambientTo0.setToolTip(
            "Set the color of the objects without any light to 0 (black)")

        self.groupBoxLayout.addWidget(self.ambientTo0)

        self.groupBox.setLayout(self.groupBoxLayout)
        self.wrapperLayout.addWidget(self.groupBox)
        self.setLayout(self.wrapperLayout)

    def getRadiosity(self):
        """Returns the current radiosity settings from the tab.

        Returns:
            dict: Dictionary with "radiosityName" and "ambientTo0"
        """

        radiosity = {
            "radiosityName": "",
            "ambientTo0": True
        }

        if self.groupBox.isChecked():
            radiosity["radiosityName"] = "Radiosity_" + self.getRadiosityName()
        else:
            radiosity["radiosityName"] = -1

        if self.ambientTo0.isChecked():
            radiosity["ambientTo0"] = True
        else:
            radiosity["ambientTo0"] = False

        return radiosity

    def getRadiosityName(self):
        """Return the currently selected name of the radiosity template.

        Returns:
            str: Name of the radiosity mode
        """

        return self.modesComboBox.currentText()


    def applyIniSettings(self, csvLines):
        """Read and apply the setting from the given CSV lines.

        Args:
            csvLines (Array): Array of lines from the settings part of the ini file.
        """

        # parse CSV
        csvReader = csv.reader(csvLines, delimiter=',')
        for row in csvReader:
            if row[0] == "radiosity":
                if row[1] == "on":
                    self.groupBox.setChecked(True)
                else:
                    self.groupBox.setChecked(False)

                for index, text in enumerate(self.radiosityModes):
                    if text == row[2]:
                        self.modesComboBox.setCurrentIndex(index)
                        break

                if row[3] == "stdAmbient":
                    self.ambientTo0.setChecked(False)
                else:
                    self.ambientTo0.setChecked(True)

    def settingsToIniFormat(self):
        """Convert the current project dependent settings to the ini file format (CSV).

        Returns:
            str: Settings in ini format (CSV) with ";" at the beginning.
        """

        csv = ";"
        csv += "radiosity"

        if self.groupBox.isChecked():
            csv += ",on"
        else:
            csv += ",off"

        csv += "," + self.getRadiosityName()

        if self.ambientTo0.isChecked():
            csv += "," + "ambientToZero"
        else:
            csv += "," + "stdAmbient"

        return csv + "\n"

    def saveQSettings(self, qSettingsObject):
        """Save the project independent settings with QSettings (nothing).

        Args:
            qSettingsObject (QSettings Object): QSettings object that should be used to save the settings.
        """

        pass

    def applyQSettings(self, qSettingsObject):
        """Read and apply the project independent settings with QSettings (nothing).

        Args:
            qSettingsObject (QSettings Object): QSettings object that should be used to save the settings.
        """

        pass


#######################
### Environment Tab ###
#######################

class EnvironmentTab(QtGui.QWidget):
    """The class for the environment tab (derived by QWidget)."""

    # emitted when the validity of the hdr path changed
    hdrPathValidityChanged = QtCore.Signal(bool)

    def __init__(self):
        super(EnvironmentTab, self).__init__()
        self.qSettingsGroup = "environmentTab"
        self.exporter = ExportToPovRay()
        self.initUIElements()

    def initUIElements(self):
        """Create all UI elements for the tab."""

        self.wrapperLayout = QtGui.QVBoxLayout()

        self.wrapperGroupBox = QtGui.QGroupBox("Export Environment")
        self.wrapperGroupBox.setCheckable(True)
        self.wrapperGroupBoxLayout = QtGui.QVBoxLayout()
        self.wrapperGroupBox.setLayout(self.wrapperGroupBoxLayout)
        self.wrapperLayout.addWidget(self.wrapperGroupBox)

        # Radio Buttons
        self.options = ["FreeCAD Background",
            "HDRI Environment"]
        self.radioButtonOptions = []

        for option in self.options:
            radioButton = QtGui.QRadioButton(option)
            radioButton.toggled.connect(self.checkTabValidity)
            self.wrapperGroupBoxLayout.addWidget(radioButton)
            self.radioButtonOptions.append(radioButton)

        # HDRI Widget
        self.hdriWidget = QtGui.QWidget()
        self.hdriLayout = QtGui.QVBoxLayout()
        self.hdriWidget.setLayout(self.hdriLayout)
        self.wrapperGroupBoxLayout.addWidget(self.hdriWidget)

        # Help Label
        helpText = """<div>
            HDRI images are 360° images with min 10 bits per color (but 32 bits are very 
            common for HDRI images) and not 8 as usual pictures like JPG. So the contrast 
            is a lot better and the images can be used to do the lightning of the scene.
            <h4>Tips</h4>
            <ul>
                <li>turn on indirect lightning (other tab)</li>
                <li>turn of every global light, only flash lights (the HDRI environment <i>is</i> the global light)</li>
            </ul>
        </div>"""

        self.helpLabel = QtGui.QLabel()
        self.helpLabel.setWordWrap(True)
        self.helpLabel.setText(helpText)
        self.hdriLayout.addWidget(self.helpLabel)

        # HDR File Choosing
        self.fileChoosingLayout = QtGui.QGridLayout()

        self.hdriPathLabel = QtGui.QLabel("HDRI Path (*.hdr)")

        self.hdriPathLineEdit = QtGui.QLineEdit()
        self.hdriPathLineEdit.setPlaceholderText("Path to the *.hdr file")

        self.openFileDialogButton = QtGui.QPushButton("...")

        self.invalidPathLabel = QtGui.QLabel()
        self.invalidPathLabel.setStyleSheet("QLabel { color : #ff0000; }")
        self.invalidPathLabel.setWordWrap(True)

        self.fileChoosingLayout.addWidget(self.hdriPathLabel, 0, 0, 1, 2)
        self.fileChoosingLayout.addWidget(self.hdriPathLineEdit, 1, 0)
        self.fileChoosingLayout.addWidget(self.openFileDialogButton, 1, 1)
        self.fileChoosingLayout.addWidget(self.invalidPathLabel, 2, 0, 1, 2)

        self.hdriLayout.addLayout(self.fileChoosingLayout)

        # Translation
        self.translationLayout = QtGui.QHBoxLayout()

        self.translationLabel = QtGui.QLabel("Translation")
        self.translationLayout.addWidget(self.translationLabel)

        self.translationX = QtGui.QDoubleSpinBox()
        self.translationX.setMaximum(999999)
        self.translationX.setMinimum(-999999)
        self.translationX.setDecimals(3)
        self.translationX.setPrefix("x: ")
        self.translationLayout.addWidget(self.translationX)

        self.translationY = QtGui.QDoubleSpinBox()
        self.translationY.setMaximum(999999)
        self.translationY.setMinimum(-999999)
        self.translationY.setDecimals(3)
        self.translationY.setPrefix("y: ")
        self.translationLayout.addWidget(self.translationY)

        self.translationZ = QtGui.QDoubleSpinBox()
        self.translationZ.setMaximum(999999)
        self.translationZ.setMinimum(-999999)
        self.translationZ.setDecimals(3)
        self.translationZ.setPrefix("z: ")
        self.translationLayout.addWidget(self.translationZ)

        self.hdriLayout.addLayout(self.translationLayout)

        # Rotation
        self.rotationLayout = QtGui.QHBoxLayout()

        self.rotationLabel = QtGui.QLabel("Rotation")
        self.rotationLayout.addWidget(self.rotationLabel)

        self.rotationX = QtGui.QDoubleSpinBox()
        self.rotationX.setMaximum(360)
        self.rotationX.setMinimum(-360)
        self.rotationX.setDecimals(3)
        self.rotationX.setPrefix("x: ")
        self.rotationX.setSuffix(" deg")
        self.rotationLayout.addWidget(self.rotationX)

        self.rotationY = QtGui.QDoubleSpinBox()
        self.rotationY.setMaximum(360)
        self.rotationY.setMinimum(-360)
        self.rotationY.setDecimals(3)
        self.rotationY.setPrefix("y: ")
        self.rotationY.setSuffix(" deg")
        self.rotationLayout.addWidget(self.rotationY)

        self.rotationZ = QtGui.QDoubleSpinBox()
        self.rotationZ.setMaximum(360)
        self.rotationZ.setMinimum(-360)
        self.rotationZ.setDecimals(3)
        self.rotationZ.setPrefix("z: ")
        self.rotationZ.setSuffix(" deg")
        self.rotationLayout.addWidget(self.rotationZ)

        self.hdriLayout.addLayout(self.rotationLayout)

        # Preview
        self.preview = Preview("environment")
        self.wrapperGroupBoxLayout.addWidget(self.preview)

        self.setLayout(self.wrapperLayout)

        # Connect Signals
        self.radioButtonOptions[1].toggled.connect(self.hdriWidget.setEnabled)

        self.wrapperGroupBox.toggled.connect(self.checkTabValidity)

        self.openFileDialogButton.clicked.connect(self.handleFileDialog)
        self.hdriPathLineEdit.textChanged.connect(self.handleFileName)
        self.rotationX.editingFinished.connect(self.updatePreview)
        self.rotationY.editingFinished.connect(self.updatePreview)
        self.rotationZ.editingFinished.connect(self.updatePreview)
        self.translationX.editingFinished.connect(self.updatePreview)
        self.translationY.editingFinished.connect(self.updatePreview)
        self.translationZ.editingFinished.connect(self.updatePreview)

        # set default values
        self.radioButtonOptions[0].setChecked(True)

        self.wrapperGroupBox.setChecked(True)
        
        self.rotationX.setValue(90.0)
        self.rotationY.setValue(0.0)
        self.rotationZ.setValue(0.0)

        self.translationX.setValue(0.0)
        self.translationY.setValue(0.0)
        self.translationZ.setValue(0.0)

        self.hdriPathLineEdit.setText("") # at the end to avoid updatePreview to early

        # check FreeCAD Background
        self.radioButtonOptions[0].setChecked(True)
        self.hdriWidget.setEnabled(False)

    def checkTabValidity(self):
        fileName = self.hdriPathLineEdit.text()
        radioButton = self.radioButtonOptions[0]
        enabled = self.wrapperGroupBox.isChecked()

        if radioButton.isChecked() or (isAscii(fileName) and os.path.isfile(fileName) and fileName != "") or not enabled:
            self.hdrPathValidityChanged.emit(True)
        else:
            self.hdrPathValidityChanged.emit(False)

    def handleFileDialog(self):
        defaultPath = self.hdriPathLineEdit.text()

        fileName = QtGui.QFileDialog.getOpenFileName(
            self, "Select a HDRI File", defaultPath, "HDR Images (*.hdr)")[0]

        if fileName and fileName != u'' and fileName != '':
            self.hdriPathLineEdit.setText(fileName)

    def handleFileName(self, fileName):
        self.checkTabValidity()

        if isAscii(fileName) and os.path.isfile(fileName):
            self.invalidPathLabel.setText("")
        else:
            self.invalidPathLabel.setText("The name of the *.hdr file contains mutated vowels,"\
                "POV-Ray isn't able to handle, you typed no path or the file doesn't exist."\
                "Please rename / create the file and open it again.")

        self.updatePreview()

    def getHdriDict(self):
        """Return dictionary with path to *.hdr file and the rotation.

        Returns:
            str: Dictionary with path to *.hdr ("hdrPath") file and the rotation ("rotX", "rotY", "rotZ")
        """

        option = "FreeCAD Background"
        for radioButton in self.radioButtonOptions:
            if radioButton.isChecked():
                option = radioButton.text()
                break

        return {"enabled": self.wrapperGroupBox.isChecked(),
            "option": option,
            "hdrPath": self.hdriPathLineEdit.text(),
            "transX": self.translationX.value(),
            "transY": self.translationY.value(),
            "transZ": self.translationZ.value(),
            "rotX": self.rotationX.value(),
            "rotY": self.rotationY.value(),
            "rotZ": self.rotationZ.value()}

    def updatePreview(self):
        return 

        hdriPath = self.hdriPathLineEdit.text()

        if hdriPath == "" or hdriPath == u'':
            # show FreeCAD Background

            povCode = '''#version 3.7;
                global_settings { assumed_gamma 1.0 }
                #default { finish { ambient 0.2 diffuse 0.9 } }
                #default { pigment { rgb <0.800, 0.800, 0.800> } }

                #include "colors.inc"
                #include "textures.inc"

                // Camera ----------------------------------
                #declare CamUp = <0, 0, 1>;
                #declare CamRight = <1.33, 0, 0>;
                #declare CamRotation = <-35.264390534, 1.9538003485e-05, 45.0000026303>;
                #declare CamPosition = <12.0710725784, -12.0710668564, 12.0710678101>;
                camera {
                    location <0, 0, 0>
                    direction <0, 1, 0>
                    up CamUp
                    right CamRight
                    rotate CamRotation
                    translate CamPosition
                    angle 57.82
                }

                // Background ------------------------------
                sky_sphere {
                    pigment {
                        gradient z
                        color_map {
                            [ 0.00  color rgb<0.592, 0.592, 0.667> ]
                            [ 0.30  color rgb<0.592, 0.592, 0.667> ]
                            [ 0.70  color rgb<0.200, 0.200, 0.396> ]
                            [ 1.00  color rgb<0.200, 0.200, 0.396> ]
                        }
                        scale 2
                        translate -1
                        rotate<-35.264390534, 1.9538003485e-05, 45.0000026303>
                    }
                }'''

            bgColor1 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor')
            bgColor2 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor2')
            bgColor3 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor3')
            bgColor4 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor4')

            povCode += "sky_sphere {\n\tpigment {\n"
            if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Simple'):
                povCode += "\t\tcolor rgb" + self.exporter.uintColorToRGB(bgColor1) + "\n"

            elif App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Gradient'):
                povCode += "\t\tgradient z\n"
                povCode += "\t\tcolor_map {\n"
                povCode += "\t\t\t[ 0.00  color rgb" + \
                    self.exporter.uintColorToRGB(bgColor3) + " ]\n"
                povCode += "\t\t\t[ 0.30  color rgb" + \
                    self.exporter.uintColorToRGB(bgColor3) + " ]\n"
                if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('UseBackgroundColorMid'):
                    povCode += "\t\t\t[ 0.50  color rgb" + \
                        self.exporter.uintColorToRGB(bgColor4) + " ]\n"
                povCode += "\t\t\t[ 0.70  color rgb" + \
                    self.exporter.uintColorToRGB(bgColor2) + " ]\n"
                povCode += "\t\t\t[ 1.00  color rgb" + \
                    self.exporter.uintColorToRGB(bgColor2) + " ]\n"
                povCode += "\t\t}\n"
                povCode += "\t\tscale 2\n"
                povCode += "\t\ttranslate -1\n"
                povCode += "\t\trotate CamRotation\n"
            povCode += "\t}\n}\n"

            self.preview.render(povCode)

        elif isAscii(hdriPath) and os.path.isfile(hdriPath):
            # preview HDRI environment
            hdriDict = self.getHdriDict()

            povCode = '''#version 3.7;
                global_settings { assumed_gamma 1.0 }
                #default { finish { ambient 0.2 diffuse 0.9 } }
                #default { pigment { rgb <0.800, 0.800, 0.800> } }

                #include "colors.inc"
                #include "textures.inc"

                #declare CamUp = <0, 0, 1>;
                #declare CamRight = <1.33, 0, 0>;
                #declare CamRotation = <-35.264390534, 1.9538003485e-05, 45.0000026303>;
                #declare CamPosition = <15.3931512833, -12.0864868164, 16.4180793762>;
                camera {
                    location <0, 0, 0>
                    direction <0, 1, 0>
                    up CamUp
                    right CamRight
                    rotate CamRotation
                    translate CamPosition
                    angle 57.82
                }

                //----- z -----
                union {

                    cone { <0, 0, 0>, 0.2
                        <0, 0, 0.5>, 0.0
                        translate <0.0, 0.0, 10.0>
                    }
                    
                    cylinder { <0, 0, 0>, <0, 0, 10.0>, 0.1
                    }
                    
                    pigment { color rgb <0.000, 0.000, 1.000> }
                    
                }

                //----- y -----
                union {

                    cone { <0, 0, 0>, 0.2
                        <0, 0, 0.5>, 0.0
                        translate <0.0, 0.0, 10.0>
                    }
                    
                    cylinder { <0, 0, 0>, <0, 0, 10.0>, 0.1
                    }
                    
                    rotate <-90.0, -0.0, 0.0>
                    pigment { color rgb <0.000, 0.670, 0.000> }
                    
                }

                //----- x -----
                union {

                    cone { <0, 0, 0>, 0.2
                        <0, 0, 0.5>, 0.0
                        translate <0.0, 0.0, 10.0>
                    }
                    
                    cylinder { <0, 0, 0>, <0, 0, 10.0>, 0.1
                    }
                    
                    rotate <0.0, 90.0, 0.0>
                    pigment { color rgb <1.000, 0.000, 0.000> }
                    
                }'''

            povCode += "sky_sphere {\n"
            povCode += "\tpigment {\n"
            povCode += "\t\timage_map { hdr \"" + hdriDict["hdrPath"] + "\"\n"
            povCode += "\t\t\tgamma 1.1\n"
            povCode += "\t\t\tmap_type 1 interpolate 2\n"
            povCode += "\t\t}\n"
            povCode += "\t}\n"
            povCode += "\trotate <" + \
                str(hdriDict["rotX"]) + ", " + str(hdriDict["rotY"]) + \
                ", " + str(hdriDict["rotZ"]) + ">\n"
            povCode += "\ttranslate <" + \
                str(hdriDict["transX"]) + ", " + str(hdriDict["transY"]) + \
                ", " + str(hdriDict["transZ"]) + ">\n"
            povCode += "}\n"

            self.preview.render(povCode)
        else:
            # show error text because it is an invalid path
            self.preview.setErrorText("Without a valid path, it is not possible "\
                "to preview the environment.")

    def applyIniSettings(self, csvLines):
        """Apply the settings from the given lines from the ini file
        to the tab.

        Args:
            csvLines (Array): Array of lines for the CSV parser
        """

        # parse CSV
        csvReader = csv.reader(csvLines, delimiter=',')
        for row in csvReader:
            if row[0] == "environment":
                self.wrapperGroupBox.setChecked(strToBool(row[1]))

                for radioButton in self.radioButtonOptions:
                    if row[2] == radioButton.text():
                        radioButton.setChecked(True)
                        break

                self.translationX.setValue(float(row[4]))
                self.translationY.setValue(float(row[5]))
                self.translationZ.setValue(float(row[6]))

                self.rotationX.setValue(float(row[7]))
                self.rotationY.setValue(float(row[8]))
                self.rotationZ.setValue(float(row[9]))

                self.hdriPathLineEdit.setText(row[3]) # at the end to avoid updatePreview to early

    def settingsToIniFormat(self):
        """Convert the settings from the tab to CSV.

        Returns:
            str: The created CSV with ";" for the ini file at the
            beginning
        """

        csv = ";"
        csv += "environment"

        hdriDict = self.getHdriDict()

        csv += "," + str(hdriDict["enabled"]) + "," + hdriDict["option"] + "," + hdriDict["hdrPath"] + "," + str(hdriDict["transX"]) + "," + str(hdriDict["transY"]) + "," + str(hdriDict["transZ"]) + "," + str(hdriDict["rotX"]) + "," + str(
            hdriDict["rotY"]) + "," + str(hdriDict["rotZ"])

        return csv + "\n"

    def applyQSettings(self, settingsObject):
        """Apply the settings stored with QSettings to the tab.

        Args:
            settingsObject (QSettings Object): The QSettings Object to read the data from
        """

        self.preview.applyQSettings(settingsObject)

    def saveQSettings(self, settingsObject):
        """Save the settings from the tab with QSettings.

        Args:
            settingsObject (QSettings Object): QSettings object to store the data
        """

        self.preview.saveQSettings(settingsObject)
