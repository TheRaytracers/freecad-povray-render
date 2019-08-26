# CSG Export to POVray - Documentation
#### The macro that creates user friendly .pov files from CSG objects

This macro is intended to export CSG objects from the Part Workbench to a good readable and editable POVray file. For that, the macro converts the content of the FreeCAD object tree into the POVray language.
An important principle is WYSIWYG (**W**hat **Y**ou **S**ee **I**s **W**hat **Y**ou **G**et). So in the first step the rendered picture should look the same as displayed in FreeCAD view.
In a second step the user can add textures, materials or additional lightning to render a photorealistic scene.
This can be either done by directly editing of the resulting POV-Ray file or by adding an include file with additional contents.

![Normal FreeCAD View]( ./img/Chess/Chess_01.png "Here is the normal FreeCAD view with some CSG Chessfigures")| ![Simple POV-Ray rendering]( ./img/Chess/Chess_02.png "This is what you should get if you try our macro the first time")

## I'm a developer
You want to contribute to our macro? Great! Here you can find our [Developer Documentation](developer.md)

## I'm a user
You want to learn how to use our macro? Then this site will be right for you: [User Documentation](user.md)

## FAQ
We made a little FAQ for you: [FAQ](FAQ.md)
