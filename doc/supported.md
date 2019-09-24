# Supported Features
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

The macro doesn't support AngleN (Angle, Angle1, Angle2, etc.) for cylinder, sphere, cone, torus and ellipsoid

### Boolean

- [x] Union
- [x] Cut
- [x] Difference

## Draft Workbench

- [x] Clone
- [x] Array linear pattern
- [x] Array polar pattern

## Other

- [x] Group
- [x] Part


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

The macro simulates objects which aren't supported already with a mesh. The meshes are in an extra file with the name `name_meshes.inc`. But doubt, that the creation of a mesh needs a lot of cpu time.
