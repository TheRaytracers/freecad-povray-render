// Area light
light_source {
    <0, 0, 0>
    color rgb <0.5,0.5,0.5>
    area_light <10, 0, 0>, <0, 0, 10>, 10, 10
    adaptive 1
    jitter
    rotate CamRotation
    translate CamPosition
}

// Raytracing
#include "rad_def.inc"
global_settings {
   radiosity {
      Rad_Settings(Radiosity_OutdoorLight, off, off)
   }
}
