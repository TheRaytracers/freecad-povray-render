#version 3.6; // 3.7
global_settings { assumed_gamma 1.0 }
#default { finish { ambient 0.2 diffuse 0.9 } }
#default { pigment { rgb <0.800, 0.800, 0.800> } }

//------------------------------------------
#include "colors.inc"
#include "textures.inc"

//------------------------------------------
#include "PointLight_textures.inc"

//------------------------------------------
// Camera ----------------------------------
#declare CamUp = <0, 0, 1>;
#declare CamRight = <1.33, 0, 0>;
#declare CamRotation = <-44.0465063967, -4.01493999706, 24.8395519912>;
#declare CamPosition = <105.441390991, -38.7394180298, 99.3645935059>;
camera {
	location <0, 0, 0>
	direction <0, 1, 0>
	up CamUp
	right CamRight
	rotate CamRotation
	translate CamPosition
	angle 57.82
}

// Background ------------------------------
sky_sphere {
	pigment {
		gradient z
		color_map {
			[ 0.00  color rgb<0.592, 0.592, 0.667> ]
			[ 0.30  color rgb<0.592, 0.592, 0.667> ]
			[ 0.50  color rgb<1.000, 0.333, 0.000> ]
			[ 0.70  color rgb<0.200, 0.200, 0.396> ]
			[ 1.00  color rgb<0.200, 0.200, 0.396> ]
		}
		scale 2
		translate -1
		rotate<-44.0465063967, -4.01493999706, 24.8395519912>
	}
}

//------------------------------------------
// Objects in Scene ------------------------

//----- Board -----
polygon { 5, <0, 0>, <160.0, 0>, <160.0, 160.0>, <0, 160.0>, <0, 0>
	translate <-10.0, -10.0, 0.01>

	material {Board_material }
	
}

//----- Black_pieces -----
union {

	//----- Pawn_A5 -----
	union {
	
		//----- Torus014 -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Kugel007 -----
		sphere { <0, 0, 0> 4.1 
			translate <0.0, 0.0, 20.0>
		}
		
		//----- Zylinder016 -----
		cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
		}
		
		//----- Torus015 -----
		torus { 3.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 14.5>
		}
		
		//----- Ellipsoid015 -----
		sphere { <0, 0, 0> 1
			scale <5.0, 5.0, 1.0>
			translate <0.0, 0.0, 16.0>
		}
		
		//----- Kegel008 -----
		cone { <0, 0, 0>, 6.0
		    <0, 0, 13.0>, 3.0
			translate <0.0, 0.0, 3.0>
		}
		
