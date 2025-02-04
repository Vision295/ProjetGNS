import ipaddress



interfaces = ["f0/0", "g1/0", "g2/0", "g3/0"]
get_network = lambda addr: str(ipaddress.IPv6Network(addr, strict=False).network_address) + '/' + str(ipaddress.IPv6Network(addr, strict=False).prefixlen)


def without_net_suffix(addr:str):
    new_addr = ""
    for i in addr:
        new_addr += i
        if i == "/" : return new_addr
        
    
without_net_suffix = lambda addr : addr[:-4]

def get_interface_name(interface_shortcut:str) -> str:
      match(interface_shortcut):
            case "g1/0" : return "Gigabitethernet1/0"
            case "g2/0" : return "Gigabitethernet2/0"
            case "g3/0" : return "Gigabitethernet2/0"
            case "f0/0" : return "Fastethernet0/0"
            case _ : return ""
<<<<<<< HEAD
            
def get_border_router(intent: dict) -> list[str]:
    border_routers = []
    as_data = intent["AS"]
    for asn, asv in as_data.items():
        for routers in asv["routers"].keys():
            for interface, ip in asv["routers"][routers].items(): #gets through all routers a first round
                for asn2, asv2 in as_data.items():
                    if asn2 != asn:
                        for routers2 in asv2["routers"].keys():
                            for interface2,ip2 in asv2["routers"][routers2].items():
                                if get_network(ip) == get_network(ip2):
                                    border_routers.append(routers)
                                    border_routers.append(routers2)
    border_routers = set(border_routers)
    border_routers = list(border_routers)  
    return border_routers
    

def get_border_router_ips(intent: dict) -> list[tuple[str, str]]:
    border_routers = []
    as_data = intent["AS"]
    
    for asn, as_info in as_data.items():
        for router_id, interfaces in as_info["routers"].items():
            for iface, ip in interfaces.items():
                current_network = ipaddress.ip_interface(ip).network
                
                for other_asn, other_as_info in as_data.items():
                    if other_asn != asn:
                        for other_router, other_interfaces in other_as_info["routers"].items():
                            for other_ip in other_interfaces.values():
                                other_network = ipaddress.ip_interface(other_ip).network
                                if current_network.network_address == other_network.network_address:
                                    border_routers.append((ip.split('/')[0], other_asn))
    
    return border_routers
=======
>>>>>>> 91cb750f002b6536afe6526534e9bdfd8755327e

