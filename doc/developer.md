# Developer Documentation
## Skeletal structure of the macro
The macro works in this order:
1. Create the skeletal structure of the POVray file
1. Ask for the file and try if the pov and inc file exists
1. Add [global settings](#globalsettings) to the .pov file
1. Add the [camera](#camera)
1. Add the [lightsource](#lightsource)
1. Add the [background](#background)
1. Add the [objects from the scene](#objectsFromScene)
2. transform the object
2. add texture properties from FreeCAD or user declaration from .inc file
1. Write the pov file
1. Start POVray

## General
* The macro uses a right handed koordinate system like FreeCAD (specified in [camera](#camera))

<a name="globalsettings"></a>
## Global settings
First some global settings are added to the .pov file.
The important one is the standard object color from the settings dialog.
In objects with standard color and texture the `getPigment()` function will skip color and finish declaration of the pov object. 

<a name="camera"></a>
## Camera
The idea for creation of the camera is to create a camera at <0, 0, 0> and translate and rotate them into the right position.

<a name="lightsource"></a>
## Lightsource
The lightsource position is the same as the camera position

<a name="background"></a>
## Background
All FreeCAD background color modes from the settings dialog are supported.
The color(s) are mapped on the POV-Ray sky-sphere and afterwards the skysphere is rotated in the camera direction to fit the horizon

<a name="objectsFromScene"></a>
## Objects from Scene
First the macro gets the `firstLayer`, the highest level in the tree view in FreeCAD. The macro calls and recursive function `createPovrayCode()` which creates the real POVray code. The `main()` function calls it for every object in the `firstLayer`. `createPovrayCode()` calls itself for every child, so a recursive function.

### createPovrayCode()
