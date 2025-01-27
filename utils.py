import ipaddress


<<<<<<< HEAD
get_network = lambda addr: str(ipaddress.IPv6Network(addr, strict=False).network_address) + '/' + str(ipaddress.IPv6Network(addr, strict=False).prefixlen)
=======
#get_network = lambda addr: addr[:-5] + '0' + addr[-4:]
def get_network(addr:str) -> str:
      mid = addr.index('/')
      network_size = int(addr[mid+1:])
      
      ipaddress.ip_network()
      
      return network_size

print(get_network("123:123:123::123/127"))

>>>>>>> 1779ec59be166cd63b0b1d4e03f95928f61fdb0d
without_net_suffix = lambda addr : addr[:-4]

def get_interface_name(interface_shortcut:str) -> str:
      match(interface_shortcut):
            case "g1/0" : return "Gigabitethernet1/0"
            case "g2/0" : return "Gigabitethernet2/0"
            case "g3/0" : return "Gigabitethernet2/0"
            case "f0/0" : return "Fastethernet0/0"
            case _ : return ""