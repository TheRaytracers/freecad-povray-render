# Macro for exporting a FreeCAD model to POVray

## Wiki
Here is the wiki for the macro: [Wiki](doc/index.md)

---

Das ExportToPovRay Makro soll möglichst alle soliden CSG Objekte aus
der FreeCAD part Workbench in eine entsprechende POVray
Szenenbeschreibung konvertieren. Dabei wird der Objektbaum mit seinen
boolschen Operationen in der Povray Datei abgebildet.
Der User soll anschießend die POVray Datei abändern können, so daß die
umfangreichen Möglichkeiten von POVray für eine fotorealiste Darstellung
genutzt werden können (Texturen, Lichteffekte u.ä.)
Oberstes Prinzip ist dabei, die POVray Datei so übersichtlich zu halten,
dass Objekte schnell auffindbar sind.
Ein zweites wichtiges Prinzip ist "what you see is what you get".
Das Renderergebnis sieht der jeweiligen Ansicht im FreeCAD Gui so
ähnlich wie möglich (Kameraperspektive, Hintergrund, Objektfarben...).
Da eine vollständige Übernahme aller FreeCAD Konstruktionsmöglichkeiten
zu aufwändig wäre, beschränkt sich das Makro zunächst auf CSG-Objekte -
Diese Limitierung ist für den User aber klar nachvollziehbar - entweder
durch eine gute Dokumentation oder aber im Programm z.B. durch farbliche
Markierung von übernommenen Objekten im Objektbaum.

---

The ExportToPovRay macro is intended to export as many solid CSG objects as possible from
of the FreeCAD Part workbench into a corresponding POVray
Convert scene description. The object tree with its
Boolean operations in the Povray file.
The user should then be able to modify the POVray file so that the
extensive possibilities of POVray for a photorealistic display
can be used (textures, light effects, etc.)
The main principle is to keep the POVray file as clear as possible,
that objects can be found quickly.
A second important principle is "what you see is what you get".
The render result of the respective view in FreeCAD Gui looks like this
as possible (camera perspective, background, object colors...).
Since a complete transfer of all FreeCAD construction possibilities is possible
would be too complex, the macro is initially limited to CSG objects -
However, this limitation is clearly comprehensible for the user - either
through a good documentation or in the program e.g. through colored
Selection of transferred objects in the object tree.

Translated with www.DeepL.com/Translator
