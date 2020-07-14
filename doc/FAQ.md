# FAQ

* **I get no image, only the other files**
  * Are you sure, that you installed POV-Ray?
  * Does the path to the executable exists in the settings of the workbench?
  * Maybe there is an error in your _user.inc file. You will get a error window and a error file can be found in the directory of the .pov file.
  * If there is a mistake in the pov file, then the workbench has a bug. Please report the bug (see below), so that other users won't have this problem.

* **Which objects are supported?**  
  We created a page with all supported objects and the objects we support hopefully soon: [Supported Features](Supported.md)

* **The created mesh looks very rough, what can I do?**  
  You can change two parameters to adjust the mesh resolution. Select the object in FreeCAD and go to the view tab, there you can find the two options `Angular Deflection` and `Deviation`, the smaller you set them, the more accurate the mesh becomes, but the longer it takes to create the mesh.  
  Both parameters are related, `Angular Deflection` indicates the maximum deviation of the angle, and `Deviation` indicates the maximum distance between the mesh and the original object.  

  **Tip:** Don't set the parameters too small, instead start with a larger value and find good textures, etc. first. When you're done, set the mesh accuracy higher and finish your final rendering. The creation of a fine mesh needs a lot of time.

* **The rendered image doesn't look realistic, but plastic**  
  Look here for tips to [Get a more realistic rendering](Realistic.md).

* **I found a bug in the workbench**  
  Please report the bug to us, so we hopefully can fix it soon.  
  You can report the bug via
  * A GitLab Issue: [Create an Issue](https://gitlab.com/usbhub/exporttoPOV-Ray/issues) (Green button top right)
  * Email: the.raytracersABCweb.de replace ABC with an @
  * The FreeCAD Forum: XXX

* **I want to learn more about POV-Ray**  
  * You can watch this very good tutorial:  
  [http://f-lohmueller.de/pov_tut/pov__eng.htm](http://f-lohmueller.de/pov_tut/pov__eng.htm)  
  * You can find the official POV-Ray documentation here:  
  [http://www.POV-Ray.org/documentation/index-3.6.php](http://www.POV-Ray.org/documentation/index-3.6.php)

* **I want to contribute to the workbench**  
  Cool, a software is never finished :-)  
  Please read [How to Contribute](../CONTRIBUTING.md) and start coding!  
  Or report a bug (see above), this is also contributing and not less important than coding! Without bug reporting the problem won't be solved and every user will have it!
