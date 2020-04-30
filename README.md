# Workbench for exporting a FreeCAD model to POV-Ray

**With this workbench you will be able to create easily photorealistic pictures of your model, even if you're a beginner in raytracing. If you're an advanced users with more knowledge, you can get the full control about all detailed settings.**

![Logo and Renderings](README_img.png)

The export macro is intended to export the FreeCAD model structure with their equivalent in POV-Ray.
In contrast to other solutions for exporting FreeCAD models to POV-Ray, this macro tries to make the file clearly and easy to edit. For that, it doesn't create gigantic meshes, it moves the tree structure with the boolean operations into a POV-Ray file.  
Until now, the macro supports most objects from the Part Workbench and some features from the Part design and Draft workbench. Not supported objects are simulated with meshes (see [Supported Objects](doc/Supported.md)).

To give the user the full control, you can define extra things or another surface as in FreeCAD (Please visit the [Wiki](doc/index.md) for more information).

## Installation

**Automatic Installation**  
The recommended way of installing this workbench is to use the addon manager (Tools / Addon Manager). In the addon manager in the workbenches tab, select the XXX-Workbench and click install.

**Manual Installation**  
Download the repository from [gitlab.com/usbhub/exporttopovray](https://gitlab.com/usbhub/exporttopovray) XXX and unpack the zip in ~/.FreeCAD/Mod.

**Install POV-Ray**  
In the background, POV-Ray is used to create the images. So you have to install POV-Ray too:
How you can do this on your system is explained in the [POV-Ray Wiki](http://wiki.povray.org/content/HowTo:Install_POV)

**Set the POV-Ray Executable Path**  
After installing POV-Ray, you have to tell the workbench, where you installed POV-Ray. To do this, go into the POV-Ray workbench and go to Edit/Preferences/POV-Ray. Under "POV-Ray Executable" you can define, where you installed POV-Ray. After that, restart FreeCAD and have fun with our workbench :)

## Features

* easy applying of textures including a preview
* easy use of indirect lightning to create realistic images
* easy inserting and configuration of different types of lights  
  **⇨ simple handling and operation**
* power users can get the full control about the whole configuration with the user inc file (see [Power Users](doc/powerusers.md))  
  **⇨ offering all settings for advanced users**
* the model is not converted into meshes, the model will be converted into a mathematical way of describing the object shape, so you will get a better object and a better picture
* very good readability of the created files → easy editing of these files
* WYSIWYG - You can pan your model and render and you will get this point of view from FreeCAD

## Get your first image

1. open your model you want to render
2. go to the POV-Ray workbench
3. click on ![Settings & Render Icon](icons/logo.svg) after that a dialog should appear
4. click on the "..." button to select, where you want to store the ini file (something like a project file), all other files that are created during the rendering process will be also stored there
5. make sure you have the following settings:
  
   * Width: 800px
   * Height: 600px
   * [x] Export FreeCAD Background
   * [x] Export FreeCAD Light
   * [ ] Repair Rotation
   * [ ] Export FreeCAD View
  
6. press "Start Render"
7. depending on the complexity of the model it can take a while until a window appears, where you see how the rendered image are growing until the rendering process is finished. Now click on the window and it will close itself
8. go into the folder you selected, there you will find all files including the image

You will see, your image won't look much nicer than the FreeCAD view. To get a better image, you have to apply textures and lights, etc. How to do that is explained in the [Wiki](doc/).

## Wiki

The workbench have a lot of features that cannot explained all in the README. So we created a wiki with tutorials and a explanation of all features: [POV-Ray Workbench Wiki](doc/)
