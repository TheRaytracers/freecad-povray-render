# Developer Documentation

## The Goal of the Project

The ExportToPovRay workbench is intended to export as many solid CSG objects as possible from the FreeCAD object tree with its
Boolean operations into a corresponding POV-Ray scene description file.
The user should be able to render realistic scenes by easy adding of textures und lights.
Because of the unnumbered POV-Ray features that would be hard to implement there should be a kind of backdor to make them accessible. 

The main principle is to keep the POV-Ray file as clear as possible, so that objects can be found quickly.
A second important principle is WYSIWYG (**W**hat **Y**ou **S**ee **I**s **W**hat **Y**ou **G**et).
So without textures the render result of POV-Ray should look the same as in FreeCAD view
(camera perspective, background, object colors...).  

Since a complete transfer of all FreeCAD construction possibilities would be too complex, the workbench should initially be focused on CSG objects -
This limitation should be clearly comprehensible for the user for example through a good documentation.

## Working on the code is not the only way to contribute

The documentation is not less important than the code! If you found a thing, which can be improved, clone this repository, do and commit you changes and make a pull request.

But it is not necessary to edit files, make a pull request and so on. If you found an bug and report it, that is contributing too! An improvement suggestion is also a contribution to the macro.
And often forgotten: If someone has a problem and ask in the forum and you help to solve the problem, you contributed!

You see, contribution to a project is not only possible with coding skills. Anything that advances our macro in any way is a contribution.

**Without your reports, ideas, etc. the macro won't get better or only very slow. So report all, that comes to your mind.**

Before you create a new issue, please read the [Issue Guidelines](https://gitlab.com/usbhub/exporttopovray/issues/26).

## Contribute to the Code

### Skeletal structure of the workbench

The macro works in this order:

1. Open the dialog and get the parameters from the user
2. Create the skeletal structure of the POV-Ray file
3. Try whether the pov and inc file exists
4. Add [global settings](#global-settings) to the .pov file
5. Add the [camera](#camera)
6. Add the [light source](#light-source)
7. Add the [background](#background)
8. Add the [objects from the scene](#objects-from-scene)
   1. create the basing object
   2. rotate the object
   3. transform the object
   4. add texture properties from FreeCAD or user declaration from .inc file
9. Write the pov file
10. Start POV-Ray

Here's a flowchart of the rough **program structure** (if you need a higher resolution, in the doc/img folder is an additional pdf file of this chart):
![Flowchart of the macro](/doc/img/Workbench%20Structure.png)

## General Characteristics

* The macro uses a right handed coordinate system like FreeCAD (specified in [However, this limitation is clearly comprehensible for the user - either
through a good documentation or in the program e.g. through colored
selection of transferred objects in the object tree.camera](#camera))
* All objects are created at <0, 0, 0> and translated later to the right position (see [Characteristics](#general-characteristics))

## Global settings

First, some general settings are added to the .pov file.
The important one is the standard object color from the settings dialog.
In objects with standard color and texture the `getPigment()` function will skip color and finish declaration of the pov object.

## Camera

The idea for creation of the camera is to create a camera at <0, 0, 0> and translate and rotate them into the right position.
global

## Light source

The light source position is the same as the camera position.

## Background

All FreeCAD background color modes from the settings dialog are supported.
The color(s) are mapped on the POV-Ray sky-sphere and afterwards the skysphere is rotated in the camera direction to fit to the horizon.

## Objects from Scene

First the macro gets the `firstLayer`, the highest level in the tree view in FreeCAD. The macro calls and recursive function `createPovCode()` which creates the real POV-Ray code. The `main()` function calls it for every object in the `firstLayer`. `createPovCode()` calls itself for every child, so a recursive function.

### Object transformation

The macro creates all objects at <0, 0, 0> and translates the objects later. The reason for that is, that POV-Ray rotates an object independently from its position around <0, 0, 0>, FreeCAD rotates relative to the object.

### `createPovCode()`

1. The variable povCode will be initialized with the label / name of the object.
2. Add the basing POV-Ray object to povCode but don't close the object
3. Add the rotation to the POV-Ray object
4. Add the translation to the POV-Ray object
5. Add the look to the POV-Ray object
6. Close the POV-Ray object by adding `}`
7. Return the created code
