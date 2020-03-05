import FreeCADGui as Gui
import FreeCAD as App

class PovRay (Workbench):
	"Workbench object to export models to POV-Ray"
	
	Icon = """
			/* XPM */
			static char * logo_xpm[] = {
			"16 16 121 2",
			"  	c None",
			". 	c #3C8CF4",
			"+ 	c #3D91F5",
			"@ 	c #3F99F5",
			"# 	c #419EF6",
			"$ 	c #3168F2",
			"% 	c #336DF2",
			"& 	c #3573F3",
			"* 	c #367AF3",
			"= 	c #3980F3",
			"- 	c #3A86F4",
			"; 	c #3C8DF4",
			"> 	c #3E93F5",
			", 	c #4099F5",
			"' 	c #43A0F7",
			") 	c #44A7F7",
			"! 	c #44ACF7",
			"~ 	c #48B2F7",
			"{ 	c #4AB9F7",
			"] 	c #2D5CF1",
			"^ 	c #2F62F1",
			"/ 	c #3169F2",
			"( 	c #336FF2",
			"_ 	c #3575F3",
			": 	c #377CF3",
			"< 	c #3982F4",
			"[ 	c #3B88F4",
			"} 	c #3D8FF5",
			"| 	c #3E95F5",
			"1 	c #409BF5",
			"2 	c #42A2F6",
			"3 	c #44A8F6",
			"4 	c #46AEF7",
			"5 	c #48B5F7",
			"6 	c #4ABBF9",
			"7 	c #2C57F1",
			"8 	c #2E5EF1",
			"9 	c #3064F2",
			"0 	c #326AF2",
			"a 	c #3471F2",
			"b 	c #3677F3",
			"c 	c #377DF3",
			"d 	c #3984F4",
			"e 	c #3B8AF4",
			"f 	c #3D90F5",
			"g 	c #3F97F5",
			"h 	c #419DF6",
			"i 	c #43A3F6",
			"j 	c #45AAF6",
			"k 	c #47B0F7",
			"l 	c #48B6F7",
			"m 	c #2B54F1",
			"n 	c #2F60F2",
			"o 	c #326CF2",
			"p 	c #3472F3",
			"q 	c #3E92F5",
			"r 	c #419FF6",
			"s 	c #43A5F6",
			"t 	c #47B2F7",
			"u 	c #294EF1",
			"v 	c #2D5BF1",
			"w 	c #2F61F1",
			"x 	c #336AF2",
			"y 	c #3A87F4",
			"z 	c #43A4F6",
			"A 	c #3C8EF4",
			"B 	c #42A0F5",
			"C 	c #46ADF7",
			"D 	c #2849F1",
			"E 	c #3063F2",
			"F 	c #294CF0",
			"G 	c #44A3F6",
			"H 	c #3C89F4",
			"I 	c #3D8FF6",
			"J 	c #3F96F5",
			"K 	c #44A9F6",
			"L 	c #2745EF",
			"M 	c #2A52F0",
			"N 	c #2C58F1",
			"O 	c #3165F2",
			"P 	c #2133EF",
			"Q 	c #3A84F4",
			"R 	c #3B8BF4",
			"S 	c #2641EF",
			"T 	c #2648EF",
			"U 	c #294DF0",
			"V 	c #2B54F0",
			"W 	c #2D5AF1",
			"X 	c #2F60F1",
			"Y 	c #367AF4",
			"Z 	c #3880F4",
			"` 	c #42A0F6",
			" .	c #243CEF",
			"..	c #2642EF",
			"+.	c #2849F0",
			"@.	c #2A4FF0",
			"#.	c #2C55F1",
			"$.	c #377BF3",
			"%.	c #3D8EF5",
			"&.	c #2337ED",
			"*.	c #253EEF",
			"=.	c #2644EF",
			"-.	c #284AF0",
			";.	c #2A51F0",
			">.	c #2E5DF1",
			",.	c #3470F2",
			"'.	c #3983F4",
			").	c #3F96F4",
			"!.	c #2338F0",
			"~.	c #2640EF",
			"{.	c #2746EF",
			"].	c #2B53F0",
			"^.	c #2D59F1",
			"/.	c #2E5FF1",
			"(.	c #3067F3",
			"_.	c #326CF3",
			":.	c #3572F3",
			"<.	c #3679F3",
			"[.	c #3880F3",
			"}.	c #3A85F4",
			"|.	c #3D8BF4",
			"                                ",
			"                                ",
			"            . + @ #             ",
			"  $ % & * = - ; > , ' ) ! ~ {   ",
			"] ^ / ( _ : < [ } | 1 2 3 4 5 6 ",
			"7 8 9 0 a b c d e f g h i j k l ",
			"m   n   o p       ; q   r s   t ",
			"u   v w     x y z   A   1 B ) C ",
			"D       E   F / - G H I J   2 K ",
			"L   M N 8 O P F /   Q R     # z ",
			"S T U V W X $     Y Z - ; > , ` ",
			" ...+.@.#.] ^ $ ( _ $.< [ %.| 1 ",
			"&.*.=.-.;.7 >.9 0 ,.b c '.e f ).",
			"  !.~.{.F ].^./.(._.:.<.[.}.|.  ",
			"                                ",
			"                                "};
			"""
			
	MenuText = "POV-Ray"
	ToolTip = "Export FreeCAD Models to POV-Ray"
	
	def GetClassName(self):
		return "Gui::PythonWorkbench"
	
	def Initialize(self):
		import Export, LightCommands, helpDefs
		self.appendToolbar("POV-Ray", ["Export", "PointLightCommand"])
		self.appendMenu("&POV-Ray", ["Export", "PointLightCommand"])

		Gui.addIconPath(helpDefs.initGui__iconPath)

		Log ("Loading Export to POV-Ray... done\n")

	def Activated(self):
		Msg ("PovRay.Activated()\n")

	def Deactivated(self):
		Msg ("PovRay.Deactivated()\n")

Gui.addWorkbench(PovRay)
