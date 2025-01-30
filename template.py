INTRO_TEMPLATE = \
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
!"""

INTERFACE = \
"""
interface {}
 no ip address
 ipv6 address {}
 {}
!"""

ROUTER_OSPF = \
"""
router ospf 1
 router-id {}.{}.{}.{}"""
 
BGP_INTRO = \
"""
!
router bgp {}
 bgp router-id {}.{}.{}.{}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast"""

BGP_NEIGHBOR = \
""" 
 neighbor {} remote-as {}
 neighbor {} update-source loopback0
"""

TRANSI_BGP = \
""" !
 address-family ipv4
  exit-address-family
 !
 address-family ipv6
"""           

INTRO_OF_OUTRO = \
"""!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!"""

OUTRO_OSPF = \
"""
ipv6 router ospf 1
 router-id {}.{}.{}.{}
!"""

OUTRO_RIP = \
"""
ipv6 router rip 1
 redistribute connected
!"""

OUTRO_OF_OUTRO = \
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








