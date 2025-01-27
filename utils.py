


get_igp = lambda self: "ospf" if self.is_igp_ospf else "rip"
get_network = lambda addr: addr[:-5] + '0' + addr[-4:]
without_net_suffix = lambda addr : addr[:-4]

def get_interface_name(interface_shortcut:str) -> str:
      match(interface_shortcut):
            case "g1/0" : return "Gigabitethernet1/0"
            case "g2/0" : return "Gigabitethernet2/0"
            case "g3/0" : return "Gigabitethernet2/0"
            case "f0/0" : return "Fastethernet0/0"
            case _ : return ""