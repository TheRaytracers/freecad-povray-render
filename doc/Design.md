# Design Decisions

To understand the design and workflow of the workbench you have to know the history of it.

## How it started

The project started from a quick idea as a proof of concept. Because it was never planned to create such a workbench, it started with a macro. But the macro grew and grew and with every new feature it became harder to change to a workbench, so we kept the macro.

## The inc file

One problem of the old raytracing workbench was that it was very hard to do changes or apply textures. When you changes something in the file it was necessary to render it again with POV-Ray manually. In addition to that, a change in the FreeCAD model overwrote any changes in the file and it was necessary to do all the changes again. It's obvious that this isn't the best way.

Our approach was to have the changes in an own file that is included and won't be touched. In this file you can add anything you want and it will not be overwritten by the macro/workbench. In addition to that we implemented a reading of the file, so it's possible to apply the textures via this file. With the inc file, theoretically everything was possible. But many things were complicated to do with file and not very user friendly.

## The tabs

As a macro you cannot insert objects and so all settings couldn't be saved in objects. So we decided to create tabs and save the settings with QSettings independent from FreeCAD.

### The ini file

Later we wanted to add a feature to make it possible to set textures and materials to objects, but this needed complete new structures. Before that, all settings were saved independently from FreeCAD and the model. But that would become a problem if you have a cube with a wood texture in one project and in another project a cube with the same name and e.g a glass texture. It was necessary to save the settings together with the project. Another problem with QSettings was, that you would have to do all settings again on another computer.

So we decided to make something like a project file. The ini file is a file where you save set all settings for POV-Ray in one file and just give it to POV-Ray. So we decided to use this file to save and reload the settings. With this powerful new way of saving, it was possible to implement the texture tab and more.

## The macro became a workbench

The next big step would be to add lights to give the possibility to create more advanced lightnings easily without using the inc file. This made it necessary to add lights in the model. We decided against a new tab for configuring lights because you have to real imagination of a light at the position 10, 0.5, 34 with the color red and a fading of 2.5.

To add lights it was necessary to add objects to the FreeCAD model, that wasn't possible by a macro, so this was the final reason the change the macro to a workbench. The tabs kept staying because a changing of the saving would be hard to implement and without a real use.

### The light objects

One goal of the workbench is to be easy to use and without any special knowledge about raytracing. We added the three most common light types (point lights, area lights, spot lights) including a visualization in the model. This visualization makes it possible to get a good imagination of the lights in the scene.

## More tabs were added

With time, more tabs were added, e.g the tab for configuring indirect lightning. 
