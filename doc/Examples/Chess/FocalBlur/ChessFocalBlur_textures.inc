#declare Board_material = material { 
	texture { 
		pigment { checker color White color Black }
	}
	scale <20.0, 20.0, 20.0>
	translate <10.0, 10.0, 0.0>
}

#declare Black_pieces_material = material { 
	texture { 
		pigment { color Black }
	finish {
	ambient 0.35
brilliance 2
diffuse 0.3
metallic
specular 0.80
roughness 1/20
reflection 0.1	}
	}
}

#declare White_pieces_material = material { M_Glass3
}

#declare Frame_material = material { 
	texture { Cherry_Wood
	}
	scale <2.0, 2.0, 2.0>
}

