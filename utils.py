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
            case "g3/0" : return "Gigabitethernet3/0"
            case "f0/0" : return "Fastethernet0/0"
            case _ : return ""
            
 
def get_border_router_ips(nb:str, isLast:bool):
    if not isLast:
        match int(nb):
            case 6:
                return "  neighbor 3::1:2 remote-as 222\n"
            case 16:
                return "  neighbor 3::1:1 remote-as 111\n"
            case 7:
                return "  neighbor 3::2:2 remote-as 222\n"
            case 17:
                return "  neighbor 3::2:1 remote-as 111\n"
            case _:
                return ""
    else:
        match int(nb):
            case 6:
                return "  neighbor 3::1:2 activate\n"
            case 16:
                return "  neighbor 3::1:1 activate\n"
            case 7:
                return "  neighbor 3::2:2 activate\n"
            case 17:
                return "  neighbor 3::2:1 activate\n"
            case _:
                return ""
 
"""
def get_border_router_ips(intent: dict) -> list[tuple[str, str]]:
    border_routers = []
    as_data = intent["AS"]  # Récupération des données des AS
    
    # Parcours de chaque AS
    for asn, as_info in as_data.items():
        for router_id, interfaces in as_info["routers"].items():  # Parcours des routeurs de l'AS
            for iface, ip in interfaces.items():  # Parcours des interfaces et de leurs IPs
                ip_network = ipaddress.ip_network(ip, strict=False)  # Conversion en réseau
                
                # Vérification si l'IP est dans un autre AS
                for other_asn, other_as_info in as_data.items():
                    if other_asn != asn:  # Éviter la comparaison avec soi-même
                        for other_router, other_interfaces in other_as_info["routers"].items():
                            for other_ip in other_interfaces.values():
                                other_ip_network = ipaddress.ip_network(other_ip, strict=False)
                                if ip_network.compare_networks(other_ip_network) == 0:  # Comparaison des réseaux
                                    border_routers.append((without_net_suffix(ip), other_asn))  # Ajout à la liste
    
    return border_routers  # Retourne la liste des routeurs frontières
  """          