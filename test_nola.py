def get_router_num(content: str) -> int:
    list_content = list(content)
    for i, v in enumerate(list_content): 
        if v == 'h' and list_content[i+1] == 'o':
            # Find the number starting from i+2 (after "ho")
            num_str = ''
            # Iterate to collect digits until a non-digit character is found
            for j in range(i+10, len(list_content)):
                if list_content[j].isdigit():
                    num_str += list_content[j]
                else:
                    break
            # Convert the collected digits to an integer
            if num_str:
                return int(num_str)
    # Return -1 or some other value if no valid hostname is found
    return -1

str = """!
!
! Last configuration change at 16:23:14 UTC Sat Jan 11 2025
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname R3094873094873094837
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
!
interface Loopback0
 no ip address
 ipv6 address 2001:DB8:2::3/128
 ipv6 rip 1 enable
!
interface FastEthernet0/0
 no ip address
 duplex full
 ipv6 address 2001:DB8:1:4::2/64
 ipv6 rip 1 enable
!
interface GigabitEthernet1/0
 no ip address
 shutdown
 negotiation auto
!
interface GigabitEthernet2/0
 no ip address
 shutdown
 negotiation auto
!
interface GigabitEthernet3/0
 no ip address
 shutdown
 negotiation auto
!
router bgp 112
 bgp router-id 6.6.6.6
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 2001:DB8:1:2::1 remote-as 112
 neighbor 2001:DB8:1:4::1 remote-as 112
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
  network 2001:DB8:1:4::/64
  neighbor 2001:DB8:1:2::1 activate
  neighbor 2001:DB8:1:4::1 activate
 exit-address-family
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
ipv6 router rip 1
 redistribute connected
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
end"""

print(get_router_num(str))
