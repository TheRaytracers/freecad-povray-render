# Power User

## Textures and Materials in the inc file
If the texture tab hasn't enough possibilities for you, you can use another option, where you have the full control about just everything.  
Before we started to implement the texture tab, special textures were only possible with another file: the user inc file. This file is a file with the same name and path as the ini file you selected, but not with the ending "ini", but with the ending "inc".

Describing all surface and interior modifiying features of POV-Ray would burst this chapter. Our advice for the workflow is to model your objects in FreeCAD without changing any colors and in a second step add textures and materials to the .inc file. The link from a FreeCAD object to its material in the .inc file is the name of the object in the FreeCAD object tree, more accurately: the object label.
If you want to apply a material to an object you add a declaration to the .inc file with the following syntax:

```
#declare ObjectLabel_material = material { }
```
This is the .inc file for the following example:

```
#include "metals.inc"

#declare My_Sphere_material = material{
    texture {
        pigment { P_Chrome1 }
        finish { F_MetalD }
    }
}

#declare My_Box_material = material{
    texture {
        checker
        texture { pigment{ color rgb <0,0,0> }}
        texture { pigment{ color rgb <1,1,1> }}
    }
}

```

![Object labels]( ./img/textures_1.png "Object labels")

The first thing our macro will do, is looking for an .inc file with the same name as the .pov file in the same folder.
For example the corresponding .inc file for "example.pov" is "example.inc".
If the .inc file exsists, it will be included in the .pov file with the following line:

```
#include "example.inc"

```
In the next step, the macro will look for material declarations in the .inc file matching the object labels.
If found, the FreeCAD textures in the .pov file will be replaced:


```
material {My_Sphere_material}
```
Because POV-Ray can't deal with spaces and special characters we use a replacement function.
If you have problems with object labels, just look up the .pov file - every object has a outcommented header with the correct label.
Everything put together, this is how the sphere declaration in the .pov file looks like:

```
//----- My_Sphere -----
sphere { <0, 0, 0> 5
    translate <0.0, -6.0, 0.0>

    material {My_Sphere_material}

}
```
It is important to take care of the material hierarchie. The macro only looks for the material statement to be replaced. In our example we use a predefined pigment and finish for the sphere. Both are two levels lower than the material statement. And they need an additional include file. Put this line at the top of the inc file to include the file:
```
"metals.inc"
```
For a wrong syntax an error message will pop up, where you can find some debugging information.
Together with the [POV-Ray Wiki](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_6)  you will be able to create any texture you want.

### Where is the advantage of using the inc file
The big advantage in using the inc file is, that you can adjust __every__ single option. In addition to that, you can add POV-Ray objects like fogs, skies, planes, etc. Actually, this is only possible via the user inc file.

## How to add new predefined textures
If you often use the macro, the few predefined textures will be quickly not enough anymore. Then you have two options:
1. using the user inc file (see above)
2. adding new textures to the predefined file

The second way should be the preferred way, because then you can also share your new texture with the community (on the same way, you can report a bug, see the FAQ XXX LINK).

### predefined.xml
If you look into your macro folder, you will see your macros and a predefined.xml file. This is the file, where all textures, that are shown to you in the tab, are defined.