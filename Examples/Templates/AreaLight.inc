/*
* You can use this template for your inc file. Just copy and paste
* this code to your inc file to get a more realistic image.
* But doubt, that this is only a pattern, you can edit values
* for your specific case.
*
* This template defines an area light at the position of the camera.
* The area light creates softer and more realistic shadows.
*
* You can use this values as are variable (in POVray a "#declare"):
* CamPosition : The position of the camera
* CamRotation : The rotation of the camera (with no rotation, the camera looks to <0, 1, 0>)
* CamRight    : The up vector of the camera
* CamUp       : The right vector of the camera
*/

// Area light
light_source {
    <0, 0, 0>
    color rgb <0.5,0.5,0.5>
    area_light <10, 0, 0>, <0, 0, 10>, 10, 10
    adaptive 1
    jitter
    rotate CamRotation
    translate CamPosition
}
