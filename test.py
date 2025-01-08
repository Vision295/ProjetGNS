import gns3fy
import telnetlib
import time

server = gns3fy.Gns3Connector("http://localhost:3080")


lab = gns3fy.Project(name="testprojetGNS", connector=server)
lab.get()

print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}")
lab.open()

print(lab.stats)


for node in lab.nodes:
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}")
    print(node.console)
    
    # Get the console port
    console_host = node.console_host
    console_port = node.console


    try:
        tn = telnetlib.Telnet(console_host, console_port)
        print("Connected to Telnet!")
    except Exception as e:
        print(f"Failed to connect: {e}")

    # Example: Send a batch of commands
    commands = [
        "enable",
        "configure terminal",
        "interface FastEthernet0/0",
        "ip address 192.168.1.1 255.255.255.0",
        "no shutdown",
        "exit",
        "exit",
        "write memory"
    ]
    for cmd in commands:
        tn.write(f"{cmd}\r\n".encode("utf-8"))
        print(cmd)
        time.sleep(0.01)

    # Close the connection
    tn.close()
