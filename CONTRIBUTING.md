# Developer Documentation

- [Developer Documentation](#developer-documentation)
  - [The Goal of the Project](#the-goal-of-the-project)
  - [Working on the code is not the only way to contribute](#working-on-the-code-is-not-the-only-way-to-contribute)
  - [Contribute to the Code](#contribute-to-the-code)
    - [Structure of the Dialog](#structure-of-the-dialog)
      - [Structure of Tab Classes](#structure-of-tab-classes)
    - [Structure of the Exporter](#structure-of-the-exporter)
      - [`createPovCode`](#createpovcode)
        - [General Characteristics of the Creation](#general-characteristics-of-the-creation)
        - [Rough Steps](#rough-steps)
      - [`initExport`](#initexport)

## The Goal of the Project

This workbench is intended to export as many objects as possible from FreeCAD into a corresponding mathematical POV-Ray object.

The object tree with its boolean operations and other objects should be converted with the same structure in the POV-Ray file.

The user must be able to modify the POV-Ray file and include own pov-code so that the extensive possibilities of POV-Ray for a photorealistic presentation can be used (e.g. textures and light effects). For this, one of the main principle is to keep the POV-Ray file as clear as possible, so that objects can be found quickly.

The user should be able to render realistic scenes easily by adding of textures und lights without needing to write POV-Ray code. As many as possible POV-Ray features should be available via the GUI, but due to the amount of POV-Ray features, only the most important ones are implemented.

Since a complete transfer of all FreeCAD construction possibilities would be too complex, the workbench was initially focused to CSG objects, but with time other features e.g. from PartDesign workbench were implemented. Depending on time more features will be implemented.

The limitations of the workbench must not lead to missing objects in the rendered scene. So not supported objects must be rendered as mesh but this limitation should be clearly comprehensible for the user for example through a good documentation.

## Working on the code is not the only way to contribute

The documentation is not less important than the code! If you found a thing, which can be improved, clone this repository, do and commit you changes and make a pull request.

But it is not necessary to edit files, make a pull request and so on. If you found an bug and report it, that is contributing too! An improvement suggestion is also a contribution to the workbench.
And often forgotten: If someone has a problem and ask in the forum and you help to solve the problem, you contributed!

You see, contribution to a project is not only possible with coding skills. Anything that advances our workbench in any way is a contribution.

**Without your reports, ideas, etc. the workbench won't get better or only very slow. So report all, that comes to your mind.**

Before you create a new issue, please read the [Issue Guidelines](https://gitlab.com/usbhub/exporttopovray/issues/26).

## Contribute to the Code

Here's a flowchart of the rough **program structure** (if you need a higher resolution, in the doc/img folder is an additional pdf file of this chart):

![Flowchart of the workbench](/doc/img/Workbench%20Structure.png)

### Structure of the Dialog

Everything concerning the dialog is programmed in Dialog.py. There you have the main class `Dialog`. This class creates the dialog window and the general tab and the help tab. The texture tab and the indirect lightning tab are defined in its own classes (`TextureTab` and `RadiosityTab`). They are derived by QWidget, so they can be added to the tabs directly by the main class.

In addition there are three little help classes:

* **`Predefined`**  
  An instance of this class represents an conditioned predefined material from `predefined.xml`.
* **`ListObject`**  
  An instance of this class saves all information regarding to one object showed in the list of objects in the texture tab.
* **`RenderSettings`**  
  This object is given to the exporter class and saves all settings and file paths and names.

#### Structure of Tab Classes

As said above, the class has to be derived by QWidget, so that it can be added to the tabs. The methods

* `applyQSettings(qSettingsObject)`
* `saveQSettings(qSettingsObject)`
* `applyIniSettings(csvLines)`
* `settingsToIniFormat()`

are mandatory. They are called to give the tab the chance to save the settings of the tab.

In `applyQSettings` and `saveQSettings` the method takes a QSettingsObject that should be used to save/read the settings, that are project independent, e.g. the size of the preview image. Be aware, that you have to begin and end a group, we recommend to name the group with the same name as the tab. If you don't want to save any things via QSettings, just put a `pass` command in the method.

`applyIniSettings` and `settingsToIniFormat` are a bit different. They should be used to save/read the settings, that are different for every project, e.g. the textures. At the beginning of the ini file, a section is commented out where all these things are stored in CSV format. To make clear, which settings are for which tab, it is good to add a prefix to the entry in the first column.

`settingsToIniFormat` returns the csv string with an `;` at the beginning (to comment out), this csv string will be added to the beginning of the ini file (the delimiter should be a `,`). Example (from the texture tab):

```csv
;obj_Plane,Checkerb166,20.0,20.0,20.0,0.0,0.0,0.0,10.0,10.0,0.0
```

`applyIniSettings` is to read the settings from the ini file and apply them to the tab. This method takes the csv lines, they should be given to csv.reader and then you iterate over the rows. Then you check for the prefix and read the rest of the columns and apply the read settings to your tab.

### Structure of the Exporter

Everything that creates POV-Ray code is stored in `Exporter.py`.

The most important methods are `initExport()` and `createPovCode()`.

#### `createPovCode`

This method is the heart of the exporter. It takes a FreeCAD object and several parameters to specify what will be exported in which way. `createPovCode()` is a recursive method: It calls itself for every child object of the given object. For example if you give a boolean operation to `createPovCode()`, the method will call itself again with the child objects of the boolean operation.

##### General Characteristics of the Creation

* The workbench uses a right handed coordinate system like FreeCAD (specified in [However, this limitation is clearly comprehensible for the user - either through a good documentation or in the program e.g. through colored selection of transferred objects in the object tree.camera](#camera))
* The workbench creates all objects at <0, 0, 0> and translates the objects later. The reason for that is, that POV-Ray rotates an object independently from its position around <0, 0, 0>, FreeCAD rotates relative to the object.

##### Rough Steps

1. `initExport()`
   1. apply all settings from `renderSettings` to fields of the class
   2. call `startExport()`
2. `startExport()`
   1. create the `firstLayer` array
   2. create the POV-Ray code of the objects
      1. `createPovCode`
         1. create the basing object
         2. rotate the object
         3. translate the object
         4. add material
         5. add photons
   3. create the skeletal structure of the POV-Ray file
   4. write files
   5. start POV-Ray

#### `initExport`

This method is called by the `Dialog` class with the `RenderSettings` object as argument. It initializes the exporting process for the current FreeCAD model.
