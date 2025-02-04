from utils import *

with open('intent4.json', 'r') as file:
      data = json.load(file)

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
    #border_routers = set(border_routers)
    #border_routers = list(border_routers)
    return border_routers

list1 = get_border_router(data)

print("bonjours les amis", list1)
