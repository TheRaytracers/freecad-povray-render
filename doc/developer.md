# Developer Documentation
## Skeletal structure of the macro
The macro works in this order:
1. Create the skeletal structure of the POVray file
1. Ask for the file and try if the pov and inc file exists
1. Add the [camera](#camera)
1. Add the [background](#background)
1. Add the [objects from the scene](#objectsFromScene)
1. Write the pov file
1. Start POVray

## General
* The macro uses a right handed koordinate system like FreeCAD (specified in [camera](#camera))

<a name="camera"></a>
## Camera
The idea for creation of the camera is to create a camera at <0, 0, 0> and translate and rotate them into the right position.

<a name="background"></a>
## Background
@DerUhrmacher Please add some information about the	principle of operation

<a name="objectsFromScene"></a>
## Objects from Scene
First the macro gets the `firstLayer`, the highest level in the tree view in FreeCAD. The macro calls and recursive function `createPovrayCode()` which creates the real POVray code. The `main()` function calls it for every object in the `firstLayer`. `createPovrayCode()` calls itself for every child, so a recursive function.

### createPovrayCode()
