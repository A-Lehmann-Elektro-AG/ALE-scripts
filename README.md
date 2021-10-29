# ALE-scripts
Python library to automate Alcatel-Lucent Enterprise switch configs. 

Tested with AOS 6 only.

# Getting Started
1. make sure that python >3 is installed
`python --version`
--> install python https://www.python.org/downloads/
2. make sure that pip is installed (should be installed together with python)
`pip --version`
3. install dependencies
`pip install netmiko`
4. copy switches.csv.template to configs folder and remove `.template`
5. add switches with credentials to the csv, format
```
name,ip,username,password
```
5. make sure that the correct csv file name is used in main.py
```
f_switches = open("configs/switches.csv", "r")
```
6. uncomment required functions in main.py
```
####################################################################################################
# code can be added here and will be executed on each switch

# 1. find prompt (test connectivity)
print(switch.net_connect.find_prompt())

# 2. add VLAN on switch
# switch.add_vlan(502, "VLAN502_physio")

# 3. get ports for VLAN
# ports_vlan_102 = switch.get_ports_for_vlan(102)
# print(ports_vlan_102)

# 4. tag VLAN on filtered ports
# switch.port_vlan_tagging(ports_vlan_102, 502)

# 5. get lldp remote systems
# switch.get_lldp_remote_system()

# 6. filter ports which have at least one remote system with system description containing "OAW-AP", requires get_lldp_remote_system() to be called first
# filtered_ports_aos_uplink = switch.find_ports("remote-systems", "OAW-AP")
# print(filtered_ports_aos_uplink)

# 7. tag vlan on ports
# switch.port_vlan_tagging(filtered_ports_aos_uplink, 402)

# 8. save config
# switch.save_config()

print("----------------------------------------------------\n\n")
```

7. run the script
```
python main.py
```

# Logging
SSH session logs are written to `session_logs` folder. One file per switch

netmiko debugging logs are written to `netmiko_global.log`

# Support
A. Lehmann Elektro AG
informatik@lehmann.ch