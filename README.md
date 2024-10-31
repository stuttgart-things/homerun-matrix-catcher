Modes:
	- image
		- file: Name of file within visual_aid/ or url.
		- time: Time to display image. Input 0 for infinit display.
		- size: Size of image within matrix. Ex. 32x32. Input "full" for fullscreen.

	- gif
		- file: Name of file within visual_aid/ or url.
		- time: Time to display gif. Input 0 for infinit display.
		- size: Size of gif within matrix. Ex. 32x32. Input "full" for fullscreen.
		- speed: Speed of gif. Speed options [1,2,3,4,5]. Default speed: 2.

	- text
		- text:
		- font:
		- color:
		- speed: 
		- time:

	- ticker
		- text:
		- font:
		- color:
		- speed: 
		- loops: 


Input Example:

	- {"Mode":"text", "Args":{"text":"Hallo Sthings!","font":"9x18.bdf", "color":"(164,38,201)"}}
	- {"Mode":"image"}
	- {"Mode":"gif", "Args":{"file":"https://i.gifer.com/XOsX.gif"}}
	- {"Mode":"gif", "Args":{"file":"https://i.gifer.com/XOsX.gif","size":"32x32", "speed":"5"}}
