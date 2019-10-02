# Macro for exporting a FreeCAD model to Pov-Ray

**This macro exports your FreeCAD model to Pov-Ray and is very easy to use, also for absolute beginners in the rendering of images. But advanced users have also the full control about the process & settings and can use all Pov-Ray features.**

![Rendering Example](/doc/img/Chess/Chess_08.png)

The export macro is intended to export the FreeCAD model structure with their equivalent in Pov-Ray.
In contrast to other solutions for exporting FreeCAD models to Pov-Ray, this macro tries to make the file clearly and easy to edit. For that, it doesn't create gigantic meshes, it moves the tree structure with the boolean operations into a Pov-Ray file.  
Until now, the macro supports most objects from the Part Workbench and some features from the Part design and Draft workbench. Not supported objects are simulated with meshes (see [Supported Objects](#supportedObjects)).

To give the user the full control, you can define extra things or another surface as in FreeCAD (Please visit the [Wiki](doc/user.md) for more information).


## Content of wiki

* [Installation](doc/quickstart.md#Installation-of-POV-Ray)
* [Usage of macro](doc/quickstart.md#Usage)
* [Adding features like material and textures](doc/quickstart.md#Make-changes)
* [Tips, Tricks and limitations](doc/tipsAndTricks.md)
* [Realistic Rendering example](doc/realistic.md)
* [Supported Features](/doc/supported.md)
* [FAQ](doc/FAQ.md)
* [More examples and templates](Examples/index.md)
* [Contributing](doc/developer.md)
* [Future developement](doc/roadmap.md)

## Advantages compared with the Raytracing Workbench
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
