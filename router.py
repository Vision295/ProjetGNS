from pathlib import Path
from utils import *
from template import *
from intentGen import IntentGen



# List all directories in the given path
class Router:
      
      """
      classe for creating a router
      """ 
      
      # à changer c'est trop moche ta fonction
      def get_router_num(self):
            """
            From the original "content" of the current config file, get the number of the router.
            No input -> returns int.
            """
            list_content = list(self.content)
            for i, v in enumerate(list_content): 
                  if v == 'h' and list_content[i+1] == 'o':
            # Start collecting digits starting from i+2, which is the first digit after 'ho'
                        num_str = ''
            # Collect digits until a non-digit character is found
                        j = i + 10
                        while j < len(list_content) and list_content[j].isdigit():
                              num_str += list_content[j]
                              j += 1
                              print(num_str)
            # If a number is found, convert to int and store
                        if num_str:
                              self.router_num = int(num_str)
            self.nb = str(self.router_num)
                              
      def get_asn(self):
            for asn, asv in self.data.items():
                  if self.nb in asv["routers"].keys():
                        self.asn = asn
                              
      def get_igp(self):      
            self.igp = self.data[self.asn]["igp"]
            self.is_igp_ospf = self.igp == "ospf"
                                       
      def print_intro(self) : self.new_content += INTRO_TEMPLATE.format(self.nb)
           
      def print_ospf_or_rip(self):
            if self.is_igp_ospf:
                  text_igp = "ipv6 ospf 1 area 0"
            else:
                  text_igp = "ipv6 rip 1 enable"
                  
            self.new_content += INTERFACE.format("Loopback0", self.data[self.asn]["routers"][self.nb]["loopback"], text_igp)
            for interface in interfaces: 
                  if interface in self.data[self.asn]["routers"][self.nb]:
                        self.new_content += INTERFACE.format(
                              get_interface_name(interface),
                              self.data[self.asn]["routers"][self.nb][interface],
                              text_igp
                        )

            if self.is_igp_ospf:
                  self.new_content += ROUTER_OSPF.format(self.nb, self.nb, self.nb, self.nb)


                  key_from_val = lambda d, f : next((k for k, v in d.items() if v == f), None)

                  for elem in get_border_router_ips(self.data):
                        if elem[0] in self.data[self.asn]["routers"][self.nb].values():
                              self.new_content += "\n passive-interface {}".format(
                                    get_interface_name(key_from_val(self.data[self.asn]["routers"][self.nb], elem[0]))
                              )

                  self.new_content += "\n!"

            return self.new_content

      def print_bgp(self):

            self.new_content += BGP_INTRO.format(
                  self.asn,
                  *[self.router_num for _ in range(4)]
            )


            for key in self.data[self.asn]["routers"].keys():
                  if key != self.router_num:
                        self.new_content += BGP_NEIGHBOR.format(
                              without_net_suffix(self.data[self.asn]["routers"][key]["loopback"]),
                              self.asn,
                              without_net_suffix(self.data[self.asn]["routers"][key]["loopback"])
                        )

            # if the router is border router than it has info in the "bgp" section of the intent file
            for ip, asnum in self.ebgp_neighbors : 
                  for v in self.data[self.asn]["routers"][self.nb].values():
                        if get_network(ip) == get_network(v) and v != ip: 
                              self.new_content += " neighbor {} remote-as {}\n".format(ip, asnum)
 
            self.new_content += TRANSI_BGP
            # get the ip networks from igp

            for key, value in self.data[self.asn]["routers"][self.nb].items():
                 if key != "loopback":
                       self.new_content += "  network {}\n".format(get_network(value))
                       
                       
            # get the ip address of neighbors in igp
            for key, value in self.data[self.asn]["routers"].items():
                  if key != self.nb:
                        self.new_content += "  neighbor {} activate\n".format(without_net_suffix(value["loopback"]))
                  
            # if the router is border router than it has info in the "bgp" section of the intent file
            for ip, _ in self.ebgp_neighbors : 
                  if ip in self.data[self.asn]["routers"][self.nb].values():
                        self.new_content += "  neighbor {} activate\n".format(ip)

            self.new_content += " exit-address-family\n!\n"
            return self.new_content
    
      def print_outro(self):
            self.new_content += INTRO_OF_OUTRO
            if self.is_igp_ospf:
                  self.new_content += OUTRO_OSPF.format(self.nb, self.nb, self.nb, self.nb)
            else:
                  self.new_content += OUTRO_RIP

            self.new_content += OUTRO_OF_OUTRO

      def __init__(self, input:str, new_intent:IntentGen):
            self.content = input
            self.data = new_intent.new_content["AS"]
            self.new_content = ""

            self.get_router_num()
            self.get_asn()
            self.get_igp()

            self.ebgp_neighbors = get_border_router_ips(self.data)

            self.print_intro() 
            self.print_ospf_or_rip() 
            self.print_bgp() 
            self.print_outro() 

            print(self.new_content)
          