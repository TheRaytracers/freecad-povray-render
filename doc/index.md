# CSG Export to POV-Ray - Documentation

**The workbench for rendering with POV-Ray that supports Constructive Solid Geometry and more.**

This workbench is intended to export CSG objects from the Part Workbench to a good readable POV-Ray file. For that, the macro converts the content of the FreeCAD object tree into the POV-Ray scene description language.
An important principle is WYSIWYG (**W**hat **Y**ou **S**ee **I**s **W**hat **Y**ou **G**et). So in the first step the rendered picture should look the same as displayed in FreeCAD view.
In a second step the user can add textures, materials or additional lightning to render a photorealistic scene.

## Get started

Look in the [README](../README.md) if you want to know, how to install and get started.

## How to render a photorealistic Scene from your FreeCAD model

You are just a few steps away from rendering realistic scenes.  
Read how it works in the [step by step description](realistic.md) of the following example:

![Step by step]( ./img/Chess_steps.png "Step by step from FreeCAD CSG Objects to a photorealistic POV-Ray scene")

## More examples

Some more [examples](./Examples/index.md) to play with.

## Limitations, tips and tricks

Learn more about the concepts of FreeCAD and POV-Ray and our way we adapted them for the features of the scene description. [read more](tipsAndTricks.md)

## Supported features

A list of all [features the workbench supports](supported.md)

## Files

An [overview about the files](Projectfiles.md) that are used or will be created by the workbench.

## FAQ

We made a little FAQ for you: [FAQ](FAQ.md)

## History of the project

It took more than a year to develop this workbench. We explain some milestones for you to understand [design decisions](Design.md).

## Power User

If you want to learn more about advanced techniques and settings, checkout the [Power User](PowerUser.md) section.
## For developers

![Flowchart of the macro](img/Workbench%20Structure.png)  
You want to contribute to our macro? Great! Here you can find [CONTRIBUTING.md](../CONTRIBUTING.md)
