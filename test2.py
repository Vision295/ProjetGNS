from gns3fy import Gns3Connector, Project, Node

# Step 1: Connect to the GNS3 server
server = Gns3Connector("http://localhost:3080")  # Replace with your GNS3 server address if needed

# Step 2: Access the existing project
project_name = "testprojetGNS"  # Project ID from your example
lab = Project(name=project_name, connector=server)
lab.get()  # Fetch the project details

switch = Node(
      project_id=lab.project_id,
      connector=server,
      name="Ethernet-switch",
      template="Ethernet switch"
)
switch.create()