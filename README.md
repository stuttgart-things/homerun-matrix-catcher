
# Raspbian Setup:

OS-Requirement:
* Raspberry Pi OS (Legacy) Lite
* Release date: October 22nd 2024
* System: 32-bit
* Kernel version: 6.1
* Debian version: 11 (bullseye)

(Python: Python3.9)

(donwload-link: [https://downloads.raspberrypi.com/raspios_oldstable_lite_armhf/images/raspios_oldstable_lite_armhf-2024-10-28/2024-10-22-raspios-bullseye-armhf-lite.img.xz])


## Activate SSH

```bash
# Use the arrow keys to navigate to Interface Options and press Enter.
# Select SSH and press Enter.
# You will be asked if you want to enable the SSH server. Select Yes and press Enter.
# After enabling SSH, navigate to Finish and press Enter.
# You may be prompted to reboot your Raspberry Pi. If so, select Yes to reboot.
sudo raspi-config
```

## Virtual environment download, install and setup

```bash
sudo apt install python3-venv
python3 -m venv .venv
```

```bash
# Activate venv on login
echo -e "\n# Activate virtual environment on login\nif [ -d \"/home/sthings/.venv\" ]; then\n    source .venv/bin/activate\nfi" >> /home/sthings/.profile
source /home/sthings/.profile
```

## Run Ansible to install tools

Inventory
```bash
cat <<EOF > /tmp/inventory_raspi
192.168.1.xxx ansible_user=sthings ansible_password=<password> ansible_become_pass=<password> ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
```

Ansible play
```bash
cat <<EOF > /tmp/raspi-betankung.yaml
- name: Install essential tools on Raspbian
  hosts: "{{ target_host | default('all') }}"
  become: yes
  vars:
    os_packages:
      - git
      - curl
      - unzip
      - wget
      - make
      - g++
      - python3-pip
      - python3-dev
      - cython3

  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: yes

    - name: Install git, curl, and wget etc..
      ansible.builtin.apt:
        name: "{{ os_packages }}"
        state: present
EOF
```

```bash
ansible-playbook -i /tmp/inventory_raspi /tmp/raspi-betankung.yaml -vv
```

## Create Directories and download Repos

```bash
mkdir lib &&
mkdir homerun-matrix-catcher
```

```bash
cd lib &&
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
```

```bash
cd /home/sthings/ &&
wget https://github.com/stuttgart-things/homerun-matrix-catcher/releases/download/0.1.1/homerun-matrix-catcher.tar.gz &&
tar -xzf homerun-matrix-catcher.tar.gz -C ./homerun-matrix-catcher
```

## Install python requirements

```bash
pip install -r /home/sthings/homerun-matrix-catcher/requirements_new_raspi.txt
```

OR

<details><summary>Save requirements to file and scp to new raspi</summary>

```bash
# execute on original raspi
pip freeze > /tmp/requirements_new_raspi.txt
scp /tmp/requirements_new_raspi.txt sthings@192.168.1.xxx:/tmp/requirements_new_raspi.txt

# execute on new raspi
pip install -r /tmp/requirements_new_raspi.txt
```

</details>

## Build and install matrix library

(reference Readme at: [https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python])

Edit /lib/Makefile
```
# Comment out this line (no):
HARDWARE_DESC?=regular

# Uncomment this line (yes):
#HARDWARE_DESC=adafruit-hat-pwm
```

```bash
sudo nano /home/sthings/lib/rpi-rgb-led-matrix/lib/Makefile
```

```bash
sudo -i
```

```bash
# Activate venv while root
cd /home/sthings &&
source .venv/bin/activate
```

```bash
# Build and install matrix library
cd lib/rpi-rgb-led-matrix//bindings/python
make build-python 
make install-python 
```

## Deaktivate Audiodriver

```bash
# save for reboot
cat <<EOF > /etc/modprobe.d/blacklist
snd_bcm2835
EOF
```

```bash
sudo update-initramfs -u
```

## Execute

```bash
cd /home/sthings/homerun-matrix-catcher &&
python3 -E demo_generate.py --profile rules/test-matrix-config.yaml
```
