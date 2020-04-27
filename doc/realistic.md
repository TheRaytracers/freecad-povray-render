# Rendering a photorealistic Scene - Step by Step

POV-Ray is a very powerful renderer developed in the early 90'ys. It has a mathematical approach not only for description of objects but also for textures an even for the visualisation of mathematical functions. So with adding only a few lines you can create great effects.

In the Part Workbench of FreeCAD you can also find objects which can be described by a mathematical function. A sphere for example is described by a centerpoint and a radius. If we combine different mathematical described objects with boolean operations we come to the concept of **CSG** (**C**onstructive **S**olid **G**eometry). The Part Workbench of FreeCAD and the object description language of POV-Ray both share the **CSG** concept.

So our chess example is based on CSG and each solid we have implemented in our macro is at least used once.

![Chess_figures]( ./img/Chess/Chess_01.png "Normal FreeCAD view")

You can download the chess example: [Chess FreeCAD File](../Examples/Chess/ChessPieces.fcstd).  
If you start the macro a pop-up window appears where you can choose a filename for the output file and the size of the picture to be rendered.
Be sure your pathname contains no spaces because POV-Ray can't deal with this.
Now start the rendering by clicking OK. If POV-Ray is installed correctly, this image should appear.
To close the image click on the image!

![First render]( ./img/Chess/Chess_02.png "First render")

Maybe the result is not very exciting for you. Without any textures and just the basic settings the macro follws the **WYSIWYG** principle. **W**hat **Y**ou **S**ee (in FreeCAD) **I**s **W**hat **Y**ou **G**et (in POV-Ray). If you checked the "Export FreeCAD view" checkbox in the popup window you can find a second picture with the FreeCAD view in the output directory. Both pictures have the same image size and camera view. But if you look carefully you can see litte differences: POV-Ray will not render the outlines of the objects and if you look even closer, the shadows are not the same. It is that way because FreeCAD illuminates each object individually but in POV-Ray we used a single lightsource at the position of the camera. If there are bigger differences you should check our [Tips & Tricks Section](tipsAndTricks.md).

Now let's take the first step into realistic rendering! To add some textures you must change into the texture tab. On the left side of this tab you can see all visible objects of our example. On the right side you can find some predefined textures.
If you want to add a texture to an object choose it in the left list and then the desired texture in the right list. In our example we take "Crystal glass" for the white pieces and "Shungit" for the black pieces. There is also a predefined texture called "Checker" to be found under the "Pattern" cathegorie. It is important to scale this pattern with factor 20 and translate it 10 units in x and y direction to fit the dimensions of the board.

Another thing we did in the following example: We changed the background color in FreeCAD settings by adding a middle color.

Now start the Rendering again and you will get something like this:

![First texture]( ./img/Chess/Chess_04.png "First texture")

The texture tab is for quick and easy results. But we know you will get addicted to improve your rendering abilities.

To use the whole power of POV-Ray you can create your own include file where you can place all your rendering dreams.
You will need a include file in the same directory of our .pov output file. To be recognized by our macro its name have to  be the same as the POV-Ray file but with the .inc extension. If you choose Chess01.pov for your output file the corresponding texture file is Chess01.inc.

With the following files you can try how it works

[ChessGame.FCstd](../Examples/Chess/ChessGame.fcstd) is derived from the chess pieces above but now with a complete gaming scene.

[RealChess.inc](../Examples/Chess/RealChess.inc)  is the corresponding include file. The content is explained in the section below the next image.

After downloading the include file move it to the right directory and rename it as mentioned above.

Start your rendering and you should get this result:

![Lights and radiosity]( ./img/Chess/Chess_08.png "Add lights and radiosity")

---------- section below needs further update ----------------

If you create your own textures, make sure, you use the right syntax. Replace the "xxx" in the following declaration with the object name from the object tree in FreeCAD:

```pov
#declare xxx_material = material { }
```

Before you create your own textures, take a look at our example which can be downloaded by clicking at [Chess inc File](../Examples/Chess/ChessTextures.inc).
Just put it in the right folder, rename it and start the macro again. The result should be like this:

Put your material declaration inside the brackets. Be aware of the hierarchy of material declaration. We only provide `material { }` in our macro because it is the wrapper of all other POV-Ray statements like texture, pigment, finish, pattern etc. POV-Ray has an excellent documentation, so you will find further information in the [POV-Ray wiki](http://www.povray.org/documentation/3.7.0/r3_4.html#r3_4_5_5_3).
Ignoring the material hierarchy will lead to a POV-Ray error and nothing will be rendered. How to get the console output from POV-Ray for debugging see the [Tips & Tricks Section](tipsAndTricks.md).

Now let's try to add more reality to the chess Example. You can download another FreeCAD file for a gaming scene and a corresponding include file:

In the example we defined our own camera with a focus blur statement so our scene looks more like a photo. If you put your own camera in the user inc file, the macro will detect it and the camera statement in the .pov file will be outcommented. But you can still use camera position and rotation of the FreeCAD viewport because we provide them as declarations. For special effects POV-Ray provides much more camara types then FreeCAD and they can be modified. So lots of fun is waiting for you.

In the last example we added a second light source. It is a spotlight that turns the focus on the white king - maybe he is in danger - what do you think?
We also added some radiosity for more realistic light. There are different types of lightsources and lightning effects available.

If you don't have that much knowledge about POV-Ray, you can use a few templates, we created. You can find them in the [Template Folder](../Examples/Templates/).  
And you can find some more examples in the [Examples Folder](../Examples/index.md)