		translate <0.0, 80.0, 0.0>
	}
	
	//----- Pawn_C4 -----
	union {
	
		//----- Torus016 -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Kugel008 -----
		sphere { <0, 0, 0> 4.1 
			translate <0.0, 0.0, 20.0>
		}
		
		//----- Zylinder017 -----
		cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
		}
		
		//----- Torus017 -----
		torus { 3.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 14.5>
		}
		
		//----- Ellipsoid016 -----
		sphere { <0, 0, 0> 1
			scale <5.0, 5.0, 1.0>
			translate <0.0, 0.0, 16.0>
		}
		
		//----- Kegel009 -----
		cone { <0, 0, 0>, 6.0
		    <0, 0, 13.0>, 3.0
			translate <0.0, 0.0, 3.0>
		}
		
		translate <40.0, 60.0, 0.0>
	}
	
	//----- Pawn_D4 -----
	union {
	
		//----- Torus007 -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Kugel001 -----
		sphere { <0, 0, 0> 4.1 
			translate <0.0, 0.0, 20.0>
		}
		
		//----- Zylinder005 -----
		cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
		}
		
		//----- Torus008 -----
		torus { 3.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 14.5>
		}
		
		//----- Ellipsoid004 -----
		sphere { <0, 0, 0> 1
			scale <5.0, 5.0, 1.0>
			translate <0.0, 0.0, 16.0>
		}
		
		//----- Kegel004 -----
		cone { <0, 0, 0>, 6.0
		    <0, 0, 13.0>, 3.0
			translate <0.0, 0.0, 3.0>
		}
		
		translate <60.0, 60.0, 0.0>
	}
	
	//----- King_C3 -----
	union {
	
		//----- Torus018 -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Kegel010 -----
		cone { <0, 0, 0>, 6.0
		    <0, 0, 22.0>, 3.5
			translate <0.0, 0.0, 3.0>
		}
		
		//----- Torus019 -----
		torus { 4.0, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 23.5>
		}
		
		//----- Wuerfel006 -----
		box { <0,0,0>, <6.4, 2.0, 2.0>
			translate <-3.2, -1.0, 34.0>
		}
		
		//----- Wuerfel007 -----
		box { <0,0,0>, <2.0, 2.0, 5.5>
			translate <-1.0, -1.0, 33.0>
		}
		
		//----- Ellipsoid018 -----
		sphere { <0, 0, 0> 1
			scale <5.5, 5.5, 1.0>
			translate <0.0, 0.0, 31.0>
		}
		
		//----- Zylinder018 -----
		cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
		}
		
		//----- Ellipsoid017 -----
		sphere { <0, 0, 0> 1
			scale <5.5, 5.5, 1.0>
			translate <0.0, 0.0, 25.0>
		}
		
		//----- Kugel009 -----
		sphere { <0, 0, 0> 1.8 
			translate <0.0, 0.0, 33.0>
		}
		
		//----- Cut024 -----
		difference {
		
			//----- Kegel011 -----
			cone { <0, 0, 0>, 2.8
			    <0, 0, 9.0>, 5.5
				translate <0.0, 0.0, 22.0>
			}
			
			//----- Torus020 -----
			torus { 12.0, 8.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 26.3>
			}
			
		}
		
		translate <40.0, 40.0, 0.0>
	}
	
	//----- Knight_G4 -----
	union {
	
		//----- Fusion025 -----
		union {
		
			//----- Zylinder019 -----
			cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
			}
			
			//----- Torus021 -----
			torus { 3.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 11.5>
			}
			
			//----- Ellipsoid022 -----
			sphere { <0, 0, 0> 1
				scale <5.0, 5.0, 1.0>
				translate <0.0, 0.0, 13.0>
			}
			
			//----- Kegel012 -----
			cone { <0, 0, 0>, 6.0
			    <0, 0, 10.0>, 3.0
				translate <0.0, 0.0, 3.0>
			}
			
			//----- Torus022 -----
			torus { 5.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 4.5>
			}
			
		}
		
		//----- Fusion027 -----
		union {
		
			//----- Cut025 -----
			difference {
			
				//----- Cut029 -----
				difference {
				
					//----- Cut027 -----
					difference {
					
						//----- Cut028 -----
						difference {
						
							//----- Common001 -----
							intersection {
							
								//----- Cut026 -----
								difference {
								
									//----- Cut030 -----
									difference {
									
										//----- Fusion026 -----
										union {
										
											//----- Ellipsoid023 -----
											sphere { <0, 0, 0> 1
												scale <5.0, 40.0, 8.0>
												rotate <0.0, 45.0, 0.0>
												translate <-3.5, 0.0, 24.5>
											}
											
											//----- Ellipsoid019 -----
											sphere { <0, 0, 0> 1
												scale <5.0, 40.0, 10.0>
												rotate <0.0, 9.0, 0.0>
												translate <1.0, 0.0, 21.0>
											}
											
										}
										
										//----- Ellipsoid024 -----
										sphere { <0, 0, 0> 1
											scale <5.0, 40.0, 20.0>
											rotate <0.0, 31.0, 0.0>
											translate <-6.5, 0.0, 32.5>
										}
										
									}
									
									//----- Ellipsoid020 -----
									sphere { <0, 0, 0> 1
										scale <2.5, 40.0, 10.0>
										rotate <0.0, 42.0, 0.0>
										translate <-8.5, 0.0, 13.5>
									}
									
								}
								
								//----- Wuerfel010 -----
								box { <0,0,0>, <22.0, 10.0, 22.0>
									translate <-13.0, -5.0, 11.0>
								}
								
							}
							
							//----- Wuerfel009 -----
							box { <0,0,0>, <22.0, 4.0, 22.0>
								rotate <0.0, 0.0, -6.0>
								translate <-13.0, -5.0, 11.0>
							}
							
						}
						
						//----- Wuerfel011 -----
						box { <0,0,0>, <22.0, 4.0, 22.0>
							rotate <0.0, 0.0, 6.0>
							translate <-13.0, 1.0, 11.0>
						}
						
					}
					
					//----- Wuerfel008 -----
					box { <0,0,0>, <10.0, 6.0, 10.0>
						translate <-8.0, -3.0, 29.0>
					}
					
				}
				
				//----- Ellipsoid021 -----
				sphere { <0, 0, 0> 1
					scale <6.0, 2.0, 4.0>
					translate <3.0, 0.0, 33.0>
				}
				
			}
			
			//----- Kugel010 -----
			sphere { <0, 0, 0> 0.8 
				translate <-1.5, -2.2, 26.6>
			}
			
			//----- Kugel011 -----
			sphere { <0, 0, 0> 0.8 
				translate <-1.5, 2.2, 26.6>
			}
			
		}
		
		rotate <0.0, 0.0, 27.0>
		translate <120.0, 60.0, 0.0>
	}
	
	//----- Bishop_E1 -----
	difference {
	
		//----- Fusion008 -----
		union {
		
			//----- Fusion007 -----
			union {
			
				//----- Fusion006 -----
				union {
				
					//----- Fusion005 -----
					union {
					
						//----- Fusion004 -----
						union {
						
							//----- Zylinder003 -----
							cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
							}
							
							//----- Kegel001 -----
							cone { <0, 0, 0>, 6.0
							    <0, 0, 18.0>, 3.5
								translate <0.0, 0.0, 3.0>
							}
							
						}
						
						//----- Torus003 -----
						torus { 4.0, 1.0
							rotate <90.0, 0.0, 0.0>
							translate <0.0, 0.0, 19.5>
						}
						
					}
					
					//----- Torus002 -----
					torus { 5.5, 1.0
						rotate <90.0, 0.0, 0.0>
						translate <0.0, 0.0, 4.5>
					}
					
				}
				
				//----- Ellipsoid -----
				sphere { <0, 0, 0> 1
					scale <5.5, 5.5, 1.0>
					translate <0.0, 0.0, 21.0>
				}
				
			}
			
			//----- Ellipsoid001 -----
			sphere { <0, 0, 0> 1
				scale <4.0, 4.0, 6.0>
				translate <0.0, 0.0, 25.0>
			}
			
		}
		
		//----- Quader005 -----
		box { <0,0,0>, <10.0, 10.0, 1.5>
			rotate <0.0, -40.0, 0.0>
			translate <1.0, -5.0, 24.5>
		}
		
		rotate <0.0, 0.0, 140.0>
		translate <80.0, 0.0, 0.0>
	}
	

	material {Black_pieces_material }
	
}

