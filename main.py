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
  f_switches = open("configs/switches.csv", "r")
  for l in f_switches.readlines():
    s = l.strip().split(",")

    with ALESwitch(s[0], s[1], s[2], s[3]) as switch:
      if not switch.error:

        print("----------------------------------------------------")
        print("configure switch: " + switch.name + ", " + switch.ip)
        
        ####################################################################################################
        # code can be added here and will be executed on each switch

        # find prompt (test connectivity)
        print(switch.net_connect.find_prompt())

        # add VLAN on switch
        # switch.add_vlan(502, "SZK_VLAN502_physio")
        # switch.add_vlan(402, "SZK_VLAN402_avd")
        # switch.add_vlan(503, "SZK_VLAN503_bob")
        # switch.add_vlan(705, "SZK_VLAN705_notlicht")
        # switch.add_vlan(706, "SZK_VLAN706_usv")

        # get ports for VLAN
        #ports_vlan_102 = switch.get_ports_for_vlan(102)

        # tag VLAN on filtered ports
        #switch.port_vlan_tagging(ports_vlan_102, 502)
        

        # # get lldp remote systems
        # switch.get_lldp_remote_system()

        # # filter ports which have at least one remote system with name containing "OmniAccess Stellar" 
        # # requires get_lldp_remote_system() to be called first
        # filtered_ports_aos_uplink = switch.find_ports("remote-systems", "Alcatel-Lucent Enterprise OS")
        # switch.port_vlan_tagging(filtered_ports_aos_uplink, 402)
        # switch.port_vlan_tagging(filtered_ports_aos_uplink, 503)
        # switch.port_vlan_tagging(filtered_ports_aos_uplink, 705)
        # switch.port_vlan_tagging(filtered_ports_aos_uplink, 706)

        # save config
        switch.save_config()

        print("----------------------------------------------------\n\n")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

