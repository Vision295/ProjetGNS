import json
from pathlib import Path

local_path = Path("C:/Users/theop/GNS3/projects/testprojetGNS3/project-files/dynamips")

# List all directories in the given path


with open('intent.json', 'r') as file:
      data = json.load(file)


directories = [d for d in local_path.iterdir() if d.is_dir()]

def get_interface_name(interface_shortcut:str) -> str:
    match(interface_shortcut):
        case "g1/0" : return "gigabitethernet1/0"
        case "g2/0" : return "gigabitethernet2/0"
        case "g3/0" : return "gigabitethernet2/0"
        case "f0/0" : return "fastethernet0/0"
        case _ : return ""


def get_router_num(content:str) -> int:
    list_content = list(content)
    for i, v in enumerate(list_content): 
        if v == 'h' and list_content[i+1] == 'o':
            return int(list_content[i+10])
def print_intro(router_number:int) -> str:
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
!""".format(str(router_number))
def print_ospf(router_number:int, data: dict) -> str:
    nb = str(router_number)
    what_to_add = \
"""
interface Loopback0
 no ip address
 ipv6 address {}
 ipv6 ospf 1 area 0
!""".format(data["ospf"][nb]["loopback"])
    if "f0/0" in data["ospf"][nb]:
        what_to_add += \
"""
interface FastEthernet0/0
 no ip address
 duplex full
 ipv6 address {}
 ipv6 ospf 1 area 0
!""".format(data["ospf"][nb]["f0/0"])
    if "g1/0" in data["ospf"][nb]:
        what_to_add += \
"""
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address {}
 ipv6 ospf 1 area 0
!""".format(data["ospf"][nb]["g1/0"])
    if "g2/0" in data["ospf"][nb]:
        what_to_add += \
"""
interface GigabitEthernet2/0
 no ip address
 negotiation auto
 ipv6 address {}
 ipv6 ospf 1 area 0
!""".format(data["ospf"][nb]["g2/0"])
    if "g3/0" in data["ospf"][nb]:
        what_to_add += \
"""
interface GigabitEthernet3/0
 no ip address
 negotiation auto
 ipv6 address {}
 ipv6 ospf 1 area 0
!""".format(data["ospf"][nb]["g3/0"])
    
    what_to_add += \
"""
router ospf 1
 router-id {}.{}.{}
!""".format(nb, nb, nb, nb)

    return what_to_add
def print_bgp(router_number:int, data:dict):
    return ""
def print_outro(router_number:int) -> str:
    return \
"""!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
ipv6 router ospf 1
 router-id {}.{}.{}.{}
!
!
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
end""".format(*[str(router_number) for _ in range(4)])


for d in directories:
      dir = d / "configs/"
      print(dir)
      for item in dir.iterdir():
            if item.name.startswith("i") and item.name.endswith("_startup-config.cfg"):
                with open(item, 'r') as file:
                    content = file.read()
                    router_num = get_router_num(content)
                    new_content = \
                        print_intro(router_num) +\
                        print_ospf(router_num, data) +\
                        print_bgp(router_num, data) +\
                        print_outro(router_num)
                    print(new_content)
                with open(item, 'w') as file:
                    file.write(new_content)