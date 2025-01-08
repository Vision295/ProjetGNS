import gns3fy
import requests

# Connect to GNS3 server
server = gns3fy.Gns3Connector("http://localhost:3080")

# Create/Get project
lab = gns3fy.Project(name="testprojetGNS", connector=server)
lab.get()
lab.open()

# Find the correct template ID for Ethernet switch
ethernet_switch_template = None
for template in server.get_templates():
    if template["name"].lower() == "ethernet switch":
        ethernet_switch_template = template
        break

if not ethernet_switch_template:
    raise ValueError("Ethernet switch template not found")

# Create node payload without using gns3fy Node class
node_data = {
    "name": "Ethernet-switch",
    "node_type": "ethernet_switch",
    "compute_id": "local",
    "template_id": ethernet_switch_template["template_id"],
    "x":100,
    "y":100
}

# Make direct API call to create the node
response = requests.post(
    f"http://localhost:3080/v2/projects/{lab.project_id}/nodes",
    json=node_data
)

# Check if creation was successful
if response.status_code == 201:
    node_info = response.json()
    print(f"Switch created successfully with node_id: {node_info['node_id']}")
    print(f"Switch name: {node_info['name']}")
    print(f"Switch status: {node_info['status']}")
else:
    print(f"Failed to create switch. Status code: {response.status_code}")
    print(f"Error message: {response.text}")