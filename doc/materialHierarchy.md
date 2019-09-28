If you try to add textures to your objects via the .inc file you may start with some error messages.
A common cause of these messages is a incorrect usage of the material hierarchy. In the [future developement](roadmap.md) of the macro things should become easier. But actually `material{}` is the only statement one can use to add properties to objects. The macro won't look for other statements like `texture{}` or `pigment{}`.
But that does not mean, that you can't use these statements. You just have to put them into the `material` brackets in their right hierarchical order:
```
XXX hierarchy code
```
