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

from FreeCAD import Base
from FreeCAD import Part
from pivy import coin
import os
import math
import MeshPart
import platform
import subprocess

from helpDefs import *

class ExportToPovRay:
    """Export the FreeCAD model to POV-Ray"""
    def __init__(self):
        #get default shape color (editable in FreeCAD settings) (default rgb(0.8, 0.8, 0.8))
        self.DefaultShapeColor = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('DefaultShapeColor')

        self.os = platform.system() #get system informations

    def initExport(self, renderSettings):
        self.doc = App.ActiveDocument
        self.objs = self.doc.Objects

        #get all paths, file names, directories, etc.
        self.projectName = renderSettings.projectName
        self.directory = renderSettings.directory

        self.iniName = renderSettings.iniName
        self.iniPath = renderSettings.iniPath
        self.povName = renderSettings.povName
        self.povPath = renderSettings.povPath

        self.incName = renderSettings.incName
        self.incPath = renderSettings.incPath
        self.meshName = renderSettings.meshName
        self.meshPath = renderSettings.meshPath
        self.errorName = renderSettings.errorName
        self.errorPath = renderSettings.errorPath
        self.fcViewName = renderSettings.fcViewName
        self.fcViewPath = renderSettings.fcViewPath
        self.texIncName = renderSettings.texIncName
        self.texIncPath = renderSettings.texIncPath

        self.meshFileContent = ""

        #get all output options
        self.width = renderSettings.width
        self.height = renderSettings.height

        self.expBg = renderSettings.expBg
        self.expLight = renderSettings.expLight
        self.repRot = renderSettings.repRot
        self.expFcView = renderSettings.expFcView

        #get camera
        self.CamOri = Gui.ActiveDocument.ActiveView.getCameraOrientation()
        self.CamType = Gui.ActiveDocument.ActiveView.getCameraType()
        self.CamPos = Gui.ActiveDocument.ActiveView.viewPosition()
        self.CamNode = Gui.ActiveDocument.ActiveView.getCameraNode()
        self.EulerCam = Gui.ActiveDocument.ActiveView.getCameraOrientation().toEuler()

        #exist a user inc file
        self.userInc = False

        if self.povPath != -1 and self.povPath != "" and self.povPath != " ": #is there a pov file
            try: #try to open pov file
                file = open(self.povPath, "w+") #XXX really "w+"?
                file.close()
            except:
                App.Console.PrintError("Can't open the pov file\n\n")
                return -1

            try: #try to open inc file
                file = open(self.incPath, "r")
                self.incContent = file.read()
                file.close()

                App.Console.PrintMessage("Include file found: " + self.incPath + "\n")
                self.incContent = self.delComments(self.incContent)
                self.userInc = True
            except:
                self.incContent = ""

            #open texture inc file
            file = open(self.texIncPath, "r")
            self.texIncContent = file.read()
            file.close()
        else:
            App.Console.PrintMessage("\n\nCanceled\n\n")
            return -1

        #get statistics
        objs = App.ActiveDocument.Objects
        self.statistics = self.getStatistics(objs)
        App.Console.PrintMessage(self.statistics)

        #clear old mesh file
        try:
            file = open(self.meshPath, "w")
            file.close()
        except:
            pass


        self.startExport() #start the export

    def startExport(self): #start the export to POV-Ray
        firstLayer = [] #the highest objects in the model tree

        #repair rotation (see documentation)
        if self.repRot:
            self.repairRotation(self.objs)

        #export FreeCAD view
        if self.expFcView:
            self.exportFcView()

        #get the first layer and check visibility of parent objects
        for obj in self.objs:
            guiObject = obj.ViewObject
            if guiObject.Visibility and obj.TypeId != "App::DocumentObjectGroup" and not self.hasBodyAsParent(obj) and not self.hasPartAsParent(obj):
                firstLayer.append(obj)

        #create pov code of objects
        objPovCode = ""
        for obj in firstLayer:
            objPovCode += self.createPovCode(obj, True, True, True, True, True)

        #add general pov code / "header"
        finalPovCode = "#version 3.6; // 3.7\nglobal_settings { assumed_gamma 1.0 }\n#default { finish { ambient 0.2 diffuse 0.9 } }\n"

        finalPovCode += "#default { pigment { rgb " + self.uintColorToRGB(self.DefaultShapeColor) + " } }\n"

        finalPovCode += "\n//------------------------------------------\n"
        finalPovCode += "#include \"colors.inc\"\n#include \"textures.inc\"\n"

        #add textures inc include
        finalPovCode += "#include \"" + self.texIncName + "\"\n"

        #if model contains mesh objects, a mesh file will be included
        if self.meshFileContent != "":
            finalPovCode += "#include \"" + self.meshName + "\"\n"

        finalPovCode += "\n//------------------------------------------\n"
        finalPovCode += "// Camera ----------------------------------\n"
        finalPovCode += self.getCam()

        if self.expLight:
            finalPovCode += "\n// FreeCAD Light -------------------------------------\n"
            finalPovCode += self.getFCLight()

        if self.expBg:
            finalPovCode += "\n// Background ------------------------------\n"
            finalPovCode += self.getBackground()

        finalPovCode += "\n//------------------------------------------\n"

        if self.userInc: #include user inc file if there is a file
            finalPovCode += "\n#include \"" + self.incName + "\"\n\n"

        finalPovCode += "// Objects in Scene ------------------------\n"

        finalPovCode += objPovCode

        #change line breaks for windows
        if self.os == "Windows":
            finalPovCode.replace("\n", "\r\n")
            self.meshFileContent.replace("\n", "\r\n")

        #write mesh file
        if self.meshFileContent != "":
            self.meshFile = open(self.meshPath, "w")
            self.meshFile.write(self.meshFileContent)
            self.meshFile.close()

        self.writeFile(finalPovCode) #write the final code to the output file
        self.openPovRay() #start povray


    def createPovCode(self, fcObj, expPlacement, expPigment, expClose, expLabel, expMeshDef): #returns the povray code for the object
        if expLabel:
            povCode = "\n//----- " + stringCorrection(fcObj.Label) + " -----" #add the name of the object
        else:
            povCode = ""

        if fcObj.TypeId == "Part::Box": #Box
            povBox = "\nbox { <0,0,0>, <" + str(float(fcObj.Length)) + ", " + str(float(fcObj.Width)) + ", " + str(float(fcObj.Height)) + ">"
            povCode += povBox

        elif fcObj.TypeId == "Part::Sphere": # Sphere
            radius = fcObj.Radius.getValueAs("mm")

            povSphere = "\nsphere { <0, 0, 0> " + str(radius)

            povCode += povSphere

        elif fcObj.TypeId == "Part::Ellipsoid": # Ellipsoid
            r1 = fcObj.Radius1.getValueAs("mm").Value
            r2 = fcObj.Radius2.getValueAs("mm").Value
            r3 = fcObj.Radius3.getValueAs("mm").Value

            povSphere = "\nsphere { <0, 0, 0> 1\n"

            povSphere += "\tscale <" + str(r2) + ", " + str(r3) + ", " + str(r1) + ">"

            povCode += povSphere

        elif fcObj.TypeId == "Part::Cone": #Cone
            r1 = fcObj.Radius1.getValueAs("mm").Value
            c1 = "<0, 0, 0>"
            r2 = fcObj.Radius2.getValueAs("mm").Value
            c2 = "<0, 0, " + str(fcObj.Height.getValueAs("mm").Value) + ">"

            povCone = "\ncone { "
            povCone += c1 + ", " + str(r1) + "\n    "
            povCone += c2 + ", " + str(r2)

            povCode += povCone

        elif fcObj.TypeId == "Part::Cylinder": #Cylinder
            r = fcObj.Radius.getValueAs("mm").Value
            baseP = "<0, 0, 0>"
            CapP = "<0, 0, " + str(fcObj.Height.getValueAs("mm").Value) + ">"

            povCylinder = "\ncylinder { "
            povCylinder += baseP + ", " + CapP + ", " + str(r)

            povCode += povCylinder

        elif fcObj.TypeId == "Part::Torus": #Torus
            r1 = fcObj.Radius1.getValueAs("mm").Value
            r2 = fcObj.Radius2.getValueAs("mm").Value

            povTorus = "\ntorus { "
            povTorus += str(r1) + ", " + str(r2)

            povCode += povTorus

        elif fcObj.TypeId == "Part::Plane": #Plane
            width = fcObj.Width.getValueAs("mm").Value
            length = fcObj.Length.getValueAs("mm").Value

            povPlane = "\npolygon { "
            povPlane += "5, <0, 0>, <" + str(length) + ", 0>, <" + str(length) + ", " + str(width) + ">, <0, " + str(width) + ">, <0, 0>"

            povCode += povPlane

        elif fcObj.TypeId == "Part::Cut":  #Cut
            childs = fcObj.OutList
            povCut = "\ndifference {\n"
            for child in childs:
                childCode = self.createPovCode(child, True, expPigment, True, expLabel, expMeshDef) #call createPovCode for the child
                povCut += childCode.replace("\n", "\n\t") #add the indents

            povCode += povCut

        elif fcObj.TypeId == "Part::MultiFuse" or fcObj.TypeId == "Part::Fuse" or fcObj.TypeId == "Part::Compound": #Fusion
            childs = fcObj.OutList
            povFusion = "\nunion {\n"
            for child in childs:
                childCode = self.createPovCode(child, True, expPigment, True, expLabel, expMeshDef) #call createPovCode for the child
                povFusion += childCode.replace("\n", "\n\t") #add the indents

            povCode += povFusion

        elif fcObj.TypeId == "Part::MultiCommon" or fcObj.TypeId == "Part::Common": #Common
            childs = fcObj.OutList
            povCommon = "\nintersection {\n"
            for child in childs:
                childCode = self.createPovCode(child, True, expPigment, True, expLabel, expMeshDef) #call createPovCode for the child
                povCommon += childCode.replace("\n", "\n\t") #add the indents

            povCode += povCommon

        elif fcObj.TypeId == "Part::FeaturePython" and fcObj.Name.startswith("Array"): #Array from Draft workbench
            povArr = ""
            if fcObj.ArrayType == "polar":
                child = fcObj.Base
                #for child in childs:
                center = "<" + str(fcObj.Center.x) + ", " + str(fcObj.Center.y) + ", " + str(fcObj.Center.z) + ">"
                axisX = fcObj.Axis.x
                axisY = fcObj.Axis.y
                axisZ = fcObj.Axis.z
                highestAxis = max(axisX, axisY, axisZ) #get highest value
                axisX /= highestAxis
                axisY /= highestAxis
                axisZ /= highestAxis


                axis = "<" + str(axisX) + ", " + str(axisY) + ", " + str(axisZ) + ">"
                intervalAxis = "<" + str(fcObj.IntervalAxis.x) + ", " + str(fcObj.IntervalAxis.y) + ", " + str(fcObj.IntervalAxis.z) + ">"
                number = fcObj.NumberPolar
                angle = fcObj.Angle.getValueAs("deg").Value

                declareName = stringCorrection(child.Label.capitalize()) + "_" + child.Name
                povArr += "\n#declare " + declareName + " = "
                childCode = self.createPovCode(child, True, expPigment, True, expLabel, expMeshDef) #call createPovCode for the child
                povArr += childCode

                povArr += "\n#declare i = 0;\n"
                povArr += "#declare endNo = " + str(number) + ";\n"
                povArr += "#declare axis = " + axis + ";\n"
                povArr += "#declare arrAngle = " + str(angle) + ";\n"
                povArr += "#while (i < endNo)\n"
                povArr += "\tobject { " + declareName + "\n"
                if fcObj.Center.x != 0 or fcObj.Center.y != 0 or fcObj.Center.z != 0:
                    povArr += "\t\ttranslate -" + center + "\n"

                povArr += "\t\t#declare rotAngle = i * arrAngle / (endNo-1);\n"
                povArr += "\t\t#local vX = vaxis_rotate(x, axis, rotAngle);\n"
                povArr += "\t\t#local vY = vaxis_rotate(y, axis, rotAngle);\n"
                povArr += "\t\t#local vZ = vaxis_rotate(z, axis, rotAngle);\n"
                povArr += "\t\ttransform {\n"
                povArr += "\t\t\tmatrix <vX.x, vX.y, vX.z, vY.x, vY.y, vY.z, vZ.x, vZ.y, vZ.z, 0, 0, 0>\n"
                povArr += "\t\t}\n"

                if fcObj.Center.x != 0 or fcObj.Center.y != 0 or fcObj.Center.z != 0:
                    povArr += "\t\ttranslate " + center + "\n"

                if expPlacement:
                    rotation = self.getRotation(fcObj)
                    if rotation != "": #test if the object is rotated
                        povArr += "        " + rotation + "\n"

                if fcObj.IntervalAxis.x != 0 or fcObj.IntervalAxis.y != 0 or fcObj.IntervalAxis.z != 0:
                    povArr += "\t\ttranslate " + intervalAxis + " * i\n"

                if expPlacement:
                    translation = self.getTranslation(fcObj)
                    if translation != "": #test if the object is translated
                        povArr += "\t" + translation + "\n"

                if expPigment:
                    pigment = self.getPigment(fcObj)
                    if pigment != "": #test if the object has the standard pigment
                        povArr += "\t" + pigment + "\n"

                povArr += "    }\n\t#declare i = i + 1;\n"
                povArr += "#end\n"

            elif fcObj.ArrayType == "ortho":
                child = fcObj.Base
                #for child in childs:
                intervalX = "<" + str(fcObj.IntervalX.x) + ", " + str(fcObj.IntervalX.y) + ", " + str(fcObj.IntervalX.z) + ">"
                intervalY = "<" + str(fcObj.IntervalY.x) + ", " + str(fcObj.IntervalY.y) + ", " + str(fcObj.IntervalY.z) + ">"
                intervalZ = "<" + str(fcObj.IntervalZ.x) + ", " + str(fcObj.IntervalZ.y) + ", " + str(fcObj.IntervalZ.z) + ">"

                numX = fcObj.NumberX
                if numX == 0:
                    numX = 1

                numY = fcObj.NumberY
                if numY == 0:
                    numY = 1

                numZ = fcObj.NumberZ
                if numZ == 0:
                    numZ = 1

                declareName = stringCorrection(child.Label.capitalize()) + "_" + child.Name
                povArr += "\n#declare " + declareName + " = "
                childCode = self.createPovCode(child, True, expPigment, True, expLabel, True) #call createPovCode for the child
                povArr += childCode

                povArr += "#declare intervalX = " + intervalX + ";\n"
                povArr += "#declare intervalY = " + intervalY + ";\n"
                povArr += "#declare intervalZ = " + intervalZ + ";\n\n"

                povArr += "#declare numX = " + str(numX) + ";\n"
                povArr += "#declare ix = 0;\n"
                povArr += "#while (ix < numX)\n"

                povArr += "\t#declare numY = " + str(numY) + ";\n"
                povArr += "\t#declare iy = 0;\n"
                povArr += "\t#while (iy < numY)\n"

                povArr += "\t\t#declare numZ = " + str(numZ) + ";\n"
                povArr += "\t\t#declare iz = 0;\n"
                povArr += "\t\t#while (iz < numZ)\n"

                povArr += "\t\t\tobject { " + declareName + "\n"
                povArr += "\t\t\t\ttranslate intervalX * ix\n"
                povArr += "\t\t\t\ttranslate intervalY * iy\n"
                povArr += "\t\t\t\ttranslate intervalZ * iz\n"

                if expPlacement:
                    translation = self.getTranslation(fcObj)
                    if translation != "": #test if the object is translated
                        povArr += "\t\t\t\t" + translation + "\n"

                    rotation = self.getRotation(fcObj)
                    if rotation != "": #test if the object is rotated
                        povArr += "\t\t\t\t" + rotation + "\n"

                if expPigment:
                    pigment = self.getPigment(fcObj)
                    if pigment != "": #test if the object has the standard pigment
                        povArr += "\t\t\t\t" + pigment + "\n"

                povArr += "\t\t\t}\n"

                povArr += "\t\t\t#declare iz = iz + 1;\n"
                povArr += "\t\t#end\n"
                povArr += "\t\t#declare iy = iy + 1;\n"
                povArr += "\t#end\n"
                povArr += "\t#declare ix = ix + 1;\n"
                povArr += "#end\n"

            else:
                povCode += self.createMesh(fcObj, expPlacement, expPigment, expClose, expMeshDef)

            povArr = povArr.replace("\n", "\n\t")
            povCode += "\nunion {\n"
            povCode += povArr
            expPigment = False
            expPlacement = False

        elif fcObj.TypeId == "Part::FeaturePython" and fcObj.Name.startswith("Clone"): #Clone from Draft workbench
            povClone = ""

            childs = fcObj.Objects
            for child in childs:
                povClone += self.createPovCode(child, False, False, False, False, True)

            if fcObj.Scale.x != 1 or fcObj.Scale.y != 1 or fcObj.Scale.z != 1:
                povClone += "\n\tscale <" + str(fcObj.Scale.x) + ", " + str(fcObj.Scale.y) + ", " + str(fcObj.Scale.z) + ">"

            povCode += povClone

        elif fcObj.TypeId == "Part::Extrusion":
            spline = self.sketchToBezier(fcObj.Base)

            if not self.isExtrudeSupported(fcObj) or spline == -1:
                povCode += self.createMesh(fcObj, expPlacement, expPigment, expClose, expMeshDef)
                return povCode #return because the mesh may not translated and rotated

            startHeight = 0
            endHeight = fcObj.LengthFwd.getValueAs("mm").Value

            if fcObj.Symmetric:
                endHeight /= 2
                startHeight = -endHeight

            startHeight -= fcObj.LengthRev.getValueAs("mm").Value

            if not fcObj.Reversed:
                startHeight *= -1
                endHeight *= -1

            povPad = ""
            povPad += "\nprism {\n"
            povPad += "\tbezier_spline\n"
            povPad += "\t" + str(startHeight) + ", " + str(endHeight) + ", " + str(spline[1])
            povPad += spline[0].replace("\n", "\n\t") + "\n" #add the indents

            rotation = self.getRotation(fcObj.Base)
            if rotation != "": #test if the object is rotated
                povPad += "\t" + rotation + "\n"

            translation = self.getTranslation(fcObj.Base)
            if translation != "": #test if the object is translated
                povPad += "\t" + translation + "\n"

            povCode += povPad

        elif fcObj.TypeId == "Image::ImagePlane":
            image = fcObj.ImageFile
            imgType = image[-3:]

            width = fcObj.XSize.getValueAs("mm").Value
            height = fcObj.YSize.getValueAs("mm").Value

            povImg = "\npolygon { "
            povImg += "5, <0, 0>, <" + str(width) + ", 0>, <" + str(width) + ", " + str(height) + ">, <0, " + str(height) + ">, <0, 0>"

            povPigment = "\npigment {\n"
            povPigment += "\timage_map {\n"
            povPigment += "\t\t" + imgType + ' "' + image + '"\n'
            povPigment += "\t\tmap_type 0\n"
            povPigment += "\t}\n"
            povPigment += "\tscale <" + str(width) + ", " + str(height) + ", 1>\n"
            povPigment += "}\n"

            povImg += povPigment.replace("\n", "\n\t")
            povImg += "\ttranslate -<" + str(width / 2) + ", " + str(height / 2) + ", 0>\n"

            expPigment = False
            povCode += povImg

        elif fcObj.TypeId == "App::Part": #Part
            povPart = "\nunion {\n"

            childs = fcObj.OutList
            for child in childs:
                guiChild = child.ViewObject
                if guiChild.Visibility:
                    childCode = self.createPovCode(child, True, expPigment, True, expLabel, expMeshDef) #call createPovCode for the child
                    povPart += childCode.replace("\n", "\n\t") #add the indents

            povCode += povPart
            expPigment = False #part has no pigment


        elif fcObj.TypeId == "PartDesign::Body": #Body from PartDesign
            if not self.isBodySupported(fcObj):
                povCode += self.createMesh(fcObj, expPlacement, expPigment, expClose, expMeshDef)
                return povCode #return because the mesh may not translated and rotated

            povBody = "\nunion {\n"
            if fcObj.Tip != None:
                povBody += self.createPovCode(fcObj.Tip, True, True, True, True, True).replace("\n", "\n\t") #add chld code and indents
                povCode += povBody
            else:
                return ""

        elif fcObj.TypeId == "PartDesign::Pad" or fcObj.TypeId == "PartDesign::Pocket": #Pad or Pocket from PartDesign
            povPad = ""
            spline = self.sketchToBezier(fcObj.Profile[0])

            if (self.isSketchSupported(fcObj.Profile[0]) == False) or spline == -1 or (self.isPadPocketSupported(fcObj) == False):
                povPad += self.createMesh(fcObj, expPlacement, True, expClose, expMeshDef)
                povCode += povPad
                return povCode

            startHeight = 0
            if fcObj.TypeId == "PartDesign::Pocket":
                startHeight = -0.0001
            endHeight = fcObj.Length.getValueAs("mm").Value
            if fcObj.Midplane:
                endHeight /= 2
                startHeight = -endHeight
            if not fcObj.Reversed:
                startHeight *= -1
                endHeight *= -1
            if fcObj.TypeId == "PartDesign::Pocket":
                startHeight *= -1
                endHeight *= -1

            try:
                if fcObj.TypeId == "PartDesign::Pocket":
                    povPad += "\ndifference {\n"
                else:
                    povPad += "\nunion {\n"
            except:
                povPad += "\nunion {\n"

            if fcObj.BaseFeature != None:
                povBase = self.createPovCode(fcObj.BaseFeature, True, True, True, True, True)
                povPad += povBase.replace("\n", "\n\t") #add the indents

            povPad += "\n\tprism {\n"
            povPad += "\t\tbezier_spline\n"
            povPad += "\t\t" + str(startHeight) + ", " + str(endHeight) + ", " + str(spline[1])
            povPad += spline[0].replace("\n", "\n\t\t") + "\n" #add the indents

            if expPlacement:
                rotation = self.getRotation(fcObj.Profile[0])
                if rotation != "": #test if the object is rotated
                    povPad += "\t\t" + rotation + "\n"

                translation = self.getTranslation(fcObj.Profile[0])
                if translation != "": #test if the object is translated
                    povPad += "\t\t" + translation + "\n"
            else:
                rotation = "\t\trotate <-90, 0, 0>"
                povPad += rotation

            povPad += "\n\t}\n"

            if expClose:
                povPad += "\n}\n"

            povCode += povPad
            return povCode


        elif fcObj.TypeId == "Part::FeaturePython" and fcObj.Name.startswith("PointLight"):
            povLight = "\nlight_source { "
            povLight += "<0, 0, 0>"
            povLight += "\n\tcolor rgb<" + str(fcObj.Color[0]) + ", " + str(fcObj.Color[1]) + ", " + str(fcObj.Color[2]) + ">"
            
            if fcObj.Fade_Distance.getValueAs("mm").Value != 0 and fcObj.Fade_Power != 0:
                povLight += "\n\tfade_distance " + str(fcObj.Fade_Distance.getValueAs("mm").Value)
                povLight += "\n\tfade_power " + str(fcObj.Fade_Power)

            povCode += povLight

        elif fcObj.TypeId == "Part::FeaturePython" and fcObj.Name.startswith("AreaLight"):
            povLight = "\nlight_source { "
            povLight += "<0, 0, 0>"
            povLight += "\n\tcolor rgb<" + str(fcObj.Color[0]) + ", " + str(fcObj.Color[1]) + ", " + str(fcObj.Color[2]) + ">"
            povLight += "\n\tarea_light"

            povLight += "\n\t<" + str(fcObj.Length.getValueAs("mm").Value) + ", 0, 0>, "
            povLight += "<0, " + str(fcObj.Width.getValueAs("mm").Value) + ", 0>"

            povLight += "\n\t" + str(fcObj.LengthLights) + ", " + str(fcObj.WidthLights)

            povLight += "\n\tadaptive " + str(fcObj.Adaptive)

            if fcObj.Area_Illumination:
                povLight += "\n\tarea_illumination on"

            if fcObj.Jitter:
                povLight += "\n\tjitter"
            
            if fcObj.Fade_Distance.getValueAs("mm").Value != 0 and fcObj.Fade_Power != 0:
                povLight += "\n\tfade_distance " + str(fcObj.Fade_Distance.getValueAs("mm").Value)
                povLight += "\n\tfade_power " + str(fcObj.Fade_Power)

            povCode += povLight

        elif fcObj.TypeId == "Part::FeaturePython" and fcObj.Name.startswith("SpotLight"):
            povLight = "\nlight_source { "
            povLight += "<0, 0, 0>"
            povLight += "\n\tcolor rgb<" + str(fcObj.Color[0]) + ", " + str(fcObj.Color[1]) + ", " + str(fcObj.Color[2]) + ">"
            povLight += "\n\tspotlight"
            povLight += "\n\tpoint_at <0, -1, 0>"

            povLight += "\n\tradius " + str(fcObj.Radius.getValueAs("deg").Value)
            povLight += "\n\tfalloff " + str(fcObj.FallOff.getValueAs("deg").Value)
            povLight += "\n\ttightness " + str(fcObj.Tightness)

            povCode += povLight


        else: #not a supported object
            povCode += self.createMesh(fcObj, expPlacement, expPigment, expClose, expMeshDef)
            return povCode #return because the mesh may not translated and rotated

        povCode += "\n"

        if expPlacement:
            rotation = self.getRotation(fcObj)
            if rotation != "": #test if the object is rotated
                povCode += "\t" + rotation + "\n"

            translation = self.getTranslation(fcObj)
            if translation != "": #test if the object is translated
                povCode += "\t" + translation + "\n"

        if expPigment:
            pigment = self.getPigment(fcObj)
            if pigment != "": #test if the object has the standard pigment
                povCode += pigment.replace("\n", "\n\t") + "\n"

        if expClose:
            povCode += "}\n"

        return povCode


    def sketchToBezier(self, sketch): #create pov bezier_spline from sketch
        try:
            povSpline = "\n"

            unsortedLines = sketch.Geometry #unordered lines / original order

            #delete construction geometry and points
            unsortedLines = [line for line in unsortedLines if not (line.Construction or type(line) == Part.Point)]

            numOfPoints = 0 #counter for povray bezier points

            sortedLines = [] #lines in the right order

            while unsortedLines: #until the unsortedLines array is empty
                sortedLines.append(unsortedLines[0]) # put first line in sorted lines array
                startLine = unsortedLines[0]         # and
                del unsortedLines[0]                 # delete from unsorted lines array

                if type(startLine) != Part.Circle and type(sortedLines[len(sortedLines) - 1]) != Part.Circle:
                    while not self.isSamePoint(startLine.StartPoint, sortedLines[len(sortedLines) - 1].EndPoint): # search for matching line
                        # handling of -1 missing
                        nextLineI = self.getNextLine(unsortedLines, sortedLines[len(sortedLines) - 1])

                        #change direction
                        if self.isSamePoint(sortedLines[len(sortedLines) - 1].EndPoint, unsortedLines[nextLineI].EndPoint):
                            unsortedLines[nextLineI].reverse()

                        sortedLines.append(unsortedLines[nextLineI])
                        del unsortedLines[nextLineI]

        except:
            return -1

        #create povSpline
        for line in sortedLines:
            if type(line) == Part.LineSegment:
                povSpline += "<" + str(round(line.StartPoint.x, 3)) + ", " + str(round(line.StartPoint.y, 3)) + ">, "
                povSpline += "<" + str(round(line.StartPoint.x, 3)) + ", " + str(round(line.StartPoint.y, 3)) + ">, "
                povSpline += "<" + str(round(line.EndPoint.x, 3)) + ", " + str(round(line.EndPoint.y, 3)) + ">, "
                povSpline += "<" + str(round(line.EndPoint.x, 3)) + ", " + str(round(line.EndPoint.y, 3)) + ">//line\n"

                numOfPoints += 4

            elif type(line) == Part.Circle:
                r = line.Radius
                cx = round(line.Center.x, 3)
                cy = round(line.Center.y, 3)
                dTC = round((4.0/3.0) * math.tan(math.pi / 8.0) * r, 3) #distance to control point

                posP0 = "<" + str(cx) + ", " + str(cy + r) + ">"
                controlP0_0 = "<" + str(cx - dTC) + ", " + str(cy + r) + ">"
                controlP0_1 = "<" + str(cx + dTC) + ", " + str(cy + r) + ">"

                posP1 = "<" + str(cx + r) + ", " + str(cy) + ">"
                controlP1_0 = "<" + str(cx + r) + ", " + str(cy + dTC) + ">"
                controlP1_1 = "<" + str(cx + r) + ", " + str(cy - dTC) + ">"

                posP2 = "<" + str(cx) + ", " + str(cy - r) + ">"
                controlP2_0 = "<" + str(cx + dTC) + ", " + str(cy - r) + ">"
                controlP2_1 = "<" + str(cx - dTC) + ", " + str(cy - r) + ">"

                posP3 = "<" + str(cx - r) + ", " + str(cy) + ">"
                controlP3_0 = "<" + str(cx - r) + ", " + str(cy - dTC) + ">"
                controlP3_1 = "<" + str(cx - r) + ", " + str(cy + dTC) + ">"

                povSpline += posP0 + ", " + controlP0_1 + ", " + controlP1_0 + ", " + posP1 + "//circle\n"
                povSpline += posP1 + ", " + controlP1_1 + ", " + controlP2_0 + ", " + posP2 + "//circle\n"
                povSpline += posP2 + ", " + controlP2_1 + ", " + controlP3_0 + ", " + posP3 + "//circle\n"
                povSpline += posP3 + ", " + controlP3_1 + ", " + controlP0_0 + ", " + posP0 + "//circle\n"

                numOfPoints += 16

            elif type(line) == Part.ArcOfCircle:
                arc = line
                a = arc.LastParameter - arc.FirstParameter

                #correct direction of arc if necessary
                if arc.Axis.z < 0:
                    arc.reverse()
                    reversed = True
                else:
                    reversed = False

                #split arc in segments <90°
                if a % math.pi / 2 == 0:
                    numOfSegments = a / (math.pi / 2)
                else:
                    numOfSegments = math.floor(a / (math.pi / 2)) + 1

                if numOfSegments % 1 != 0.0:
                    raise ValueError("numOfSegments is not an integer.")

                numOfSegments = int(numOfSegments)
                angleOfSegment = a / numOfSegments

                segments = []
                for i in range(numOfSegments):
                    if reversed:
                        segment = {"startAngle": arc.LastParameter - i * angleOfSegment,
                                   "endAngle": arc.LastParameter - (i+1) * angleOfSegment,
                                   "direction": "clockwise"}
                    else:
                        segment = {"startAngle": arc.FirstParameter + i * angleOfSegment,
                                   "endAngle": arc.FirstParameter + (i+1) * angleOfSegment,
                                   "direction": "anticlockwise"}

                    segments.append(segment)

                #segment to bezier
                for segment in segments:
                    numOfSegmentsPerCircle = (2 * math.pi) / angleOfSegment
                    controlDistance = (4.0/3.0) * math.tan(math.pi / (2 * numOfSegmentsPerCircle)) * arc.Radius

                    startX = round(math.cos(segment["startAngle"]) * arc.Radius + arc.Location.x, 3)
                    startY = round(math.sin(segment["startAngle"]) * arc.Radius + arc.Location.y, 3)
                    startControlX = round(-math.cos(math.pi/2 - segment["startAngle"]) * controlDistance, 3)
                    startControlY = round(math.sin(math.pi/2 - segment["startAngle"]) * controlDistance, 3)

                    endX = round(math.cos(segment["endAngle"]) * arc.Radius + arc.Location.x, 3)
                    endY = round(math.sin(segment["endAngle"]) * arc.Radius + arc.Location.y, 3)
                    endControlX = round(math.cos(math.pi/2 - segment["endAngle"]) * controlDistance, 3)
                    endControlY = round(-math.sin(math.pi/2 - segment["endAngle"]) * controlDistance, 3)

                    if reversed:
                        startControlX *= -1
                        startControlY *= -1
                        endControlX *= -1
                        endControlY *= -1
                    
                    startControlX += startX
                    startControlY += startY
                    endControlX += endX
                    endControlY += endY

                    povSpline += "<" + str(startX) + ", " + str(startY) + ">, "
                    povSpline += "<" + str(startControlX) + ", " + str(startControlY) + ">, "
                    povSpline += "<" + str(endControlX) + ", " + str(endControlY) + ">, "
                    povSpline += "<" + str(endX) + ", " + str(endY) + ">//arc\n"

                    numOfPoints += 4
                
        return [povSpline, numOfPoints]

    def getNextLine(self, lines, lastLine): #get index of next line for the given last line
        #returns index
        i = 0
        for line in lines:
            if self.isSamePoint(line.EndPoint, lastLine.EndPoint) or self.isSamePoint(line.StartPoint, lastLine.EndPoint):
                return i
            i += 1
        return -1

    def isSamePoint(self, point1, point2): #are two points equal
        #round because FreeCAD has rounding mistakes
        if round(point1.x, 3) == round(point2.x, 3) and round(point1.y, 3) == round(point2.y, 3) and round(point1.z, 3) == round(point2.z, 3):
            return True
        return False

    def hasLinesConstructive(self, lines): #are constructive lines in lines array
        for line in lines:
            if line.Construction:
                return True
        return False

    def isBodySupported(self, body): #is a body full supported
        supportedTypeIds = ["App::Origin",
                            "App::Line",
                            "App::Plane",
                            "Sketcher::SketchObject",
                            "PartDesign::Pad",
                            "PartDesign::Pocket",
                            "PartDesign::Point",
                            "PartDesign::Line",
                            "PartDesign::Plane"]

        childs = body.OutListRecursive

        #are objects supported
        for obj in childs:
            if not obj.TypeId in supportedTypeIds:
                return False

        #get sketches
        sketches = []
        for obj in childs:
            if obj.TypeId == "Sketcher::SketchObject":
                sketches.append(obj)

        #test sketches
        for sketch in sketches:
            if not self.isSketchSupported(sketch):
                return False

        supportedTypes = ["Length"]
        #get pads and pockets
        padsPockets = []
        for obj in childs:
            if obj.TypeId == "PartDesign::Pad" or obj.TypeId == "PartDesign::Pocket":
                padsPockets.append(obj)

        #test types
        for obj in padsPockets:
            if not obj.Type in supportedTypes:
                return False

        return True

    def isPadPocketSupported(self, fcObj):
        supportedTypes = ["Length"]

        if not (fcObj.TypeId == "PartDesign::Pad" or fcObj.TypeId == "PartDesign::Pocket"):
            return False

        if not fcObj.Type in supportedTypes:
            return False

        if not self.isSketchSupported(fcObj.Profile[0]):
            return False

        return True

    def isExtrudeSupported(self, fcObj):
        #test mode of direction
        if fcObj.DirMode != "Normal":
            return False

        #test TaperAngle and TaperAngleRev
        if fcObj.TaperAngle.getValueAs("deg").Value != 0 or fcObj.TaperAngleRev.getValueAs("deg").Value:
            return False
        
        #test base shape (only sketches are supported)
        if fcObj.Base.TypeId != "Sketcher::SketchObject":
            return False

        #test sketch
        if not self.isSketchSupported(fcObj.Base):
            return False

        return True

    def isSketchSupported(self, sketch):
        supportedGeometryTypes = [Part.LineSegment, Part.Circle, Part.Point, Part.ArcOfCircle]
        for line in sketch.Geometry:
            if not type(line) in supportedGeometryTypes and not line.Construction:
                return False

        return True

    def createMesh(self, fcObj, expPlacement, expPigment, expClose, expMeshDef): #create pov mesh from object
        povCode = ""

        if expMeshDef:
            mesh = 0

            if fcObj.isDerivedFrom("Mesh::Feature"): #is fcObj a mesh
                mesh = fcObj.Mesh
            else:
                try:
                    shape = fcObj.Shape.copy()
                    try:
                        angularDeflection = fcObj.ViewObject.AngularDeflection.getValueAs("rad").Value
                    except:
                        angularDeflection = 0.5
                    deviation = fcObj.ViewObject.Deviation

                    try:
                        mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=deviation, AngularDeflection=angularDeflection, Relative=False)
                    except:
                        mesh = MeshPart.meshFromShape(shape, deviation, angularDeflection)

                except:
                    return ""


            if not mesh or len(mesh.Topology[0]) == 0 or len(mesh.Topology[1]) == 0:
                #warningMessage = "\n\nNo mesh created - Object " + fcObj.Label + " won't be rendered"
                #App.Console.PrintWarning(warningMessage)
                return ""

            #create mesh2 object
            povMesh = "#declare " + stringCorrection(fcObj.Label) + "_mesh ="
            povMesh += "\nmesh2 {\n\tvertex_vectors {\n"

            #create vertex_vectors
            numOfVertex = len(mesh.Topology[0])
            povMesh += "\t\t" + str(numOfVertex)

            for point in mesh.Topology[0]:
                povMesh += ",\n\t\t<" + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + ">"
            povMesh += "\n\t}\n\n"

            #create face_indices
            povMesh += "\tface_indices {\n"
            numOfTriangles = len(mesh.Topology[1])
            povMesh += "\t\t" + str(numOfTriangles)

            for triangle in mesh.Topology[1]:
                povMesh += ",\n\t\t<" + str(triangle[0]) + ", " + str(triangle[1]) + ", " + str(triangle[2]) + ">"
            povMesh += "\n\t}\n\n"

            #add inside vector
            povMesh += "\tinside_vector <1, 1, 1>\n"

            povMesh += "}\n\n"

            #write mesh in inc file
            self.meshFileContent += povMesh

        #return pov code
        povCode += "\nobject { " + stringCorrection(fcObj.Label) + "_mesh\n"
        pigment = self.getPigment(fcObj)

        if expPlacement == False: #meshes are already translated, so if they shouldnt translated, they translated back
            translation = self.getTranslation(fcObj)
            if translation != "": #test if the object is translated
                povCode += "\t" + translation + " * (-1)\n"
            
            rotation = self.getInvertedRotation(fcObj)
            if rotation != "": #test if the object is rotated
                povCode += rotation.replace("\n", "\t\n")

        if pigment != "": #test if the object has the standard pigment
            povCode += "\t" + pigment + "\n"

        if expClose:
            povCode += "}\n"

        return povCode


    def getStatistics(self, objs): #get statistics about the model the user want to render
        statistics = ""
        noCsgCount = 0
        CsgCount = 0
        ParentCount = 0
        supportedTypeIds = ["Part::Sphere",
                            "Part::Box",
                            "Part::Torus",
                            "Part::Cylinder",
                            "Part::Cone",
                            "Part::Ellipsoid",
                            "Part::Plane",
                            "Part::Cut",
                            "Part::MultiFuse", "Part::Fuse",
                            "Part::MultiCommon", "Part::Common",
                            "Part::Extrusion",
                            "PartDesign::Body"
                            "PartDesign::Pad",
                            "PartDesign::Pocket",
                            "Sketcher::SketchObject",
                            "App::DocumentObjectGroup",
                            "App:Part",
                            "Part::Compound",
                            "Image::ImagePlane"]
        supportedNames = ["Array", "Clone", "PointLight", "AreaLight", "SpotLight"]

        for obj in objs:
            if not obj.TypeId in supportedTypeIds and not self.isNameSupported(obj.Name, supportedNames):
                noCsgCount = noCsgCount + 1
            else:
                CsgCount = CsgCount + 1
            if obj.InList == []:
                ParentCount = ParentCount + 1

        statistics += "Path to *.pov File: " + self.povPath + "\n"
        statistics += str(ParentCount) + " parent objects found in highest layer\n"
        statistics += "containing totally " + str(CsgCount + noCsgCount) + " objects\n"
        if noCsgCount != 0:
            statistics += "Your model contains " + str(noCsgCount) + " objects which aren't supported (will be represented as mesh).\n"

        if self.CamType == "Perspective":
            camInfo = "Perspective Camera\n"
        elif self.CamType == "Orthographic":
            camInfo = "Orthographic camera\n"
        else:
            camInfo = "Unknown camera type - rudimentary camera statement will be used\n"
        if self.incContent.find("camera") != -1:
            camInfo = "User defined camera found - FreeCAD camera will be commented out in *.pov file\n"

        statistics += camInfo
        statistics += "\n"

        return statistics

    def getFCLight(self): #get the FreeCAD light
        povLight = ""

        povLight += "light_source { CamPosition color rgb <0.5, 0.5, 0.5> }\n"

        return povLight

    def getBackground(self): #get the FreeCAD background
        bgColor1 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor')
        bgColor2 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor2')
        bgColor3 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor3')
        bgColor4 = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned('BackgroundColor4')
        ViewDir = Gui.ActiveDocument.ActiveView.getViewDirection()

        AspectRatio = self.width / float(self.height)
        povBg = ""

        if self.CamType == "Orthographic":
            if AspectRatio >= 1:
                up = self.CamNode.height.getValue()
                right = up * AspectRatio
            else:
                right = self.CamNode.height.getValue()
                up = right/AspectRatio
            povBg += "\npolygon {\n"
            povBg += "\t5, <" + str(-right/2) + ", " + str(-up/2) + ">, <" + str(-right/2) + ", "
            povBg += str(up/2) + ">, <" + str(right/2) + ", " + str(up/2) + ">, <" + str(right/2) + ", " + str(-up/2)
            povBg += ">, <" + str(-right/2) + ", " + str(-up/2) + ">\n"
            povBg += "\tpigment {"
            if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Simple'):
                povBg += " color rgb" + self.uintColorToRGB(bgColor1) + " }\n"
            elif App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Gradient'):
                povBg += "\n\t\tgradient y\n"
                povBg += "\t\tcolor_map {\n"
                povBg += "\t\t\t[ 0.00  color rgb" + self.uintColorToRGB(bgColor3) +" ]\n"
                povBg += "\t\t\t[ 0.05  color rgb" + self.uintColorToRGB(bgColor3) +" ]\n"
                if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('UseBackgroundColorMid'):
                    povBg += "\t\t\t[ 0.50  color rgb" + self.uintColorToRGB(bgColor4) +" ]\n"
                povBg += "\t\t\t[ 0.95  color rgb" + self.uintColorToRGB(bgColor2) +" ]\n"
                povBg += "\t\t\t[ 1.00  color rgb" + self.uintColorToRGB(bgColor2) +" ]\n"
                povBg += "\t\t}\n"
                povBg += "\t\tscale <1," + str(up) + ",1>\n"
                povBg += "\t\ttranslate <0," + str(-up/2) + ",0>\n"
                povBg += "\t}\n"
            #color rgb<0,0,1>}\n"
            povBg += "\tfinish { ambient 1 diffuse 0 }\n"
            povBg += "\trotate <" + str(self.EulerCam[2]) + ", " + str(self.EulerCam[1]) + ", " + str(self.EulerCam[0]) + ">\n"
            povBg += "\ttranslate <" + str(self.CamPos.Base.x) + ", " + str(self.CamPos.Base.y) + ", " + str(self.CamPos.Base.z) + ">\n"
            povBg += "\ttranslate <" + str(ViewDir[0]*100000) + ", " + str(ViewDir[1]*100000) + ", " + str(ViewDir[2]*100000) + ">\n"
            povBg += "}\n"

        povBg += "sky_sphere {\n\tpigment {\n"
        if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Simple'):
            povBg += "\t\tcolor rgb" + self.uintColorToRGB(bgColor1) + "\n"

        elif App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('Gradient'):
            povBg += "\t\tgradient z\n"
            povBg += "\t\tcolor_map {\n"
            povBg += "\t\t\t[ 0.00  color rgb" + self.uintColorToRGB(bgColor3) +" ]\n"
            povBg += "\t\t\t[ 0.30  color rgb" + self.uintColorToRGB(bgColor3) +" ]\n"
            if App.ParamGet("User parameter:BaseApp/Preferences/View").GetBool('UseBackgroundColorMid'):
                povBg += "\t\t\t[ 0.50  color rgb" + self.uintColorToRGB(bgColor4) +" ]\n"
            povBg += "\t\t\t[ 0.70  color rgb" + self.uintColorToRGB(bgColor2) +" ]\n"
            povBg += "\t\t\t[ 1.00  color rgb" + self.uintColorToRGB(bgColor2) +" ]\n"
            povBg += "\t\t}\n"
            povBg += "\t\tscale 2\n"
            povBg += "\t\ttranslate -1\n"
            povBg += "\t\trotate<" + str(self.EulerCam[2]-90) + ", " + str(self.EulerCam[1]) + ", " + str(self.EulerCam[0]) + ">\n"
        povBg += "\t}\n}\n"

        return povBg

    def getCam(self): #get the FreeCAD camera
        AspectRatio = self.width / float(self.height)

        PovCam = ""
        incCamera = False

        PovCamType = ""
        PovCamAngle = ""
        PovCamUp = ""
        PovCamRight = ""

        if self.CamType == "Perspective":
            PovCamUp = "<0, 0, 1>"
            PovCamRight = "<" + "{0:1.2f}".format(AspectRatio) + ", 0, 0>"

            if AspectRatio <= 1:
                CamAngle = 45
            else:
                CamAngle = math.degrees(math.atan2(AspectRatio/2, 1.2071067812))*2
            PovCamAngle = "\tangle {0:1.2f}".format(CamAngle) + "\n"

        elif self.CamType == "Orthographic":
            if AspectRatio >= 1:
                up = up = self.CamNode.height.getValue()
                right = up*AspectRatio
            else:
                right = self.CamNode.height.getValue()
                up = right/AspectRatio
            PovCamType = "\torthographic\n"
            PovCamUp = "< 0, 0, " + "{0:1.2f}".format(up) + ">"
            PovCamRight = "<" + "{0:1.2f}".format(right) +", 0, 0>"

        PovCam += "#declare CamUp = " + PovCamUp + ";\n"
        PovCam += "#declare CamRight = " + PovCamRight + ";\n"
        PovCam += "#declare CamRotation = <" + str(self.EulerCam[2]-90) + ", " + str(self.EulerCam[1]) + ", " + str(self.EulerCam[0]) + ">;\n"
        PovCam += "#declare CamPosition = <" + str(self.CamPos.Base.x) + ", " + str(self.CamPos.Base.y) + ", " + str(self.CamPos.Base.z) + ">;\n"

        if self.incContent.find("camera") != -1:
            incCamera = True
            PovCam += "/*"

        PovCam += "camera {\n"
        PovCam += PovCamType
        PovCam += "\tlocation <0, 0, 0>\n"
        PovCam += "\tdirection <0, 1, 0>\n"
        PovCam += "\tup CamUp\n"
        PovCam += "\tright CamRight\n"
        PovCam += "\trotate CamRotation\n"
        PovCam += "\ttranslate CamPosition\n"
        PovCam += PovCamAngle
        PovCam += "}\n"
        if incCamera:
            PovCam += "*/\n"

        return PovCam


    def getTranslation(self, fcObj): #get the translation of an object
        translation = ""
        x = fcObj.Placement.Base.x #get the position in every axis
        y = fcObj.Placement.Base.y
        z = fcObj.Placement.Base.z
        if x != 0 or y != 0 or z != 0: #test whether the position is 0,0,0
            translation += "translate <" + str(x) + ", " + str(y) + ", " + str(z) + ">" #create translation vector

        return translation

    def getRotation(self, fcObj): #get the rotation of an object
        rotate = ""
        eulerRot = fcObj.Placement.Rotation.toEuler() #convert the rotation to euler angles
        x = eulerRot[2] #get rotation in every axis
        y = eulerRot[1]
        z = eulerRot[0]

        #if fcObj is a torus it is necessary to rotate it in x axis
        if fcObj.TypeId == "Part::Torus" or (fcObj.Name.startswith("Clone") and fcObj.OutList[0].TypeId == "Part::Torus"):
            x += 90
        elif fcObj.TypeId == "Sketcher::SketchObject":
            x -= 90

        if x != 0 or y != 0 or z != 0:
            rotate = "rotate <" + str(x) + ", " + str(y)+ ", "  + str(z) + ">" #create roation vector

        return rotate

    def getInvertedRotation(self, fcObj):
        rotate = ""
        eulerRot = fcObj.Placement.Rotation.toEuler() #convert the rotation to euler angles
        x = eulerRot[2] #get rotation in every axis
        y = eulerRot[1]
        z = eulerRot[0]

        #if fcObj is a torus it is necessary to rotate it in x axis
        if fcObj.TypeId == "Part::Torus" or (fcObj.Name.startswith("Clone") and fcObj.OutList[0].TypeId == "Part::Torus"):
            x += 90
        elif fcObj.TypeId == "Sketcher::SketchObject":
            x -= 90

        rotate = "\n"

        if z != 0:
            rotate += "rotate <0, 0, " + str(-z) + ">\n"
        if y != 0:
            rotate += "rotate <0, " + str(-y) + ", 0>\n"
        if x != 0:
            rotate += "rotate <" + str(-x) + ", 0, 0>\n"

        return rotate

    def getPigment(self, fcObj): #get the pigment of an object
        appObject = fcObj.ViewObject
        material = ""
        pigment = ""
        transparency = ""
        finish = ""
        ambient = ""
        emission = ""
        phong = ""
        if appObject.Transparency != 0:
            transparency += " transmit " + str(appObject.Transparency / float(100))
        ShapeColorRGB = "<{0:1.3f}, {1:1.3f}, {2:1.3f}>".format(appObject.ShapeColor[0], appObject.ShapeColor[1], appObject.ShapeColor[2])
        if transparency != "" or ShapeColorRGB != self.uintColorToRGB(self.DefaultShapeColor):
            pigment += "\tpigment { color rgb " + ShapeColorRGB + transparency + " }\n"
        material += pigment
        if appObject.ShapeMaterial.AmbientColor != (0.20000000298023224, 0.20000000298023224, 0.20000000298023224, 0):
            ambient += "ambient rgb<"
            ambient += "{0:1.3f}, {1:1.3f}, {2:1.3f}".format(appObject.ShapeMaterial.AmbientColor[0],
                                                             appObject.ShapeMaterial.AmbientColor[1],
                                                             appObject.ShapeMaterial.AmbientColor[2])
            ambient += ">"
        if appObject.ShapeMaterial.EmissiveColor != (0, 0, 0, 0):
            emission += "emission rgb<"
            emission += "{0:1.3f}, {1:1.3f}, {2:1.3f}".format(appObject.ShapeMaterial.EmissiveColor[0],
                                                              appObject.ShapeMaterial.EmissiveColor[1],
                                                              appObject.ShapeMaterial.EmissiveColor[2])
            emission += ">"
        if appObject.ShapeMaterial.SpecularColor != (0, 0, 0, 0):
            phong += "phong "
            phong += "{0:1.2f}".format((appObject.ShapeMaterial.SpecularColor[0] +
                                        appObject.ShapeMaterial.SpecularColor[1] +
                                        appObject.ShapeMaterial.SpecularColor[2]) / 3)
            phong += " phong_size "
            phong += str(appObject.ShapeMaterial.Shininess * 50)
            phong += " "
        if ambient != "" or emission != "" or  phong != "":
            finish = "finish {"
            finish += "\n\t" + ambient
            finish += "\n\t" + emission
            finish += "\n\t" + phong
            finish += "\n}\n"
        material += finish

        if self.texIncContent.find("#declare " + stringCorrection(fcObj.Label) + "_material_hollow") != -1:
            material = "\nhollow\nmaterial {" + stringCorrection(fcObj.Label) + "_material_hollow }\n"
        
        elif self.texIncContent.find("#declare " + stringCorrection(fcObj.Label) + "_") != -1:
            if self.texIncContent.find("#declare " + stringCorrection(fcObj.Label) + "_material") != -1:
                material = "\nmaterial {" + stringCorrection(fcObj.Label) + "_material }\n"
            elif self.texIncContent.find("#declare " + stringCorrection(fcObj.Label) + "_texture") != -1:
                material = "\ntexture {" + stringCorrection(fcObj.Label) + "_texture }\n"
            elif self.texIncContent.find("#declare " + stringCorrection(fcObj.Label) + "_pigment") != -1:
                material = "\npigment {" + stringCorrection(fcObj.Label) + "_pigment }\n"
            else:
                return ""

        if self.incContent.find("#declare " + stringCorrection(fcObj.Label) + "_material") != -1:
            material = "\nmaterial {" + stringCorrection(fcObj.Label) + "_material }\n"
        
        
            
        return material

    
    def listObjectToPov(self, obj, label=None):
        if label == None:
            label = obj.label

        if obj.predefObject.material == None: #for FreeCAD materials
            return "" #texture will be applied in the exporter class

        povContent = ""

        if obj.predefObject.inc != None and obj.predefObject.inc != "": #only if include file is necessary
            povContent += "#include \"" + obj.predefObject.inc + "\"\n"

        povContent += "#declare " + label + "_material"
        if obj.predefObject.media != "":
            povContent += "_hollow"
        povContent += " = material { "
        
        povContent += obj.predefObject.material + "\n"

        #pigment and texture
        if obj.predefObject.texture != "" or obj.predefObject.pigment != "" or obj.predefObject.normal != "" or obj.predefObject.finish != "":
            povContent += "\ttexture { " + obj.predefObject.texture + "\n"
            
            #pigment
            if obj.predefObject.pigment != "":
                povContent += "\t\tpigment { " + obj.predefObject.pigment + " }\n"

            #finish
            if obj.predefObject.finish != "":
                povContent += "\tfinish {\n\t" + obj.predefObject.finish + "\t}\n"

            #normal
            if obj.predefObject.normal != "":
                povContent += "\tnormal {\n\t" + obj.predefObject.normal + "\t}\n"

            povContent += "\t}\n"

        #interior and media
        if obj.predefObject.interior != "" or obj.predefObject.media != "":
            povContent += "\tinterior {\n\t" + obj.predefObject.interior + "\n"
            
            #media
            if obj.predefObject.media != "":
                povContent += "\t\tmedia { " + obj.predefObject.media + " }\n"
            
            povContent += "\t}\n"

        #scale
        if obj.scaleX != 1 or obj.scaleY != 1 or obj.scaleZ != 1:
            povContent += "\tscale <" + str(obj.scaleX) + ", " + str(obj.scaleY) + ", " + str(obj.scaleZ) + ">\n"
        #rotate
        if obj.rotationX != 0 or obj.rotationY != 0 or obj.rotationZ != 0:
            povContent += "\trotate <" + str(obj.rotationX) + ", " + str(obj.rotationY) + ", " + str(obj.rotationZ) + ">\n"
        #translate
        if obj.translationX != 0 or obj.translationY != 0 or obj.translationZ != 0:
            povContent += "\ttranslate <" + str(obj.translationX) + ", " + str(obj.translationY) + ", " + str(obj.translationZ) + ">\n"

        povContent += "}\n\n"

        if platform.system() == "Windows":
            povContent.replace("\n", "\r\n")

        return povContent

    def writeFile(self, povText): #write the final pov file
        #povText: the code for POV-Ray
        try:
            file = open(self.povPath, "w+") #XXX open file (Really "w+"?)
            file.write(povText) #write code
            file.close() #close file
        except:
            return -1

    def openPovRay(self): #start POV-Ray
        povExec = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing").GetString('PovrayExecutable')
        if os.path.isfile(povExec) == False:
            povExec = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Render").GetString('PovrayExecutable')
            if os.path.isfile(povExec) == False:
                errorText = "To start the rendering you must\n"
                errorText += "set the path to the POV-Ray executable\n"
                errorText += "either in the settings of Render workbench\n"
                errorText += "or in the settings of Raytracing workbench\n"
                showError(errorText, "POV-Ray executable not found")
                return -1
            povOptions = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Render").GetString('OutputParameters')
        povOptions = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Raytracing").GetString('OutputParameters')

        #create output directory
        os.chdir(str(self.directory))

        #write user options to ini file
        iniHandler = open(self.iniPath, "a")
        iniHandler.write("\n;User Options from FreeCAD Settings\n" + povOptions)
        iniHandler.close()

        #start povray
        subprocess.call([povExec, self.iniName])

        self.checkErrFile()

    def checkErrFile(self): #check error file for errors
        error = ""
        #open error file
        if os.path.isfile(self.errorPath) == True:
            file = open(self.errorPath, "r")
            #read error file
            error = file.read()
            file.close()
        #is there any content in the file
        if error != "": #error occured
            #show error message
            errorText = ""
            errorText += "An error occured while rendering:\n-----------------------------------------\n"
            errorText += error
            errorText += "\n-----------------------------------------\n"
            errorText += "If the error occured in the pov file or the mesh file, please report a bug to us."
            errorText += "(See the wiki, link is in the help tab of the dialog)\n\n"
            errorText += "You can see the error message in the error file too."
            showError(errorText, "An error ocurred while rendering")
        else:
            self.delErrorFile()

    def delErrorFile(self): #delete error file
        os.remove(self.errorPath)

    def repairRotation(self, objs): #repair the rotation of objects (likely a bug in FreeCAD)
        for obj in objs:
            if hasattr(obj, 'Placement'):
                ObjLocation = obj.Placement
                posX = ObjLocation.Base.x
                posY = ObjLocation.Base.y
                posZ = ObjLocation.Base.z
                rotX = ObjLocation.Rotation.Axis[0]
                rotY = ObjLocation.Rotation.Axis[1]
                rotZ = ObjLocation.Rotation.Axis[2]
                rotAngle = math.degrees(ObjLocation.Rotation.Angle)
                obj.Placement = App.Placement(App.Vector(posX, posY, posZ), App.Rotation(App.Vector(rotX, rotY, rotZ), rotAngle), App.Vector(0, 0, 0))

    def exportFcView(self): #export the current FreeCAD view like Tools / Save Picture...
        Gui.ActiveDocument.ActiveView.saveImage(self.fcViewPath, self.width, self.height)

    def hasPartAsParent(self, fcObj):
        for parent in fcObj.InList:
            if parent.TypeId == "App::Part":
                return True

        return False

    def hasBodyAsParent(self, fcObj):
        for parent in fcObj.InList:
            if parent.TypeId == "PartDesign::Body":
                return True

        return False

    def uintColorToRGB(self, uintColor): #convert uint color to a rgb color
        Blue = (uintColor >> 8) & 255
        Green = (uintColor >> 16) & 255
        Red = (uintColor >> 24) & 255
        rgbString = "<{0:1.3f}, {1:1.3f}, {2:1.3f}>".format(Red / float(255), Green / float(255), Blue / float(255))
        return rgbString

    def delComments(self, code): #delete the comments in incContent
        #delete big comments
        while code.find("/*") is not -1:
            comStart = code.find("/*")
            comEnd = code.find("*/", comStart + 2)

            if comEnd is -1:
                App.Console.PrintError("Unable to delete all comments in the inc file!\nThere is an unclosed multi line comment.\n")
                return
            code = code[0:comStart] + code[comEnd + 2:]

        #delete little comments
        while code.find("//") is not -1:
            comStart = code.find("//")
            comEnd = code.find("\n", comStart + 2)

            if comEnd is -1:
                App.Console.PrintError("Unable to delete all comments in the inc file!\nThere is a misstake in a one line comment")
                return
            code = code[0:comStart] + code[comEnd:]
        return code

    def isNameSupported(self, objName, supportedNames): #is fcObj.Name part of the supported names
        for name in supportedNames:
            if objName.startswith(name):
                return True

        return False
