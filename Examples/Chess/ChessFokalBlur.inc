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

#declare Weiss_material = material{ M_Glass3 }

#declare Schwarz_material = material{
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

#declare Brett_material = material{
    texture {
        checker
            texture { pigment{ color rgb<1,1,1> }}
            texture { pigment{ color rgb<0,0,0> }}
            scale 20 translate <10,10,0>
        }
    }

#declare Rahmen_material = material{
    texture { Cherry_Wood }
    scale 2
    }
