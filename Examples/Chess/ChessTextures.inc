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

