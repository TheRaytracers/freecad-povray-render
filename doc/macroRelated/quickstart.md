# Quick start

## Installation of the macro

The easiest way is to install it via the **Addon Manager** under Tools / Addon Manager / Macros.  
Alternative you can download the macro via [Macro Recipes](https://freecadweb.org/wiki/Macros_recipes) or download it directly from our [Gitlab Repository](https://gitlab.com/usbhub/exporttopovray) with the right button about the last commit message to get the most actual version.  
Now you have to put the .FCMacro file in your macro directory. You can look under Edit / Preferences / General / Macro for your path. It is important, that you don't have the .FCMacro in an extra folder, it have to be directly in the macro directory.

**Right (Example):**
`/home/usbhub/.FreeCAD/Macro/ExportToPovRay.FCMacro`  
**False (Example):**
`/home/usbhub/.FreeCAD/Macro/RenderMacro/ExportToPovRay.FCMacro`

## Installation of POV-Ray

* Linux - we recommend the installation with the Application Manager
* Windows - Get the Windows installer from the [POV-Ray website](http://www.povray.org/download/)

## POV-Ray executable Path and options

The macro must know how to find the POV-Ray executable. The path will be taken from the settings of either the raytracing workbench or the render workbench.
To reach the raytracing settings menu you must load the raytracing workbench first and second go to the settings menu.
The name of the POV-Ray executable is different in Windows and Linux:

* `povray` (Linux)
* `pvengine.exe` (Windows)

It is important to write the complete path into the textfield.
These are the standard paths but they may vary depending on your installation:

* `/usr/bin/povray` (Linux)
* `XXX` (Windows)

For the executable options in the next field you should take

* `+P +A`

`+P` causes POV-Ray to show the rendered image.
`+A` is for Antialiasing - this is optional.

For Windows the following options can be useful:

* `/EXIT +P +A`

because without the `/EXIT` otion you have to close three windows after rendering  
(terminal, POV-Ray Editor Window and the rendered image)

If the raytracing workbench works with these settings, the macro should do also.

## Usage

### How to get your first result

1. Open a document or create a new one with some objects
2. Pan the model in the right view
3. Start the macro about Macro / Macros... / ExportToPovRay.FCMacro / Execute
4. Click on "Browse .pov Output File"
5. Select / create a file with the ending .pov
6. Click on Save in the file dialog
7. Change the width of the picture to 800px and the height to 600px
8. Turn on the options
   * [x] Export FreeCAD Background
   * [x] Export FreeCAD Light
9. Click on OK
10. A window pops up with your rendering
11. Close the window by clicking on it

To understand all options, take a closer look to the wiki or look at the help tab.

## Make changes

To use the full power of POV-Ray you can add textures, lights, athmosperic effects and many more to your model.
For this you have to create an include file manually with the same name as the pov file in directory of your pov file. Change the extension to `.inc`.  
For example

```pov
pov file: myPOV-RayFile.pov
inc file: myPOV-RayFile.inc
```

You should define all additional features in the include file. It will not be overwritten by the macro.

### Add textures and material

Be aware to use the right syntax if you want to define a texture for a specific object.  
For example if you want to add the material `M_Glass3` to an object, labeled with `White_pieces` in the object tree,

![Object Tree]( ./img/ObjectTree.png "ObjectTree")

you have to type this in your inc file:

```pov
#declare White_pieces_material = material { M_Glass3 }
```

It is also important to take care of the [material hierarchy](materialHierarchy.md) because otherwise POV-Ray will abort the rendering with an error message

### Add objects

If you want to add POV-Ray objects (e.g. another lamp, a special background or any other object) you can do this also with the .inc file. Just add the POV-Ray object to the .inc file and restart the macro. Now POV-Ray also renders your own object which is defined in the inc file.  
The macro will comment out the camera if you define your own.
FreeCAD light and background can be switched off in the dialog box if you define your own one.

### Change global settings

There are several ways to influence the way and quality of rendering.
For example you can add a global ambient light:

```pov
global_settings { ambient_light rgb<1, 0, 0> }
```

or if you want to use [radiosity](https://en.wikipedia.org/wiki/Radiosity_(computer_graphics)) in your rendering, you can add this information in the inc file.  

```pov
#include "rad_def.inc"
global_settings {
   radiosity {
      Rad_Settings(MODE, off, off)
   }
}
```

Replace MODE with the one of the modes described in [POV-Ray wiki](http://wiki.povray.org/content/HowTo:Use_radiosity).
