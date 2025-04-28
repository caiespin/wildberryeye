#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check for SSID and Password arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SSID PASSWORD"
    exit 1
fi

SSID=$1
PASSWORD=$2

# Install necessary packages
echo "Installing necessary packages..."
apt-get update
apt-get install -y debconf-utils
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections
apt-get install -y dhcpcd5 hostapd dnsmasq iptables-persistent

# Stop and disable potentially conflicting services
echo "Stopping and disabling wpa_supplicant..."
systemctl stop wpa_supplicant
systemctl disable wpa_supplicant

# Ensure the wireless interface is up
echo "Bringing up wlan0 interface..."
ip link set wlan0 up

# Configure DHCP client
echo "Configuring DHCP client..."
cat <<EOF >> /etc/dhcpcd.conf
interface wlan0
static ip_address=10.42.0.1/24
EOF

# Configure hostapd
echo "Setting up hostapd..."
cat <<EOF > /etc/hostapd/hostapd.conf
country_code=US
interface=wlan0
ssid=$SSID
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PASSWORD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# Point hostapd to the configuration file
sed -i '/#DAEMON_CONF=""/c\DAEMON_CONF="/etc/hostapd/hostapd.conf"' /etc/default/hostapd

# Configure dnsmasq
echo "Configuring dnsmasq..."
cat <<EOF > /etc/dnsmasq.conf
interface=wlan0
dhcp-range=10.42.0.50,10.42.0.150,255.255.255.0,24h
dhcp-option=option:router,10.42.0.1
dhcp-option=option:dns-server,10.42.0.1
EOF

# Configure NetworkManager to ignore wlan0
echo "Configuring NetworkManager to ignore wlan0..."
echo -e "[keyfile]\nunmanaged-devices=interface-name:wlan0" >> /etc/NetworkManager/NetworkManager.conf

# Enable IP forwarding
echo "Enabling IP forwarding..."
sed -i '/#net.ipv4.ip_forward=1/c\net.ipv4.ip_forward=1' /etc/sysctl.conf
sysctl -p

# Set up IP tables and save
echo "Setting up IP tables..."
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
netfilter-persistent save

# Restart services
echo "Restarting services..."
systemctl unmask hostapd
systemctl enable hostapd
systemctl restart hostapd
systemctl restart dhcpcd
systemctl restart dnsmasq

echo "Setup complete. Please reboot the Raspberry Pi."
