#declare BasicDice_material = material {
  texture {
    pigment{ color rgbt<1,0,0,0.25> }
    finish {
      phong 1.0
      brilliance 4
    }
  }

  interior {
    ior 1.0
  }
}
