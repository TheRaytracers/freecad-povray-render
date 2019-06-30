#version 3.6; // 3.7
global_settings{assumed_gamma 1.0}
#default{ finish{ ambient 0.2 diffuse 0.9 }}
#default{pigment{rgb <0.800, 0.800, 0.800>}}
//------------------------------------------
#include "colors.inc"
#include "textures.inc"
//------------------------------------------
// camera ----------------------------------
camera {
     location <0, 0, 0>
     direction < 0, 1, 0>
     up    < 0, 0, 1>
     right   <1.78, 0, 0>
     rotate <-35.264390534, 1.9538003485e-05, 45.0000026303>
     translate <28.933719635, -16.4337062836, 26.4337100983>
     angle 55
    }
// sun -------------------------------------
light_source{<28.933719635, -16.4337062836, 26.4337100983> color rgb<0.5,0.5,0.5>}
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
   rotate<-35.264390534, 1.9538003485e-05, 45.0000026303>
   }
}
//------------------------------------------
// objects in scene ------------------------

//----- Cube -----
box{ <0,0,0>, <10.0, 10.0, 10.0>
    pigment{color rgb<0.800, 0.000, 0.000>}

}

//----- Cube001 -----
box{ <0,0,0>, <10.0, 10.0, 10.0>
    translate <5.0, 0.0, 0.0>
    pigment{color rgb<0.000, 1.000, 0.000>}

}
