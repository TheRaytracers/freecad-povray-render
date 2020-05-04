# Light Properties

The light objects have many properties and settings that we explain here.

## General Light Properties for all Lights

* **Color**  
  Here you can define in which color the lights should shine  
  **Tip**: With the color you can also change the intensity. Just change the brightness of the color in the color dialog.

In reality the light intensity decreases with distance. With Fading Distance and Fading Power you can set the specific fading settings (if one of the two values are 0, fading is disabled):

* **Fading Distance**  
  This is the distance from the light to where the light has the intensity of the light without fading.
* **Fading Power**  
  This is the exponent of the decreasing. Higher the value, higher the decreasing.  
  ![Comparison between different fading powers](img/LightFadingPower.png)  
  **Tip**: A good starting point for fading power is 2.

## Point Light

The point light has no additional properties (except the placement).

## Area Light

![Image to explain Area Light](img/AreaLight.png)

* **Adaptive**  
  XXX
* **Area Illumination**  
  XXX
* **Jitter**  
  XXX
* **Length**  
  The length (x axis) of the area light.
* **Length Lights**  
  The number of lights along the length axis.
* **Width**  
  The width (y axis) of the area light.
* **Width Lights**  
  The number of lights along the width axis.

## Spot Light

![Image to explain Spot Lights](img/SpotLight.png)

* **Fall Off**  
  The angle of the cone where the light is fading down.
* **Radius**  
  The angle of the cone where the light has the full intensity.
* **Tightness**  
  Exponential softening of the light (higher = sharper).
