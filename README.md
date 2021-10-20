# ALE-scripts
ALE Scripts

# Get Started
1. make sure that python 3< is installed
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
    #####################################
    # code can be added here and will be executed on each switch

    # find prompt (test connectivity)
    print(switch.net_connect.find_prompt())

    # # add VLAN on switch
    # switch.add_vlan(402, "TEST_VLAN_402")

    # # get lldp remote systems
    # switch.get_lldp_remote_system()

    # # filter ports which have at least one remote system with name containing "OmniAccess Stellar" 
    # # requires get_lldp_remote_system() to be called first
    # filtered_ports_aos_uplink = s.find_ports("remote-systems", "Alcatel-Lucent Enterprise OS")

    # # tag VLAN on filtered ports
    # s.port_vlan_tagging(filtered_ports_aos_uplink, 402)
```

7. run the script
```
python main.py
```

# Logging
SSH session logs are written to `session_logs` folder. One file per switch

netmiko debugging logs are written to `netmiko_global.log`