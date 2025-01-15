from gns3fy import Gns3Connector, Project, Node
import telnetlib
import json
import time





server = Gns3Connector("http://localhost:3080")  
project_name = "testprojetGNS3"
project = Project(name=project_name, connector=server)
project.get()  

# Check if the project is running
if not project.status == "opened":
    project.open()




def get_interface_name(interface_shortcut:str) -> str:
    match(interface_shortcut):
        case "g1/0" : return "gigabitethernet1/0"
        case "g2/0" : return "gigabitethernet2/0"
        case "g3/0" : return "gigabitethernet2/0"
        case "f0/0" : return "fastethernet0/0"
        case _ : return ""


def addresses_ospf(node: Node) -> None:
    commands = [
        "en",
        "interface",
        "ipv6 address",
        "no shutdown"
    ]
    
    router_name = node.name
    router_number = str(list(router_name)[1])
    local_data = data["ospf"][router_number]
    tn = telnetlib.Telnet(node.console_host, node.console)
    
    for key, value in local_data.items():
        tn.write(f"en\r\n".encode("utf-8"))
        time.sleep(0.1)
        tn.write("conf t\r\n".encode("utf-8"))
        time.sleep(0.1)
        tn.write(f"interface {get_interface_name(key)}\r\n".encode("utf-8"))
        time.sleep(0.1)
        tn.write(f"ipv6 address {value}\r\n".encode("utf-8"))
        time.sleep(0.1)
        tn.write(f"no shutdown\r\n".encode("UTF-8"))
 

with open('intent.json', 'r') as file:   
    data = json.load(file)


for node in project.nodes:
    
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}")
    print(node.console)
    
    try:
        tn = telnetlib.Telnet(node.console_host, node.console)
        print("Connected to Telnet!")
    except Exception as e:
        print(f"Failed to connect: {e}")
    time.sleep(4)
    addresses_ospf(node)
    tn.close()

