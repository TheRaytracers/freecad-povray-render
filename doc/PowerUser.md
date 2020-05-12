# Power User

## Textures and Materials in the inc file

If the texture tab hasn't enough possibilities for you, you can use another option, where you have the full control about just everything.  
Before we started to implement the texture tab, special textures were only possible with another file: the _user.inc file. This file is a file with the same name plus "_user" and path as the ini file you selected, but not with the ending "ini", but with the ending "inc":

```
      ini file: /home/usbhub/Documents/myProject.ini
_user.inc file: /home/usbhub/Documents/myProject_user.inc
```

Describing all surface and interior modifying features of POV-Ray would burst this chapter. Our advice for the workflow is to model your objects in FreeCAD without changing any colors and in a second step add textures and materials to the .inc file. The link from a FreeCAD object to its material in the .inc file is the name of the object in the FreeCAD object tree, more accurately: the object label.
If you want to apply a material to an object you add a declaration to the .inc file with the following syntax:

```pov
#declare ObjectLabel_material = material { }
```

This is the content of the _user.inc file for the following example:

```pov
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
        texture { pigment{ color rgb <0, 0, 0> } }
        texture { pigment{ color rgb <1, 1, 1> } }
    }
}

```

![Object labels]( ./img/textures_1.png "Object labels")

In the next step, the workbench will look for material declarations in the .inc file matching the object labels.
If found, the FreeCAD textures in the .pov file will be replaced:

```pov
material { My_Sphere_material }
```

Because POV-Ray can't deal with spaces and special characters we use a replacement function.
If you have problems with object labels, just look up the .pov file - every object has a commented out header with the correct label.
Everything put together, this is how the sphere declaration in the .pov file looks like:

```pov
//----- My_Sphere -----
sphere { <0, 0, 0> 5
    translate <0.0, -6.0, 0.0>

    material { My_Sphere_material }
}
```

It is important to take care of the material hierarchy. The workbench only looks for the material statement to be replaced. In our example we use a predefined pigment and finish for the sphere. Both are two levels lower than the material statement. And they need an additional include file. Put this line at the top of the inc file to include the file:

```pov
"metals.inc"
```

For a wrong syntax an error message will pop up, where you can find some debugging information.
Together with the [POV-Ray Wiki](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_6) you will be able to create any texture you want.

### The material hierarchy

If you try to add textures to your objects via the .inc file you may start with some error messages.
A common cause of these messages is a incorrect usage of the material hierarchy. In the future development of the workbench things should become easier. But actually `material{}` is the only statement one can use to add properties to objects. The workbench won't look for other statements like `texture{}` or `pigment{}`.
But that does not mean, that you can't use these statements. You just have to put them into the `material` brackets in their right hierarchical order:

```pov
object {                                // the type of object 'sphere' for example
    properties                      // like the radius of the sphere
    interior type                   // 'hollow' for example - unfortunately it is not possible to declare this in the .inc file
    ...                             // other object modifiers eg. 'scale', 'translate'
    material {                      // all statements inside the brackets can be used
        texture {
            pigment {
                ...      // eg. color or color map
            }
        }

        normal {
            ...          // surface modifiers like 'bumps'
        }

        finish{
            ...          // 'transparency' or 'reflection' for example
        }

        interior{
            ...          // good for glass - but you can't use media
        }
    }
}
```

POV-Ray provides a lot of predefined materials. If you want to use them take care of two points:

* put them in the right place in the material hierarchy (see above)
* include the corresponding .inc file in your own include file

This is easy for some glasses:

```pov
#declare Object_Label_material = material{ M_Glass3 }
```

You don't need any include file because Glass is included as standard and 'M_Glass3' is toplevel of the material hierarchy.
But it is a little bit more tricky for metals:

```pov
#include "metals.inc"

#declare My_Sphere_material = material {
    texture {
        pigment { P_Chrome1 }
        finish { F_MetalD }
    }
}

```

Here you need the include file and pigment and finish are two levels below 'material{}'.
This makes sense, because you can combine different metal colors with the way of surface treatment like polishing or brushing.

### Use own Camera

If you define an own camera in the _user.inc file, the workbench will detect this and won't export the FreeCAD camera, so yours will be used. Don't forget to make sure, that the camera uses a right handed coordinate system like FreeCAD (a good tip is to copy the camera from the pov file, paste it into the inc file and edit it).

### Use Photons

Please read [POV-Ray Wiki: Photons](http://wiki.povray.org/content/Reference:Photons) if you don't know, what photons are and how to use it. In short version, with photons it is possible to create realistic caustics and reflections.

You can use them by defining the photons block in the _user.inc file. But how to set the photons blocks per object: Declaring them like materials is not possible, because POV-Ray throws an error if you do that. So we introduced another syntax. This is an example for an object with the label "myObject":

```pov
#declare myObject_photons_reflection = off;
#declare myObject_photons_refraction = on;
#declare myObject_photons_collect = off;
```

The conversion of the label is the same as for materials. If you know photons, this syntax should be self explaining. It is not necessary to turn the `target` on, because the workbench does this automatically (the `target` keyword isn't added to light sources of course).

### Where is the advantage of using the inc file

The big advantage in using the inc file is, that you can adjust __every__ single option. In addition to that, you can add POV-Ray objects like fogs, skies, planes, etc. Actually, this is only possible via the user inc file (we hope to enable as many possibilities via FreeCAD as possible soon).

## How to add new predefined textures

If you often use the workbench, the few predefined textures will be quickly not enough anymore. Then you have two options:

1. using the user inc file (see above)
2. adding new textures to the predefined file

The second way should be the preferred way, because then you can also share your new texture with the community (on the same way, you can report a bug, see the [FAQ](FAQ.md)).

### predefined.xml

If you look into your FreeCAD config folder, you will find `Mod/exporttopovray/predefined.xml`. This is the file, where all textures, that are shown to you in the tab, are defined. As you can easily see, this XML file is representing the exactly structure you see in the texture tab. Predef-Tag defines an texture and has this following attributes:

* **`inc`**  
  Which file(s) needs to be included
* **`comment`**  
  Here you can type a comment if something is special with this texture.
* **`pigment`**  
  Here you define the content of the `pigment` block. This works the same for the following blocks:
  * `finish`
  * `interior`
  * `texture`
  * `normal`
  * `media`
