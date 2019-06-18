#version 3.6; // 3.7
global_settings{assumed_gamma 1.0}
#default{ finish{ ambient 0.2 diffuse 0.9 }}
#default{pigment{rgb <0.800, 0.800, 0.800>}}
//------------------------------------------
#include "colors.inc"
#include "textures.inc"

#include "/home/otto/Dokumente/exporttopovray/Examples/Dice.inc"
//------------------------------------------
// camera ----------------------------------
camera {
     location <0, 0, 0>
     direction < 0, 1, 0>
     up    < 0, 0, 1>
     right   < 1.33, 0, 0>
     rotate <-48.6108313164, -1.44788331122, 32.7632984383>
     translate <14.2887821198, -10.3919305801, 25.3781394958>
     angle 55
    }
// sun -------------------------------------
light_source{<14.2887821198, -10.3919305801, 25.3781394958> color rgb<0.5,0.5,0.5>}
// background ------------------------------
sky_sphere {
  pigment {
   gradient z
   color_map {
        [ 0.00  color rgb<0.592, 0.592, 0.667> ]
        [ 0.20  color rgb<0.592, 0.592, 0.667> ]
        [ 0.60  color rgb<0.200, 0.200, 0.396> ]
        [ 1.00  color rgb<0.200, 0.200, 0.396> ]
       }
   scale 2
   translate -1
   rotate<-48.6108313164, -1.44788331122, 32.7632984383>
   }
}
//------------------------------------------
// objects in scene ------------------------

//----- Dice -----
difference {

    //----- BasicDice -----
    intersection {
    
        //----- Cube -----
        box{ <0,0,0>, <10.0, 10.0, 10.0>
        }
        
        //----- Sphere -----
        sphere { <0, 0, 0> 7
            translate <5.0, 5.0, 5.0>
        }
        
        
    material {BasicDice_material}
    
    }
    
    //----- Sides -----
    union {
    
        //----- Side6 -----
        union {
        
            //----- Sphere020 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 5.0>
            }
            
            //----- Sphere019 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 5.0>
            }
            
            //----- Sphere018 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 3.0>
            }
            
            //----- Sphere017 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 7.0>
            }
            
            //----- Sphere016 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 3.0>
            }
            
            //----- Sphere015 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 7.0>
            }
            
            translate <0.0, 10.5, 0.0>
        }
        
        //----- Side5 -----
        union {
        
            //----- Sphere014 -----
            sphere { <0, 0, 0> 1
                translate <5.0, 0.0, 5.0>
            }
            
            //----- Sphere013 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 3.0>
            }
            
            //----- Sphere012 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 7.0>
            }
            
            //----- Sphere011 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 3.0>
            }
            
            //----- Sphere010 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 7.0>
            }
            
            rotate <0.0, 0.0, 90.0>
            translate <10.5, 0.0, 0.0>
        }
        
        //----- Side1 -----
        sphere { <0, 0, 0> 1
            translate <5.0, -0.5, 5.0>
        }
        
        //----- Side3 -----
        union {
        
            //----- Sphere005 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 3.0>
            }
            
            //----- Sphere004 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 7.0>
            }
            
            //----- Sphere003 -----
            sphere { <0, 0, 0> 1
                translate <5.0, 0.0, 5.0>
            }
            
            rotate <-90.0, 0.0, 0.0>
            translate <0.0, 0.0, -0.5>
        }
        
        //----- Side4 -----
        union {
        
            //----- Sphere009 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 3.0>
            }
            
            //----- Sphere008 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 7.0>
            }
            
            //----- Sphere007 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 3.0>
            }
            
            //----- Sphere006 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 7.0>
            }
            
            rotate <-90.0, 0.0, 0.0>
            translate <0.0, 0.0, 10.5>
        }
        
        //----- Side2 -----
        union {
        
            //----- Sphere002 -----
            sphere { <0, 0, 0> 1
                translate <3.0, 0.0, 3.0>
            }
            
            //----- Sphere001 -----
            sphere { <0, 0, 0> 1
                translate <7.0, 0.0, 7.0>
            }
            
            rotate <0.0, 0.0, 90.0>
            translate <-0.5, 0.0, 0.0>
        }
        
        pigment{color rgb<1.000, 1.000, 1.000>}
    
    }
    
    pigment{color rgb<0.800, 0.000, 0.000>}

}
