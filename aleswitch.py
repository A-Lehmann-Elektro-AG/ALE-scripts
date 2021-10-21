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

logging.basicConfig(filename='netmiko_global.log', filemode='a', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

class ALESwitch(object):
  def __init__(self, name, ip, username, password):
    self.name = name
    self.username = username
    self.password = password
    self.ip = ip
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

  def find_ports(self, port_filter_key, port_filter_value_contains):
    ports = []
    for p in self.ports:
      if port_filter_key in self.ports[p]:
        if port_filter_value_contains in self.ports[p][port_filter_key]:
          ports.append(p)
    return ports

  def port_vlan_tagging(self, ports, vlan_id):
    for p in ports:
      self.net_connect.send_command("vlan " + str(vlan_id) + " 802.1q " + p)
      print("vlan " + str(vlan_id) + " 802.1q " + p)

  def add_vlan(self, vlan_id, vlan_name):
    self.net_connect.send_command("vlan " + str(vlan_id) + " enable name " + str(vlan_name))
    print("vlan " + str(vlan_id) + " enable name " + str(vlan_name))

  def save_config(self):
    self.net_connect.send_command("write memory flash-synchro")
    print("write memory flash-synchro")

  def get_ports_for_vlan(self, vlan_id):
    res = self.net_connect.send_command("show vlan " + str(vlan_id) + " port")
    ports = []
    for x in res.split("\n"):
      regexsearch = re.search(r'([0-9]/)+[0-9]+', x)
      if regexsearch: 
        ports.append(regexsearch.group(0))
    return ports