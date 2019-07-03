# User Documentation
## Installation
Download the macro here: [link] or install it via the addon manager  
Now you have to put the .FCMacro file in your macro directory. You cant look under Edit / Preferences / General for your path.
### Standard Macro Paths 
* Linux: `/home/USERNAME/.FreeCAD/Macro/`  
* Windows: `C:\Users\otto\AppData\Roaming\FreeCAD\Macro/`
* Mac: `XXX`

## Use the Macro
The macro takes your actual view on the model, so pan your view how you would like the rendering. Now you can [Start the Macro](#startTheMacro). After that, select / create the file where you want to save the POVray code. Now the macro creates the POVray code and start the POVray. POVray opens a windows with the rendering result. To close this window, click on the windows.

### Tips & Tricks
* If you create a cut with two touching surfaces in FreeCAD, nothing remains. With POVray, however, an infinitely thin layer remains:
![FreeCAD before cutting](img/tipsAndTricks/01_FC.png "FreeCAD before cutting")
![POVray before cutting](img/tipsAndTricks/01_PR.png "POVray before cutting")
![FreeCAD after cutting](img/tipsAndTricks/02_FC.png "FreeCAD after cutting")
![POVray after cutting](img/tipsAndTricks/02_PR.png "POVray after cutting")
To avoid this, the part to be removed should be slightly larger than the other part.

## Make changes
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

### Add objects
If you want to add POVray objects (e.g. a second lamp or a super torus) you can do this also with the inc file. Just add the POVray object to the inc file and restart the macro. Now POVray also renders your own object which is defined in the inc file.  
The macro will comment out the camera / light source if you defined another in the inc file.

<a name="startTheMacro"></a>
## Start the Macro
Go to Macro/Macros… and start the installed macro by double clicking on it.

## Supported Objects
### Part Workbench
- [x] Cube
- [x] Cylinder
- [x] Sphere
- [x] Cone
- [x] Torus
- [x] Ellipsoid
- [ ] Wedge
- [ ] Plane
- [ ] Prism

The macro doesn't support AngleN (Angle, Angle1, Angle2, etc.) for cylinder, sphere, cone, torus and ellipsoid

### Other
- [x] Color
- [x] Background (you can change the background under Edit/Preferences/Display/Colors/Background Color)
- [x] Transparency
- [x] AmbientColor
- [x] EmissiveColor
- [x] SpecularColor
- [x] Shininess
