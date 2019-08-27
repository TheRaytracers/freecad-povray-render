# Tips & Tricks for the macro

* You can change the background of FreeCAD under Edit/Preferences/Display/Colors/Background Color. You can also add a middle color.
* For side views, try the orthographic view. But for a non side view, don't use the orthographic view. That doesn't look realistic
* Try to get a more realistic image: [Rendering a photorealistic Scene - Step by Step](realistic.md)
* If you have a big scene with a lot of objects and many materials with light refraction, try a little size of the image first, because then you not must wait for a long time.
* If you create a cut with two touching surfaces in FreeCAD, nothing remains. With POVray, however, an infinitely thin layer remains:

  ![FreeCAD before cutting](img/tipsAndTricks/01_FC.png "FreeCAD before cutting")
  ![POVray before cutting](img/tipsAndTricks/01_PR.png "POVray before cutting")

  Then you cut the two boxes.

  ![FreeCAD after cutting](img/tipsAndTricks/02_FC.png "FreeCAD after cutting")
  ![POVray after cutting](img/tipsAndTricks/02_PR.png "POVray after cutting")

  To avoid this, the part to be removed should be slightly larger than the other part.