//----- White_pieces -----
union {

	//----- Knight_H3 -----
	union {
	
		//----- Fusion015 -----
		union {
		
			//----- Zylinder015 -----
			cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
			}
			
			//----- Torus013 -----
			torus { 3.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 11.5>
			}
			
			//----- Ellipsoid008 -----
			sphere { <0, 0, 0> 1
				scale <5.0, 5.0, 1.0>
				translate <0.0, 0.0, 13.0>
			}
			
			//----- Kegel007 -----
			cone { <0, 0, 0>, 6.0
			    <0, 0, 10.0>, 3.0
				translate <0.0, 0.0, 3.0>
			}
			
			//----- Torus012 -----
			torus { 5.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 4.5>
			}
			
		}
		
		//----- Fusion017 -----
		union {
		
			//----- Cut023 -----
			difference {
			
				//----- Cut022 -----
				difference {
				
					//----- Cut021 -----
					difference {
					
						//----- Cut020 -----
						difference {
						
							//----- Common -----
							intersection {
							
								//----- Cut019 -----
								difference {
								
									//----- Cut018 -----
									difference {
									
										//----- Fusion016 -----
										union {
										
											//----- Ellipsoid013 -----
											sphere { <0, 0, 0> 1
												scale <5.0, 40.0, 8.0>
												rotate <0.0, 45.0, 0.0>
												translate <-3.5, 0.0, 24.5>
											}
											
											//----- Ellipsoid009 -----
											sphere { <0, 0, 0> 1
												scale <5.0, 40.0, 10.0>
												rotate <0.0, 9.0, 0.0>
												translate <1.0, 0.0, 21.0>
											}
											
										}
										
										//----- Ellipsoid011 -----
										sphere { <0, 0, 0> 1
											scale <5.0, 40.0, 20.0>
											rotate <0.0, 31.0, 0.0>
											translate <-6.5, 0.0, 32.5>
										}
										
									}
									
									//----- Ellipsoid012 -----
									sphere { <0, 0, 0> 1
										scale <2.5, 40.0, 10.0>
										rotate <0.0, 42.0, 0.0>
										translate <-8.5, 0.0, 13.5>
									}
									
								}
								
								//----- Wuerfel002 -----
								box { <0,0,0>, <22.0, 10.0, 22.0>
									translate <-13.0, -5.0, 11.0>
								}
								
							}
							
							//----- Wuerfel005 -----
							box { <0,0,0>, <22.0, 4.0, 22.0>
								rotate <0.0, 0.0, -6.0>
								translate <-13.0, -5.0, 11.0>
							}
							
						}
						
						//----- Wuerfel004 -----
						box { <0,0,0>, <22.0, 4.0, 22.0>
							rotate <0.0, 0.0, 6.0>
							translate <-13.0, 1.0, 11.0>
						}
						
					}
					
					//----- Wuerfel003 -----
					box { <0,0,0>, <10.0, 6.0, 10.0>
						translate <-8.0, -3.0, 29.0>
					}
					
				}
				
				//----- Ellipsoid014 -----
				sphere { <0, 0, 0> 1
					scale <6.0, 2.0, 4.0>
					translate <3.0, 0.0, 33.0>
				}
				
			}
			
