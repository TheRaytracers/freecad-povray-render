# Developer Documentation

## The Goal of the Project
The ExportToPovRay macro is intended to export as many solid CSG objects as possible from the FreeCAD Part workbench into a corresponding Pov-Ray.
Convert scene description. The object tree with its
Boolean operations in the Pov-Ray file.  
The user should be able to modify the Pov-Ray file so that the
extensive possibilities of Pov-Ray for a photorealistic display
can be used (textures, light effects, etc.)  
The main principle is to keep the POV-Ray file as clear as possible,
so that objects can be found quickly.
A second important principle is WYSIWYG (**W**hat **Y**ou **S**ee **I**s **W**hat **Y**ou **G**et).
The render result of the respective view in FreeCAD Gui looks like this
as possible (camera perspective, background, object colors…).  

Since a complete transfer of all FreeCAD construction possibilities
would be too complex, the macro is initially limited to CSG objects -
However, this limitation is clearly comprehensible for the user - either through a good documentation or in the program e.g. through colored
selection of transferred objects in the object tree.

# You cannot only contribute to the code
The documentation is not less important than the code! If you found a thing, which can be improved, clone this repository, do and commit you changes and make a pull request.

But it is not necessary to edit files, make a pull request and so on. If you found an bug and report it, that is contributing too! An improvement suggestion is also a contribution to the macro.
And often forgotten: If someone has a problem and ask in the forum and you help to solve the problem, you contributed!

You see, contribution to a project is not only possible with coding skills. Anything that advances our macro in any way is a contribution.

**Without your reports, ideas, etc. the macro won't get better or only very slow. So report all, that comes to your mind.**

Before you create a new issue, please read the [Issue Guidelines](https://gitlab.com/usbhub/exporttopovray/issues/26).

# Contribute to the Code
## Skeletal structure of the macro
The macro works in this order:
1. Open the dialog and get the parameters from the user
1. Create the skeletal structure of the POV-Ray file
1. Try whether the pov and inc file exists
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
1. Start POV-Ray

## General Characteristics
* The macro uses a right handed koordinate system like FreeCAD (specified in [However, this limitation is clearly comprehensible for the user - either
through a good documentation or in the program e.g. through colored
selection of transferred objects in the object tree.camera](#camera))
* All objects are created at <0, 0, 0> and translated later to the right position (see [Characteristics](#characteristics))

<a name="generalsettings"></a>
## General settings
First, some general settings are added to the .pov file.
The important one is the standard object color from the settings dialog.
In objects with standard color and texture the `getPigment()` function will skip color and finish declaration of the pov object.

<a name="camera"></a>
## Camera
The idea for creation of the camera is to create a camera at <0, 0, 0> and translate and rotate them into the right position.
global
<a name="lightsource"></a>
## Lightsource
The lightsource position is the same as the camera position.

<a name="background"></a>
## Background
All FreeCAD background color modes from the settings dialog are supported.
The color(s) are mapped on the POV-Ray sky-sphere and afterwards the skysphere is rotated in the camera direction to fit to the horizon.

<a name="objectsFromScene"></a>
## Objects from Scene
First the macro gets the `firstLayer`, the highest level in the tree view in FreeCAD. The macro calls and recursive function `createPovrayCode()` which creates the real POV-Ray code. The `main()` function calls it for every object in the `firstLayer`. `createPovrayCode()` calls itself for every child, so a recursive function.

<a name="characteristics"></a>
### Characteristics
The macro creates all objects at <0, 0, 0> and translates the objects later. The reason for that is, that POV-Ray rotates an object independently of the position of it <0, 0, 0>, FreeCAD rotates relative to the object.

### createPovrayCode()
1. The variable povCode will be initialised with the label / name of the object.
1. Add the basing POV-Ray object to povCode but don't close the object
1. Add the rotation to the POV-Ray object
1. Add the translation to the POV-Ray object
1. Add the look to the POV-Ray object
1. Close the POV-Ray object by adding `}`
1. Return the created code
