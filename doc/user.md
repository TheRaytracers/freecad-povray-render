# User Documentation
## Installation
Download the macro here: [link]  
Now you have to put the .FCMacro file in your macro directory. You cant look under Edit / Preferences / General for your path. Under Linux you have often this path:  
`/home/USERNAME/.FreeCAD/Macro/`  

## Use the Macro
The macro takes your actual view on the model, so pan your view how you would like the rendering. Now you can [Start the Macro](#startTheMacro). After that, select / create the file where you want to save the POVray code. Now the macro creates the POVray code and start the POVray. POVray opens a windows with the rendering result. To close this window, click on the windows.

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
