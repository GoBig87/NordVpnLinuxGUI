#!/bin/bash

install_manjaro() {
  pamac build nordvpn-bin
  sudo systemctl enable --now nordvpnd

  pamac install xclip
  pamac install python3-pip
  pamac install python3-venv
}

install_debian() {
  # Install nordvpn
  sudo apt install curl
  sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

  sudo apt update
  sudo apt install -y xclip
  sudo apt install python3-pip
  sudo apt install python3-venv
}

if [ "$EUID" -eq 0 ]
  then echo "Please do not run as root.  Commands that need root access will request it."
  exit
fi

version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "No Python3 detected.  Install Python3 to install"
    exit
fi
echo $version

source /etc/lsb-release
if [ "$DISTRIB_ID" = "ManjaroLinux" ]; then
  install_manjaro
else
  install_debian
fi

sudo usermod -aG nordvpn $USER

python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt

echo "Creating desktop Icon"
FILE_NAME="${PWD}/NordVPN.desktop"
echo ${FILE_NAME}
touch NordVPN.desktop
cat > $FILE_NAME <<EOF
#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec=${PWD}/NordVPNLinuxGUI.sh
Name=NordVPN
Icon=${PWD}/icon.jpg
X-Desktop-File-Install-Version=0.24

EOF

sudo cp $FILE_NAME /usr/share/applications/NordVPN.desktop
sudo cp /usr/share/applications/NordVPN.desktop /home/$USER/Desktop/NordVPN.desktop
sudo chown $USER /home/$USER/Desktop/NordVPN.desktop
echo "Finished Installation"
echo "To Enable desktop launching, right click on the NordVPN.desktop cog Icon and right click and select 'Allow Launching'"

