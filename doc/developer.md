# Developer Documentation
## Skeletal structure of the macro
The macro works in this order:
1. Open the dialog and get the parameters from the user
1. Create the skeletal structure of the POVray file
1. Try if the pov and inc file exists
1. Add [global settings](#globalsettings) to the .pov file
1. Add the [camera](#camera)
1. Add the [lightsource](#lightsource)
1. Add the [background](#background)
1. Add the [objects from the scene](#objectsFromScene)
  1. create the basing object
  1. rotate the object
  1. transform the object
  1. add texture properties from FreeCAD or user declaration from .inc file
1. Write the pov file
1. Start POVray

## General Characteristics
* The macro uses a right handed koordinate system like FreeCAD (specified in [camera](#camera))
* All objects are created at <0, 0, 0> and translated later to the right position (see [Characteristics](#characteristics))

<a name="globalsettings"></a>
## Global settings
First, some global settings are added to the .pov file.
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
The color(s) are mapped on the POVray sky-sphere and afterwards the skysphere is rotated in the camera direction to fit the horizon

<a name="objectsFromScene"></a>
## Objects from Scene
First the macro gets the `firstLayer`, the highest level in the tree view in FreeCAD. The macro calls and recursive function `createPovrayCode()` which creates the real POVray code. The `main()` function calls it for every object in the `firstLayer`. `createPovrayCode()` calls itself for every child, so a recursive function.

<a name="characteristics"></a>
### Characteristics
The macro creates all objects at <0, 0, 0> and translates the object later. The reason for that is, that POVray rotates a object independent of the position around <0, 0, 0>, FreeCAD rotates relative to the object.

### createPovrayCode()
1. The variable povCode will initialised with the label / name of the object.
1. Add the basing POVray object to povCode but don't close the object
1. Add the rotation to the POVray object
1. Add the translation to the POVray object
1. Add the look to the POVray object
1. Close the POVray object by adding a `}`
1. Return the created code
