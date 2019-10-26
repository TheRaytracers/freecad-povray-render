# CSG Export to POV-Ray - Documentation
#### The macro that creates user friendly .pov files from CSG objects

This macro is intended to export CSG objects from the Part Workbench to a good readable POV-Ray file. For that, the macro converts the content of the FreeCAD object tree into the POV-Ray scene description language.
An important principle is WYSIWYG (**W**hat **Y**ou **S**ee **I**s **W**hat **Y**ou **G**et). So in the first step the rendered picture should look the same as displayed in FreeCAD view.
In a second step the user can add textures, materials or additional lightning to render a photorealistic scene.
This can be done by adding an include file with the additional contents.

## Get started

A quick overview about [installation and usage](quickstart.md)

## How to render a photorealistic Scene from your FreeCAD model

You are just a few steps away from rendering realistic scenes with our macro.  
Read how it works in the [step by step description](realistic.md) of the following example:

![Step by step]( ./img/Chess/Chess_steps.png "Step by step from FreeCAD CSG Objects to a photorealistic POV-Ray scene")

## Limitations, tips and tricks

Learn more about the concepts of FreeCAD and POV-Ray and our way we adapted them for the features of the scene description. [read more](tipsAndTricks.md)

## Supported features

A list of all [features the macro supports](supported.md)

## FAQ
We made a little FAQ for you: [FAQ](FAQ.md)


## For developers
You want to contribute to our macro? Great! Here you can find our [Developer Documentation](developer.md)
