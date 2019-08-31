# Limitations, Tips & Tricks

Even if FreeCAD an POV-Ray both support Constructive Solid Geometry we found a lot of differences in the details we had to deal with, while developing this macro.
So if your rendering looks not like you expected it may not be a bug, it can also be a compromise to adapt the different concepts of FreeCAD and POV-Ray.

## The camera

Normally you wont have to deal with camera settings. The macro both supports orthographic and perspective view. You just choose the view in FreeCAD and the result of the rendering should have the same point of view and viewing angle. There may be some clipping of the borders of the rendered image if the size of the viewport in FreeCAD isn't exacly the same size you choose in the Macro popup. If you choose the "Export FreeCAD View" option you will find a image of the FreeCAD view in your output folder with the size of the rendered image. It should match the camera perspective exactly.
If you define your own camera in the .inc file the macro will detect this and the camera statement will be outcommented in the .pov file. If you want to use special camera types and effects from POV-Ray but still want to take the camera point of view from FreeCAD we provide some declarations in the .pov file that you can use in your .inc file:
```
#declare CamUp = < 0, 0, 1>;
#declare CamRight = <1.33, 0, 0>;
#declare CamRotation = <-50, -1, 25>;
#declare CamPosition = <120, -25.6932964325, 100>;
```
The example is also the key to the right handedness of the coordinate system we use. While POV-Ray uses a left handed coordinate system FreeCAD like many other CAD Programs uses a right handed one. In the above declaration you can see the up vector pointing in the z direction and the right vector in the x direction. In POV-Ray examles you will often find the following declaration:
```
camera{
    up < 0, 1, 0>
    right< 1.33, 0, 0>
    ...
    }
```
So y and z axis are swaped and the result ist a left handed coordinate system.
You may ask why right is 1.33. This is the aspect ratio of your image - If the value ist not correct the rendered image will be streched or compressed.

If you want to know more about the coordinate system see:

[POV-Ray Reference](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_2_1_7)

and

[POV-Ray Tutorial](http://www.povray.org/documentation/3.7.0/t2_2.html#t2_2_1_1)

## Background

The Background of the rendered image was a challenge to implement. In FreeCAD you can choose the background colors via the settings menu. You can choose plain color or a gradient of two or three colors. The color you choose in the settings menu is not exactly the same you see in the viewport. FreeCAD darkens the Background slightly. So we had to make a decision either to take the original color or the darkened. We took the original - it looks bright and friendly.

The background in POV-Ray is realised by a skysphere statement. [See POV-Ray wiki](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_3_4)
It is like an infinite sphere around the scene. The skysphere is rotated according to the camera rotation. If you use your own camera declaration the background may tilt. If the tilted background affects your inner balance - switch it of in the macro dialog and declare your own.

A further problem was the background for the orthographic camera. The skysphere won't render a color gradient even if declared. So we placed a patch with exactly the size of the orthographic camera view behind the scene. But we also add the skysphere for realistic reflection on the objects.
This "look from outside" illustrates the "orthographic background":

![Orthographic bacground illustration]( ./img/Chess/Orthographic_background.png "Orthographic background")

## Lights

By default we defined a lightsource which is placed exactly at the position of the camera. If you switch it of some ambient light will remain. With our default lightsource the shadows are not so impressing. You can define as many lights as you want from different types in the .inc file. For more information about light see [POV-Ray wiki](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_4).

## Textures and materials

* You can change the background of FreeCAD under Edit/Preferences/Display/Colors/Background Color. You can also add a middle color.
* For side views, try the orthographic view. But for a non side view, don't use the orthographic view. That doesn't look realistic
* Try to get a more realistic image: [Rendering a photorealistic Scene - Step by Step](realistic.md)
* If you have a big scene with a lot of objects and many materials with light refraction, try a little size of the image first, because then you not must wait for a long time.
* If you create a cut with two touching surfaces in FreeCAD, nothing remains. With POVray, however, an infinitely thin layer remains:

  ![FreeCAD before cutting](img/tipsAndTricks/01_FC.png "FreeCAD before cutting")
  ![POVray before cutting](img/tipsAndTricks/01_PR.png "POVray before cutting")

  Then you cut the two boxes.

  ![FreeCAD after cutting](img/tipsAndTricks/02_FC.png "FreeCAD after cutting")
  ![POVray after cutting](img/tipsAndTricks/02_PR.png "POVray after cutting")

  To avoid this, the part to be removed should be slightly larger than the other part.
