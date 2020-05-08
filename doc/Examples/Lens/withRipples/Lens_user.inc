#include "glass.inc"

light_source {
    CamPosition color rgb <0.5, 0.5, 0.5>
    rotate <-30, 0, 0>
}

#declare Lens_material = material {
    texture { T_Glass3
      normal {
        ripples 0.1
        sine_wave
        frequency 10
        scale 1.0
        //translate<0,0.5,0>
      }
    }
    interior { I_Glass3 }
}

#declare Spheres_material = material {
    texture {
        pigment {
            color Green
        }
    }
}

#declare Cube_material = material {
    texture {
        pigment {
            checker color White color Black
            scale 0.3
        }
    }
}
