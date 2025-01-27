from pathlib import Path
from utils import *



# List all directories in the given path
class Router:
      
      """
      classe for creating a router
      """ 
      
      get_igp = lambda self: "ospf" if self.is_igp_ospf else "rip"

      def get_router_num(self):
            """
            from the original "content" of the current config file gets the number of the router
            no input -> returns int
            """
            list_content = list(self.content)
            for i, v in enumerate(list_content): 
                  if v == 'h' and list_content[i+1] == 'o':
                        if list_content[i+11] in "1234567890":
                              self.router_num = int(list_content[i+10] + list_content[i+11])
                        else:
                              self.router_num = int(list_content[i+10])
           
      def print_intro(self):
          self.new_content += \
"""!
!
!
! Last configuration change at 10:48:16 UTC Fri Jan 10 2025
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname R{}
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ipv6 unicast-routing
ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!""".format(self.nb)
           
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
            self.new_content += \
"""
interface Loopback0
 no ip address
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][self.nb]["loopback"], text_igp[1])
            if "f0/0" in self.data[text_igp[0]][self.nb]:
                  self.new_content += \
"""
interface FastEthernet0/0
 no ip address
 duplex full
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][self.nb]["f0/0"], text_igp[1])
            if "g1/0" in self.data[text_igp[0]][self.nb]:
                  self.new_content += \
"""
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][self.nb]["g1/0"], text_igp[1])
            if "g2/0" in self.data[text_igp[0]][self.nb]:
                  self.new_content += \
"""
interface GigabitEthernet2/0
 no ip address
 negotiation auto
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][self.nb]["g2/0"], text_igp[1])
            if "g3/0" in self.data[text_igp[0]][self.nb]:
                  self.new_content += \
"""
interface GigabitEthernet3/0
 no ip address
 negotiation auto
 ipv6 address {}
!""".format(self.data[text_igp[0]][self.nb]["g3/0"], text_igp[1])


            if self.nb in self.data["bgp"]: 
                  if "g1/0" in self.data["bgp"][self.nb]:
                        self.new_content += \
"""
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address {}
!""".format(self.data["bgp"][self.nb]["g1/0"])

            if self.nb in self.data["bgp"]:
                  if "g3/0" in self.data["bgp"]:
                        self.new_content += \
"""
interface GigabitEthernet3/0
 no ip address
 negotiation auto
 ipv6 address {}
!""".format(self.data["bgp"][self.nb]["g3/0"])

            if self.is_igp_ospf:
                  self.new_content += \
"""
router ospf 1
 router-id {}.{}.{}.{}""".format(self.nb, self.nb, self.nb, self.nb)

            if self.nb in self.data["bgp"] and self.is_igp_ospf:
                  for key in self.data["bgp"][self.nb].keys():
                        self.new_content += \
""" 
 passive-interface {}""".format(get_interface_name(key))

            if self.is_igp_ospf:
                  self.new_content += \
"""
!"""
            return self.new_content

      def print_bgp(self):
            self.igp = self.get_igp()
            self.new_content += \
"""
!
router bgp {}
 bgp router-id {}.{}.{}.{}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
""".format(
      111 if self.is_igp_ospf else 222,
      *[self.router_num for _ in range(4)]
)
            for key in self.data[self.igp].keys():
                  if key != self.router_num:
                        self.new_content += \
""" neighbor {} remote-as {}
 neighbor {} update-source loopback0
""".format(
      without_net_suffix(self.data[self.igp][key]["loopback"]),
      111 if self.is_igp_ospf else 222,
      without_net_suffix(self.data[self.igp][key]["loopback"])
)
 
            # if the router is border router than it has info in the "bgp" section of the intent file
            match self.router_num:
                  case 6: 
                        self.new_content += "  neighbor 3::1:2 remote-as 222\n"
                  case 16:
                        self.new_content += "  neighbor 3::1:1 remote-as 111\n"
                  case 7: 
                        self.new_content += "  neighbor 3::2:2 remote-as 222\n"
                  case 17: 
                        self.new_content += "  neighbor 3::2:1 remote-as 111\n"
 
            self.new_content += \
 """ !
 address-family ipv4
  exit-address-family
 !
 address-family ipv6
"""           
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
                  
            # if the router is border router than it has info in the "bgp" section of the intent file
            match self.router_num:
                  case 6: 
                        self.new_content += "  neighbor 3::1:2 activate\n"
                  case 16:
                        self.new_content += "  neighbor 3::1:1 activate\n"
                  case 7: 
                        self.new_content += "  neighbor 3::2:2 activate\n"
                  case 17: 
                        self.new_content += "  neighbor 3::2:1 activate\n"

            self.new_content += " exit-address-family\n!\n"
            return self.new_content
    
      def print_outro(self):
            self.new_content += \
"""!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!"""
            if self.is_igp_ospf:
                  self.new_content += \
"""
ipv6 router ospf 1
 router-id {}.{}.{}.{}
!""".format(self.nb, self.nb, self.nb, self.nb)
            else:
                  self.new_content += \
"""
ipv6 router rip 1
 redistribute connected
!"""
            self.new_content += \
"""
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end"""
            return self.new_content

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
          