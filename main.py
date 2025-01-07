import gns3fy

server = gns3fy.Gns3Connector("http://localhost:3080")


lab = gns3fy.Project(name="testprojetGNS", connector=server)
lab.get()

print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}")
lab.open()

print(lab.stats)


for node in lab.nodes:
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}")
    print(node.console)
    