import copy
import ipaddress
import json
from itertools import islice

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
      
      def get_networks(self):
            self.networks = {}
      
            nb_subnet_taken = 0
            for index, value in enumerate(self.alpha):
                  for i, v in enumerate(self.beta[self.alpha[index-1]:value+1]):
                        key = (index, v)
                             
                        if not key in networks.keys() and not key in networks.keys() and key[0] != key[1]:
                              self.networks[key] = self.subnets[nb_subnet_taken].compressed
                              nb_subnet_taken += 1

      def get_connections(self):
            self.connections = {}
            for index, value in self.networks.items():
                  if index[0] in self.connections.keys():
                        self.connections[index[0]].append((ipaddress.ip_interface(value) + 1).compressed)    
                  else:
                        self.connections[index[0]] = [(ipaddress.ip_interface(value) + 1).compressed]
                  
                  if index[1] in self.connections.keys():
                        self.connections[index[1]].append((ipaddress.ip_interface(value) + 2).compressed)
                  else:
                        self.connections[index[1]] = [(ipaddress.ip_interface(value) + 2).compressed]


            for values in self.connections.values():
                  if len(values) > 4:
                        print("Router cannot have more than 4 connections !")
            
            
      def get_new_intent(self):
            self.new_intent = {}
            self.what_to_add = {}            

            interfaces = ["f0/0", "g1/0", "g2/0", "g3/0"]

            for key, value in connections.items():
                  self.what_to_add[str(key)] = {interfaces[i]: v for i, v in enumerate(value)}
                  
            new_intent = copy.deepcopy(data)
            for key, value in self.data["AS"].items():
                  routers_to_loop = value['routers']
                  self.new_intent['AS'][key]['routers'] = {}
                  for i in routers_to_loop:
                        self.new_intent['AS'][key]['routers'][i] = self.what_to_add[str(i)]
      
      def write_on_intent(self, name:str): 
            with open(name+".json", "w") as json_file:
                  json.dump(self.new_intent, json_file, indent=6)
                  
            
networks = {}

ipRange = ipaddress.ip_network(input("Enter the IP network for the range like this XXXX:...:0/Y where Y < 64 : "))

with open('intent2.json', 'r') as file : data = json.load(file)

alpha, beta = data["alpha"], data["beta"]
nb_subnets = len(beta) #if no duplicates
subnets = list(islice(ipRange.subnets(new_prefix=PREFIX), 0, nb_subnets))

nb_subnet_taken = 0
for index, value in enumerate(alpha):
      for i, v in enumerate(beta[alpha[index-1]:value+1]):
            key = (index, v)
                 
            if not key in networks.keys() and not key in networks.keys() and key[0] != key[1]:
                  networks[key] = subnets[nb_subnet_taken].compressed
                  nb_subnet_taken += 1
            
print("networks : ", networks)
            
connections = {}
for index, value in networks.items():
      if index[0] in connections.keys():
            connections[index[0]].append((ipaddress.ip_interface(value) + 1).compressed)    
      else:
            connections[index[0]] = [(ipaddress.ip_interface(value) + 1).compressed]
      
      if index[1] in connections.keys():
            connections[index[1]].append((ipaddress.ip_interface(value) + 2).compressed)
      else:
            connections[index[1]] = [(ipaddress.ip_interface(value) + 2).compressed]


for values in connections.values():
      if len(values) > 4:
            print("Router cannot have more than 4 connections !")
            
print("connections : ", connections)



intent = {}            

interfaces = ["f0/0", "g1/0", "g2/0", "g3/0"]

for key, value in connections.items():
      intent[str(key)] = {interfaces[i]: v for i, v in enumerate(value)}
      
new_intent = copy.deepcopy(data)
for key, value in data["AS"].items():
      routers_to_loop = value['routers']
      new_intent['AS'][key]['routers'] = {}
      for i in routers_to_loop:
            new_intent['AS'][key]['routers'][i] = intent[str(i)]

print("new_intent : ", new_intent)

print("intent : ", intent)
with open("intent3.json", "w") as json_file:
      json.dump(new_intent, json_file, indent=6)


