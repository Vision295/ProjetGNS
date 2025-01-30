import copy
import ipaddress
import json
from itertools import islice
from utils import interfaces

##### GIVEN THE FOLLOWING EXAMPLE
 
PREFIX = 64


class IntentGen():
      
      
      def getIpRange(self):
            try:
                  return ipaddress.ip_network(self.data["ipRange"])
            except:
                  try:
                        self.data["ipRange"]
                        raise TypeError("Enterred an incorrect ipv6 address format : ", self.data["ipRange"])
                  except:
                        raise ValueError("No value in ipRange key of intent file")
      
      def __init__(self, data:dict) -> None:
            self.data = data
            
            self.ipRange = self.getIpRange()
            self.alpha = data["alpha"]
            self.beta = data["beta"]

            self.nb_subnets = len(self.beta)
            self.all_subnets = list(islice(self.ipRange.subnets(new_prefix=PREFIX), 0, self.nb_subnets))
            
      def gen(self):
            self.get_networks()
            self.get_connections()
            self.get_new_intent()
            print("networks : ", self.networks)
            print("connections : ", self.connections)
            print("new_intent : ", self.new_intent)
      
      def get_networks(self):
            self.networks = {}
            nb_subnets = len(self.beta)
            self.subnets = list(islice(self.ipRange.subnets(new_prefix=PREFIX), 0, nb_subnets))
      
            nb_subnet_taken = 0
            for index, value in enumerate(self.alpha):
                  for i, v in enumerate(self.beta[self.alpha[index-1]:value+1]):
                        key = (index, v)
                             
                        if not key in self.networks.keys() and not key in self.networks.keys() and key[0] != key[1]:
                              self.networks[key] = self.subnets[nb_subnet_taken].compressed
                              nb_subnet_taken += 1

      def get_connections(self):
            self.connections = {}
            
            for index, value in self.networks.items():
                  net = ipaddress.ip_network(value)
                  if index[0] in self.connections.keys():
                        self.connections[index[0]].append(ipaddress.ip_interface(f"{net.network_address + 1}/{net.prefixlen}").compressed)    
                  else:
                        self.connections[index[0]] = [ipaddress.ip_interface(f"{net.network_address + 1}/{net.prefixlen}").compressed]
                  
                  if index[1] in self.connections.keys():
                        self.connections[index[1]].append(ipaddress.ip_interface(f"{net.network_address + 2}/{net.prefixlen}").compressed)    
                  else:
                        self.connections[index[1]] = [ipaddress.ip_interface(f"{net.network_address + 2}/{net.prefixlen}").compressed]   


            for values in self.connections.values():
                  if len(values) > 4:
                        print("Router cannot have more than 4 connections !")
            
            
      def get_new_intent(self):
            self.new_intent = {}
            self.what_to_add = {}            


            for key, value in self.connections.items():
                  self.what_to_add[str(key)] = {interfaces[i]: v for i, v in enumerate(value)}
                  
            self.new_intent = copy.deepcopy(self.data)
            for key, value in self.data['AS'].items():
                  routers_to_loop = value['routers']
                  self.new_intent['AS'][key]['routers'] = {}
                  for i in routers_to_loop:
                        self.new_intent['AS'][key]['routers'][i] = self.what_to_add[str(i)]
      
      def write_on_intent(self, name:str): 
            with open(name+".json", "w") as json_file:
                  json.dump(self.new_intent, json_file, indent=6)
                              