import json
from pathlib import Path


print(get_network("1::1:1/127"))

# List all directories in the given path
class Router:
      
      """
      classe for creating a router
      """ 
      
      without_net_suffix = lambda addr : "".join(list(addr[:-4]))
      get_igp = lambda self: "ospf" if self.is_igp_opsf else "rip"
      get_network = lambda addr: addr[:-5] + '0' + addr[-4:]

      def get_router_num(self) -> int:
            """
            from the original "content" of the current config file gets the number of the router
            no input -> returns int
            """
            list_content = list(self.content)
            for i, v in enumerate(list_content): 
                  if v == 'h' and list_content[i+1] == 'o':
                        if list_content[i+11] in "1234567890":
                              return int(list_content[i+10] + list_content[i+11])
                        else:
                              return int(list_content[i+10])
           
      def print_intro(self) -> str:
          return \
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
!""".format(str(self.router_num))
           
      def print_ospf_or_rip(self) -> str:
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
            nb = str(self.router_num)
            what_to_add = \
"""
interface Loopback0
 no ip address
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][nb]["loopback"], text_igp[1])
            if "f0/0" in self.data[text_igp[0]][nb]:
                  what_to_add += \
"""
interface FastEthernet0/0
 no ip address
 duplex full
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][nb]["f0/0"], text_igp[1])
            if "g1/0" in self.data[text_igp[0]][nb]:
                  what_to_add += \
"""
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][nb]["g1/0"], text_igp[1])
            if "g2/0" in self.data[text_igp[0]][nb]:
                  what_to_add += \
"""
interface GigabitEthernet2/0
 no ip address
 negotiation auto
 ipv6 address {}
 {}
!""".format(self.data[text_igp[0]][nb]["g2/0"], text_igp[1])
            if "g3/0" in self.data[text_igp[0]][nb]:
                  what_to_add += \
"""
interface GigabitEthernet3/0
 no ip address
 negotiation auto
 ipv6 address {}
{}
!""".format(self.data[text_igp[0]][nb]["g3/0"], text_igp[1])
            return what_to_add

      def print_bgp(self) -> str:
            self.igp = self.get_igp()
            what_to_add = \
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
                              what_to_add += \
""" neighbor {} remote-as {}
 neighbor {} update-source loopback0
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6""".format(
      Router.without_net_suffix(self.data[self.igp][key]["loopback"]),
      111 if self.is_igp_opsf else 222,
      Router.without_net_suffix(self.data[self.igp][key]["loopback"])
)
            for key, value in self.data[self.igp][self.router_num].items():
                 if key != "loopback":
                       what_to_add += \
""" 

""" 

            return what_to_add
    
      def print_outro(self) -> str:
            nb = str(self.router_num)
            what_to_add = \
"""!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!"""
            if self.is_igp_ospf:
                  what_to_add += \
"""
ipv6 router ospf 1
 router-id {}.{}.{}.{}
!""".format(nb, nb, nb, nb)
            else:
                  what_to_add += \
"""
ipv6 router rip 1
 redistribute connected
!"""
            what_to_add += \
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
end""".format(*[str(self.router_num) for _ in range(4)])
            return what_to_add

      def __init__(self, content:str, data:dict):
            self.content = content
            self.data:dict = data
            self.router_num:int = self.get_router_num()
            self.is_igp_ospf:bool = self.router_num <= 7 # todo : à changer 
            self.new_content = \
                  self.print_intro() +\
                  self.print_ospf_or_rip() +\
                  self.print_bgp() +\
                  self.print_outro() 
          
      def get_interface_name(self, interface_shortcut:str) -> str:
            match(interface_shortcut):
                  case "g1/0" : return "gigabitethernet1/0"
                  case "g2/0" : return "gigabitethernet2/0"
                  case "g3/0" : return "gigabitethernet2/0"
                  case "f0/0" : return "fastethernet0/0"
                  case _ : return ""