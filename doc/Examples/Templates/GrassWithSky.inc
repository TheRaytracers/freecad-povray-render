/*
* You can use this template for your inc file. Just copy and paste
* this code to your inc file to get a more realistic image.
* But doubt, that this is only a pattern, you can edit values
* for your specific case. Depending on the template you must change some values.
*
* This template is a sky with clouds and a underground. Probably you have to change
* a few values, especially the height of the ground.
*/

// sky
plane { z, 1 hollow  
    texture {
        pigment { bozo turbulence 0.76
            color_map {
                [0.5 rgb <0.20, 0.20, 1.0>]
                [0.6 rgb <1, 1, 1>]
                [1.0 rgb <0.5, 0.5, 0.5>]
            }
        }

        finish {ambient 1 diffuse 0}
    }      
    
    scale 10000
}

// fog
fog {
    fog_type 2
    distance 50
    color White
    fog_offset 0.1
    fog_alt 2.0
    turbulence 0.8
}

// ground
plane { z, 0 
    texture{
        pigment { color rgb <0.35, 0.65, 0.0> * 0.9 }
	    normal { bumps 0.75 scale 0.015 }
        finish { phong 0.1 }
    }
}