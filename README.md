# Workbench for exporting a FreeCAD model to POV-Ray

**With this workbench you will be able to create easily photorealistic pictures of your model, even if you're a beginner in raytracing. If you're an advanced users with more knowledge, you can get the full control about all detailed settings.**

![Logo and Renderings](README_img.png)

In contrast to the other rendering solutions of FreeCAD we are focused on using POV-Ray as the only renderer.
The workbench is intended to map the FreeCAD model on the POV-Ray equivalent as good as possible.
Besides the rendered image the result will be a well organized file structure that gives the user a chance to understand and manipulate the content. For that, the render project is divided into different files for a better overview. Until now most objects from the "Part Workbench" and some important featuers vom "Part design" are supported and the tree structure with the boolean operations can be found in the POV-Ray file. Not supported objects will be simulated with meshes and outsourced to an include file. (see [Supported Objects](doc/Supported.md) and [Project Files](doc/Projectfiles.md)).

To give the user the full control, you can define extra things or another surface as in FreeCAD (Please visit the [Wiki](doc/index.md) for more information).

## Installation

**Automatic Installation**  
The recommended way of installing this workbench is to use the addon manager (Tools / Addon Manager). In the addon manager in the workbenches tab, select the XXX-Workbench and click install.

**Manual Installation**  
Download the repository from [gitlab.com/usbhub/exporttopovray](https://gitlab.com/usbhub/exporttopovray) XXX and unpack the zip in the `Mod` folder of your FreeCAD config folder (for Linux by default `~/.FreeCAD/Mod`, Mac `~/⁨Library⁩/⁨Preferences/⁨FreeCAD⁩/⁨Mod`, Windows `XXX`.

**Install POV-Ray**  
In the background, POV-Ray is used to create the images. So you have to install POV-Ray too:
How you can do this on your system is explained in the [POV-Ray Wiki](http://wiki.povray.org/content/HowTo:Install_POV)

**Set the POV-Ray Executable Path**  
After installing POV-Ray, you have to tell the workbench, where you installed POV-Ray. To do this, go into the POV-Ray workbench and go to Edit/Preferences/POV-Ray. Under "POV-Ray Executable" you can define, where you installed POV-Ray. After that, restart FreeCAD and have fun with our workbench :)

## Features

* easy applying of textures including a preview
* easy inserting and configuration of different types of lights
* easy use of indirect lightning to create realistic images  
  **⇨ simple handling and operation**
* power users can get the full control about the whole configuration with the user inc file (see [Power Users](doc/PowerUser.md))  
  **⇨ offering all settings for advanced users**
* the model is not converted into meshes, the model will be converted into a mathematical way of describing the object shape, so you will get a better object and a better picture
* very good readability of the created files → easy editing of these files
* WYSIWYG - You can pan your model and render and you will get this point of view from FreeCAD

## Get your first image

1. open your model you want to render
2. go to the POV-Ray workbench
3. click on ![Settings & Render Icon](icons/logo.svg) after that a dialog should appear
4. click on the "..." button to select, where you want to store the ini file (something like a project file), all other files that are created during the rendering process will be also stored there
5. the following settings will be good for initial render:
  
   * Width: 800px
   * Height: 600px
   * [x] Export FreeCAD Background
   * [x] Export FreeCAD Light
   * [ ] Repair Rotation
   * [ ] Export FreeCAD View
  
6. press "Start Render"
7. depending on the complexity of the model it can take a while until a window appears, where you see how the rendered image is growing until the rendering process is finished. To close the rendering window click in the middle of the image.
8. go into the folder you selected, there you will find all files including the image

The rendered image will look nearly the same than the FreeCAD view. The following steps will change this dramatically:

## Add textures

Adding Textures is easy: Go to the dialog window again and switch to the texture tab. In the left list you will find all objects to which you can apply textures. **First** select an object in the left list. **Second** select a texture in the right list. These two steps can be repeated.
Start the rendering again.

## Add lights

Lights are Objects and can be added via the workbench. You can move them to the desired position as you are used to do with other FreeCAD objects.
Want to know more about lights? Look in the [Light properties chapter](doc/LightProperties.md). The effects of light to your scene are explained in [Realistic.md](doc/Realistic.md).

## Wiki

The workbench have a lot of features that cannot explained all in the README. So we created a wiki with tutorials and a explanation of all features: [POV-Ray Workbench Wiki](doc/)
