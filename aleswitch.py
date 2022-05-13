"""
  Alcatel Lucent Python Class

  author:   Marco Lehmann, marco.lehmann@lehmann.ch, A. Lehmann Elektro AG
  date:     19.10.2021

  ToDo:
    - 

"""

from netmiko import ConnectHandler
import re
import time

import logging

logging.basicConfig(filename='netmiko_global.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

class ALESwitch(object):
  def __init__(self, name, ip, username, password, aos_version):
    self.name = name
    self.username = username
    self.password = password
    self.ip = ip
    self.aos_version = aos_version
    self.ports = {}
    self.error = False
    self.net_connect = False

  def __enter__(self):
    try:
      self.net_connect = ConnectHandler(
        device_type="alcatel_aos",
        host=self.ip,
        username=self.username,
        password=self.password,
        session_log="session_logs/ssh_session_" + self.name + "_" + self.ip + ".log"
      )
    except Exception as e:
      print('can\'t connect to switch: ' + self.ip)
      self.error = e
      time.sleep(2)
    return self

  def __exit__(self, exception_type, exception_value, traceback):
    if self.net_connect:
      self.net_connect.disconnect()

  # get system info (AOS Version, ...)
  def get_system(self):
    res = self.net_connect.send_command("show system")
    print(res)

  # get lldp Remote Systems
  def get_lldp_remote_system(self):
    r_sys_res = self.net_connect.send_command("show lldp remote-system")
    port = False

    for x in r_sys_res.split("\n"):
      if "Remote LLDP Agents" in x:
        res = re.search(r'([0-9]/)+[0-9]+', x)
        if res: 
          port = res.group(0)
        else:
          print('error: Remote LLDP Agents line without port')
          port = False

      if "System Description" in x:
        name = x.split("=")[1].strip()
        if port in self.ports:  # port already declared
          if "remote-systems" in self.ports[port]:
            self.ports[port]["remote-systems"] += name
          else:
            self.ports[port]["remote-systems"] = name
        else:
          self.ports[port] = {"remote-systems": name}

  # find in local port dictionary (e.g. containing lldp remote systems for each port)  
  def find_ports(self, port_filter_key, port_filter_value_contains):
    ports = []
    for p in self.ports:
      if port_filter_key in self.ports[p]:
        if port_filter_value_contains in self.ports[p][port_filter_key]:
          ports.append(p)
    return ports

  # tag VLAN on array of ports
  def port_vlan_tagging(self, ports, vlan_id):
    if self.aos_version == "6":
      for p in ports:
        self.net_connect.send_command("vlan " + str(vlan_id) + " 802.1q " + p)
        print("vlan " + str(vlan_id) + " 802.1q " + p)
    elif self.aos_version == "8":
      for p in ports:
        self.net_connect.send_command("vlan " + str(vlan_id) + " members port " + p + " tagged")
        print("vlan " + str(vlan_id) + " members port " + p + " tagged")

  # add a VLAN on the switch
  def add_vlan(self, vlan_id, vlan_name):
    if self.aos_version == "6":
      self.net_connect.send_command("vlan " + str(vlan_id) + " enable name " + str(vlan_name))
      print("vlan " + str(vlan_id) + " enable name " + str(vlan_name))
    elif self.aos_version == "8":
      self.net_connect.send_command("vlan " + str(vlan_id) + " name " + str(vlan_name))
      print("vlan " + str(vlan_id) + " name " + str(vlan_name))

  # save Config 
  def save_config(self):
    self.net_connect.send_command("write memory flash-synchro")
    print("write memory flash-synchro")

  # get ports for vlan_id
  def get_ports_for_vlan(self, vlan_id):
    ports = []
    if self.aos_version == "6":
      res = self.net_connect.send_command("show vlan " + str(vlan_id) + " port")
      for x in res.split("\n"):
        regexsearch = re.search(r'([0-9]/)+[0-9]+', x)
        if regexsearch: 
          ports.append(regexsearch.group(0))
    elif self.aos_version == "8":
      res = self.net_connect.send_command("show vlan " + str(vlan_id) + " members")
      for x in res.split("\n"):
        regexsearch = re.search(r'[0-9]/[0-9]/[0-9]+', x)
        if regexsearch: 
          ports.append(regexsearch.group(0))

    return ports
  
  # get mac address table
  def get_mac_address_table(self):
    mac_entries= []
    if self.aos_version == "6":
      res = self.net_connect.send_command("show mac-address-table")
      # loop through lines of output
      for x in res.split('\n'):
        l = x.strip()
        # find lines which contain a MAC address
        if re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', l):
          d = l.split()
          # if len(d) == 6
          if len(d) == 6:
            mac_entries.append({"vlan": d[0], "mac": d[1], "port": d[5]})
    elif self.aos_version == "8":
      res = self.net_connect.send_command("show mac-learning")
      # loop through lines of output
      for x in res.split('\n'):
        l = x.strip()
        # find lines which contain a MAC address
        if re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', l):
          d = l.split()
          if len(d) == 6:
            mac_entries.append({"vlan": d[1], "mac": d[2], "port": d[5]})
    return mac_entries

  # execute custom command
  def execute_command(self, command):
    res = self.net_connect.send_command(command)
    print(res)
