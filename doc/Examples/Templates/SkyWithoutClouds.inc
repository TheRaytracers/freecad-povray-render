/*
* You can use this template for your inc file. Just copy and paste
* this code to your inc file to get a more realistic image.
* But doubt, that this is only a pattern, you can edit values
* for your specific case.
*
* This template is a sky without clouds. You could also create this background with the FreeCAD background
* But doubt, that this background doesn't look realistic without an underground (see other templates)
*/

//sky
sky_sphere{
  pigment { gradient <0, 0, 1>
    color_map {
      [0.0 color rgb <1, 1, 1> ]
      [0.8 color rgb <0.1, 0.25, 0.75> ]
      [1.0 color rgb <0.1, 0.25, 0.75> ]
    }
  }
}
