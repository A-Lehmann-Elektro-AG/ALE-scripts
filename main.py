#!/usr/bin/env python3

"""
  Alcatel Lucent Python examples

  author:   Marco Lehmann, marco.lehmann@lehmann.ch, A. Lehmann Elektro AG
  date:     19.10.2021

  pip3 install https://github.com/ktbyers/netmiko/archive/develop.zip

"""

from aleswitch import ALESwitch
from netmiko import ConnectHandler
import time

def main():

  # import switches from config csv
  f_switches = open("./configs/switches.csv", "r")
  for l in f_switches.readlines():
    s = l.strip().split(",")
    if len(s) == 5:
      with ALESwitch(s[0], s[1], s[2], s[3], s[4]) as switch:
        if not switch.error:

          print("----------------------------------------------------")
          print("configure switch: " + switch.name + ", " + switch.ip)
          
          ####################################################################################################
          # code can be added here and will be executed on each switch

          # # 1. find prompt (test connectivity)
          # print(switch.net_connect.find_prompt())
          # print(switch.get_system())

          # # 2. add VLAN on switch
          # switch.add_vlan(7, "vlan-7")

          # # 3. get ports for VLAN
          # ports_vlan_6 = switch.get_ports_for_vlan(6)
          # print(ports_vlan_6)

          # # 4. tag VLAN on filtered ports
          # switch.port_vlan_tagging(ports_vlan_6, 7)
          
          # # 5. get lldp remote systems
          # switch.get_lldp_remote_system()

          # # 6. filter ports which have at least one remote system with system description containing "OAW-AP", requires get_lldp_remote_system() to be called first
          # filtered_ports_aos_uplink = switch.find_ports("remote-systems", "OAW-AP")
          # print(filtered_ports_aos_uplink)

          # # 7. tag vlan on ports
          # switch.port_vlan_tagging(filtered_ports_aos_uplink, 402)

          # # 8. run custom command
          # switch.execute_command('show system')

          # # 99. save config
          # switch.save_config()

          print("----------------------------------------------------\n\n")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

