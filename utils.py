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




import json
with open("intent3.json") as file:
    print(get_border_router_ips(json.load(file)))