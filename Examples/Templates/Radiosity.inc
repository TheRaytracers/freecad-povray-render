/*
* You can use this template for your inc file. Just copy and paste
* this code to your inc file to get a more realistic image.
* But doubt, that this is only a pattern, you can edit values
* for your specific case.
*
* This template uses raytracing with the Radiosity_OutdoorHQ mode.
*/

// Raytracing
#include "rad_def.inc"
global_settings {
   radiosity {
      Rad_Settings(Radiosity_OutdoorHQ, off, off)
   }
}
