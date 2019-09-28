#include "rad_def.inc"

global_settings {
   radiosity {
        Rad_Settings(Radiosity_OutdoorLight, off, off)
        }
    }
    
camera {
    location <0, 0, 0>
    direction < 0, 1, 0>
    up CamUp
    right CamRight
    rotate CamRotation
    translate CamPosition
    angle 57.82
    focal_point <100,80,10>
    aperture 6     // 0.05 ~ 1.5
    blur_samples 100 // 4 ~ 100
    confidence 0.9   // 0 ~ 1
    variance 1/128   // 1/64 ~ 1/1024 ~
    }


light_source{
    <40,40,100>
    color rgb <1,1,1>   
    spotlight
    point_at<80,60,0>
    radius 60  // hotspot
    tightness 100
    falloff 60
    }
            
#declare White_pieces_material = material{ M_Glass3 }

#declare Black_pieces_material = material{
    texture{
        pigment{color rgb <0,0,0>} 
        finish {
            ambient 0.35
            brilliance 2
            diffuse 0.3
            metallic
            specular 0.80
            roughness 1/20
            reflection 0.1
            }
        }
    }

#declare Board_material = material{
    texture {
        checker
            texture { pigment{ color rgb<1,1,1> }}
            texture { pigment{ color rgb<0,0,0> }}
            scale 20 translate <10,10,0>
        }
    }

#declare Frame_material = material{
    texture { Cherry_Wood }
    scale 2
    }
