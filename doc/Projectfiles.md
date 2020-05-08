# Project files

Different files will be created if you start the export/rendering.
This is a graphic overview:
![Project Files](img/Projectfiles.svg)

## .ini file

The heart of the project. Here are also the settings stored that will be read by the workbench to restore the settings.

## .pov file

Here is the converted model stored.

## _textures.inc

Here are all textures defined, that you set in the texture tab.

## _meshes.inc

Because we don't support all objects, some objects need to be converted to meshes. They are stored in this extra file to avoid unreadable pov file.

## _user.inc

Here you can define your own stuff. You find more information at [Power User](PowerUser.md).

## .png

This is the rendered image.

## _FC-View.png 

This is a screenshot of the view in FreeCAD but with the same dimensions as the rendered image.