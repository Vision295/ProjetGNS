from gns3fy import Gns3Connector, Project, Node

# Step 1: Connect to the GNS3 server
server = Gns3Connector("http://localhost:3080")  # Replace with your GNS3 server address if needed

# Step 2: Access an existing project
project_name = "testprojetGNS"
project = Project(name=project_name, connector=server)
project.get()  # Fetch the project details

# Check if the project is running
if not project.status == "opened":
    project.open()

# Step 3: Create the router node
router_node = Node(name="VPCS 1", node_type="vpcs", compute_id="local")
# Step 4: Add the router node to the project
router_node.create()  # Create the node in the GNS3 project
print(f"Router {router_node.name} created with ID {router_node.node_id}")

# Step 5: Start the router (optional)
router_node.start()
print(f"Router {router_node.name} started.")
