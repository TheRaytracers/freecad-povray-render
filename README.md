# Macro for exporting a FreeCAD model to Pov-Ray

**This macro exports your FreeCAD model to Pov-Ray and is very easy to use, also for absolute beginners in the rendering of images. But advanced users have also the full control about the process & settings and can use all Pov-Ray features.**

![Rendering Example](/doc/img/Chess/Chess_08.png)

The export macro is intended to export the FreeCAD model structure with their equivalent in Pov-Ray.
In contrast to other solutions for exporting FreeCAD models to Pov-Ray, this macro tries to make the file clearly and easy to edit. For that, it doesn't create gigantic meshes, it moves the tree structure with the boolean operations into a Pov-Ray file.  
Until now, the macro only supports objects from the Part Workbench, other objects are simulated with meshes (see [Supported Objects](#supportedObjects)).

To give the user the full control, you can define extra things or another surface as in FreeCAD (Please visit the [Wiki](doc/user.md) for more information).


## Installation
Download the macro here: [link] or install it via the addon manager  
Now you have to put the .FCMacro file in your macro directory. You cant look under Edit / Preferences / General for your path.
### Standard Macro Paths
* Linux: `/home/USERNAME/.FreeCAD/Macro/`  
* Windows: `C:\Users\USERNAME\AppData\Roaming\FreeCAD\Macro/`
* Mac: `XXX`

## Usage
The macro takes your actual view on the model, so pan your view how you would like the rendering. Now you can [Start the Macro](#startTheMacro). After that, select / create the file where you want to save the Pov-Ray code. Now the macro creates the Pov-Ray code and start the Pov-Ray. If you have many no CSG object the creation of the code can take a while. Pov-Ray opens a windows with the rendering result. To close this window, click on the windows.

<a name="startTheMacro"></a>
### Start the Macro
Go to Macro/Macros… and start the installed macro by double clicking on it.

### More Features
The macro supports a lot more. Please visit our [wiki for users](doc/user.md) for further information about features like using all Pov-Ray features or creating custom materials.

<a name="supportedObjects"></a>
## Supported Objects
The macro simulates objects which aren't supported already with a mesh. The meshes are in an extra file with the name `name_meshes.inc`. But doubt, that the creation of a mesh needs a lot of cpu time.


### Part Workbench
- [x] Cube
- [x] Cylinder
- [x] Sphere
- [x] Cone
- [x] Torus
- [x] Ellipsoid
- [x] Plane
- [ ] Wedge
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

## Advantages over the Raytracing Workbench
* You can use **all** POV-Ray features
* Easy changing of materials / textures of objects
  - If you edit a material in the pov file of the Raytracing Workbench and change the model later, you have to do all changes in the file again. With the macro you don't have to do that (define all changes in the inc file).
* The macro is easier to use
* WYSIWYG
* The macro is written in Python, so it is easier for extending
* The macro takes more object properties than the workbench
* The macro reproduces the tree structure and doesn't create gigantic meshs
  * → Better understanding & editing of the file
  * → Better performance
  * → Better renderings

## FAQ
We created a little FAQ for you: [FAQ](doc/FAQ.md)

## Wiki
For the full documentation, please visit our [Wiki](doc/index.md)

## Contributing
You want to contribute? Thank you, please look to our [wiki for developers](doc/developer.md).
