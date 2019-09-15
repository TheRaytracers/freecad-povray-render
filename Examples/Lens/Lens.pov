#version 3.6; // 3.7
global_settings{assumed_gamma 1.0}
#default{ finish{ ambient 0.2 diffuse 0.9 }}
#default{pigment{rgb <0.800, 0.800, 0.800>}}
//------------------------------------------
#include "colors.inc"
#include "textures.inc"

//------------------------------------------
// camera ----------------------------------
#declare CamUp = < 0, 0, 1>;
#declare CamRight = <1.33, 0, 0>;
#declare CamRotation = <0.0, 0.0, 0.0>;
#declare CamPosition = <0.253216475248, -9.33913040161, 1.22930979729>;
camera {
	location <0, 0, 0>
	direction < 0, 1, 0>
	up CamUp
	right CamRight
	rotate CamRotation
	translate CamPosition
	angle 57.82
}

// background ------------------------------
sky_sphere {
	pigment {
		gradient z
		color_map {
			[ 0.00  color rgb<0.592, 0.592, 0.667> ]
			[ 0.30  color rgb<0.592, 0.592, 0.667> ]
			[ 0.70  color rgb<0.200, 0.200, 0.396> ]
			[ 1.00  color rgb<0.200, 0.200, 0.396> ]
		}
		scale 2
		translate -1
		rotate<0.0, 0.0, 0.0>
	}
}

//------------------------------------------

#include "Lens.inc"

// objects in scene ------------------------

//----- Lens -----
intersection {

	//----- Sphere -----
	sphere { <0, 0, 0> 10 
		translate <0.0, 9.85, 0.0>
	}
	
	//----- Sphere001 -----
	sphere { <0, 0, 0> 10 
		translate <0.0, -9.85, 0.0>
	}
	
	translate <0.0, 0.0, 1.2>

	material {Lens_material}
	
}

//----- Cube -----
box{ <0,0,0>, <3.0, 1.5, 1.5>
	translate <0.0, 4.0, 0.0>

	material {Cube_material}
	
}

//----- Spheres -----
#declare Sphere002_Sphere002 = 
//----- Sphere002 -----
sphere { <0, 0, 0> 0.35 
}
#declare intervalX = <1.0, 0.0, 0.0>;
#declare intervalY = <0.0, 1.0, 0.0>;
#declare intervalZ = <0.0, 0.0, 1.0>;

#declare numX = 1;
#declare ix = 0;
#while (ix < numX)
	#declare numY = 10;
	#declare iy = 0;
	#while (iy < numY)
		#declare numZ = 1;
		#declare iz = 0;
		#while (iz < numZ)
			object { Sphere002_Sphere002
				translate intervalX * ix
				translate intervalY * iy
				translate intervalZ * iz
				translate <-3.0, -2.0, 0.5>
				rotate <0.0, 0.0, -13.0>
				
material {Spheres_material}

			}
			#declare iz = iz + 1;
		#end
		#declare iy = iy + 1;
	#end
	#declare ix = ix + 1;
#end
