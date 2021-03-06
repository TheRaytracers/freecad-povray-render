# Supported Features

The workbench supports many objects from FreeCAD but not all. Here's a list of the supported objects (checked) and the not supported objects (unchecked) we hope to support soon.

## Part Workbench

### Solids

- [x] Cube
- [x] Cylinder
- [x] Sphere
- [x] Cone
- [x] Torus
- [x] Ellipsoid
- [x] Plane
- [ ] Wedge
- [ ] Prism
- [x] Compound
- [x] Extrude (only sketches as base)

The workbench doesn't support AngleN (Angle, Angle1, Angle2, etc.) for cylinder, sphere, cone, torus and ellipsoid

### Boolean

- [x] Union
- [x] Cut
- [x] Difference

## PartDesign Workbench

- [x] Body
- [x] Pad
- [x] Pocket
- [ ] Revolution
- [ ] Groove
- [ ] Linear Pattern
- [ ] Polar Pattern

### Sketches

- [x] Line Segment
- [x] Arc
- [x] Circle
- [x] B-Spline
- [ ] Ellipse
- [ ] B-Spline

## Draft Workbench

- [x] Clone
- [x] Linear Array
- [x] Polar Array

## Image Workbench

- [x] Image Plane

## Lights

- [x] Point Light
- [x] Area Light
- [x] Spot Light
- [x] Light Fading
- [x] Light Color
- [x] Indirect Lightning

## Other

- [x] Group
- [x] Std Part

## Texture

- [x] Color
- [x] Transparency
- [x] AmbientColor
- [x] EmissiveColor
- [x] SpecularColor
- [x] Shininess

## Camera

- [x] Orthographic
- [x] Perspective

## Background

- [x] Background (you can change the background under Edit/Preferences/Display/Colors/Background Color)

## Non supported objects

- [x] will be rendered as mesh

The workbench simulates objects which aren't supported already with a mesh. The meshes are in an extra file with the name `name_meshes.inc`. But doubt, that the creation of a mesh needs a lot of cpu time. See [Mesh resolution and rendering time](tipsAndTricks.md#mesh-resolution-and-rendering-time)
