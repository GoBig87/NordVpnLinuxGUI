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
pip install -r requirements.txt

echo "Finished Installation"