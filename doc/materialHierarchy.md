# The material hierarchy

If you try to add textures to your objects via the .inc file you may start with some error messages.
A common cause of these messages is a incorrect usage of the material hierarchy. In the [future developement](roadmap.md) of the macro things should become easier. But actually `material{}` is the only statement one can use to add properties to objects. The macro won't look for other statements like `texture{}` or `pigment{}`.
But that does not mean, that you can't use these statements. You just have to put them into the `material` brackets in their right hierarchical order:
```
object{                 // the type of object 'sphere' for example
    properties          // like the radius of the sphere
    interior type       // 'hollow' for example - unfortunately it is not possible to declare this in the .inc file
        ...             // other object modifiers eg. 'scale', 'translate' 
    material{           // all statements inside the brackets can be used
        texture{
            pigment{
                    ... // eg. color or color map
                }
            normal{
                    ... // surface modyfiers like 'bumps'
                }
            finish{
                    ... // 'transparency' or 'reflection' for example
                }    
            }
        interior{
                  ...   // good for glass - but you can't use media
            }
        }
    }
```
POV-Ray provides a lot of predefined materials. If you whant to use them take care of two points:
* put them in the right place in the material hierarchy (see above)
* include the corresponding .inc file in your own include file

This is easy for some glasses:
```
#declare Object_Label_material = material{ M_Glass3 }
```
You don't need any include file because Glass is included as standard and 'M_Glass3' ist toplevel of the material hierarchy.
But it is a little bit more tricky for metals:

```
#include "metals.inc"

#declare My_Sphere_material = material{
    texture {
        pigment { P_Chrome1 }
        finish { F_MetalD }
    }
}

```
Here you need the include file and pigment and finish are two levels below 'material{}'.
This makes sense, because you can combine different metal colors with the way of surface treatment like polishing or brushing.