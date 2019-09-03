/*
* You can use this template for your inc file. Just copy and paste
* this code to your inc file to get a more realistic image.
* But doubt, that this is only a pattern, you can edit values
* for your specific case.
*
* This template is a sky with clouds.
* But doubt, that this background doesn't look realistic with an underground (see other templates)
* Doubt secondly, that you disable the export of the FreeCAD background
* If get not the expected result, please try to edit the scaling (at the end)
*/

sphere { <0, 0, 0>, 1 hollow
  texture {
    pigment { color rgb <0.1, 0.3, 0.75> * 0.6 }
    finish { ambient 1 diffuse 0}
  }

  texture {
    pigment {
      bozo turbulence 0.65
      octaves 6
      omega 0.7
      lambda 2
      color_map {
        [0.0  color rgb <0.95, 0.95, 0.95> * 0.5 ]
        [0.1  color rgb <1, 1, 1> * 1.1 ]
        [0.15 color rgb <0.85, 0.85, 0.85> ]
        [0.5 color rgbt <1, 1, 1, 1> ]
        [1.0 color rgbt <1, 1, 1, 1> ]
      }

      rotate<10,23,0>
      scale <0.3, 0.4, 0.2>*0.7
    }

    finish { ambient 1 diffuse 0 }
  }

  scale 999
}
