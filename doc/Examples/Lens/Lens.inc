#include "glass.inc"

light_source {
    CamPosition color rgb <0.5, 0.5, 0.5>
    rotate <-30, 0, 0>
}

#declare Lens_material = material {
    texture{T_Glass3}
    interior{I_Glass3}
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
