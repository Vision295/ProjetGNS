import ipaddress


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
                                    border_routers.append((ipaddress.ip_interface(ip).compressed, other_asn))  # Ajout à la liste
    
    return border_routers  # Retourne la liste des routeurs frontières

# Exemple d'utilisation
new_intent = {
    'ipRange': '1::/60',
    'alpha': [0, 2, 2],
    'beta': [1, 0, 2],
    'AS': {
        '111': {
            'igp': 'ospf',
            'routers': {
                1: {'f0/0': '1::1/64', 'g1/0': '1:0:0:1::1/64'}
            }
        },
        '222': {
            'igp': 'ospf',
            'routers': {
                2: {'f0/0': '1:0:0:1::2/64'}
            }
        },
        '333': {
            'igp': 'rip',
            'routers': {
                0: {'f0/0': '1::2/64'}
            }
        }
    }
}

result = get_border_router_ips(new_intent)
print(result)
