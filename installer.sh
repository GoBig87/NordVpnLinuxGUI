#!/bin/bash
# Install nordvpn
sudo usermod -aG nordvpn $USER
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

# Setup venv and install packages
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "No Python3 detected"
fi
echo $version
sudo apt update
sudo apt install -y xclip
sudo apt install python3-pip
sudo apt install python3-venv
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
sudo cp /usr/share/applications/NordVPN.desktop ~/Desktop/NordVPN.desktop
sudo chown $USER ~/Desktop/NordVPN.desktop
echo "Finished Installation"
echo "To Enable desktop launching, right click on the NordVON.desktop cog Icon and right click and select 'Allow Launching'"