			//----- Kugel004 -----
			sphere { <0, 0, 0> 0.8 
				translate <-1.5, -2.2, 26.6>
			}
			
			//----- Kugel005 -----
			sphere { <0, 0, 0> 0.8 
				translate <-1.5, 2.2, 26.6>
			}
			
		}
		
		rotate <0.0, 0.0, 27.0>
		translate <140.0, 40.0, 0.0>
	}
	
	//----- Rook_B2 -----
	union {
	
		//----- Torus -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Fusion002 -----
		union {
		
			//----- Torus001 -----
			torus { 4.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 19.5>
			}
			
			//----- Fusion001 -----
			union {
			
				//----- Zylinder -----
				cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
				}
				
				//----- Fusion -----
				union {
				
					//----- Kegel -----
					cone { <0, 0, 0>, 6.0
					    <0, 0, 18.0>, 4.5
						translate <0.0, 0.0, 3.0>
					}
					
					//----- Cut005 -----
					difference {
					
						//----- Cut004 -----
						difference {
						
							//----- Cut003 -----
							difference {
							
								//----- Cut002 -----
								difference {
								
									//----- Cut001 -----
									difference {
									
										//----- Cut -----
										difference {
										
											//----- Zylinder001 -----
											cylinder { <0, 0, 0>, <0, 0, 5.0>, 6.0
												translate <0.0, 0.0, 20.5>
											}
											
											//----- Zylinder002 -----
											cylinder { <0, 0, 0>, <0, 0, 10.0>, 4.5
												translate <0.0, 0.0, 22.5>
											}
											
										}
										
										//----- Quader -----
										box { <0,0,0>, <14.0, 1.7, 4.0>
											translate <-7.0, -1.0, 23.5>
										}
										
									}
									
									//----- Quader001 -----
									box { <0,0,0>, <14.0, 1.7, 4.0>
										rotate <0.0, 0.0, 36.0>
										translate <-5.07533370833, -4.92351376042, 23.5>
									}
									
								}
								
								//----- Quader002 -----
								box { <0,0,0>, <14.0, 1.7, 4.0>
									rotate <0.0, 0.0, 72.0>
									translate <-1.21206244433, -6.96641260844, 23.5>
								}
								
							}
							
							//----- Quader003 -----
							box { <0,0,0>, <14.0, 1.7, 4.0>
								rotate <0.0, 0.0, 108.0>
								translate <3.11417547692, -6.34837861969, 23.5>
							}
							
						}
						
						//----- Quader004 -----
						box { <0,0,0>, <14.0, 1.7, 4.0>
							rotate <0.0, 0.0, 144.0>
							translate <6.25090421292, -3.30547977167, 23.5>
						}
						
					}
					
				}
				
			}
			
		}
		
		translate <20.0, 20.0, 0.0>
	}
	
	//----- King_E4 -----
	union {
	
		//----- Torus004 -----
		torus { 5.5, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 4.5>
		}
		
		//----- Kegel002 -----
		cone { <0, 0, 0>, 6.0
		    <0, 0, 22.0>, 3.5
			translate <0.0, 0.0, 3.0>
		}
		
		//----- Torus005 -----
		torus { 4.0, 1.0
			rotate <90.0, 0.0, 0.0>
			translate <0.0, 0.0, 23.5>
		}
		
		//----- Wuerfel001 -----
		box { <0,0,0>, <6.4, 2.0, 2.0>
			translate <-3.2, -1.0, 34.0>
		}
		
		//----- Wuerfel -----
		box { <0,0,0>, <2.0, 2.0, 5.5>
			translate <-1.0, -1.0, 33.0>
		}
		
		//----- Ellipsoid003 -----
		sphere { <0, 0, 0> 1
			scale <5.5, 5.5, 1.0>
			translate <0.0, 0.0, 31.0>
		}
		
		//----- Zylinder004 -----
		cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
		}
		
		//----- Ellipsoid002 -----
		sphere { <0, 0, 0> 1
			scale <5.5, 5.5, 1.0>
			translate <0.0, 0.0, 25.0>
		}
		
		//----- Kugel -----
		sphere { <0, 0, 0> 1.8 
			translate <0.0, 0.0, 33.0>
		}
		
		//----- Cut007 -----
		difference {
		
			//----- Kegel003 -----
			cone { <0, 0, 0>, 2.8
			    <0, 0, 9.0>, 5.5
				translate <0.0, 0.0, 22.0>
			}
			
			//----- Torus006 -----
			torus { 12.0, 8.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 26.3>
			}
			
		}
		
		translate <80.0, 60.0, 0.0>
	}
	
	//----- Queen_E2 -----
	union {
	
		//----- Fusion012 -----
		union {
		
			//----- Torus009 -----
			torus { 5.5, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 4.5>
			}
			
			//----- Kegel005 -----
			cone { <0, 0, 0>, 6.0
			    <0, 0, 22.0>, 3.5
				translate <0.0, 0.0, 3.0>
			}
			
			//----- Kugel002 -----
			sphere { <0, 0, 0> 1.2 
				translate <0.0, 0.0, 32.0>
			}
			
			//----- Torus010 -----
			torus { 4.0, 1.0
				rotate <90.0, 0.0, 0.0>
				translate <0.0, 0.0, 21.5>
			}
			
			//----- Ellipsoid005 -----
			sphere { <0, 0, 0> 1
				scale <5.5, 5.5, 1.0>
				translate <0.0, 0.0, 23.0>
			}
			
			//----- Zylinder006 -----
			cylinder { <0, 0, 0>, <0, 0, 3.5>, 7.0
			}
			
			//----- Ellipsoid007 -----
			sphere { <0, 0, 0> 1
				scale <3.5, 3.5, 5.5>
				translate <0.0, 0.0, 26.0>
			}
			
		}
		
		//----- Cut017 -----
		difference {
		
			//----- Cut016 -----
			difference {
			
				//----- Cut015 -----
				difference {
				
					//----- Cut014 -----
					difference {
					
						//----- Cut013 -----
						difference {
						
							//----- Cut012 -----
							difference {
							
								//----- Cut011 -----
								difference {
								
									//----- Cut010 -----
									difference {
									
										//----- Cut009 -----
										difference {
										
											//----- Fusion011 -----
											union {
											
												//----- Cut008 -----
												difference {
												
													//----- Kegel006 -----
													cone { <0, 0, 0>, 2.8
													    <0, 0, 9.0>, 5.4
														translate <0.0, 0.0, 19.0>
													}
													
													//----- Torus011 -----
													torus { 12.0, 8.0
														rotate <90.0, 0.0, 0.0>
														translate <0.0, 0.0, 23.3>
													}
													
												}
												
												//----- Ellipsoid006 -----
												sphere { <0, 0, 0> 1
													scale <5.4, 5.4, 2.0>
													translate <0.0, 0.0, 28.0>
												}
												
											}
											
											//----- Kugel003 -----
											sphere { <0, 0, 0> 5 
												translate <0.0, 0.0, 31.0>
											}
											
										}
										
										//----- Zylinder007 -----
										cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
											rotate <0.0, -45.0, 0.0>
											translate <7.0, 0.0, 26.5>
										}
										
									}
									
									//----- Zylinder008 -----
									cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
										rotate <3.14858849648e-14, -45.0, 45.0>
										translate <4.94974746831, 4.94974746831, 26.5>
									}
									
								}
								
								//----- Zylinder009 -----
								cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
									rotate <0.0, -45.0, 90.0>
									translate <2e-15, 7.0, 26.5>
								}
								
							}
							
							//----- Zylinder010 -----
							cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
								rotate <4.49798356639e-15, -45.0, 135.0>
								translate <-4.94974746831, 4.94974746831, 26.5>
							}
							
						}
						
						//----- Zylinder011 -----
						cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
							rotate <0.0, -45.0, 180.0>
							translate <-7.0, 1e-15, 26.5>
						}
						
					}
					
					//----- Zylinder012 -----
					cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
						rotate <-3.82328603144e-14, -45.0, -135.0>
						translate <-4.94974746831, -4.94974746831, 26.5>
					}
					
				}
				
				//----- Zylinder013 -----
				cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
					rotate <-8.09637041951e-14, -45.0, -90.0>
					translate <-2e-15, -7.0, 26.5>
				}
				
			}
			
			//----- Zylinder014 -----
			cylinder { <0, 0, 0>, <0, 0, 6.0>, 1.2
				rotate <-3.14858849648e-14, -45.0, -45.0>
				translate <4.94974746831, -4.94974746831, 26.5>
			}
			
		}
		
		translate <80.0, 20.0, 0.0>
	}
	

	material {White_pieces_material }
	
}

//----- Frame -----
box { <0,0,0>, <180.0, 180.0, 6.0>
	translate <-20.0, -20.0, -6.02>

	material {Frame_material }
	
}

//----- SpotLight -----
light_source { <0, 0, 0>
	color rgb<1.0, 1.0, 1.0>
	spotlight
	point_at <0, -1, 0>
	radius 60.0
	falloff 60.0
	tightness 100
	rotate <90.0, 0.0, 0.0>
	translate <80.0, 60.0, 100.0>
}

//----- PointLight -----
light_source { <0, 0, 0>
	color rgb<0.219999998808, 0.219999998808, 0.219999998808>
	translate <100.0, -40.0, 100.0>
}
