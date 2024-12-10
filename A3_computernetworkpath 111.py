from netmiko import ConnectHandler
from getpass import getpass

# Collect device login details
device = {
    'device_type': 'cisco_ios',--
    'ip': '192.168.56.101',
    'username': input('Enter Username: '),
    'password': getpass('Enter Password: '),
    'secret': getpass('Enter Secret Password: ')
}

# Connect to the device and enter enable mode
net_connect = ConnectHandler(**device)
net_connect.enable()

# Configure the Loopback interface
loopback_config = [
    'interface loopback0',
    'ip address 1.1.1.1 255.255.255.255'
]
net_connect.send_config_set(loopback_config)

# Configure the GigabitEthernet2 interface
interface_config = [
    'interface GigabitEthernet2',
    'ip address 192.168.1.1 255.255.255.0',
    'no shutdown'
]

# Advertise OSPF
ospf_config = [
    'router ospf 1',                        
    'network 1.1.1.1 0.0.0.0 area 0',       
    'network 192.168.1.1 0.0.0.0 area 0'
]

# Change the hostname of the device
hostname_change = [
    'configure terminal',
    f'hostname R1'
]
net_connect.send_config_set(hostname_change)

# Save the running configuration to a file
running_config = net_connect.send_command('show running-config')
with open('running_config.txt', 'w') as file:
    file.write(running_config)

# Show IP interface details
ip_interface_brief = net_connect.send_command('show ip interface brief')
print('---- IP Interface Brief ----')
print(ip_interface_brief)

# Disconnect from the device
net_connect.disconnect()
