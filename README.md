Run Python rgb-led-sink:
sudo python -E demo_redis.py --profile test_files/test-matrix-config.yaml

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


---------------------
## Raspi betankung:

clone repository for library: https://github.com/hzeller/rpi-rgb-led-matrix

clone repository homerun matrix: https://github.com/stuttgart-things/homerun-matrix-catcher.git

```bash
sudo apt install python3.12-venv -y
python3 -m venv .venv
source .venv/bin/activate

sudo apt install make -y
sudo apt install g++ -y 
sudo apt install python3-pip -y

# cd homerun-matrix-catcher/
pip install -r requirements.txt

```

lib installieren:
ref:
https://codehub.sva.de/Lab/stuttgart-things/dev/homerun-matrix-catcher
auf hier klicken
https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python

in lib/Makefile HARDWARE_DESC? auf adafruit-hat-pwm

```bash
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
cd /bindings/python
make build-python 
sudo make install-python 

#Audiotreiber deaktivieren
cd /etc/modprobe.d/blacklist #rebootfeste einstellung - snd_bcm2835 in die file schreiben
# nicht reboot fester command
modprobe -r snd_bcm2835
```

---------------------------------------------------



(make -C examples-api-use)
(sudo examples-api-use/demo -D 1 examples-api-use/runtext.ppm --led-no-hardware-pulse --led-gpio-mapping=adafruit-hat)


execute:
sudo -E  python3 -E demo_generate.py --profile test_files/test-matrix-config.yaml
oder 
deactivate venv
sudo  python3 -E demo_generate.py --profile test_files/test-matrix-config.yaml


next steps:
https://docs.python.org/3/library/unittest.mock.html

