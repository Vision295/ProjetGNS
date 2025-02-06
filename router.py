from pathlib import Path
from utils import *
from template import *



# List all directories in the given path
class Router:
      
      """
      classe for creating a router
      """ 
      
      get_igp = lambda self: "ospf" if self.is_igp_ospf else "rip"

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
                              
      def print_intro(self) : self.new_content += INTRO_TEMPLATE.format(self.nb)
           
      def print_ospf_or_rip(self):
            if self.is_igp_ospf:
                  text_igp = [
                        "ospf",
                        "ipv6 ospf 1 area 0",
                        ]
            else:
                  text_igp = [
                        "rip",
                        "ipv6 rip 1 enable"
                        ]
                  
            self.new_content += INTERFACE.format("Loopback0", self.data[text_igp[0]][self.nb]["loopback"], text_igp[1])
            for interface in interfaces: 
                  if interface in self.data[text_igp[0]][self.nb]:
                        self.new_content += INTERFACE.format(
                              get_interface_name(interface),
                              self.data[text_igp[0]][self.nb][interface],
                              text_igp[1]
                        )


            for interface in interfaces:
                  if self.nb in self.data["bgp"]: 
                        if interface in self.data["bgp"][self.nb]:
                              self.new_content += INTERFACE.format(
                                    get_interface_name(interface),
                                    self.data["bgp"][self.nb][interface],
                                    "!",
                              )

            if self.is_igp_ospf:
                  self.new_content += ROUTER_OSPF.format(self.nb, self.nb, self.nb, self.nb)

            if self.nb in self.data["bgp"] and self.is_igp_ospf:
                  for key in self.data["bgp"][self.nb].keys():
                        self.new_content += "\n passive-interface {}".format(get_interface_name(key))

            if self.is_igp_ospf:
                  self.new_content += "\n!"
            return self.new_content

      def print_bgp(self):
            self.igp = self.get_igp()
            self.new_content += BGP_INTRO.format(
                  111 if self.is_igp_ospf else 222,
                  *[self.router_num for _ in range(4)]
            )

            for key in self.data[self.igp].keys():
                  if key != self.router_num:
                        self.new_content += BGP_NEIGHBOR.format(
                              without_net_suffix(self.data[self.igp][key]["loopback"]),
                              111 if self.is_igp_ospf else 222,
                              without_net_suffix(self.data[self.igp][key]["loopback"])
                        )

            if self.nb in self.data["bgp"].keys():
                  self.new_content += "  neighbor {} remote-as {}\n".format(self.data["bgp"][self.nb].values(), 111 if self.is_igp_ospf else 222)

            self.new_content += get_border_router_ips(self.nb, False)
 
            self.new_content += TRANSI_BGP
            # get the ip networks from igp

            for key, value in self.data[self.igp][self.nb].items():
                 if key != "loopback":
                       self.new_content += "  network {}\n".format(get_network(value))

            # get the ip networks from bgp
            if self.nb in self.data["bgp"]:
                  for value in self.data["bgp"][self.nb].values():
                       self.new_content += "  network {}\n".format(get_network(value))
                       
                       
            # get the ip address of neighbors in igp
            for key, value in self.data[self.igp].items():
                  if key != self.nb:
                        self.new_content += "  neighbor {} activate\n".format(without_net_suffix(value["loopback"]))
                  
            self.new_content += get_border_router_ips(self.nb, True)

            self.new_content += " exit-address-family\n!\n"
            return self.new_content
    
      def print_outro(self):
            self.new_content += INTRO_OF_OUTRO
            if self.is_igp_ospf:
                  self.new_content += OUTRO_OSPF.format(self.nb, self.nb, self.nb, self.nb)
            else:
                  self.new_content += OUTRO_RIP

            self.new_content += OUTRO_OF_OUTRO

      def __init__(self, content:str, data:dict):
            self.content = content
            self.data:dict = data
            self.get_router_num()
            self.nb = str(self.router_num)
            self.is_igp_ospf:bool = self.router_num <= 7 # todo : à changer 
            self.new_content = ""
            self.print_intro() 
            self.print_ospf_or_rip() 
            self.print_bgp() 
            self.print_outro() 
            print(self.new_content)
          