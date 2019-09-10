# User Documentation
## Installation of the macro
The easiest way is to install it via the **Addon Manager** under Tools / Addon Manager / Macros.  
Alternative you can download the macro via [Macro Recipes](https://freecadweb.org/wiki/Macros_recipes) or download it directly from our [Gitlab Repository](https://gitlab.com/usbhub/exporttopovray) with the blue button top right to get the most actual version.  
Now you have to put the .FCMacro file in your macro directory. You cant look under Edit / Preferences / General / Macro for your path.
### Standard Macro Paths
* Linux: `/home/USERNAME/.FreeCAD/Macro/`  
* Windows: `C:\Users\USERNAME\AppData\Roaming\FreeCAD\Macro/`
* Mac: `XXX`

## Installation of POV-Ray

## Usage
Create a model with the part workbench.
The macro takes your actual view on the model, so pan your view how you would like the rendering. Now you can [Start the Macro](#startTheMacro). After that, select / create the file where you want to save the POVray code. Now the macro creates the POVray code and start the POVray. If you have many no CSG object the creation of the code can take a while. POVray opens a windows with the rendering result. To close this window, click on the windows.

<a name="startTheMacro"></a>
### Start the Macro
Go to Macro/Macros… and start the installed macro by double clicking on it.

### Tips & Tricks
* You can change the background of FreeCAD under Edit/Preferences/Display/Colors/Background Color. You can also add a middle color.
* For side views, try the orthographic view. But for a non side view, don't use the orthographic view. That doesn't look realistic
* Try to get a more realistic image: [Rendering a photorealistic Scene - Step by Step](realistic.md)
* If you have a big scene with a lot of objects and many materials with light refraction, try a little size of the image first, because then you not must wait for a long time.
* If you create a cut with two touching surfaces in FreeCAD, nothing remains. With POVray, however, an infinitely thin layer remains:

  ![FreeCAD before cutting](img/touchingSurfaceFreeCAD.png")

  ![FreeCAD after cutting](img/touchingSurfacePovRay.png")

  To avoid this, the part to be removed should be slightly larger than the other part.


### Make changes
If you want to change the texture / pigment / finish / etc. you have to create a file with the same name as the pov file in directory of your pov file. Change the ending to `inc`. To example
```
pov file: myPOVrayFile.pov
inc file: myPOVrayFile.inc
```
There you can define changes for specific parts of your model. You have to use the following syntax:  
FreeCAD Tree View:
* `Cut001`
  * `Box001`
  * `Box002`
* `MySphere`  

If you want to change the material of `MySphere` to `M_Glass3` you have to type this in your inc file:

```
#declare MySphere_material = material { M_Glass3 }

```

If you want to change the texture of `Box001` to `White_Marble` you have to add this to the inc file:
```
#declare MySphere_material = material {
  texture {
    pigment{ White_Marble}
  }
}
```

#### Add objects
If you want to add POVray objects (e.g. another lamp or a super torus) you can do this also with the inc file. Just add the POVray object to the inc file and restart the macro. Now POVray also renders your own object which is defined in the inc file.  
The macro will comment out the camera / light source if you defined another in the inc file.

#### Use Radiosity
If you want to use [radiosity](https://en.wikipedia.org/wiki/Radiosity_(computer_graphics)) in your rendering, you have to add this information in the inc file.  
POVray knows many different modes:
* Radiosity_Default
* Radiosity_Debug
* Radiosity_Fast
* Radiosity_Normal
* Radiosity_2Bounce
* Radiosity_Final
* Radiosity_OutdoorLQ
* Radiosity_OutdoorHQ
* Radiosity_OutdoorLight
* Radiosity_IndoorLQ
* Radiosity_IndoorHQ

To use radiosity add these lines to your inc file:
```
#include "rad_def.inc"
global_settings {
   radiosity {
      Rad_Settings(MODE, off, off)
   }
}
```
Replace MODE with the one of the modes above.

For more information please visit the [POVray wiki](http://wiki.povray.org/content/HowTo:Use_radiosity).
